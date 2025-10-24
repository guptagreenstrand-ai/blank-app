"""
Greenstrand Packaging - 3D Wooden Cutting Plan Optimizer
Professional web application for optimizing wooden cutting plans
"""

import streamlit as st
import pandas as pd
from typing import List
import time

# Import custom modules
from data_models import (
    LumberStock, Part, CuttingParameters, OptimizationPriority, 
    GrainDirection, OptimizationResult
)
from optimizer import optimize_cutting_plan
from visualizer import CuttingPlanVisualizer, generate_cutting_sequence
from export_utils import (
    generate_csv_summary, generate_cutting_instructions,
    generate_parts_summary_csv, generate_inventory_csv,
    prepare_download_filename
)
from sample_data import (
    get_sample_inventory, get_sample_parts_pallet,
    get_default_cutting_parameters, SAMPLE_SCENARIOS, get_scenario
)


# Page configuration
st.set_page_config(
    page_title="Greenstrand Packaging - Cutting Plan Optimizer",
    page_icon="🪵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #4CAF50;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1976D2;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #FFEBEE;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F44336;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'parts' not in st.session_state:
    st.session_state.parts = []
if 'optimization_result' not in st.session_state:
    st.session_state.optimization_result = None
if 'cutting_params' not in st.session_state:
    st.session_state.cutting_params = get_default_cutting_parameters()


def main():
    """Main application entry point"""
    
    # Header
    st.markdown('<div class="main-header">🪵 Greenstrand Packaging - Cutting Plan Optimizer</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <b>Professional 3D Wooden Cutting Plan Optimizer</b><br>
    Maximize material utilization • Minimize waste • Generate clear cutting diagrams for operators
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/250x80/2E7D32/FFFFFF?text=Greenstrand+Packaging", 
                use_column_width=True)
        
        st.markdown("### 📋 Navigation")
        page = st.radio(
            "Select Step:",
            ["🏠 Home", "📦 Inventory Setup", "🔧 Parts List", 
             "⚙️ Cutting Parameters", "🚀 Optimize", "📊 Results & Export"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📥 Load Sample Data"):
            load_sample_data()
            st.success("✅ Sample data loaded!")
            st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset All"):
                reset_all_data()
                st.success("✅ Data reset!")
                st.rerun()
        
        with col2:
            if st.button("💾 Save State"):
                st.info("💾 State auto-saved")
        
        st.markdown("---")
        
        # Current Status
        st.markdown("### 📈 Current Status")
        st.metric("Inventory Items", len(st.session_state.inventory))
        st.metric("Part Types", len(st.session_state.parts))
        if st.session_state.optimization_result:
            st.metric("Sticks Used", st.session_state.optimization_result.total_sticks_used)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Version:** 1.0.0  
        **For:** Industrial designers, woodworkers, packaging engineers  
        **Support:** support@greenstrand.com
        """)
    
    # Main content based on page selection
    if "Home" in page:
        show_home_page()
    elif "Inventory" in page:
        show_inventory_page()
    elif "Parts" in page:
        show_parts_page()
    elif "Parameters" in page:
        show_parameters_page()
    elif "Optimize" in page:
        show_optimize_page()
    elif "Results" in page:
        show_results_page()


def show_home_page():
    """Home page with overview and getting started"""
    
    st.markdown("## 👋 Welcome to the Cutting Plan Optimizer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 What This App Does
        
        This professional tool helps you:
        
        1. **📦 Manage Inventory** - Track available lumber and board stock
        2. **🔧 Define Parts** - Specify required cut parts with dimensions and quantities
        3. **⚙️ Set Parameters** - Configure kerf, tolerances, and optimization priorities
        4. **🚀 Optimize** - Run advanced 3D guillotine cutting algorithm
        5. **📊 View Results** - Get detailed cutting plans, visualizations, and reports
        6. **📥 Export** - Download PDF, CSV, and SVG files for operators
        
        ### 🚀 Getting Started
        
        **Option 1: Load Sample Data** (Recommended for first-time users)
        - Click "📥 Load Sample Data" in the sidebar
        - Explore a complete pallet packing example
        - Run optimization to see results
        
        **Option 2: Manual Setup**
        - Navigate to "📦 Inventory Setup" to add your lumber stock
        - Go to "🔧 Parts List" to define required parts
        - Adjust "⚙️ Cutting Parameters" as needed
        - Click "🚀 Optimize" to generate cutting plans
        
        ### 📖 Key Features
        
        ✅ **3D Guillotine Cutting Algorithm** - Advanced optimization with material nesting  
        ✅ **Rotation Support** - Automatic part rotation with grain direction enforcement  
        ✅ **Offcut Tracking** - Track and reuse leftover materials  
        ✅ **Visual Cutting Plans** - Color-coded diagrams for operators  
        ✅ **Multiple Export Formats** - PDF, CSV, SVG/PNG  
        ✅ **Real-time Validation** - Instant feedback on material availability  
        """)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Inventory Items", len(st.session_state.inventory), delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Part Types", len(st.session_state.parts), delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.optimization_result:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Optimization Status", "✅ Complete", delta=None)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            efficiency = st.session_state.optimization_result.overall_efficiency
            st.metric("Material Efficiency", f"{efficiency:.1f}%", 
                     delta=f"{efficiency - 70:.1f}% vs. 70% target")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("⚠️ **No optimization run yet**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🎓 Learn More")
        with st.expander("📚 User Guide"):
            st.markdown("""
            1. **Add inventory items** with dimensions and costs
            2. **Define parts** with quantities per product
            3. **Set cutting parameters** (kerf, tolerances)
            4. **Run optimization** algorithm
            5. **Review results** and cutting plans
            6. **Export** for production use
            """)
        
        with st.expander("🎬 Quick Demo"):
            st.markdown("""
            **Try this:**
            1. Click "📥 Load Sample Data"
            2. Go to "🚀 Optimize"
            3. Click "Run Optimization"
            4. View results in "📊 Results & Export"
            """)
        
        with st.expander("💡 Tips"):
            st.markdown("""
            - Use realistic kerf values (2-4mm for most saws)
            - Set min offcut to 100-200mm for reusability
            - Enable rotation for blocks and supports
            - Disable rotation for visible surface parts
            - Higher priority parts get assigned first
            """)


def show_inventory_page():
    """Inventory management page"""
    
    st.markdown("## 📦 Lumber Inventory Management")
    
    st.markdown("""
    <div class="info-box">
    Add your available lumber and board stock. Include dimensions (in mm), quantities, and costs.
    </div>
    """, unsafe_allow_html=True)
    
    # Add new inventory item
    with st.expander("➕ Add New Inventory Item", expanded=len(st.session_state.inventory) == 0):
        with st.form("add_inventory_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Stock Name *", 
                                    placeholder="e.g., Aus KD Pine 8'×7\"×3.5\"")
                length = st.number_input("Length (mm) *", min_value=1.0, value=2400.0, step=10.0)
                width = st.number_input("Width (mm) *", min_value=1.0, value=175.0, step=5.0)
            
            with col2:
                thickness = st.number_input("Thickness (mm) *", min_value=1.0, value=90.0, step=5.0)
                quantity = st.number_input("Quantity *", min_value=1, value=10, step=1)
                cost = st.number_input("Cost per Unit ($)", min_value=0.0, value=45.50, step=0.5)
            
            submitted = st.form_submit_button("➕ Add to Inventory")
            
            if submitted:
                if name:
                    stock = LumberStock(
                        name=name,
                        length=length,
                        width=width,
                        thickness=thickness,
                        quantity=quantity,
                        cost_per_unit=cost
                    )
                    st.session_state.inventory.append(stock)
                    st.success(f"✅ Added: {name}")
                    st.rerun()
                else:
                    st.error("❌ Please provide a stock name")
    
    # Display current inventory
    if st.session_state.inventory:
        st.markdown("### 📋 Current Inventory")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        total_items = len(st.session_state.inventory)
        total_pieces = sum(s.quantity for s in st.session_state.inventory)
        total_value = sum(s.quantity * s.cost_per_unit for s in st.session_state.inventory)
        total_volume = sum(s.quantity * s.volume_cft for s in st.session_state.inventory)
        
        with col1:
            st.metric("Stock Types", total_items)
        with col2:
            st.metric("Total Pieces", total_pieces)
        with col3:
            st.metric("Total Value", f"${total_value:.2f}")
        with col4:
            st.metric("Total Volume", f"{total_volume:.2f} CFT")
        
        # Inventory table
        inventory_data = []
        for i, stock in enumerate(st.session_state.inventory):
            inventory_data.append({
                'Index': i,
                'Name': stock.name,
                'Length (mm)': stock.length,
                'Width (mm)': stock.width,
                'Thickness (mm)': stock.thickness,
                'Qty': stock.quantity,
                'Cost/Unit': f"${stock.cost_per_unit:.2f}",
                'Total Value': f"${stock.quantity * stock.cost_per_unit:.2f}",
                'Volume (CFT)': f"{stock.volume_cft * stock.quantity:.4f}"
            })
        
        df = pd.DataFrame(inventory_data)
        st.dataframe(df.drop(columns=['Index']), use_container_width=True, hide_index=True)
        
        # Delete items
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            item_to_delete = st.selectbox(
                "Select item to remove:",
                options=range(len(st.session_state.inventory)),
                format_func=lambda i: st.session_state.inventory[i].name
            )
        with col2:
            if st.button("🗑️ Remove Selected"):
                del st.session_state.inventory[item_to_delete]
                st.success("✅ Item removed")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear All"):
                st.session_state.inventory = []
                st.success("✅ Inventory cleared")
                st.rerun()
        
        # Export inventory
        st.markdown("---")
        csv_data = generate_inventory_csv(st.session_state.inventory)
        st.download_button(
            label="📥 Download Inventory CSV",
            data=csv_data,
            file_name=prepare_download_filename("inventory", "csv"),
            mime="text/csv"
        )
    else:
        st.markdown("""
        <div class="warning-box">
        ⚠️ <b>No inventory items added yet.</b><br>
        Add lumber stock using the form above or load sample data from the sidebar.
        </div>
        """, unsafe_allow_html=True)


def show_parts_page():
    """Parts list management page"""
    
    st.markdown("## 🔧 Parts List Management")
    
    st.markdown("""
    <div class="info-box">
    Define the parts you need to cut. Specify dimensions, quantities, and constraints.
    </div>
    """, unsafe_allow_html=True)
    
    # Add new part
    with st.expander("➕ Add New Part", expanded=len(st.session_state.parts) == 0):
        with st.form("add_part_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                part_name = st.text_input("Part Name *", 
                                         placeholder="e.g., Top Deck Board (Plank)")
                description = st.text_input("Description", 
                                           placeholder="e.g., Top surface boards for pallet deck")
                length = st.number_input("Length (mm) *", min_value=1.0, value=1200.0, step=10.0)
                width = st.number_input("Width (mm) *", min_value=1.0, value=100.0, step=5.0)
                thickness = st.number_input("Thickness (mm) *", min_value=1.0, value=22.0, step=1.0)
            
            with col2:
                qty_per_product = st.number_input("Quantity per Product *", 
                                                 min_value=1, value=7, step=1)
                total_products = st.number_input("Total Products *", 
                                                min_value=1, value=10, step=1)
                material_type = st.text_input("Material Type", value="Pine")
                allow_rotation = st.checkbox("Allow Rotation", value=True)
                priority = st.slider("Priority (1=Low, 10=High)", 1, 10, 8)
            
            submitted = st.form_submit_button("➕ Add Part")
            
            if submitted:
                if part_name:
                    part = Part(
                        name=part_name,
                        description=description,
                        length=length,
                        width=width,
                        thickness=thickness,
                        quantity_per_product=qty_per_product,
                        total_products=total_products,
                        material_type=material_type,
                        allow_rotation=allow_rotation,
                        priority=priority
                    )
                    st.session_state.parts.append(part)
                    st.success(f"✅ Added: {part_name}")
                    st.rerun()
                else:
                    st.error("❌ Please provide a part name")
    
    # Display current parts
    if st.session_state.parts:
        st.markdown("### 📋 Current Parts List")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        total_part_types = len(st.session_state.parts)
        total_pieces = sum(p.total_quantity for p in st.session_state.parts)
        total_volume = sum(p.total_volume for p in st.session_state.parts)
        total_volume_cft = total_volume / 28316846.592
        
        with col1:
            st.metric("Part Types", total_part_types)
        with col2:
            st.metric("Total Pieces", total_pieces)
        with col3:
            st.metric("Total Volume", f"{total_volume_cft:.2f} CFT")
        with col4:
            avg_priority = sum(p.priority for p in st.session_state.parts) / len(st.session_state.parts)
            st.metric("Avg Priority", f"{avg_priority:.1f}/10")
        
        # Parts table
        parts_data = []
        for i, part in enumerate(st.session_state.parts):
            parts_data.append({
                'Index': i,
                'Name': part.name,
                'Dims (L×W×T mm)': f"{part.length:.0f}×{part.width:.0f}×{part.thickness:.0f}",
                'Qty/Product': part.quantity_per_product,
                'Products': part.total_products,
                'Total Qty': part.total_quantity,
                'Material': part.material_type,
                'Rotate': '✓' if part.allow_rotation else '✗',
                'Priority': part.priority
            })
        
        df = pd.DataFrame(parts_data)
        st.dataframe(df.drop(columns=['Index']), use_container_width=True, hide_index=True)
        
        # Delete parts
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            part_to_delete = st.selectbox(
                "Select part to remove:",
                options=range(len(st.session_state.parts)),
                format_func=lambda i: st.session_state.parts[i].name
            )
        with col2:
            if st.button("🗑️ Remove Selected"):
                del st.session_state.parts[part_to_delete]
                st.success("✅ Part removed")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear All"):
                st.session_state.parts = []
                st.success("✅ Parts list cleared")
                st.rerun()
        
        # Export parts list
        st.markdown("---")
        csv_data = generate_parts_summary_csv(st.session_state.parts)
        st.download_button(
            label="📥 Download Parts List CSV",
            data=csv_data,
            file_name=prepare_download_filename("parts_list", "csv"),
            mime="text/csv"
        )
    else:
        st.markdown("""
        <div class="warning-box">
        ⚠️ <b>No parts added yet.</b><br>
        Add required parts using the form above or load sample data from the sidebar.
        </div>
        """, unsafe_allow_html=True)


def show_parameters_page():
    """Cutting parameters configuration page"""
    
    st.markdown("## ⚙️ Cutting Parameters")
    
    st.markdown("""
    <div class="info-box">
    Configure cutting constraints, tolerances, and optimization priorities.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Cutting Constraints")
        
        kerf = st.number_input(
            "Kerf - Saw Blade Gap (mm)",
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.cutting_params.kerf,
            step=0.5,
            help="Width of material removed by saw blade"
        )
        
        min_offcut = st.number_input(
            "Minimum Offcut to Keep (mm)",
            min_value=0.0,
            max_value=500.0,
            value=st.session_state.cutting_params.min_offcut_to_keep,
            step=10.0,
            help="Minimum size of leftover pieces worth keeping"
        )
        
        tolerance = st.number_input(
            "Tolerance - Allowable Deviation (mm)",
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.cutting_params.tolerance,
            step=0.5,
            help="Acceptable deviation from target dimensions"
        )
        
        grain_direction = st.selectbox(
            "Grain Direction Enforcement",
            options=[GrainDirection.NONE, GrainDirection.LENGTH, GrainDirection.WIDTH],
            format_func=lambda x: x.value.replace('_', ' ').title(),
            index=0,
            help="Enforce grain direction for visible parts"
        )
    
    with col2:
        st.markdown("### 🎯 Optimization Settings")
        
        optimization_priority = st.selectbox(
            "Optimization Priority",
            options=[
                OptimizationPriority.MAXIMIZE_EFFICIENCY,
                OptimizationPriority.MINIMIZE_COST,
                OptimizationPriority.FASTEST_CUT
            ],
            format_func=lambda x: x.value.replace('_', ' ').title(),
            index=0,
            help="Primary optimization goal"
        )
        
        allow_resawing = st.checkbox(
            "Allow Resawing",
            value=st.session_state.cutting_params.allow_resawing,
            help="Allow cutting stock lengthwise to reduce thickness"
        )
        
        allow_planing = st.checkbox(
            "Allow Planing",
            value=st.session_state.cutting_params.allow_planing,
            help="Allow planing to reduce thickness slightly"
        )
        
        if allow_planing:
            max_planing_depth = st.number_input(
                "Maximum Planing Depth (mm)",
                min_value=0.0,
                max_value=20.0,
                value=st.session_state.cutting_params.max_planing_depth,
                step=0.5,
                help="Maximum material that can be removed by planing"
            )
        else:
            max_planing_depth = 0.0
    
    # Update button
    if st.button("💾 Save Parameters", type="primary"):
        st.session_state.cutting_params = CuttingParameters(
            kerf=kerf,
            min_offcut_to_keep=min_offcut,
            tolerance=tolerance,
            grain_direction=grain_direction,
            optimization_priority=optimization_priority,
            allow_resawing=allow_resawing,
            allow_planing=allow_planing,
            max_planing_depth=max_planing_depth
        )
        st.success("✅ Parameters saved successfully!")
    
    # Display current parameters
    st.markdown("---")
    st.markdown("### 📋 Current Configuration")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Kerf", f"{st.session_state.cutting_params.kerf} mm")
        st.metric("Min Offcut", f"{st.session_state.cutting_params.min_offcut_to_keep} mm")
    with col2:
        st.metric("Tolerance", f"{st.session_state.cutting_params.tolerance} mm")
        st.metric("Grain Direction", st.session_state.cutting_params.grain_direction.value.title())
    with col3:
        st.metric("Priority", st.session_state.cutting_params.optimization_priority.value.replace('_', ' ').title())
        st.metric("Resawing", "Enabled" if st.session_state.cutting_params.allow_resawing else "Disabled")


def show_optimize_page():
    """Optimization execution page"""
    
    st.markdown("## 🚀 Run Optimization")
    
    # Validation
    inventory_ok = len(st.session_state.inventory) > 0
    parts_ok = len(st.session_state.parts) > 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if inventory_ok:
            st.success(f"✅ Inventory: {len(st.session_state.inventory)} items")
        else:
            st.error("❌ No inventory")
    with col2:
        if parts_ok:
            st.success(f"✅ Parts: {len(st.session_state.parts)} types")
        else:
            st.error("❌ No parts")
    with col3:
        st.info(f"⚙️ Parameters configured")
    
    if not (inventory_ok and parts_ok):
        st.markdown("""
        <div class="error-box">
        ⚠️ <b>Cannot run optimization:</b><br>
        Please add inventory items and parts before running optimization.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Pre-optimization analysis
    st.markdown("### 📊 Pre-Optimization Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Material Requirements:**")
        total_parts = sum(p.total_quantity for p in st.session_state.parts)
        total_volume_needed = sum(p.total_volume for p in st.session_state.parts)
        total_volume_needed_cft = total_volume_needed / 28316846.592
        
        st.write(f"- Total parts needed: **{total_parts}**")
        st.write(f"- Total volume needed: **{total_volume_needed_cft:.4f} CFT**")
    
    with col2:
        st.markdown("**Available Material:**")
        total_stock = sum(s.quantity for s in st.session_state.inventory)
        total_volume_available = sum(s.quantity * s.volume for s in st.session_state.inventory)
        total_volume_available_cft = total_volume_available / 28316846.592
        
        st.write(f"- Total stock pieces: **{total_stock}**")
        st.write(f"- Total volume available: **{total_volume_available_cft:.4f} CFT**")
    
    # Material sufficiency check
    if total_volume_available >= total_volume_needed:
        st.markdown("""
        <div class="success-box">
        ✅ <b>Sufficient material available</b> (based on volume comparison)
        </div>
        """, unsafe_allow_html=True)
    else:
        shortage = total_volume_needed_cft - total_volume_available_cft
        st.markdown(f"""
        <div class="warning-box">
        ⚠️ <b>Potential material shortage:</b> {shortage:.4f} CFT short<br>
        Note: This is a rough estimate. Actual fit depends on dimensions and cutting efficiency.
        </div>
        """, unsafe_allow_html=True)
    
    # Run optimization
    st.markdown("---")
    st.markdown("### 🎯 Execute Optimization")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Optimization", type="primary", use_container_width=True):
            run_optimization()


def run_optimization():
    """Execute the optimization algorithm"""
    
    with st.spinner("⏳ Running optimization algorithm..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate progress updates
        status_text.text("Analyzing inventory and parts...")
        progress_bar.progress(20)
        time.sleep(0.3)
        
        status_text.text("Sorting parts by priority...")
        progress_bar.progress(40)
        time.sleep(0.3)
        
        status_text.text("Running 3D guillotine cutting algorithm...")
        progress_bar.progress(60)
        
        # Run actual optimization
        result = optimize_cutting_plan(
            st.session_state.inventory,
            st.session_state.parts,
            st.session_state.cutting_params
        )
        
        progress_bar.progress(80)
        status_text.text("Calculating statistics...")
        time.sleep(0.2)
        
        progress_bar.progress(100)
        status_text.text("Optimization complete!")
        
        # Store result
        st.session_state.optimization_result = result
        
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
    
    # Show results summary
    if result.success:
        st.success("✅ Optimization completed successfully!")
    else:
        st.warning("⚠️ Optimization completed with unassigned parts")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sticks Used", result.total_sticks_used)
    with col2:
        st.metric("Total Cuts", result.total_cuts)
    with col3:
        st.metric("Efficiency", f"{result.overall_efficiency:.1f}%")
    with col4:
        st.metric("Time", f"{result.computation_time:.2f}s")
    
    st.info("📊 View detailed results in the 'Results & Export' page")


def show_results_page():
    """Results and export page"""
    
    st.markdown("## 📊 Optimization Results & Export")
    
    if not st.session_state.optimization_result:
        st.markdown("""
        <div class="warning-box">
        ⚠️ <b>No optimization results available.</b><br>
        Please run optimization first using the '🚀 Optimize' page.
        </div>
        """, unsafe_allow_html=True)
        return
    
    result = st.session_state.optimization_result
    
    # Overall summary
    st.markdown("### 📈 Overall Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Sticks Used", result.total_sticks_used)
    with col2:
        st.metric("Total Cuts", result.total_cuts)
    with col3:
        st.metric("Efficiency", f"{result.overall_efficiency:.1f}%", 
                 delta=f"{result.overall_efficiency - 75:.1f}%" if result.overall_efficiency > 75 else None)
    with col4:
        st.metric("Total Cost", f"${result.total_cost:.2f}")
    with col5:
        st.metric("Volume Used", f"{result.total_volume_used_cft:.2f} CFT")
    
    # Status indicator
    if result.success:
        st.markdown("""
        <div class="success-box">
        ✅ <b>All parts successfully assigned!</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="error-box">
        ❌ <b>Warning:</b> {len(result.unassigned_parts)} part type(s) could not be assigned.
        </div>
        """, unsafe_allow_html=True)
        
        # Show unassigned parts
        with st.expander("⚠️ View Unassigned Parts"):
            for part, qty in result.unassigned_parts:
                st.write(f"- **{part.name}**: {qty} pieces")
                st.write(f"  Dimensions: {part.length}×{part.width}×{part.thickness} mm")
    
    # Cutting plans visualization
    st.markdown("---")
    st.markdown("### 📐 Cutting Plans")
    
    if result.cutting_plans:
        visualizer = CuttingPlanVisualizer()
        
        # Plan selector
        plan_index = st.selectbox(
            "Select cutting plan to view:",
            options=range(len(result.cutting_plans)),
            format_func=lambda i: f"Stick #{i+1} - {result.cutting_plans[i].stock.name} ({result.cutting_plans[i].material_utilized:.1f}% utilized)"
        )
        
        plan = result.cutting_plans[plan_index]
        
        # Display SVG
        svg = visualizer.generate_cutting_plan_svg(plan, width=1200)
        st.components.v1.html(svg, height=400, scrolling=False)
        
        # Cutting sequence
        with st.expander("📋 View Cutting Sequence"):
            instructions = generate_cutting_sequence(plan)
            st.code("\n".join(instructions), language="")
        
        # Plan details
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Material Utilized", f"{plan.material_utilized:.1f}%")
        with col2:
            st.metric("Waste", f"{plan.waste_percentage:.1f}%")
        with col3:
            st.metric("Total Cuts", plan.total_cuts)
    
    # Detailed statistics
    st.markdown("---")
    st.markdown("### 📊 Detailed Statistics")
    
    tab1, tab2, tab3 = st.tabs(["📋 Parts Summary", "📦 Stock Usage", "📈 Efficiency Analysis"])
    
    with tab1:
        # Parts assignment summary
        parts_assigned = {}
        for plan in result.cutting_plans:
            for cut in plan.cuts:
                part_id = cut.part.id
                parts_assigned[part_id] = parts_assigned.get(part_id, 0) + 1
        
        parts_data = []
        for part in st.session_state.parts:
            assigned = parts_assigned.get(part.id, 0)
            required = part.total_quantity
            status = "✅ Complete" if assigned >= required else f"⚠️ Incomplete ({assigned}/{required})"
            
            parts_data.append({
                'Part Name': part.name,
                'Required': required,
                'Assigned': assigned,
                'Status': status,
                'Dimensions (mm)': f"{part.length}×{part.width}×{part.thickness}"
            })
        
        df_parts = pd.DataFrame(parts_data)
        st.dataframe(df_parts, use_container_width=True, hide_index=True)
    
    with tab2:
        # Stock usage summary
        stock_usage = {}
        for plan in result.cutting_plans:
            stock_id = plan.stock.id
            if stock_id not in stock_usage:
                stock_usage[stock_id] = {
                    'stock': plan.stock,
                    'count': 0,
                    'total_efficiency': 0
                }
            stock_usage[stock_id]['count'] += 1
            stock_usage[stock_id]['total_efficiency'] += plan.material_utilized
        
        stock_data = []
        for stock_id, usage in stock_usage.items():
            stock = usage['stock']
            count = usage['count']
            avg_efficiency = usage['total_efficiency'] / count
            total_cost = stock.cost_per_unit * count
            
            stock_data.append({
                'Stock Name': stock.name,
                'Quantity Used': count,
                'Avg Efficiency': f"{avg_efficiency:.1f}%",
                'Cost per Unit': f"${stock.cost_per_unit:.2f}",
                'Total Cost': f"${total_cost:.2f}",
                'Dimensions (mm)': f"{stock.length}×{stock.width}×{stock.thickness}"
            })
        
        df_stock = pd.DataFrame(stock_data)
        st.dataframe(df_stock, use_container_width=True, hide_index=True)
    
    with tab3:
        # Efficiency analysis
        efficiencies = [plan.material_utilized for plan in result.cutting_plans]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Efficiency", f"{sum(efficiencies)/len(efficiencies):.1f}%")
        with col2:
            st.metric("Best Plan", f"{max(efficiencies):.1f}%")
        with col3:
            st.metric("Worst Plan", f"{min(efficiencies):.1f}%")
        
        # Efficiency distribution
        import plotly.express as px
        fig = px.bar(
            x=[f"Stick #{i+1}" for i in range(len(efficiencies))],
            y=efficiencies,
            labels={'x': 'Cutting Plan', 'y': 'Material Utilization (%)'},
            title='Material Utilization by Stick'
        )
        fig.update_traces(marker_color='#4CAF50')
        st.plotly_chart(fig, use_container_width=True)
    
    # Export section
    st.markdown("---")
    st.markdown("### 📥 Export Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # CSV summary
        csv_summary = generate_csv_summary(
            result, st.session_state.parts, st.session_state.inventory
        )
        st.download_button(
            label="📊 Download CSV Summary",
            data=csv_summary,
            file_name=prepare_download_filename("cutting_plan_summary", "csv"),
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Cutting instructions
        instructions_text = generate_cutting_instructions(result)
        st.download_button(
            label="📋 Download Instructions",
            data=instructions_text,
            file_name=prepare_download_filename("cutting_instructions", "txt"),
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        # SVG export (individual plan)
        if result.cutting_plans:
            visualizer = CuttingPlanVisualizer()
            svg_data = visualizer.generate_cutting_plan_svg(result.cutting_plans[plan_index])
            st.download_button(
                label="🖼️ Download Plan SVG",
                data=svg_data,
                file_name=prepare_download_filename(f"cutting_plan_{plan_index+1}", "svg"),
                mime="image/svg+xml",
                use_container_width=True
            )
    
    with col4:
        # Parts list CSV
        parts_csv = generate_parts_summary_csv(st.session_state.parts)
        st.download_button(
            label="🔧 Download Parts CSV",
            data=parts_csv,
            file_name=prepare_download_filename("parts_list", "csv"),
            mime="text/csv",
            use_container_width=True
        )


def load_sample_data():
    """Load sample pallet packing data"""
    scenario = get_scenario("Standard Pallet (1200×1000)")
    st.session_state.inventory = scenario['inventory']
    st.session_state.parts = scenario['parts']
    st.session_state.cutting_params = scenario['parameters']
    st.session_state.optimization_result = None


def reset_all_data():
    """Reset all data to initial state"""
    st.session_state.inventory = []
    st.session_state.parts = []
    st.session_state.cutting_params = get_default_cutting_parameters()
    st.session_state.optimization_result = None


if __name__ == "__main__":
    main()
