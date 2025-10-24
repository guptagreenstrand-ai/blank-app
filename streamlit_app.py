import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import io
import base64
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import json
from datetime import datetime
import math
from scipy.optimize import linear_sum_assignment
import random

# Configure Streamlit page
st.set_page_config(
    page_title="Greenstrand Packaging - 3D Wooden Cutting Plan Optimizer",
    page_icon="🪵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E7D32, #4CAF50);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
    }
    .optimization-result {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4CAF50;
    }
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffc107;
        color: #856404;
    }
    .error-box {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dc3545;
        color: #721c24;
    }
    .step-header {
        background: #f1f3f4;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Data Models
@dataclass
class Lumber:
    """Represents available lumber stock"""
    name: str
    length: float  # mm
    width: float   # mm
    thickness: float  # mm
    quantity: int
    cost_per_unit: float = 0.0
    
    @property
    def volume(self) -> float:
        """Volume in cubic mm"""
        return self.length * self.width * self.thickness
    
    @property
    def volume_m3(self) -> float:
        """Volume in cubic meters"""
        return self.volume / 1_000_000_000

@dataclass
class Part:
    """Represents a required cut part"""
    name: str
    description: str
    length: float  # mm
    width: float   # mm
    thickness: float  # mm
    quantity_per_product: int
    total_units: int
    material_type: str
    allow_rotation: bool = True
    priority: float = 1.0  # 0-1 scale
    
    @property
    def total_quantity(self) -> int:
        return self.quantity_per_product * self.total_units
    
    @property
    def volume(self) -> float:
        """Volume in cubic mm"""
        return self.length * self.width * self.thickness

@dataclass
class CuttingParameters:
    """Cutting operation parameters"""
    kerf: float = 3.0  # mm, saw blade gap
    min_offcut: float = 50.0  # mm, minimum offcut to keep
    tolerance: float = 2.0  # mm, allowable deviation
    grain_direction_enforced: bool = True
    optimization_priority: str = "efficiency"  # efficiency, cost, speed

@dataclass
class CutAssignment:
    """Represents a cut assignment on a lumber piece"""
    part: Part
    x: float  # position on lumber
    y: float
    z: float
    rotated: bool = False

@dataclass
class CuttingPlan:
    """Complete cutting plan for a lumber piece"""
    lumber: Lumber
    assignments: List[CutAssignment] = field(default_factory=list)
    offcuts: List[Tuple[float, float, float]] = field(default_factory=list)  # remaining pieces
    
    @property
    def utilization(self) -> float:
        """Material utilization percentage"""
        used_volume = sum(assignment.part.volume for assignment in self.assignments)
        return (used_volume / self.lumber.volume) * 100 if self.lumber.volume > 0 else 0

class CuttingOptimizer:
    """Advanced 3D guillotine cutting optimizer"""
    
    def __init__(self, parameters: CuttingParameters):
        self.parameters = parameters
    
    def optimize(self, lumber_inventory: List[Lumber], parts_list: List[Part]) -> List[CuttingPlan]:
        """
        Main optimization function implementing 3D guillotine cutting algorithm
        """
        plans = []
        remaining_parts = parts_list.copy()
        
        # Sort parts by priority and volume (largest first)
        remaining_parts.sort(key=lambda p: (-p.priority, -p.volume))
        
        # Create expanded parts list with individual quantities
        expanded_parts = []
        for part in remaining_parts:
            for _ in range(part.total_quantity):
                expanded_parts.append(part)
        
        # Sort lumber by efficiency (volume/cost ratio)
        sorted_lumber = sorted(lumber_inventory, key=lambda l: l.volume, reverse=True)
        
        lumber_usage = {lumber.name: 0 for lumber in lumber_inventory}
        
        for lumber in sorted_lumber:
            available_quantity = lumber.quantity - lumber_usage[lumber.name]
            
            while available_quantity > 0 and expanded_parts:
                plan = self._create_cutting_plan(lumber, expanded_parts)
                if plan.assignments:  # If we could fit any parts
                    plans.append(plan)
                    lumber_usage[lumber.name] += 1
                    available_quantity -= 1
                    
                    # Remove assigned parts from remaining list
                    for assignment in plan.assignments:
                        if assignment.part in expanded_parts:
                            expanded_parts.remove(assignment.part)
                else:
                    break  # No more parts can fit in this lumber type
        
        return plans
    
    def _create_cutting_plan(self, lumber: Lumber, available_parts: List[Part]) -> CuttingPlan:
        """Create optimal cutting plan for a single lumber piece"""
        plan = CuttingPlan(lumber=lumber)
        
        # Available space tracking
        available_spaces = [(0, 0, 0, lumber.length, lumber.width, lumber.thickness)]
        
        # Sort parts by volume (largest first for better packing)
        sorted_parts = sorted(available_parts, key=lambda p: p.volume, reverse=True)
        
        for part in sorted_parts:
            best_fit = None
            best_space_idx = -1
            best_rotated = False
            
            # Try to fit part in available spaces
            for space_idx, (x, y, z, length, width, thickness) in enumerate(available_spaces):
                # Try normal orientation
                if self._can_fit(part, length, width, thickness):
                    if best_fit is None or self._is_better_fit(part, length, width, thickness, best_fit):
                        best_fit = (x, y, z, length, width, thickness)
                        best_space_idx = space_idx
                        best_rotated = False
                
                # Try rotated orientation if allowed
                if part.allow_rotation and self._can_fit_rotated(part, length, width, thickness):
                    if best_fit is None or self._is_better_fit_rotated(part, length, width, thickness, best_fit):
                        best_fit = (x, y, z, length, width, thickness)
                        best_space_idx = space_idx
                        best_rotated = True
            
            # If we found a fit, assign the part
            if best_fit is not None:
                x, y, z, space_length, space_width, space_thickness = best_fit
                
                # Create assignment
                assignment = CutAssignment(
                    part=part,
                    x=x, y=y, z=z,
                    rotated=best_rotated
                )
                plan.assignments.append(assignment)
                
                # Update available spaces
                available_spaces.pop(best_space_idx)
                
                # Add remaining spaces after cutting
                part_length = part.width if best_rotated else part.length
                part_width = part.length if best_rotated else part.width
                part_thickness = part.thickness
                
                # Add kerf to dimensions
                cut_length = part_length + self.parameters.kerf
                cut_width = part_width + self.parameters.kerf
                cut_thickness = part_thickness + self.parameters.kerf
                
                # Calculate remaining spaces
                remaining_spaces = self._calculate_remaining_spaces(
                    x, y, z, space_length, space_width, space_thickness,
                    cut_length, cut_width, cut_thickness
                )
                
                # Filter out spaces that are too small
                valid_spaces = [
                    space for space in remaining_spaces
                    if (space[3] >= self.parameters.min_offcut and 
                        space[4] >= self.parameters.min_offcut and 
                        space[5] >= self.parameters.min_offcut)
                ]
                
                available_spaces.extend(valid_spaces)
        
        return plan
    
    def _can_fit(self, part: Part, length: float, width: float, thickness: float) -> bool:
        """Check if part can fit in given dimensions"""
        tolerance = self.parameters.tolerance
        return (part.length <= length + tolerance and 
                part.width <= width + tolerance and 
                part.thickness <= thickness + tolerance)
    
    def _can_fit_rotated(self, part: Part, length: float, width: float, thickness: float) -> bool:
        """Check if part can fit rotated in given dimensions"""
        tolerance = self.parameters.tolerance
        return (part.width <= length + tolerance and 
                part.length <= width + tolerance and 
                part.thickness <= thickness + tolerance)
    
    def _is_better_fit(self, part: Part, length: float, width: float, thickness: float, current_best: Tuple) -> bool:
        """Determine if this fit is better than current best"""
        if current_best is None:
            return True
        
        # Calculate waste for this fit
        waste = (length * width * thickness) - part.volume
        best_waste = (current_best[3] * current_best[4] * current_best[5]) - part.volume
        
        return waste < best_waste
    
    def _is_better_fit_rotated(self, part: Part, length: float, width: float, thickness: float, current_best: Tuple) -> bool:
        """Determine if this rotated fit is better than current best"""
        if current_best is None:
            return True
        
        # Calculate waste for this fit (with rotation)
        waste = (length * width * thickness) - part.volume
        best_waste = (current_best[3] * current_best[4] * current_best[5]) - part.volume
        
        return waste < best_waste
    
    def _calculate_remaining_spaces(self, x: float, y: float, z: float, 
                                  space_length: float, space_width: float, space_thickness: float,
                                  cut_length: float, cut_width: float, cut_thickness: float) -> List[Tuple]:
        """Calculate remaining spaces after making a cut"""
        spaces = []
        
        # Right space (along length)
        if space_length > cut_length:
            spaces.append((
                x + cut_length, y, z,
                space_length - cut_length, space_width, space_thickness
            ))
        
        # Back space (along width)
        if space_width > cut_width:
            spaces.append((
                x, y + cut_width, z,
                cut_length, space_width - cut_width, space_thickness
            ))
        
        # Top space (along thickness)
        if space_thickness > cut_thickness:
            spaces.append((
                x, y, z + cut_thickness,
                cut_length, cut_width, space_thickness - cut_thickness
            ))
        
        return spaces

def create_sample_data():
    """Create sample data for testing"""
    lumber_inventory = [
        Lumber("Aus KD Pine 8'×7\"×3.5\"", 2400, 178, 89, 10, 45.50),
        Lumber("Aus KD Pine 10'×9\"×3.5\"", 3000, 228, 89, 8, 62.75),
        Lumber("Aus KD Pine 12'×7\"×3.5\"", 3600, 178, 89, 6, 68.90),
        Lumber("Hardwood Block 6\"×4\"×4\"", 152, 102, 102, 20, 12.30),
    ]
    
    parts_list = [
        Part("Pallet Deck Plank", "Main deck board", 1200, 100, 20, 7, 50, "Pine", True, 0.9),
        Part("Pallet Stringer", "Support beam", 1200, 100, 89, 3, 50, "Pine", False, 1.0),
        Part("Support Block", "Corner support", 100, 100, 89, 9, 50, "Pine", True, 0.7),
        Part("Runner Block", "Bottom runner", 145, 145, 78, 2, 50, "Hardwood", True, 0.8),
    ]
    
    return lumber_inventory, parts_list

def render_cutting_visualization(plans: List[CuttingPlan]):
    """Render 2D cutting visualization using matplotlib"""
    if not plans:
        st.warning("No cutting plans to visualize.")
        return
    
    # Color mapping for different parts
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    part_colors = {}
    
    fig, axes = plt.subplots(len(plans), 1, figsize=(12, 4 * len(plans)))
    if len(plans) == 1:
        axes = [axes]
    
    for plan_idx, plan in enumerate(plans):
        ax = axes[plan_idx]
        
        # Draw lumber outline
        lumber_rect = Rectangle((0, 0), plan.lumber.length, plan.lumber.width, 
                              linewidth=2, edgecolor='black', facecolor='lightgray', alpha=0.3)
        ax.add_patch(lumber_rect)
        
        # Draw cut assignments
        for assignment in plan.assignments:
            part = assignment.part
            
            # Assign color if not already assigned
            if part.name not in part_colors:
                part_colors[part.name] = colors[len(part_colors) % len(colors)]
            
            # Determine dimensions based on rotation
            if assignment.rotated:
                part_length, part_width = part.width, part.length
            else:
                part_length, part_width = part.length, part.width
            
            # Draw part rectangle
            part_rect = Rectangle((assignment.x, assignment.y), part_length, part_width,
                                linewidth=1, edgecolor='black', 
                                facecolor=part_colors[part.name], alpha=0.7)
            ax.add_patch(part_rect)
            
            # Add part label
            label = f"{part.name}"
            if assignment.rotated:
                label += " (R)"
            
            ax.text(assignment.x + part_length/2, assignment.y + part_width/2, label,
                   ha='center', va='center', fontsize=8, weight='bold')
        
        # Set axis properties
        ax.set_xlim(0, plan.lumber.length * 1.1)
        ax.set_ylim(0, plan.lumber.width * 1.1)
        ax.set_aspect('equal')
        ax.set_title(f'{plan.lumber.name} - Utilization: {plan.utilization:.1f}%')
        ax.set_xlabel('Length (mm)')
        ax.set_ylabel('Width (mm)')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🪵 Greenstrand Packaging</h1>
        <h2>3D Wooden Cutting Plan Optimizer</h2>
        <p>Professional tool for maximizing material utilization and minimizing waste</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a section:", [
        "📋 Input & Configuration",
        "⚙️ Optimization",
        "📊 Results & Visualization",
        "📄 Export & Reports"
    ])
    
    # Initialize session state
    if 'lumber_inventory' not in st.session_state:
        st.session_state.lumber_inventory = []
    if 'parts_list' not in st.session_state:
        st.session_state.parts_list = []
    if 'cutting_plans' not in st.session_state:
        st.session_state.cutting_plans = []
    if 'optimization_results' not in st.session_state:
        st.session_state.optimization_results = {}
    
    # Load sample data button
    if st.sidebar.button("Load Sample Data"):
        lumber_inventory, parts_list = create_sample_data()
        st.session_state.lumber_inventory = lumber_inventory
        st.session_state.parts_list = parts_list
        st.success("Sample data loaded successfully!")
    
    if page == "📋 Input & Configuration":
        render_input_page()
    elif page == "⚙️ Optimization":
        render_optimization_page()
    elif page == "📊 Results & Visualization":
        render_results_page()
    elif page == "📄 Export & Reports":
        render_export_page()

def render_input_page():
    st.markdown('<div class="step-header"><h3>📋 Input & Configuration</h3></div>', unsafe_allow_html=True)
    
    # Create tabs for different input sections
    tab1, tab2, tab3 = st.tabs(["🪵 Lumber Inventory", "🔧 Parts List", "⚙️ Cutting Parameters"])
    
    with tab1:
        st.subheader("Available Lumber Stock")
        
        # Input form for new lumber
        with st.expander("Add New Lumber", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                lumber_name = st.text_input("Lumber Name", placeholder="e.g., Aus KD Pine 8'×7\"×3.5\"")
                lumber_length = st.number_input("Length (mm)", min_value=0.0, step=1.0, value=2400.0)
                lumber_width = st.number_input("Width (mm)", min_value=0.0, step=1.0, value=178.0)
            
            with col2:
                lumber_thickness = st.number_input("Thickness (mm)", min_value=0.0, step=1.0, value=89.0)
                lumber_quantity = st.number_input("Quantity", min_value=1, step=1, value=10)
                lumber_cost = st.number_input("Cost per Unit ($)", min_value=0.0, step=0.01, value=45.50)
            
            if st.button("Add Lumber"):
                if lumber_name:
                    new_lumber = Lumber(
                        name=lumber_name,
                        length=lumber_length,
                        width=lumber_width,
                        thickness=lumber_thickness,
                        quantity=lumber_quantity,
                        cost_per_unit=lumber_cost
                    )
                    st.session_state.lumber_inventory.append(new_lumber)
                    st.success(f"Added {lumber_name} to inventory!")
                else:
                    st.error("Please provide a lumber name.")
        
        # Display current inventory
        if st.session_state.lumber_inventory:
            st.subheader("Current Inventory")
            
            inventory_data = []
            for i, lumber in enumerate(st.session_state.lumber_inventory):
                inventory_data.append({
                    "Index": i,
                    "Name": lumber.name,
                    "Dimensions (L×W×T)": f"{lumber.length}×{lumber.width}×{lumber.thickness}",
                    "Quantity": lumber.quantity,
                    "Cost/Unit": f"${lumber.cost_per_unit:.2f}",
                    "Volume (m³)": f"{lumber.volume_m3:.4f}",
                    "Total Cost": f"${lumber.cost_per_unit * lumber.quantity:.2f}"
                })
            
            df = pd.DataFrame(inventory_data)
            st.dataframe(df, use_container_width=True)
            
            # Remove lumber option
            if st.button("Remove Selected Lumber"):
                remove_idx = st.selectbox("Select lumber to remove:", 
                                        options=range(len(st.session_state.lumber_inventory)),
                                        format_func=lambda x: st.session_state.lumber_inventory[x].name)
                if st.button("Confirm Remove"):
                    st.session_state.lumber_inventory.pop(remove_idx)
                    st.success("Lumber removed!")
    
    with tab2:
        st.subheader("Required Cut Parts")
        
        # Input form for new part
        with st.expander("Add New Part", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                part_name = st.text_input("Part Name", placeholder="e.g., Pallet Deck Plank")
                part_description = st.text_input("Description", placeholder="e.g., Main deck board")
                part_length = st.number_input("Part Length (mm)", min_value=0.0, step=1.0, value=1200.0)
                part_width = st.number_input("Part Width (mm)", min_value=0.0, step=1.0, value=100.0)
                part_thickness = st.number_input("Part Thickness (mm)", min_value=0.0, step=1.0, value=20.0)
            
            with col2:
                qty_per_product = st.number_input("Quantity per Product", min_value=1, step=1, value=7)
                total_units = st.number_input("Total Units", min_value=1, step=1, value=50)
                material_type = st.selectbox("Material Type", ["Pine", "Hardwood", "Plywood", "Other"])
                allow_rotation = st.checkbox("Allow Rotation", value=True)
                priority = st.slider("Priority", min_value=0.0, max_value=1.0, step=0.1, value=0.9)
            
            if st.button("Add Part"):
                if part_name:
                    new_part = Part(
                        name=part_name,
                        description=part_description,
                        length=part_length,
                        width=part_width,
                        thickness=part_thickness,
                        quantity_per_product=qty_per_product,
                        total_units=total_units,
                        material_type=material_type,
                        allow_rotation=allow_rotation,
                        priority=priority
                    )
                    st.session_state.parts_list.append(new_part)
                    st.success(f"Added {part_name} to parts list!")
                else:
                    st.error("Please provide a part name.")
        
        # Display current parts list
        if st.session_state.parts_list:
            st.subheader("Current Parts List")
            
            parts_data = []
            for i, part in enumerate(st.session_state.parts_list):
                parts_data.append({
                    "Index": i,
                    "Name": part.name,
                    "Description": part.description,
                    "Dimensions (L×W×T)": f"{part.length}×{part.width}×{part.thickness}",
                    "Qty/Product": part.quantity_per_product,
                    "Total Units": part.total_units,
                    "Total Qty": part.total_quantity,
                    "Material": part.material_type,
                    "Rotation": "Yes" if part.allow_rotation else "No",
                    "Priority": f"{part.priority:.1f}"
                })
            
            df = pd.DataFrame(parts_data)
            st.dataframe(df, use_container_width=True)
            
            # Summary metrics
            total_parts = sum(part.total_quantity for part in st.session_state.parts_list)
            total_volume = sum(part.volume * part.total_quantity for part in st.session_state.parts_list)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Parts", total_parts)
            with col2:
                st.metric("Total Volume", f"{total_volume/1_000_000:.2f} L")
            with col3:
                st.metric("Unique Parts", len(st.session_state.parts_list))
    
    with tab3:
        st.subheader("Cutting Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            kerf = st.number_input("Kerf (Saw Blade Gap, mm)", min_value=0.0, step=0.1, value=3.0)
            min_offcut = st.number_input("Minimum Offcut to Keep (mm)", min_value=0.0, step=1.0, value=50.0)
            tolerance = st.number_input("Tolerance (mm)", min_value=0.0, step=0.1, value=2.0)
        
        with col2:
            grain_direction = st.checkbox("Enforce Grain Direction", value=True)
            optimization_priority = st.selectbox("Optimization Priority", 
                                               ["efficiency", "cost", "speed"],
                                               format_func=lambda x: x.title())
        
        # Store parameters in session state
        st.session_state.cutting_parameters = CuttingParameters(
            kerf=kerf,
            min_offcut=min_offcut,
            tolerance=tolerance,
            grain_direction_enforced=grain_direction,
            optimization_priority=optimization_priority
        )
        
        st.info("Parameters saved automatically. Proceed to Optimization when ready.")

def render_optimization_page():
    st.markdown('<div class="step-header"><h3>⚙️ Optimization Engine</h3></div>', unsafe_allow_html=True)
    
    # Check if we have required data
    if not st.session_state.lumber_inventory:
        st.error("Please add lumber inventory first.")
        return
    
    if not st.session_state.parts_list:
        st.error("Please add parts to the parts list first.")
        return
    
    # Display optimization summary
    st.subheader("Optimization Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        lumber_count = len(st.session_state.lumber_inventory)
        total_lumber_pieces = sum(lumber.quantity for lumber in st.session_state.lumber_inventory)
        st.metric("Lumber Types", lumber_count)
        st.metric("Total Pieces", total_lumber_pieces)
    
    with col2:
        parts_count = len(st.session_state.parts_list)
        total_parts_needed = sum(part.total_quantity for part in st.session_state.parts_list)
        st.metric("Part Types", parts_count)
        st.metric("Total Parts Needed", total_parts_needed)
    
    with col3:
        total_lumber_volume = sum(lumber.volume_m3 * lumber.quantity for lumber in st.session_state.lumber_inventory)
        total_parts_volume = sum(part.volume * part.total_quantity for part in st.session_state.parts_list) / 1_000_000_000
        st.metric("Available Volume", f"{total_lumber_volume:.3f} m³")
        st.metric("Required Volume", f"{total_parts_volume:.3f} m³")
    
    with col4:
        if total_lumber_volume > 0:
            volume_efficiency = (total_parts_volume / total_lumber_volume) * 100
            st.metric("Theoretical Efficiency", f"{volume_efficiency:.1f}%")
        
        total_lumber_cost = sum(lumber.cost_per_unit * lumber.quantity for lumber in st.session_state.lumber_inventory)
        st.metric("Total Lumber Cost", f"${total_lumber_cost:.2f}")
    
    # Optimization controls
    st.subheader("Run Optimization")
    
    if 'cutting_parameters' not in st.session_state:
        st.warning("Please configure cutting parameters first.")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(f"""
        **Optimization Settings:**
        - Kerf: {st.session_state.cutting_parameters.kerf}mm
        - Min Offcut: {st.session_state.cutting_parameters.min_offcut}mm
        - Tolerance: {st.session_state.cutting_parameters.tolerance}mm
        - Priority: {st.session_state.cutting_parameters.optimization_priority.title()}
        """)
    
    with col2:
        if st.button("🚀 Start Optimization", type="primary", use_container_width=True):
            with st.spinner("Running 3D guillotine cutting optimization..."):
                optimizer = CuttingOptimizer(st.session_state.cutting_parameters)
                
                try:
                    cutting_plans = optimizer.optimize(
                        st.session_state.lumber_inventory,
                        st.session_state.parts_list
                    )
                    
                    st.session_state.cutting_plans = cutting_plans
                    
                    # Calculate optimization results
                    total_lumber_used = len(cutting_plans)
                    total_parts_assigned = sum(len(plan.assignments) for plan in cutting_plans)
                    average_utilization = np.mean([plan.utilization for plan in cutting_plans]) if cutting_plans else 0
                    
                    # Calculate material costs
                    lumber_costs = {}
                    for plan in cutting_plans:
                        lumber_name = plan.lumber.name
                        if lumber_name not in lumber_costs:
                            lumber_costs[lumber_name] = 0
                        lumber_costs[lumber_name] += plan.lumber.cost_per_unit
                    
                    total_cost = sum(lumber_costs.values())
                    
                    # Store results
                    st.session_state.optimization_results = {
                        'total_lumber_used': total_lumber_used,
                        'total_parts_assigned': total_parts_assigned,
                        'average_utilization': average_utilization,
                        'total_cost': total_cost,
                        'lumber_costs': lumber_costs,
                        'optimization_time': datetime.now()
                    }
                    
                    st.success(f"Optimization completed! Generated {total_lumber_used} cutting plans.")
                    
                except Exception as e:
                    st.error(f"Optimization failed: {str(e)}")
    
    # Display optimization results if available
    if st.session_state.cutting_plans:
        st.subheader("Optimization Results")
        
        results = st.session_state.optimization_results
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Lumber Pieces Used", results['total_lumber_used'])
        with col2:
            st.metric("Parts Assigned", results['total_parts_assigned'])
        with col3:
            st.metric("Average Utilization", f"{results['average_utilization']:.1f}%")
        with col4:
            st.metric("Total Material Cost", f"${results['total_cost']:.2f}")
        
        # Utilization distribution
        utilizations = [plan.utilization for plan in st.session_state.cutting_plans]
        
        fig = px.histogram(
            x=utilizations,
            nbins=20,
            title="Material Utilization Distribution",
            labels={'x': 'Utilization (%)', 'y': 'Number of Lumber Pieces'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def render_results_page():
    st.markdown('<div class="step-header"><h3>📊 Results & Visualization</h3></div>', unsafe_allow_html=True)
    
    if not st.session_state.cutting_plans:
        st.warning("No optimization results available. Please run optimization first.")
        return
    
    # Results summary
    st.subheader("Cutting Plans Overview")
    
    plans_data = []
    for i, plan in enumerate(st.session_state.cutting_plans):
        plans_data.append({
            "Plan #": i + 1,
            "Lumber": plan.lumber.name,
            "Parts Assigned": len(plan.assignments),
            "Utilization": f"{plan.utilization:.1f}%",
            "Cost": f"${plan.lumber.cost_per_unit:.2f}",
            "Dimensions": f"{plan.lumber.length}×{plan.lumber.width}×{plan.lumber.thickness}"
        })
    
    df = pd.DataFrame(plans_data)
    st.dataframe(df, use_container_width=True)
    
    # Visualization options
    st.subheader("Cutting Plan Visualization")
    
    # Plan selection
    selected_plans = st.multiselect(
        "Select plans to visualize:",
        options=list(range(len(st.session_state.cutting_plans))),
        default=list(range(min(3, len(st.session_state.cutting_plans)))),
        format_func=lambda x: f"Plan {x+1}: {st.session_state.cutting_plans[x].lumber.name}"
    )
    
    if selected_plans:
        selected_cutting_plans = [st.session_state.cutting_plans[i] for i in selected_plans]
        
        # Generate visualization
        fig = render_cutting_visualization(selected_cutting_plans)
        st.pyplot(fig)
        
        # Detailed plan information
        st.subheader("Detailed Cut Assignments")
        
        for plan_idx in selected_plans:
            plan = st.session_state.cutting_plans[plan_idx]
            
            with st.expander(f"Plan {plan_idx + 1}: {plan.lumber.name}"):
                if plan.assignments:
                    assignment_data = []
                    for i, assignment in enumerate(plan.assignments):
                        part = assignment.part
                        assignment_data.append({
                            "Cut #": i + 1,
                            "Part": part.name,
                            "Dimensions": f"{part.length}×{part.width}×{part.thickness}",
                            "Position (X,Y,Z)": f"({assignment.x:.0f}, {assignment.y:.0f}, {assignment.z:.0f})",
                            "Rotated": "Yes" if assignment.rotated else "No",
                            "Priority": part.priority
                        })
                    
                    assignment_df = pd.DataFrame(assignment_data)
                    st.dataframe(assignment_df, use_container_width=True)
                    
                    st.info(f"**Utilization:** {plan.utilization:.1f}% | **Parts:** {len(plan.assignments)} | **Cost:** ${plan.lumber.cost_per_unit:.2f}")
                else:
                    st.warning("No parts assigned to this lumber piece.")
    
    # Analytics and insights
    st.subheader("Optimization Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Utilization by lumber type
        lumber_utilization = {}
        for plan in st.session_state.cutting_plans:
            lumber_name = plan.lumber.name
            if lumber_name not in lumber_utilization:
                lumber_utilization[lumber_name] = []
            lumber_utilization[lumber_name].append(plan.utilization)
        
        # Calculate average utilization per lumber type
        avg_utilization = {name: np.mean(utils) for name, utils in lumber_utilization.items()}
        
        fig = px.bar(
            x=list(avg_utilization.keys()),
            y=list(avg_utilization.values()),
            title="Average Utilization by Lumber Type",
            labels={'x': 'Lumber Type', 'y': 'Average Utilization (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Parts assignment success rate
        parts_assigned = {}
        for plan in st.session_state.cutting_plans:
            for assignment in plan.assignments:
                part_name = assignment.part.name
                if part_name not in parts_assigned:
                    parts_assigned[part_name] = 0
                parts_assigned[part_name] += 1
        
        parts_needed = {part.name: part.total_quantity for part in st.session_state.parts_list}
        
        success_rates = []
        part_names = []
        for part_name, needed in parts_needed.items():
            assigned = parts_assigned.get(part_name, 0)
            success_rate = (assigned / needed) * 100 if needed > 0 else 0
            success_rates.append(success_rate)
            part_names.append(part_name)
        
        fig = px.bar(
            x=part_names,
            y=success_rates,
            title="Parts Assignment Success Rate",
            labels={'x': 'Part Type', 'y': 'Success Rate (%)'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

def render_export_page():
    st.markdown('<div class="step-header"><h3>📄 Export & Reports</h3></div>', unsafe_allow_html=True)
    
    if not st.session_state.cutting_plans:
        st.warning("No optimization results available. Please run optimization first.")
        return
    
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Data Exports")
        
        # CSV Export
        if st.button("📄 Export Cutting Plans (CSV)", use_container_width=True):
            csv_data = generate_csv_export()
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"cutting_plans_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # JSON Export
        if st.button("📋 Export Configuration (JSON)", use_container_width=True):
            json_data = generate_json_export()
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"cutting_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("### 📈 Visual Exports")
        
        # PDF Report (placeholder)
        if st.button("📑 Generate PDF Report", use_container_width=True):
            st.info("PDF report generation feature coming soon!")
        
        # SVG Export (placeholder)
        if st.button("🎨 Export Cutting Diagrams (SVG)", use_container_width=True):
            st.info("SVG export feature coming soon!")
    
    # Summary Report
    st.subheader("Optimization Summary Report")
    
    if st.session_state.optimization_results:
        results = st.session_state.optimization_results
        
        st.markdown(f"""
        ### 📋 Executive Summary
        
        **Optimization Completed:** {results['optimization_time'].strftime('%Y-%m-%d %H:%M:%S')}
        
        **Material Efficiency:**
        - Total lumber pieces used: {results['total_lumber_used']}
        - Average material utilization: {results['average_utilization']:.1f}%
        - Total parts successfully assigned: {results['total_parts_assigned']}
        
        **Cost Analysis:**
        - Total material cost: ${results['total_cost']:.2f}
        - Cost per part: ${results['total_cost'] / max(results['total_parts_assigned'], 1):.2f}
        
        **Cutting Requirements:**
        - Kerf allowance: {st.session_state.cutting_parameters.kerf}mm
        - Minimum offcut retention: {st.session_state.cutting_parameters.min_offcut}mm
        - Tolerance: ±{st.session_state.cutting_parameters.tolerance}mm
        """)
        
        # Detailed lumber usage
        st.subheader("Lumber Usage Breakdown")
        
        lumber_usage_data = []
        for lumber_type, cost in results['lumber_costs'].items():
            pieces_used = sum(1 for plan in st.session_state.cutting_plans if plan.lumber.name == lumber_type)
            avg_util = np.mean([plan.utilization for plan in st.session_state.cutting_plans if plan.lumber.name == lumber_type])
            
            lumber_usage_data.append({
                "Lumber Type": lumber_type,
                "Pieces Used": pieces_used,
                "Total Cost": f"${cost:.2f}",
                "Avg Utilization": f"{avg_util:.1f}%"
            })
        
        usage_df = pd.DataFrame(lumber_usage_data)
        st.dataframe(usage_df, use_container_width=True)
        
        # Recommendations
        st.subheader("Optimization Recommendations")
        
        avg_utilization = results['average_utilization']
        
        if avg_utilization > 80:
            st.success("🎉 Excellent optimization! Material utilization is very high.")
        elif avg_utilization > 60:
            st.info("✅ Good optimization. Consider adjusting tolerances for better utilization.")
        else:
            st.warning("⚠️ Low utilization detected. Review part dimensions and lumber selection.")
        
        # Improvement suggestions
        st.markdown("""
        **Suggestions for Improvement:**
        - Consider allowing part rotation where grain direction permits
        - Review minimum offcut settings - smaller offcuts may improve utilization
        - Evaluate lumber inventory mix for better size matching
        - Consider batch processing similar parts together
        """)

def generate_csv_export():
    """Generate CSV export of cutting plans"""
    data = []
    
    for plan_idx, plan in enumerate(st.session_state.cutting_plans):
        for assignment_idx, assignment in enumerate(plan.assignments):
            part = assignment.part
            data.append({
                'Plan_ID': plan_idx + 1,
                'Lumber_Name': plan.lumber.name,
                'Lumber_Dimensions': f"{plan.lumber.length}x{plan.lumber.width}x{plan.lumber.thickness}",
                'Lumber_Cost': plan.lumber.cost_per_unit,
                'Utilization_Percent': round(plan.utilization, 2),
                'Cut_Sequence': assignment_idx + 1,
                'Part_Name': part.name,
                'Part_Description': part.description,
                'Part_Dimensions': f"{part.length}x{part.width}x{part.thickness}",
                'Position_X': assignment.x,
                'Position_Y': assignment.y,
                'Position_Z': assignment.z,
                'Rotated': assignment.rotated,
                'Part_Priority': part.priority,
                'Material_Type': part.material_type
            })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

def generate_json_export():
    """Generate JSON export of complete configuration"""
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'lumber_inventory': [
            {
                'name': lumber.name,
                'length': lumber.length,
                'width': lumber.width,
                'thickness': lumber.thickness,
                'quantity': lumber.quantity,
                'cost_per_unit': lumber.cost_per_unit
            }
            for lumber in st.session_state.lumber_inventory
        ],
        'parts_list': [
            {
                'name': part.name,
                'description': part.description,
                'length': part.length,
                'width': part.width,
                'thickness': part.thickness,
                'quantity_per_product': part.quantity_per_product,
                'total_units': part.total_units,
                'material_type': part.material_type,
                'allow_rotation': part.allow_rotation,
                'priority': part.priority
            }
            for part in st.session_state.parts_list
        ],
        'cutting_parameters': {
            'kerf': st.session_state.cutting_parameters.kerf,
            'min_offcut': st.session_state.cutting_parameters.min_offcut,
            'tolerance': st.session_state.cutting_parameters.tolerance,
            'grain_direction_enforced': st.session_state.cutting_parameters.grain_direction_enforced,
            'optimization_priority': st.session_state.cutting_parameters.optimization_priority
        },
        'optimization_results': st.session_state.optimization_results if st.session_state.optimization_results else None
    }
    
    return json.dumps(export_data, indent=2, default=str)

if __name__ == "__main__":
    main()