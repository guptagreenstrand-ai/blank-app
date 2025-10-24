"""
Sample Data for Testing and Demonstration
Provides realistic pallet packing examples
"""

from data_models import (
    LumberStock, Part, CuttingParameters, 
    OptimizationPriority, GrainDirection
)


def get_sample_inventory():
    """Get sample lumber inventory for pallet manufacturing"""
    return [
        LumberStock(
            name="Aus KD Pine 8'×7\"×3.5\"",
            length=2400,  # 8 feet in mm
            width=175,    # 7 inches in mm
            thickness=90, # 3.5 inches in mm
            quantity=20,
            cost_per_unit=45.50
        ),
        LumberStock(
            name="Hardwood 6'×5\"×2\"",
            length=1800,  # 6 feet
            width=125,    # 5 inches
            thickness=50, # 2 inches
            quantity=15,
            cost_per_unit=32.00
        ),
        LumberStock(
            name="Pine Board 10'×8\"×1.5\"",
            length=3000,  # 10 feet
            width=200,    # 8 inches
            thickness=38, # 1.5 inches
            quantity=10,
            cost_per_unit=28.75
        ),
        LumberStock(
            name="Standard 2×4×8'",
            length=2400,  # 8 feet
            width=90,     # ~3.5 inches
            thickness=40, # ~1.5 inches
            quantity=30,
            cost_per_unit=12.50
        )
    ]


def get_sample_parts_pallet():
    """Get sample parts list for standard pallet construction"""
    return [
        Part(
            name="Top Deck Board (Plank)",
            description="Top surface boards for pallet deck",
            length=1200,    # 1200mm
            width=100,      # 100mm
            thickness=22,   # 22mm
            quantity_per_product=7,
            total_products=10,
            material_type="Pine",
            allow_rotation=False,
            priority=9
        ),
        Part(
            name="Stringer",
            description="Load-bearing stringers running lengthwise",
            length=1200,    # 1200mm
            width=100,      # 100mm
            thickness=75,   # 75mm
            quantity_per_product=3,
            total_products=10,
            material_type="Hardwood",
            allow_rotation=False,
            priority=10
        ),
        Part(
            name="Block",
            description="Support blocks between decks",
            length=145,     # 145mm
            width=100,      # 100mm
            thickness=90,   # 90mm
            quantity_per_product=9,
            total_products=10,
            material_type="Pine",
            allow_rotation=True,
            priority=8
        ),
        Part(
            name="Bottom Deck Board",
            description="Bottom surface boards",
            length=1200,    # 1200mm
            width=100,      # 100mm
            thickness=22,   # 22mm
            quantity_per_product=3,
            total_products=10,
            material_type="Pine",
            allow_rotation=False,
            priority=7
        ),
        Part(
            name="Runner/Bearer",
            description="Cross supports",
            length=800,     # 800mm
            width=75,       # 75mm
            thickness=50,   # 50mm
            quantity_per_product=2,
            total_products=10,
            material_type="Hardwood",
            allow_rotation=True,
            priority=8
        )
    ]


def get_sample_parts_simple():
    """Get simple parts list for quick testing"""
    return [
        Part(
            name="Plank A",
            description="Main horizontal plank",
            length=1000,
            width=150,
            thickness=25,
            quantity_per_product=4,
            total_products=5,
            material_type="Pine",
            allow_rotation=False,
            priority=8
        ),
        Part(
            name="Block B",
            description="Support block",
            length=200,
            width=100,
            thickness=50,
            quantity_per_product=6,
            total_products=5,
            material_type="Pine",
            allow_rotation=True,
            priority=7
        )
    ]


def get_sample_parts_packaging():
    """Get sample parts for packaging crate construction"""
    return [
        Part(
            name="Crate Side Panel",
            description="Side panels for shipping crate",
            length=1500,
            width=800,
            thickness=18,
            quantity_per_product=2,
            total_products=25,
            material_type="Plywood",
            allow_rotation=True,
            priority=9
        ),
        Part(
            name="Crate End Panel",
            description="End panels for shipping crate",
            length=900,
            width=800,
            thickness=18,
            quantity_per_product=2,
            total_products=25,
            material_type="Plywood",
            allow_rotation=True,
            priority=9
        ),
        Part(
            name="Base Slat",
            description="Bottom base support slats",
            length=1500,
            width=75,
            thickness=25,
            quantity_per_product=8,
            total_products=25,
            material_type="Pine",
            allow_rotation=False,
            priority=8
        ),
        Part(
            name="Corner Reinforcement",
            description="Corner support blocks",
            length=100,
            width=100,
            thickness=75,
            quantity_per_product=4,
            total_products=25,
            material_type="Hardwood",
            allow_rotation=True,
            priority=7
        )
    ]


def get_default_cutting_parameters():
    """Get default cutting parameters"""
    return CuttingParameters(
        kerf=3.0,
        min_offcut_to_keep=150.0,
        tolerance=2.0,
        grain_direction=GrainDirection.NONE,
        optimization_priority=OptimizationPriority.MAXIMIZE_EFFICIENCY,
        allow_resawing=True,
        allow_planing=True,
        max_planing_depth=5.0
    )


# Example usage scenarios
SAMPLE_SCENARIOS = {
    "Standard Pallet (1200×1000)": {
        "description": "Complete cutting plan for 10 standard Euro pallets",
        "parts": get_sample_parts_pallet,
        "inventory": get_sample_inventory
    },
    "Simple Test": {
        "description": "Simple test case with 2 part types",
        "parts": get_sample_parts_simple,
        "inventory": get_sample_inventory
    },
    "Packaging Crates": {
        "description": "Shipping crate construction (25 units)",
        "parts": get_sample_parts_packaging,
        "inventory": get_sample_inventory
    }
}


def get_scenario(scenario_name: str):
    """
    Get a complete scenario with inventory and parts
    
    Args:
        scenario_name: Name of the scenario
        
    Returns:
        Dictionary with inventory, parts, and parameters
    """
    if scenario_name not in SAMPLE_SCENARIOS:
        scenario_name = "Standard Pallet (1200×1000)"
    
    scenario = SAMPLE_SCENARIOS[scenario_name]
    
    return {
        "description": scenario["description"],
        "inventory": scenario["inventory"](),
        "parts": scenario["parts"](),
        "parameters": get_default_cutting_parameters()
    }
