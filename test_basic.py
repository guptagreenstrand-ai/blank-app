"""
Basic Test Suite for Greenstrand Packaging Optimizer
Run with: python test_basic.py
"""

import sys
from typing import List

# Import our modules
from data_models import LumberStock, Part, CuttingParameters, OptimizationPriority
from optimizer import optimize_cutting_plan
from sample_data import get_sample_inventory, get_sample_parts_pallet, get_default_cutting_parameters


def test_data_models():
    """Test data model creation"""
    print("🧪 Testing Data Models...")
    
    # Test LumberStock
    stock = LumberStock(
        name="Test Pine",
        length=2400,
        width=150,
        thickness=75,
        quantity=10,
        cost_per_unit=35.0
    )
    assert stock.volume > 0, "Volume calculation failed"
    assert stock.volume_cft > 0, "CFT calculation failed"
    print("  ✅ LumberStock model works")
    
    # Test Part
    part = Part(
        name="Test Plank",
        description="Test part",
        length=1200,
        width=100,
        thickness=20,
        quantity_per_product=5,
        total_products=10,
        material_type="Pine"
    )
    assert part.total_quantity == 50, "Quantity calculation failed"
    assert part.volume > 0, "Volume calculation failed"
    print("  ✅ Part model works")
    
    # Test CuttingParameters
    params = CuttingParameters(
        kerf=3.0,
        min_offcut_to_keep=150.0,
        tolerance=2.0
    )
    assert params.kerf == 3.0, "Parameters not set correctly"
    print("  ✅ CuttingParameters model works")
    
    print("✅ Data Models test passed!\n")


def test_sample_data():
    """Test sample data loading"""
    print("🧪 Testing Sample Data...")
    
    inventory = get_sample_inventory()
    assert len(inventory) > 0, "No inventory loaded"
    print(f"  ✅ Loaded {len(inventory)} inventory items")
    
    parts = get_sample_parts_pallet()
    assert len(parts) > 0, "No parts loaded"
    print(f"  ✅ Loaded {len(parts)} part types")
    
    params = get_default_cutting_parameters()
    assert params.kerf > 0, "Invalid parameters"
    print("  ✅ Parameters loaded")
    
    print("✅ Sample Data test passed!\n")


def test_optimization_simple():
    """Test basic optimization"""
    print("🧪 Testing Basic Optimization...")
    
    # Create simple test case
    inventory = [
        LumberStock(
            name="Test Board",
            length=2000,
            width=200,
            thickness=50,
            quantity=5,
            cost_per_unit=20.0
        )
    ]
    
    parts = [
        Part(
            name="Small Block",
            description="Test block",
            length=400,
            width=150,
            thickness=40,
            quantity_per_product=2,
            total_products=3,
            material_type="Test"
        )
    ]
    
    params = CuttingParameters(kerf=3.0, min_offcut_to_keep=100.0, tolerance=2.0)
    
    # Run optimization
    result = optimize_cutting_plan(inventory, parts, params)
    
    assert result is not None, "Optimization returned None"
    assert result.computation_time > 0, "Computation time not recorded"
    print(f"  ✅ Optimization completed in {result.computation_time:.3f}s")
    print(f"  📊 Sticks used: {result.total_sticks_used}")
    print(f"  📊 Efficiency: {result.overall_efficiency:.1f}%")
    
    print("✅ Basic Optimization test passed!\n")


def test_optimization_complex():
    """Test complex optimization with sample pallet data"""
    print("🧪 Testing Complex Optimization (Sample Pallet)...")
    
    inventory = get_sample_inventory()
    parts = get_sample_parts_pallet()
    params = get_default_cutting_parameters()
    
    # Run optimization
    print("  ⏳ Running optimization algorithm...")
    result = optimize_cutting_plan(inventory, parts, params)
    
    assert result is not None, "Optimization failed"
    print(f"  ✅ Optimization completed in {result.computation_time:.3f}s")
    
    # Check results
    print(f"\n  📊 RESULTS:")
    print(f"     Sticks Used: {result.total_sticks_used}")
    print(f"     Total Cuts: {result.total_cuts}")
    print(f"     Efficiency: {result.overall_efficiency:.1f}%")
    print(f"     Waste: {result.total_waste:.1f}%")
    print(f"     Total Cost: ${result.total_cost:.2f}")
    print(f"     Volume: {result.total_volume_used_cft:.4f} CFT")
    
    if result.success:
        print(f"  ✅ All parts assigned successfully!")
    else:
        print(f"  ⚠️  {len(result.unassigned_parts)} part types unassigned")
        for part, qty in result.unassigned_parts:
            print(f"     - {part.name}: {qty} pieces")
    
    assert result.total_sticks_used > 0, "No sticks used"
    assert result.overall_efficiency > 0, "Zero efficiency"
    
    print("\n✅ Complex Optimization test passed!\n")


def test_visualization():
    """Test visualization generation"""
    print("🧪 Testing Visualization...")
    
    from visualizer import CuttingPlanVisualizer
    
    # Create simple cutting plan
    inventory = get_sample_inventory()
    parts = get_sample_parts_pallet()
    params = get_default_cutting_parameters()
    
    result = optimize_cutting_plan(inventory, parts, params)
    
    if result.cutting_plans:
        visualizer = CuttingPlanVisualizer()
        svg = visualizer.generate_cutting_plan_svg(result.cutting_plans[0])
        
        assert svg is not None, "SVG generation failed"
        assert "<svg" in svg, "Invalid SVG format"
        assert "</svg>" in svg, "Incomplete SVG"
        
        print(f"  ✅ Generated SVG ({len(svg)} characters)")
    else:
        print("  ⚠️  No cutting plans to visualize")
    
    print("✅ Visualization test passed!\n")


def test_export():
    """Test export utilities"""
    print("🧪 Testing Export Utilities...")
    
    from export_utils import generate_csv_summary, generate_cutting_instructions
    
    inventory = get_sample_inventory()
    parts = get_sample_parts_pallet()
    params = get_default_cutting_parameters()
    
    result = optimize_cutting_plan(inventory, parts, params)
    
    # Test CSV export
    csv_data = generate_csv_summary(result, parts, inventory)
    assert csv_data is not None, "CSV generation failed"
    assert len(csv_data) > 0, "Empty CSV"
    assert "OVERALL STATISTICS" in csv_data, "Missing CSV header"
    print(f"  ✅ Generated CSV summary ({len(csv_data)} characters)")
    
    # Test instructions export
    instructions = generate_cutting_instructions(result)
    assert instructions is not None, "Instructions generation failed"
    assert len(instructions) > 0, "Empty instructions"
    assert "CUTTING INSTRUCTIONS" in instructions, "Missing instructions header"
    print(f"  ✅ Generated cutting instructions ({len(instructions)} characters)")
    
    print("✅ Export test passed!\n")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🚀 GREENSTRAND PACKAGING OPTIMIZER - TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        ("Data Models", test_data_models),
        ("Sample Data", test_sample_data),
        ("Simple Optimization", test_optimization_simple),
        ("Complex Optimization", test_optimization_complex),
        ("Visualization", test_visualization),
        ("Export", test_export),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_name} test FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}\n")
            failed += 1
    
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("The application is ready to use!")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
