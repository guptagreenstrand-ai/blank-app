"""
Export Utilities for Cutting Plans
Handles PDF, CSV, and image export functionality
"""

import csv
import io
from typing import List
from datetime import datetime
from data_models import OptimizationResult, CuttingPlan, Part, LumberStock
from visualizer import generate_cutting_sequence


def generate_csv_summary(result: OptimizationResult, parts: List[Part], 
                        inventory: List[LumberStock]) -> str:
    """
    Generate CSV summary of optimization results
    
    Args:
        result: Optimization result
        parts: Original parts list
        inventory: Original inventory list
        
    Returns:
        CSV string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Greenstrand Packaging - Cutting Plan Summary'])
    writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])
    
    # Overall Statistics
    writer.writerow(['OVERALL STATISTICS'])
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Total Sticks Used', result.total_sticks_used])
    writer.writerow(['Total Cuts', result.total_cuts])
    writer.writerow(['Overall Efficiency', f'{result.overall_efficiency:.2f}%'])
    writer.writerow(['Total Waste', f'{result.total_waste:.2f}%'])
    writer.writerow(['Total Cost', f'${result.total_cost:.2f}'])
    writer.writerow(['Total Volume (CFT)', f'{result.total_volume_used_cft:.4f}'])
    writer.writerow(['Computation Time', f'{result.computation_time:.3f}s'])
    writer.writerow(['Success', 'Yes' if result.success else 'No'])
    writer.writerow([])
    
    # Stock Usage
    writer.writerow(['STOCK USAGE BY TYPE'])
    writer.writerow(['Stock Name', 'Dimensions (mm)', 'Quantity Used', 'Cost per Unit', 'Total Cost'])
    
    stock_usage = {}
    for plan in result.cutting_plans:
        stock_id = plan.stock.id
        if stock_id not in stock_usage:
            stock_usage[stock_id] = {
                'stock': plan.stock,
                'count': 0
            }
        stock_usage[stock_id]['count'] += 1
    
    for stock_id, usage in stock_usage.items():
        stock = usage['stock']
        count = usage['count']
        total_cost = stock.cost_per_unit * count
        writer.writerow([
            stock.name,
            f'{stock.length}×{stock.width}×{stock.thickness}',
            count,
            f'${stock.cost_per_unit:.2f}',
            f'${total_cost:.2f}'
        ])
    writer.writerow([])
    
    # Parts Breakdown
    writer.writerow(['PARTS BREAKDOWN'])
    writer.writerow(['Part Name', 'Dimensions (mm)', 'Quantity Required', 'Quantity Assigned', 'Status'])
    
    parts_assigned = {}
    for plan in result.cutting_plans:
        for cut in plan.cuts:
            part_id = cut.part.id
            parts_assigned[part_id] = parts_assigned.get(part_id, 0) + 1
    
    for part in parts:
        assigned = parts_assigned.get(part.id, 0)
        required = part.total_quantity
        status = 'Complete' if assigned >= required else f'Incomplete ({assigned}/{required})'
        
        writer.writerow([
            part.name,
            f'{part.length}×{part.width}×{part.thickness}',
            required,
            assigned,
            status
        ])
    writer.writerow([])
    
    # Unassigned Parts
    if result.unassigned_parts:
        writer.writerow(['UNASSIGNED PARTS'])
        writer.writerow(['Part Name', 'Quantity Missing', 'Reason'])
        for part, qty in result.unassigned_parts:
            writer.writerow([part.name, qty, 'Insufficient stock or incompatible dimensions'])
        writer.writerow([])
    
    # Detailed Cutting Plans
    writer.writerow(['DETAILED CUTTING PLANS'])
    writer.writerow([])
    
    for i, plan in enumerate(result.cutting_plans, 1):
        writer.writerow([f'Plan #{i} - {plan.stock.name} (Stick #{plan.stock_index + 1})'])
        writer.writerow(['Stock Dimensions', f'{plan.stock.length}×{plan.stock.width}×{plan.stock.thickness} mm'])
        writer.writerow(['Material Utilized', f'{plan.material_utilized:.2f}%'])
        writer.writerow(['Waste', f'{plan.waste_percentage:.2f}%'])
        writer.writerow(['Total Cuts', plan.total_cuts])
        writer.writerow([])
        
        writer.writerow(['Cut #', 'Part Name', 'Dimensions (mm)', 'Position (mm)', 'Rotated'])
        position = 0
        for j, cut in enumerate(plan.cuts, 1):
            dims = f'{cut.actual_length:.1f}×{cut.actual_width:.1f}×{cut.actual_thickness:.1f}'
            writer.writerow([
                j,
                cut.part.name,
                dims,
                f'{position:.1f}',
                'Yes' if cut.rotated else 'No'
            ])
            position += cut.actual_length + 3  # Add kerf
        
        if plan.offcuts:
            writer.writerow([])
            writer.writerow(['Offcuts'])
            for k, offcut in enumerate(plan.offcuts, 1):
                writer.writerow([
                    f'Offcut #{k}',
                    f'{offcut.length:.1f}×{offcut.width:.1f}×{offcut.thickness:.1f} mm'
                ])
        
        writer.writerow([])
        writer.writerow([])
    
    return output.getvalue()


def generate_cutting_instructions(result: OptimizationResult) -> str:
    """
    Generate plain text cutting instructions for operators
    
    Args:
        result: Optimization result
        
    Returns:
        Plain text instructions
    """
    output = []
    
    output.append("=" * 80)
    output.append("GREENSTRAND PACKAGING - CUTTING INSTRUCTIONS")
    output.append("=" * 80)
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"Total Sticks: {result.total_sticks_used}")
    output.append(f"Total Cuts: {result.total_cuts}")
    output.append(f"Overall Efficiency: {result.overall_efficiency:.1f}%")
    output.append("=" * 80)
    output.append("")
    
    for i, plan in enumerate(result.cutting_plans, 1):
        output.append(f"\n{'='*80}")
        output.append(f"STICK #{i} of {len(result.cutting_plans)}")
        output.append(f"{'='*80}")
        
        instructions = generate_cutting_sequence(plan)
        output.extend(instructions)
        output.append("")
    
    if result.unassigned_parts:
        output.append("\n" + "=" * 80)
        output.append("⚠️  WARNING - UNASSIGNED PARTS")
        output.append("=" * 80)
        output.append("The following parts could not be assigned:")
        for part, qty in result.unassigned_parts:
            output.append(f"  • {part.name}: {qty} pieces")
            output.append(f"    Dimensions: {part.length}×{part.width}×{part.thickness} mm")
        output.append("")
        output.append("Action Required: Additional stock needed or adjust part specifications")
        output.append("=" * 80)
    
    return "\n".join(output)


def generate_parts_summary_csv(parts: List[Part]) -> str:
    """
    Generate CSV summary of parts requirements
    
    Args:
        parts: List of parts
        
    Returns:
        CSV string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Part Name', 'Description', 'Length (mm)', 'Width (mm)', 
                    'Thickness (mm)', 'Qty per Product', 'Total Products', 
                    'Total Quantity', 'Material Type', 'Allow Rotation', 'Priority'])
    
    for part in parts:
        writer.writerow([
            part.name,
            part.description,
            part.length,
            part.width,
            part.thickness,
            part.quantity_per_product,
            part.total_products,
            part.total_quantity,
            part.material_type,
            'Yes' if part.allow_rotation else 'No',
            part.priority
        ])
    
    return output.getvalue()


def generate_inventory_csv(inventory: List[LumberStock]) -> str:
    """
    Generate CSV of inventory
    
    Args:
        inventory: List of lumber stock
        
    Returns:
        CSV string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Stock Name', 'Length (mm)', 'Width (mm)', 'Thickness (mm)', 
                    'Quantity', 'Cost per Unit', 'Total Value', 'Volume (CFT)'])
    
    for stock in inventory:
        total_value = stock.cost_per_unit * stock.quantity
        total_volume = stock.volume_cft * stock.quantity
        writer.writerow([
            stock.name,
            stock.length,
            stock.width,
            stock.thickness,
            stock.quantity,
            f'${stock.cost_per_unit:.2f}',
            f'${total_value:.2f}',
            f'{total_volume:.4f}'
        ])
    
    return output.getvalue()


def prepare_download_filename(base_name: str, extension: str) -> str:
    """
    Prepare download filename with timestamp
    
    Args:
        base_name: Base filename
        extension: File extension (without dot)
        
    Returns:
        Filename string
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{base_name}_{timestamp}.{extension}"
