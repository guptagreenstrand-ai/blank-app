import io
from typing import List, Dict

import streamlit as st

from optimizer.io import (
    load_inventory_filelike,
    load_parts_filelike,
    load_inventory_csv,
    load_parts_csv,
    default_parameters,
)
from optimizer.models import InventoryItem, PartRequirement, Dimension3D, CuttingParameters
from optimizer.guillotine import optimize_cutting_plan, OptimizationResult
from optimizer.svg import render_stick_svg, render_composite_svg
from optimizer.reports import export_csv, export_pdf


st.set_page_config(
    page_title="Greenstrand Cutting Plan Optimizer",
    page_icon="🪵",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_state() -> None:
    if "inventory_rows" not in st.session_state:
        st.session_state.inventory_rows = []  # list[dict]
    if "part_rows" not in st.session_state:
        st.session_state.part_rows = []  # list[dict]
    if "parameters" not in st.session_state:
        st.session_state.parameters = default_parameters()
    if "result" not in st.session_state:
        st.session_state.result = None


def to_inventory_items(rows: List[Dict]) -> List[InventoryItem]:
    items: List[InventoryItem] = []
    for r in rows:
        try:
            items.append(
                InventoryItem(
                    name=str(r.get("name", "")),
                    dimensions_mm=Dimension3D(
                        length_mm=float(r.get("length_mm", 0) or 0),
                        width_mm=float(r.get("width_mm", 0) or 0),
                        thickness_mm=float(r.get("thickness_mm", 0) or 0),
                    ),
                    quantity=int(r.get("quantity", 0) or 0),
                    cost_per_unit=float(r.get("cost_per_unit")) if r.get("cost_per_unit") not in (None, "") else None,
                    material=(r.get("material") or None),
                )
            )
        except Exception:
            continue
    return items


def to_part_requirements(rows: List[Dict]) -> List[PartRequirement]:
    parts: List[PartRequirement] = []
    for r in rows:
        try:
            parts.append(
                PartRequirement(
                    key=str(r.get("key", "")),
                    name=str(r.get("name", "")),
                    material=str(r.get("material", "")),
                    required_dimensions_mm=Dimension3D(
                        length_mm=float(r.get("length_mm", 0) or 0),
                        width_mm=float(r.get("width_mm", 0) or 0),
                        thickness_mm=float(r.get("thickness_mm", 0) or 0),
                    ),
                    quantity_total=int(r.get("quantity_total", 0) or 0),
                    allow_rotation_length_width=bool(r.get("allow_rotation_length_width", False)),
                    allow_rotation_width_thickness=bool(r.get("allow_rotation_width_thickness", False)),
                    allow_rotation_length_thickness=bool(r.get("allow_rotation_length_thickness", False)),
                    enforce_grain_along_length=bool(r.get("enforce_grain_along_length", True)),
                    priority=int(r.get("priority", 0) or 0),
                )
            )
        except Exception:
            continue
    return parts


def step_inputs() -> None:
    st.header("Step 1 — Input Inventory and Parts")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Inventory")
        inv_upload = st.file_uploader("Upload inventory CSV", type=["csv"], key="inv_csv")
        if inv_upload is not None:
            try:
                rows = []
                items = load_inventory_filelike(io.StringIO(inv_upload.getvalue().decode("utf-8")))
                for it in items:
                    rows.append(
                        {
                            "name": it.name,
                            "length_mm": it.dimensions_mm.length_mm,
                            "width_mm": it.dimensions_mm.width_mm,
                            "thickness_mm": it.dimensions_mm.thickness_mm,
                            "quantity": it.quantity,
                            "cost_per_unit": it.cost_per_unit,
                            "material": it.material,
                        }
                    )
                st.session_state.inventory_rows = rows
                st.success("Inventory CSV loaded")
            except Exception as e:
                st.error(f"Failed to parse inventory CSV: {e}")

    with col2:
        st.subheader("Parts")
        parts_upload = st.file_uploader("Upload parts CSV", type=["csv"], key="parts_csv")
        if parts_upload is not None:
            try:
                rows = []
                parts = load_parts_filelike(io.StringIO(parts_upload.getvalue().decode("utf-8")))
                for p in parts:
                    rows.append(
                        {
                            "key": p.key,
                            "name": p.name,
                            "material": p.material,
                            "length_mm": p.required_dimensions_mm.length_mm,
                            "width_mm": p.required_dimensions_mm.width_mm,
                            "thickness_mm": p.required_dimensions_mm.thickness_mm,
                            "quantity_total": p.quantity_total,
                            "allow_rotation_length_width": p.allow_rotation_length_width,
                            "allow_rotation_width_thickness": p.allow_rotation_width_thickness,
                            "allow_rotation_length_thickness": p.allow_rotation_length_thickness,
                            "enforce_grain_along_length": p.enforce_grain_along_length,
                            "priority": p.priority,
                        }
                    )
                st.session_state.part_rows = rows
                st.success("Parts CSV loaded")
            except Exception as e:
                st.error(f"Failed to parse parts CSV: {e}")

    st.divider()
    col3, col4 = st.columns([1, 1])
    with col3:
        if st.button("Load Sample Data", use_container_width=True):
            try:
                sample_inv = load_inventory_csv("sample_data/inventory.csv")
                st.session_state.inventory_rows = [
                    {
                        "name": it.name,
                        "length_mm": it.dimensions_mm.length_mm,
                        "width_mm": it.dimensions_mm.width_mm,
                        "thickness_mm": it.dimensions_mm.thickness_mm,
                        "quantity": it.quantity,
                        "cost_per_unit": it.cost_per_unit,
                        "material": it.material,
                    }
                    for it in sample_inv
                ]
                sample_parts = load_parts_csv("sample_data/parts.csv")
                st.session_state.part_rows = [
                    {
                        "key": p.key,
                        "name": p.name,
                        "material": p.material,
                        "length_mm": p.required_dimensions_mm.length_mm,
                        "width_mm": p.required_dimensions_mm.width_mm,
                        "thickness_mm": p.required_dimensions_mm.thickness_mm,
                        "quantity_total": p.quantity_total,
                        "allow_rotation_length_width": p.allow_rotation_length_width,
                        "allow_rotation_width_thickness": p.allow_rotation_width_thickness,
                        "allow_rotation_length_thickness": p.allow_rotation_length_thickness,
                        "enforce_grain_along_length": p.enforce_grain_along_length,
                        "priority": p.priority,
                    }
                    for p in sample_parts
                ]
                st.success("Loaded sample data")
            except Exception as e:
                st.error(f"Failed to load sample data: {e}")

    with col4:
        with st.form("manual_add_forms"):
            st.caption("Quick add a single inventory item and part")
            st.text("Inventory item")
            inv_name = st.text_input("Name", key="inv_add_name")
            inv_L = st.number_input("Length (mm)", min_value=0.0, value=2400.0, step=10.0, key="inv_add_L")
            inv_W = st.number_input("Width (mm)", min_value=0.0, value=100.0, step=1.0, key="inv_add_W")
            inv_T = st.number_input("Thickness (mm)", min_value=0.0, value=38.0, step=1.0, key="inv_add_T")
            inv_Q = st.number_input("Quantity", min_value=0, value=1, step=1, key="inv_add_Q")
            inv_cost = st.number_input("Cost/unit", min_value=0.0, value=0.0, step=0.1, key="inv_add_cost")
            inv_mat = st.text_input("Material", value="Pine", key="inv_add_mat")

            st.text("Part requirement")
            part_key = st.text_input("Part key", key="part_add_key")
            part_name = st.text_input("Part name", key="part_add_name")
            part_mat = st.text_input("Part material", value="Pine", key="part_add_mat")
            part_L = st.number_input("Part length (mm)", min_value=0.0, value=1000.0, step=10.0, key="part_add_L")
            part_W = st.number_input("Part width (mm)", min_value=0.0, value=90.0, step=1.0, key="part_add_W")
            part_T = st.number_input("Part thickness (mm)", min_value=0.0, value=38.0, step=1.0, key="part_add_T")
            part_Q = st.number_input("Part quantity", min_value=0, value=1, step=1, key="part_add_Q")
            part_priority = st.number_input("Part priority (higher first)", min_value=0, value=0, step=1, key="part_add_P")
            part_grain = st.checkbox("Enforce grain along length", value=True, key="part_add_grain")
            submitted = st.form_submit_button("Add to tables")
            if submitted:
                if inv_name:
                    st.session_state.inventory_rows.append(
                        {
                            "name": inv_name,
                            "length_mm": inv_L,
                            "width_mm": inv_W,
                            "thickness_mm": inv_T,
                            "quantity": int(inv_Q),
                            "cost_per_unit": float(inv_cost) if inv_cost else None,
                            "material": inv_mat or None,
                        }
                    )
                if part_key:
                    st.session_state.part_rows.append(
                        {
                            "key": part_key,
                            "name": part_name,
                            "material": part_mat,
                            "length_mm": part_L,
                            "width_mm": part_W,
                            "thickness_mm": part_T,
                            "quantity_total": int(part_Q),
                            "allow_rotation_length_width": False,
                            "allow_rotation_width_thickness": False,
                            "allow_rotation_length_thickness": False,
                            "enforce_grain_along_length": bool(part_grain),
                            "priority": int(part_priority),
                        }
                    )
                st.success("Added rows")

    st.subheader("Current Inventory")
    st.dataframe(st.session_state.inventory_rows, use_container_width=True)
    st.subheader("Current Parts")
    st.dataframe(st.session_state.part_rows, use_container_width=True)


def step_parameters() -> None:
    st.header("Step 2 — Cutting Parameters")
    params: CuttingParameters = st.session_state.parameters
    col1, col2, col3 = st.columns(3)
    with col1:
        params.kerf_mm = st.number_input("Kerf (mm)", min_value=0.0, value=float(params.kerf_mm), step=0.1)
        params.min_offcut_keep_mm = st.number_input(
            "Minimum offcut to keep (mm)", min_value=0.0, value=float(params.min_offcut_keep_mm), step=1.0
        )
    with col2:
        params.tolerance.length_mm = st.number_input(
            "Tolerance length (mm)", min_value=0.0, value=float(params.tolerance.length_mm), step=0.5
        )
        params.tolerance.width_mm = st.number_input(
            "Tolerance width (mm)", min_value=0.0, value=float(params.tolerance.width_mm), step=0.5
        )
        params.tolerance.thickness_mm = st.number_input(
            "Tolerance thickness (mm)", min_value=0.0, value=float(params.tolerance.thickness_mm), step=0.5
        )
    with col3:
        params.optimization_priority = st.selectbox(
            "Optimization priority", ["efficiency", "cost", "speed"], index=["efficiency", "cost", "speed"].index(params.optimization_priority)
        )
    st.session_state.parameters = params


def step_optimize() -> None:
    st.header("Step 3 — Optimize")
    inventory_items = to_inventory_items(st.session_state.inventory_rows)
    part_requirements = to_part_requirements(st.session_state.part_rows)

    if not inventory_items or not part_requirements:
        st.warning("Please provide inventory and parts before optimizing.")
        return

    if st.button("Run optimization", type="primary"):
        with st.spinner("Optimizing cutting plan..."):
            result = optimize_cutting_plan(inventory_items, part_requirements, st.session_state.parameters)
            st.session_state.result = result
            st.success("Optimization complete")


def step_results() -> None:
    st.header("Step 4 — Results and Exports")
    result: OptimizationResult | None = st.session_state.result
    if result is None:
        st.info("Run an optimization to view results.")
        return

    m1, m2, m3 = st.columns(3)
    m1.metric("Utilization %", f"{result.utilization_percent:.2f}")
    m2.metric("Waste %", f"{result.waste_percent:.2f}")
    m3.metric("Total cuts", f"{result.total_cuts}")

    st.subheader("Per-stick plans")
    stick_labels = [f"{s.inventory_name} #{s.stick_index}" for s in result.stick_plans]
    if not stick_labels:
        st.info("No sticks were used.")
    else:
        selected = st.selectbox("Stick", options=list(range(len(stick_labels))), format_func=lambda i: stick_labels[i])
        stick = result.stick_plans[selected]
        svg = render_stick_svg(stick, px_per_mm=0.25)
        st.components.v1.html(svg, height=int(stick.dims_mm.width_mm * 0.25) + 50, scrolling=True)

    st.subheader("Composite view")
    composite = render_composite_svg(result.stick_plans, px_per_mm=0.2)
    st.components.v1.html(composite, height=400, scrolling=True)

    st.subheader("Summary by part")
    part_rows = []
    for key, summary in result.summary_by_part.items():
        part_rows.append({"part_key": key, **summary})
    st.table(part_rows)

    st.subheader("Exports")
    csv_data = export_csv(result)
    st.download_button("Download CSV", data=csv_data, file_name="cutting_plan.csv", mime="text/csv")
    try:
        pdf_bytes = export_pdf(result)
        st.download_button("Download PDF", data=pdf_bytes, file_name="cutting_plan.pdf", mime="application/pdf")
    except Exception as e:
        st.warning(f"PDF generation failed: {e}")


def main() -> None:
    init_state()
    st.title("🪵 Greenstrand Packaging — Cutting Plan Optimizer")
    st.caption("Maximize material utilization, minimize waste, and produce clear cutting plans.")

    step = st.sidebar.radio(
        "Workflow",
        options=["Inputs", "Parameters", "Optimize", "Results"],
        captions=["Upload or add data", "Kerf, tolerances, etc.", "Run optimizer", "Inspect and export"],
        index=0,
    )

    if step == "Inputs":
        step_inputs()
    elif step == "Parameters":
        step_parameters()
    elif step == "Optimize":
        step_optimize()
    elif step == "Results":
        step_results()


if __name__ == "__main__":
    main()
