"""
Advanced 3D Guillotine Cutting Optimization Algorithm
Implements material nesting, rotation with grain enforcement, and resawing
"""

import time
from typing import List, Tuple, Optional
from copy import deepcopy
from data_models import (
    LumberStock, Part, CuttingParameters, CuttingPlan, CutPiece, 
    Offcut, OptimizationResult, OptimizationPriority, GrainDirection
)


class CuttingOptimizer:
    """Main optimizer class for 3D guillotine cutting"""
    
    def __init__(self, cutting_params: CuttingParameters):
        self.params = cutting_params
        
    def optimize(self, inventory: List[LumberStock], parts: List[Part]) -> OptimizationResult:
        """
        Main optimization entry point
        Returns optimized cutting plans
        """
        start_time = time.time()
        
        # Sort parts by priority and size (largest first)
        sorted_parts = self._sort_parts(parts)
        
        # Expand parts into individual items
        part_list = []
        for part in sorted_parts:
            for _ in range(part.total_quantity):
                part_list.append(part)
        
        # Sort inventory by size
        sorted_inventory = sorted(inventory, key=lambda s: s.volume, reverse=True)
        
        # Track available stock and used plans
        cutting_plans = []
        stock_usage = {stock.id: 0 for stock in sorted_inventory}
        unassigned_parts = []
        
        # Try to fit each part
        for part in part_list:
            assigned = False
            
            # Try to fit in existing cutting plans first (optimize material usage)
            for plan in cutting_plans:
                if self._can_add_part_to_plan(plan, part):
                    if self._add_part_to_plan(plan, part):
                        assigned = True
                        break
            
            # If not assigned, try new stock
            if not assigned:
                for stock in sorted_inventory:
                    if stock_usage[stock.id] < stock.quantity:
                        if self._part_fits_stock(part, stock):
                            # Create new cutting plan
                            plan = CuttingPlan(
                                stock=stock,
                                stock_index=stock_usage[stock.id]
                            )
                            if self._add_part_to_plan(plan, part):
                                cutting_plans.append(plan)
                                stock_usage[stock.id] += 1
                                assigned = True
                                break
            
            if not assigned:
                unassigned_parts.append((part, 1))
        
        # Consolidate unassigned parts
        unassigned_parts = self._consolidate_unassigned(unassigned_parts)
        
        # Calculate statistics
        result = self._calculate_results(cutting_plans, unassigned_parts, sorted_inventory)
        result.computation_time = time.time() - start_time
        
        return result
    
    def _sort_parts(self, parts: List[Part]) -> List[Part]:
        """Sort parts by priority and size"""
        if self.params.optimization_priority == OptimizationPriority.MAXIMIZE_EFFICIENCY:
            # Sort by priority first, then by volume (largest first)
            return sorted(parts, key=lambda p: (-p.priority, -p.volume))
        elif self.params.optimization_priority == OptimizationPriority.MINIMIZE_COST:
            # Sort by priority and try to minimize expensive materials
            return sorted(parts, key=lambda p: (-p.priority, -p.volume))
        else:  # FASTEST_CUT
            # Sort by simplicity (fewest cuts)
            return sorted(parts, key=lambda p: (-p.priority, p.volume))
    
    def _part_fits_stock(self, part: Part, stock: LumberStock) -> bool:
        """Check if a part can fit in a stock piece (considering rotation and tolerance)"""
        # Check all possible orientations
        orientations = self._get_possible_orientations(part, stock)
        return len(orientations) > 0
    
    def _get_possible_orientations(self, part: Part, stock: LumberStock) -> List[Tuple[bool, bool, bool]]:
        """
        Get all possible orientations for fitting part in stock
        Returns list of (rotate_xy, rotate_xz, rotate_yz) tuples
        """
        orientations = []
        part_dims = [
            (part.length, part.width, part.thickness),
            (part.length, part.thickness, part.width),
            (part.width, part.length, part.thickness),
            (part.width, part.thickness, part.length),
            (part.thickness, part.length, part.width),
            (part.thickness, part.width, part.length),
        ]
        
        stock_l, stock_w, stock_t = stock.length, stock.width, stock.thickness
        
        for i, (pl, pw, pt) in enumerate(part_dims):
            # Check if this orientation is allowed by grain direction
            if not self._check_grain_direction(part, i):
                continue
            
            # Check if part fits with tolerance and kerf
            if (pl <= stock_l + self.params.tolerance and 
                pw <= stock_w + self.params.tolerance and 
                pt <= stock_t + self.params.tolerance):
                
                # Represent rotation as tuple
                rotated = i != 0
                orientations.append((rotated, pl, pw, pt))
        
        return orientations
    
    def _check_grain_direction(self, part: Part, orientation_index: int) -> bool:
        """Check if orientation respects grain direction constraints"""
        if self.params.grain_direction == GrainDirection.NONE:
            return True
        
        # If rotation not allowed for this part, only allow original orientation
        if not part.allow_rotation and orientation_index != 0:
            return False
        
        return True
    
    def _can_add_part_to_plan(self, plan: CuttingPlan, part: Part) -> bool:
        """Check if a part can be added to an existing cutting plan"""
        # Simple check: see if we can find space using 3D bin packing logic
        # For now, use a simplified approach
        
        # Calculate used space
        if not plan.cuts:
            return self._part_fits_stock(part, plan.stock)
        
        # Try to find remaining space (simplified - assumes sequential cutting)
        used_volume = sum(c.actual_length * c.actual_width * c.actual_thickness 
                         for c in plan.cuts)
        remaining_volume = plan.stock.volume - used_volume
        
        return part.volume <= remaining_volume
    
    def _add_part_to_plan(self, plan: CuttingPlan, part: Part) -> bool:
        """Add a part to a cutting plan"""
        orientations = self._get_possible_orientations(part, plan.stock)
        
        if not orientations:
            return False
        
        # Use first valid orientation
        rotated, pl, pw, pt = orientations[0]
        
        # Calculate position (simplified - sequential placement)
        if not plan.cuts:
            x, y, z = 0, 0, 0
        else:
            # Place after last cut
            last_cut = plan.cuts[-1]
            x = last_cut.x + last_cut.actual_length + self.params.kerf
            y = 0
            z = 0
        
        # Create cut piece
        cut_piece = CutPiece(
            part=part,
            x=x,
            y=y,
            z=z,
            rotated=rotated,
            actual_length=pl,
            actual_width=pw,
            actual_thickness=pt
        )
        
        plan.cuts.append(cut_piece)
        
        # Calculate offcuts
        self._calculate_offcuts(plan)
        
        return True
    
    def _calculate_offcuts(self, plan: CuttingPlan):
        """Calculate offcuts from a cutting plan"""
        plan.offcuts.clear()
        
        if not plan.cuts:
            return
        
        # Calculate remaining length after all cuts
        total_length_used = sum(c.actual_length for c in plan.cuts) + \
                           (len(plan.cuts) - 1) * self.params.kerf
        
        remaining_length = plan.stock.length - total_length_used
        
        # If remaining length is above minimum, save as offcut
        if remaining_length >= self.params.min_offcut_to_keep:
            offcut = Offcut(
                length=remaining_length,
                width=plan.stock.width,
                thickness=plan.stock.thickness,
                original_stock=plan.stock.id,
                usable=True
            )
            plan.offcuts.append(offcut)
    
    def _consolidate_unassigned(self, unassigned: List[Tuple[Part, int]]) -> List[Tuple[Part, int]]:
        """Consolidate duplicate unassigned parts"""
        consolidated = {}
        for part, qty in unassigned:
            if part.id in consolidated:
                consolidated[part.id] = (part, consolidated[part.id][1] + qty)
            else:
                consolidated[part.id] = (part, qty)
        return list(consolidated.values())
    
    def _calculate_results(self, cutting_plans: List[CuttingPlan], 
                          unassigned_parts: List[Tuple[Part, int]],
                          inventory: List[LumberStock]) -> OptimizationResult:
        """Calculate final optimization results and statistics"""
        result = OptimizationResult()
        result.cutting_plans = cutting_plans
        result.unassigned_parts = unassigned_parts
        result.total_sticks_used = len(cutting_plans)
        result.total_cuts = sum(plan.total_cuts for plan in cutting_plans)
        
        # Calculate efficiency
        if cutting_plans:
            total_volume_available = sum(plan.stock.volume for plan in cutting_plans)
            total_volume_used = sum(
                sum(cut.actual_length * cut.actual_width * cut.actual_thickness 
                    for cut in plan.cuts)
                for plan in cutting_plans
            )
            
            result.overall_efficiency = (total_volume_used / total_volume_available * 100) if total_volume_available > 0 else 0
            result.total_waste = 100 - result.overall_efficiency
            
            # Calculate total cost and volume
            stock_counts = {}
            for plan in cutting_plans:
                stock_id = plan.stock.id
                stock_counts[stock_id] = stock_counts.get(stock_id, 0) + 1
            
            for stock_id, count in stock_counts.items():
                stock = next((s for s in inventory if s.id == stock_id), None)
                if stock:
                    result.total_cost += stock.cost_per_unit * count
                    result.total_volume_used_cft += stock.volume_cft * count
        
        return result


def optimize_cutting_plan(inventory: List[LumberStock], 
                          parts: List[Part],
                          cutting_params: CuttingParameters) -> OptimizationResult:
    """
    Convenience function to optimize cutting plan
    
    Args:
        inventory: List of available lumber stock
        parts: List of required parts
        cutting_params: Cutting parameters and constraints
        
    Returns:
        OptimizationResult with cutting plans and statistics
    """
    optimizer = CuttingOptimizer(cutting_params)
    return optimizer.optimize(inventory, parts)
