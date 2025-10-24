# 🪵 Greenstrand Packaging — Cutting Plan Optimizer

A production-ready Streamlit application to optimize wooden cutting plans for packaging manufacturing. It maximizes material utilization, minimizes waste, and produces clear operator-friendly cutting diagrams with CSV/PDF exports.

### Features
- Inventory and parts CSV upload, sample data loader
- Kerf, tolerance, offcut, and priority parameters
- 3D guillotine heuristic (length → width → thickness) with offcut tracking
- Per-stick SVG plans and composite view
- CSV and PDF report exports

### Quick start
1) Install dependencies
```
python3 -m pip install -r requirements.txt
```
2) Run the app
```
streamlit run streamlit_app.py
```
3) In the app, click “Load Sample Data” or upload your own CSVs from `sample_data/` format.

### CSV formats
Inventory (`sample_data/inventory.csv`):
```
name,length_mm,width_mm,thickness_mm,quantity,cost_per_unit,material
"KD Pine 2400x100x38",2400,100,38,10,12.5,Pine
```

Parts (`sample_data/parts.csv`):
```
key,name,material,length_mm,width_mm,thickness_mm,quantity_total,allow_rotation_length_width,allow_rotation_width_thickness,allow_rotation_length_thickness,enforce_grain_along_length,priority
"plank_1000x90x38","Plank","Pine",1000,90,38,30,True,False,False,True,2
```

### Notes
- The initial optimizer uses a greedy guillotine heuristic and respects kerf/tolerances; further enhancements (rotation with grain checks, resawing) can be added in `optimizer/guillotine.py`.
