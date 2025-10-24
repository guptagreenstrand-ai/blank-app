import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import math

@dataclass
class Part:
    name: str
    description: str
    dimensions: List[float]  # [length, width, thickness]
    quantity: int
    material_type: str
    allow_rotation: bool
    priority: float

@dataclass
class LumberStock:
    name: str
    dimensions: List[float]  # [length, width, thickness]
    quantity: int
    cost: float

@dataclass
class CutPlan:
    lumber_id: int
    lumber_name: str
    parts: List[Dict[str, Any]]
    utilization: float
    waste: float
    cuts: int

class CuttingOptimizer:
    def __init__(self):
        self.offcuts = []  # Track available offcuts for reuse
        
    def optimize(self, lumber_data: List[Dict], parts_data: List[Dict], params: Dict) -> Dict[str, Any]:
        """
        Main optimization function implementing 3D guillotine cutting algorithm
        """
        # Convert data to internal format
        lumber_stock = [LumberStock(**data) for data in lumber_data]
        parts = [Part(**data) for data in parts_data]
        
        # Initialize optimization parameters
        kerf = params.get('kerf', 3.0)
        min_offcut = params.get('min_offcut', 50.0)
        tolerance = params.get('tolerance', 1.0)
        grain_direction_enforcement = params.get('grain_direction_enforcement', True)
        optimization_priority = params.get('optimization_priority', 'efficiency')
        
        # Sort parts by priority and size
        parts.sort(key=lambda p: (-p.priority, -p.dimensions[0] * p.dimensions[1] * p.dimensions[2]))
        
        # Initialize results
        cutting_plans = []
        total_utilization = 0
        total_waste = 0
        total_cuts = 0
        used_lumber = {}
        
        # Process each part type
        for part in parts:
            remaining_quantity = part.quantity
            
            while remaining_quantity > 0:
                # Find best lumber stock for this part
                best_lumber, best_plan = self._find_best_cut_plan(
                    part, lumber_stock, kerf, min_offcut, tolerance, 
                    grain_direction_enforcement, optimization_priority
                )
                
                if best_lumber is None:
                    # No suitable lumber found
                    break
                
                # Calculate how many parts we can cut from this lumber
                max_parts = self._calculate_max_parts(best_plan, part, kerf)
                parts_to_cut = min(max_parts, remaining_quantity)
                
                # Create cut plan
                cut_plan = self._create_cut_plan(
                    best_lumber, part, parts_to_cut, best_plan, kerf
                )
                
                cutting_plans.append(cut_plan)
                
                # Update tracking
                remaining_quantity -= parts_to_cut
                total_utilization += cut_plan['utilization'] * parts_to_cut
                total_waste += cut_plan['waste']
                total_cuts += cut_plan['cuts']
                
                # Track used lumber
                lumber_name = best_lumber.name
                if lumber_name not in used_lumber:
                    used_lumber[lumber_name] = 0
                used_lumber[lumber_name] += 1
                
                # Add offcuts for future use
                self._add_offcuts(best_plan, best_lumber, part, parts_to_cut, kerf, min_offcut)
        
        # Calculate overall metrics
        total_parts = sum(part.quantity for part in parts)
        avg_utilization = total_utilization / total_parts if total_parts > 0 else 0
        
        return {
            'cutting_plans': cutting_plans,
            'utilization_percentage': avg_utilization,
            'total_waste': total_waste,
            'total_cuts': total_cuts,
            'used_lumber': used_lumber,
            'remaining_offcuts': self.offcuts
        }
    
    def _find_best_cut_plan(self, part: Part, lumber_stock: List[LumberStock], 
                           kerf: float, min_offcut: float, tolerance: float,
                           grain_direction_enforcement: bool, optimization_priority: str) -> Tuple[Optional[LumberStock], Optional[Dict]]:
        """
        Find the best lumber stock and cutting plan for a given part
        """
        best_lumber = None
        best_plan = None
        best_score = -1
        
        # Check available offcuts first
        for offcut in self.offcuts:
            if self._can_fit_part(part, offcut, tolerance, grain_direction_enforcement):
                plan = self._create_2d_cut_plan(part, offcut, kerf)
                if plan:
                    score = self._calculate_score(plan, optimization_priority)
                    if score > best_score:
                        best_score = score
                        best_plan = plan
                        best_lumber = LumberStock(
                            name=f"Offcut_{offcut['id']}",
                            dimensions=offcut['dimensions'],
                            quantity=1,
                            cost=0
                        )
        
        # Check regular lumber stock
        for lumber in lumber_stock:
            if lumber.quantity <= 0:
                continue
                
            if self._can_fit_part(part, lumber.dimensions, tolerance, grain_direction_enforcement):
                plan = self._create_2d_cut_plan(part, lumber.dimensions, kerf)
                if plan:
                    score = self._calculate_score(plan, optimization_priority)
                    if score > best_score:
                        best_score = score
                        best_plan = plan
                        best_lumber = lumber
        
        return best_lumber, best_plan
    
    def _can_fit_part(self, part: Part, lumber_dimensions: List[float], 
                     tolerance: float, grain_direction_enforcement: bool) -> bool:
        """
        Check if a part can fit in lumber with given tolerance
        """
        part_dims = part.dimensions
        lumber_dims = lumber_dimensions
        
        # Check basic fit
        if (part_dims[0] <= lumber_dims[0] + tolerance and
            part_dims[1] <= lumber_dims[1] + tolerance and
            part_dims[2] <= lumber_dims[2] + tolerance):
            return True
        
        # Check rotation if allowed
        if part.allow_rotation:
            # Try all 6 possible orientations
            orientations = [
                [part_dims[0], part_dims[1], part_dims[2]],
                [part_dims[0], part_dims[2], part_dims[1]],
                [part_dims[1], part_dims[0], part_dims[2]],
                [part_dims[1], part_dims[2], part_dims[0]],
                [part_dims[2], part_dims[0], part_dims[1]],
                [part_dims[2], part_dims[1], part_dims[0]]
            ]
            
            for orientation in orientations:
                if (orientation[0] <= lumber_dims[0] + tolerance and
                    orientation[1] <= lumber_dims[1] + tolerance and
                    orientation[2] <= lumber_dims[2] + tolerance):
                    return True
        
        return False
    
    def _create_2d_cut_plan(self, part: Part, lumber_dimensions: List[float], kerf: float) -> Optional[Dict]:
        """
        Create a 2D cutting plan for the part on lumber
        """
        part_dims = part.dimensions
        lumber_dims = lumber_dimensions
        
        # Find best orientation
        best_orientation = None
        best_utilization = 0
        
        orientations = [
            [part_dims[0], part_dims[1], part_dims[2]],
            [part_dims[0], part_dims[2], part_dims[1]],
            [part_dims[1], part_dims[0], part_dims[2]],
            [part_dims[1], part_dims[2], part_dims[0]],
            [part_dims[2], part_dims[0], part_dims[1]],
            [part_dims[2], part_dims[1], part_dims[0]]
        ]
        
        for orientation in orientations:
            if (orientation[0] <= lumber_dims[0] and
                orientation[1] <= lumber_dims[1] and
                orientation[2] <= lumber_dims[2]):
                
                # Calculate how many parts fit in 2D
                parts_x = int(lumber_dims[0] // (orientation[0] + kerf))
                parts_y = int(lumber_dims[1] // (orientation[1] + kerf))
                parts_per_layer = parts_x * parts_y
                
                # Calculate layers
                layers = int(lumber_dims[2] // (orientation[2] + kerf))
                
                total_parts = parts_per_layer * layers
                if total_parts > 0:
                    utilization = (total_parts * orientation[0] * orientation[1] * orientation[2]) / (lumber_dims[0] * lumber_dims[1] * lumber_dims[2])
                    if utilization > best_utilization:
                        best_utilization = utilization
                        best_orientation = orientation
        
        if best_orientation is None:
            return None
        
        return {
            'orientation': best_orientation,
            'parts_per_layer': int(lumber_dims[0] // (best_orientation[0] + kerf)) * int(lumber_dims[1] // (best_orientation[1] + kerf)),
            'layers': int(lumber_dims[2] // (best_orientation[2] + kerf)),
            'utilization': best_utilization
        }
    
    def _calculate_max_parts(self, plan: Dict, part: Part, kerf: float) -> int:
        """
        Calculate maximum number of parts that can be cut from the plan
        """
        return plan['parts_per_layer'] * plan['layers']
    
    def _create_cut_plan(self, lumber: LumberStock, part: Part, quantity: int, 
                        plan: Dict, kerf: float) -> Dict[str, Any]:
        """
        Create detailed cut plan for visualization
        """
        orientation = plan['orientation']
        parts_per_layer = plan['parts_per_layer']
        layers = plan['layers']
        
        # Calculate actual parts to cut
        max_parts = parts_per_layer * layers
        actual_parts = min(quantity, max_parts)
        
        # Create cutting layout
        cutting_layout = {
            'lumber_dimensions': lumber.dimensions,
            'part_dimensions': orientation,
            'parts_per_layer': parts_per_layer,
            'layers': layers,
            'kerf': kerf,
            'cuts': self._calculate_cuts(parts_per_layer, layers, kerf),
            'utilization': (actual_parts * orientation[0] * orientation[1] * orientation[2]) / (lumber.dimensions[0] * lumber.dimensions[1] * lumber.dimensions[2]),
            'waste': (lumber.dimensions[0] * lumber.dimensions[1] * lumber.dimensions[2]) - (actual_parts * orientation[0] * orientation[1] * orientation[2])
        }
        
        return {
            'lumber_name': lumber.name,
            'lumber_dimensions': lumber.dimensions,
            'part_name': part.name,
            'part_dimensions': orientation,
            'quantity': actual_parts,
            'utilization': cutting_layout['utilization'],
            'waste': cutting_layout['waste'],
            'cuts': cutting_layout['cuts'],
            'cutting_layout': cutting_layout
        }
    
    def _calculate_cuts(self, parts_per_layer: int, layers: int, kerf: float) -> int:
        """
        Calculate total number of cuts needed
        """
        # Horizontal cuts (between layers)
        horizontal_cuts = layers - 1
        
        # Vertical cuts (within each layer)
        parts_x = int(math.sqrt(parts_per_layer))
        parts_y = parts_per_layer // parts_x
        
        vertical_cuts_x = (parts_x - 1) * layers
        vertical_cuts_y = (parts_y - 1) * layers
        
        return horizontal_cuts + vertical_cuts_x + vertical_cuts_y
    
    def _calculate_score(self, plan: Dict, optimization_priority: str) -> float:
        """
        Calculate optimization score based on priority
        """
        if optimization_priority == 'efficiency':
            return plan['utilization']
        elif optimization_priority == 'cost':
            # Lower cost is better, so invert
            return 1.0 / (1.0 + plan['utilization'])
        elif optimization_priority == 'speed':
            # Fewer cuts is better
            return 1.0 / (1.0 + plan.get('cuts', 1))
        else:
            return plan['utilization']
    
    def _add_offcuts(self, plan: Dict, lumber: LumberStock, part: Part, 
                    quantity: int, kerf: float, min_offcut: float):
        """
        Add remaining offcuts to the offcut database
        """
        orientation = plan['orientation']
        parts_per_layer = plan['parts_per_layer']
        layers = plan['layers']
        
        # Calculate remaining space
        used_length = (orientation[0] + kerf) * int(math.sqrt(parts_per_layer))
        used_width = (orientation[1] + kerf) * (parts_per_layer // int(math.sqrt(parts_per_layer)))
        used_thickness = (orientation[2] + kerf) * layers
        
        remaining_length = lumber.dimensions[0] - used_length
        remaining_width = lumber.dimensions[1] - used_width
        remaining_thickness = lumber.dimensions[2] - used_thickness
        
        # Add offcuts if they're large enough
        if remaining_length >= min_offcut:
            self.offcuts.append({
                'id': len(self.offcuts),
                'dimensions': [remaining_length, lumber.dimensions[1], lumber.dimensions[2]],
                'source': lumber.name
            })
        
        if remaining_width >= min_offcut:
            self.offcuts.append({
                'id': len(self.offcuts),
                'dimensions': [lumber.dimensions[0], remaining_width, lumber.dimensions[2]],
                'source': lumber.name
            })
        
        if remaining_thickness >= min_offcut:
            self.offcuts.append({
                'id': len(self.offcuts),
                'dimensions': [lumber.dimensions[0], lumber.dimensions[1], remaining_thickness],
                'source': lumber.name
            })