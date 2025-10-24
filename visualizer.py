"""
Visualization Module for Cutting Plans
Generates SVG and PNG diagrams for saw operators
"""

import io
import base64
from typing import List, Tuple
from data_models import CuttingPlan, CutPiece, Part


class CuttingPlanVisualizer:
    """Generates visual cutting plans"""
    
    # Color palette for different part types
    COLORS = {
        'plank': '#4CAF50',      # Green
        'stringer': '#2196F3',    # Blue
        'block': '#FF9800',       # Orange
        'runner': '#9C27B0',      # Purple
        'bearer': '#F44336',      # Red
        'default': '#607D8B'      # Grey
    }
    
    KERF_COLOR = '#000000'       # Black
    OFFCUT_COLOR = '#CCCCCC'     # Light grey
    TEXT_COLOR = '#FFFFFF'       # White
    BORDER_COLOR = '#000000'     # Black
    
    def __init__(self, scale: float = 0.1):
        """
        Initialize visualizer
        
        Args:
            scale: Scale factor for display (mm to pixels)
        """
        self.scale = scale
    
    def generate_cutting_plan_svg(self, plan: CuttingPlan, width: int = 1200) -> str:
        """
        Generate SVG visualization for a single cutting plan
        
        Args:
            plan: CuttingPlan to visualize
            width: SVG canvas width in pixels
            
        Returns:
            SVG string
        """
        # Calculate dimensions
        stock = plan.stock
        aspect_ratio = stock.width / stock.length
        height = int(width * aspect_ratio)
        
        # Calculate scale to fit
        scale_x = width / stock.length
        scale_y = height / stock.width
        scale = min(scale_x, scale_y) * 0.9  # 90% to leave margin
        
        # Start SVG
        margin = 50
        svg_width = width + 2 * margin
        svg_height = height + 2 * margin
        
        svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
    <!-- Background -->
    <rect width="{svg_width}" height="{svg_height}" fill="white"/>
    
    <!-- Title -->
    <text x="{svg_width/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="black">
        {stock.name} - Stick #{plan.stock_index + 1}
    </text>
    <text x="{svg_width/2}" y="50" text-anchor="middle" font-size="14" fill="black">
        {stock.length:.0f} × {stock.width:.0f} × {stock.thickness:.0f} mm | Utilization: {plan.material_utilized:.1f}%
    </text>
    
    <!-- Main cutting area -->
    <g transform="translate({margin}, {margin + 60})">
'''
        
        # Draw stock outline
        stock_width = stock.length * scale
        stock_height = stock.width * scale
        svg += f'        <rect x="0" y="0" width="{stock_width}" height="{stock_height}" '
        svg += f'fill="#F5F5F5" stroke="{self.BORDER_COLOR}" stroke-width="2"/>\n'
        
        # Draw cuts
        x_offset = 0
        for i, cut in enumerate(plan.cuts):
            color = self._get_color_for_part(cut.part)
            
            # Draw cut piece
            cut_width = cut.actual_length * scale
            cut_height = cut.actual_width * scale
            
            svg += f'        <rect x="{x_offset}" y="0" width="{cut_width}" height="{cut_height}" '
            svg += f'fill="{color}" stroke="{self.BORDER_COLOR}" stroke-width="1" opacity="0.8"/>\n'
            
            # Add label
            label = f"{cut.part.name}"
            dims = f"{cut.actual_length:.0f}×{cut.actual_width:.0f}×{cut.actual_thickness:.0f}"
            
            # Text positioning
            text_x = x_offset + cut_width / 2
            text_y = cut_height / 2 - 10
            
            svg += f'        <text x="{text_x}" y="{text_y}" text-anchor="middle" '
            svg += f'font-size="12" font-weight="bold" fill="{self.TEXT_COLOR}">{label}</text>\n'
            svg += f'        <text x="{text_x}" y="{text_y + 15}" text-anchor="middle" '
            svg += f'font-size="10" fill="{self.TEXT_COLOR}">{dims}mm</text>\n'
            
            if cut.rotated:
                svg += f'        <text x="{text_x}" y="{text_y + 28}" text-anchor="middle" '
                svg += f'font-size="9" fill="{self.TEXT_COLOR}" font-style="italic">↻ rotated</text>\n'
            
            # Draw kerf line (saw cut)
            if i < len(plan.cuts) - 1:
                kerf_x = x_offset + cut_width
                svg += f'        <line x1="{kerf_x}" y1="0" x2="{kerf_x}" y2="{stock_height}" '
                svg += f'stroke="{self.KERF_COLOR}" stroke-width="2" stroke-dasharray="5,5"/>\n'
                x_offset = kerf_x + 2  # Small gap for kerf visualization
            else:
                x_offset += cut_width
        
        # Draw offcuts
        if plan.offcuts:
            for offcut in plan.offcuts:
                offcut_width = offcut.length * scale
                offcut_height = offcut.width * scale
                
                svg += f'        <rect x="{x_offset}" y="0" width="{offcut_width}" height="{offcut_height}" '
                svg += f'fill="{self.OFFCUT_COLOR}" stroke="{self.BORDER_COLOR}" stroke-width="1" '
                svg += f'stroke-dasharray="3,3" opacity="0.5"/>\n'
                
                svg += f'        <text x="{x_offset + offcut_width/2}" y="{offcut_height/2}" '
                svg += f'text-anchor="middle" font-size="10" fill="black">Offcut</text>\n'
                svg += f'        <text x="{x_offset + offcut_width/2}" y="{offcut_height/2 + 12}" '
                svg += f'text-anchor="middle" font-size="9" fill="black">{offcut.length:.0f}mm</text>\n'
        
        svg += '    </g>\n'
        
        # Add legend
        svg += self._generate_legend(plan, margin, svg_height - 80)
        
        svg += '</svg>'
        
        return svg
    
    def generate_all_plans_svg(self, plans: List[CuttingPlan], width: int = 1400) -> str:
        """
        Generate composite SVG showing all cutting plans
        
        Args:
            plans: List of cutting plans
            width: SVG canvas width
            
        Returns:
            SVG string
        """
        if not plans:
            return self._generate_empty_svg(width)
        
        # Calculate total height needed
        plan_height = 250  # Height per plan
        total_height = len(plans) * plan_height + 100
        
        svg = f'''<svg width="{width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{width}" height="{total_height}" fill="white"/>
    
    <text x="{width/2}" y="30" text-anchor="middle" font-size="24" font-weight="bold" fill="black">
        Complete Cutting Plan - {len(plans)} Stick(s)
    </text>
'''
        
        # Draw each plan
        y_offset = 80
        for i, plan in enumerate(plans):
            svg += f'    <g transform="translate(0, {y_offset})">\n'
            
            # Generate mini version of each plan
            plan_svg = self.generate_cutting_plan_svg(plan, width - 100)
            # Extract the inner content (without outer svg tags)
            inner_svg = plan_svg.split('<g transform=')[1].split('</svg>')[0]
            svg += f'        <g transform="{inner_svg}\n'
            
            y_offset += plan_height
        
        svg += '</svg>'
        return svg
    
    def _generate_empty_svg(self, width: int) -> str:
        """Generate empty placeholder SVG"""
        return f'''<svg width="{width}" height="200" xmlns="http://www.w3.org/2000/svg">
    <rect width="{width}" height="200" fill="white"/>
    <text x="{width/2}" y="100" text-anchor="middle" font-size="18" fill="grey">
        No cutting plans generated yet
    </text>
</svg>'''
    
    def _generate_legend(self, plan: CuttingPlan, x: float, y: float) -> str:
        """Generate legend for part types"""
        svg = f'    <g transform="translate({x}, {y})">\n'
        svg += '        <text x="0" y="0" font-size="12" font-weight="bold">Legend:</text>\n'
        
        # Collect unique part types
        part_types = set()
        for cut in plan.cuts:
            part_types.add(cut.part.name.lower().split()[0])  # First word as type
        
        x_offset = 0
        for i, part_type in enumerate(sorted(part_types)):
            color = self._get_color_for_part_name(part_type)
            
            svg += f'        <rect x="{x_offset}" y="10" width="20" height="20" fill="{color}" '
            svg += f'stroke="black" stroke-width="1"/>\n'
            svg += f'        <text x="{x_offset + 25}" y="25" font-size="10">{part_type.title()}</text>\n'
            
            x_offset += 100
        
        svg += '    </g>\n'
        return svg
    
    def _get_color_for_part(self, part: Part) -> str:
        """Get color for a part based on its name"""
        name_lower = part.name.lower()
        for key in self.COLORS:
            if key in name_lower:
                return self.COLORS[key]
        return self.COLORS['default']
    
    def _get_color_for_part_name(self, name: str) -> str:
        """Get color for a part name"""
        name_lower = name.lower()
        for key in self.COLORS:
            if key in name_lower:
                return self.COLORS[key]
        return self.COLORS['default']
    
    def svg_to_png_base64(self, svg_string: str) -> str:
        """
        Convert SVG to PNG base64 (requires cairosvg)
        Note: This is optional and requires additional dependencies
        
        Args:
            svg_string: SVG string
            
        Returns:
            Base64 encoded PNG
        """
        try:
            import cairosvg
            png_bytes = cairosvg.svg2png(bytestring=svg_string.encode('utf-8'))
            return base64.b64encode(png_bytes).decode('utf-8')
        except ImportError:
            return ""


def generate_cutting_sequence(plan: CuttingPlan) -> List[str]:
    """
    Generate human-readable cutting sequence for operators
    
    Args:
        plan: Cutting plan
        
    Returns:
        List of instruction strings
    """
    instructions = []
    instructions.append(f"Stock: {plan.stock.name}")
    instructions.append(f"Dimensions: {plan.stock.length}×{plan.stock.width}×{plan.stock.thickness} mm")
    instructions.append("")
    instructions.append("Cutting Sequence:")
    
    position = 0
    for i, cut in enumerate(plan.cuts, 1):
        instructions.append(f"\n{i}. Cut {cut.part.name}")
        instructions.append(f"   - Dimensions: {cut.actual_length:.1f} × {cut.actual_width:.1f} × {cut.actual_thickness:.1f} mm")
        instructions.append(f"   - Position: {position:.1f} mm from start")
        if cut.rotated:
            instructions.append(f"   - ⚠️  ROTATED - Check orientation")
        instructions.append(f"   - Purpose: {cut.part.description}")
        
        position += cut.actual_length + 3  # Add kerf
    
    if plan.offcuts:
        instructions.append("\n📦 Offcuts to Keep:")
        for i, offcut in enumerate(plan.offcuts, 1):
            instructions.append(f"   {i}. {offcut.length:.1f} × {offcut.width:.1f} × {offcut.thickness:.1f} mm")
    
    instructions.append(f"\nTotal Cuts: {len(plan.cuts)}")
    instructions.append(f"Material Utilization: {plan.material_utilized:.1f}%")
    
    return instructions
