# 🚀 Quick Start Guide - Greenstrand Packaging Optimizer

Get up and running in 5 minutes!

---

## ⚡ Instant Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run streamlit_app.py
```

### 3. Open in Browser

The app will automatically open at: **http://localhost:8501**

---

## 🎓 First-Time Tutorial (5 minutes)

### Step 1: Load Sample Data (30 seconds)

1. Look at the **sidebar** on the left
2. Click **"📥 Load Sample Data"** button
3. ✅ Success! You now have sample pallet data loaded

### Step 2: Explore the Data (1 minute)

**View Inventory:**
- Click **"📦 Inventory Setup"** in sidebar
- See 4 types of lumber stock with dimensions and costs
- Total value: ~$1,500

**View Parts:**
- Click **"🔧 Parts List"** in sidebar
- See 5 part types (planks, stringers, blocks, etc.)
- Total: 240 pieces needed for 10 pallets

### Step 3: Run Optimization (1 minute)

1. Click **"🚀 Optimize"** in sidebar
2. Review the pre-optimization analysis
3. Click **"🚀 Run Optimization"** button
4. Wait ~1 second for results
5. ✅ See optimization complete!

### Step 4: View Results (2 minutes)

1. Click **"📊 Results & Export"** in sidebar
2. See overall statistics:
   - Sticks used
   - Material efficiency
   - Total cost
3. View cutting plans:
   - Select different sticks from dropdown
   - See color-coded cutting diagrams
   - View cutting sequences
4. Download exports:
   - CSV summary
   - Cutting instructions (text)
   - SVG diagrams
   - Parts list

---

## 🎯 Real-World Usage Workflow

### Scenario: Planning 20 Custom Pallets

**Step 1: Clear Sample Data**
- Click **"🔄 Reset All"** in sidebar

**Step 2: Add Your Inventory**
- Go to **"📦 Inventory Setup"**
- Click **"➕ Add New Inventory Item"**
- Enter your lumber details:
  ```
  Name: Your lumber name
  Length: 2400 mm
  Width: 150 mm
  Thickness: 75 mm
  Quantity: 30
  Cost: $35.00
  ```
- Click **"➕ Add to Inventory"**
- Repeat for all lumber types

**Step 3: Define Your Parts**
- Go to **"🔧 Parts List"**
- Click **"➕ Add New Part"**
- Enter part details:
  ```
  Name: Deck Board
  Description: Top surface
  Length: 1200 mm
  Width: 100 mm
  Thickness: 20 mm
  Qty per Product: 7
  Total Products: 20
  Material: Pine
  Allow Rotation: No (visible surface)
  Priority: 9/10
  ```
- Click **"➕ Add Part"**
- Repeat for all part types

**Step 4: Adjust Parameters (Optional)**
- Go to **"⚙️ Cutting Parameters"**
- Set kerf (saw blade gap): **3 mm**
- Set min offcut to keep: **150 mm**
- Set tolerance: **2 mm**
- Choose optimization priority: **Maximize Efficiency**
- Click **"💾 Save Parameters"**

**Step 5: Optimize**
- Go to **"🚀 Optimize"**
- Review material analysis
- Click **"🚀 Run Optimization"**
- Wait for completion

**Step 6: Review & Export**
- Go to **"📊 Results & Export"**
- Review efficiency and costs
- View each cutting plan
- Download necessary files:
  - **CSV Summary** → For management reports
  - **Cutting Instructions** → For operators
  - **SVG Diagrams** → For printing/posting

---

## 💡 Pro Tips

### For Best Results

1. **Start with accurate inventory**
   - Measure your actual stock
   - Include all available lumber types
   - Set realistic costs

2. **Prioritize critical parts**
   - Set priority 9-10 for expensive/important parts
   - Set priority 6-7 for common/cheap parts

3. **Rotation guidelines**
   - ✅ Enable for: blocks, supports, internal parts
   - ❌ Disable for: visible surfaces, face boards

4. **Kerf settings**
   - Circular saw: 3-4 mm
   - Table saw: 2-3 mm
   - Precision saw: 1-2 mm

5. **Tolerance settings**
   - Tight fit: 1 mm
   - Normal: 2 mm
   - Loose fit: 3-5 mm

---

## 🔍 Understanding Results

### Efficiency Metrics

**Material Utilization: 85%** ✅ Excellent (>80%)  
**Material Utilization: 75%** ⚠️ Good (70-80%)  
**Material Utilization: 65%** ❌ Poor (<70%) - Consider adjusting parameters

### What to Look For

- **High efficiency** (>80%) = Less waste, lower costs
- **Low unassigned parts** = Good material fit
- **Reasonable stick count** = Manageable production
- **Clear cutting diagrams** = Easy for operators

---

## 🛠️ Troubleshooting

### "No optimization results"
- Make sure you added inventory and parts
- Click "🚀 Optimize" to run

### "Unassigned parts"
- Check if you have enough inventory
- Verify part dimensions fit in stock
- Consider enabling rotation for more parts
- Increase tolerance slightly

### "Low efficiency (<70%)"
- Try different lumber sizes
- Enable part rotation where possible
- Adjust min offcut threshold
- Consider different optimization priority

### Application won't start
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Run again
streamlit run streamlit_app.py
```

---

## 📱 Using on Mobile/Tablet

1. Open browser (Chrome, Safari)
2. Navigate to app URL
3. Interface adapts to screen size
4. All features available
5. Download exports work normally

---

## 🎓 Training for Operators

### Reading Cutting Diagrams

- **Green rectangles** = Planks (deck boards)
- **Blue rectangles** = Stringers (support beams)
- **Orange rectangles** = Blocks (spacers)
- **Dashed lines** = Saw cuts (kerf)
- **Grey areas** = Offcuts to keep

### Following Cutting Sequence

1. Read stick number (e.g., "Stick #1")
2. Find matching lumber in inventory
3. Follow numbered cuts in order
4. Watch for rotation indicators (↻)
5. Keep offcuts above minimum size
6. Verify dimensions before cutting

---

## 📊 Example Output

After running optimization on sample pallet data:

```
✅ Optimization Complete

Total Sticks Used:     23
Total Cuts:           142
Material Efficiency: 87.3%
Total Waste:         12.7%
Total Cost:        $892.50
Total Volume:      4.22 CFT
Computation Time:   0.85s
```

**Interpretation:**
- Need 23 pieces of lumber
- Will make 142 cuts total
- 87.3% of material used (excellent!)
- Only 12.7% waste
- Total cost under budget
- Fast computation

---

## ✅ Success Checklist

Before going to production:

- [ ] Inventory data is accurate
- [ ] All part types defined
- [ ] Parameters match your equipment
- [ ] Optimization ran successfully
- [ ] Efficiency is acceptable (>70%)
- [ ] Cutting diagrams are clear
- [ ] Operators understand instructions
- [ ] Export files downloaded
- [ ] Management approves costs

---

## 🆘 Need Help?

### Resources

1. **Full Documentation**: See `README.md`
2. **Deployment Guide**: See `DEPLOYMENT.md`
3. **Support Email**: support@greenstrand.com

### Common Questions

**Q: Can I save my work?**  
A: Currently, data is stored in browser session. Export CSV files to save. Future version will include user accounts.

**Q: Can multiple users use simultaneously?**  
A: Yes! Each user has their own session. Deploy on Streamlit Cloud or server for team access.

**Q: Can I customize colors?**  
A: Yes! Edit `visualizer.py` COLORS dictionary for custom colors.

**Q: Export to AutoCAD/CNC?**  
A: SVG export is available. DXF export planned for future version.

---

## 🚀 Next Steps

Once comfortable with the basics:

1. **Try different scenarios**
   - Load different sample data
   - Create custom inventory
   - Experiment with parameters

2. **Optimize your process**
   - Track efficiency over time
   - Compare different lumber suppliers
   - Find optimal cutting parameters

3. **Share with team**
   - Deploy on Streamlit Cloud
   - Train operators on reading diagrams
   - Establish standard procedures

4. **Provide feedback**
   - Report bugs or issues
   - Suggest new features
   - Share success stories

---

**Happy Optimizing! 🪵**

*Maximizing material usage, one cut at a time.*

---

**Last Updated:** 2025-10-24  
**Version:** 1.0.0
