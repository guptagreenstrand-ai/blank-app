"""
Data Models for Wooden Cutting Plan Optimizer
Defines structures for inventory, parts, cutting parameters, and optimization results
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum


class OptimizationPriority(Enum):
    """Optimization priority modes"""
    MAXIMIZE_EFFICIENCY = "maximize_efficiency"
    MINIMIZE_COST = "minimize_cost"
    FASTEST_CUT = "fastest_cut"


class GrainDirection(Enum):
    """Grain direction enforcement"""
    NONE = "none"
    LENGTH = "length"
    WIDTH = "width"


@dataclass
class LumberStock:
    """Represents a piece of lumber/board in inventory"""
    name: str
    length: float  # mm
    width: float  # mm
    thickness: float  # mm
    quantity: int
    cost_per_unit: float = 0.0
    id: Optional[str] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = f"stock_{id(self)}"
    
    @property
    def volume(self) -> float:
        """Calculate volume in cubic mm"""
        return self.length * self.width * self.thickness
    
    @property
    def volume_cft(self) -> float:
        """Calculate volume in cubic feet"""
        # 1 cubic foot = 28316846.592 cubic mm
        return self.volume / 28316846.592
    
    def __str__(self):
        return f"{self.name} ({self.length}×{self.width}×{self.thickness}mm) qty:{self.quantity}"


@dataclass
class Part:
    """Represents a required cut part"""
    name: str
    description: str
    length: float  # mm
    width: float  # mm
    thickness: float  # mm
    quantity_per_product: int
    total_products: int
    material_type: str = ""
    allow_rotation: bool = True
    priority: int = 5  # 1-10 scale
    tolerance: float = 0.0  # mm, allowable deviation
    id: Optional[str] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = f"part_{id(self)}"
    
    @property
    def total_quantity(self) -> int:
        """Calculate total quantity needed"""
        return self.quantity_per_product * self.total_products
    
    @property
    def volume(self) -> float:
        """Calculate volume in cubic mm"""
        return self.length * self.width * self.thickness
    
    @property
    def total_volume(self) -> float:
        """Calculate total volume needed for all parts"""
        return self.volume * self.total_quantity
    
    def fits_in_dimension(self, stock_dim: float, part_dim: float, kerf: float = 0) -> bool:
        """Check if part dimension fits in stock dimension (with kerf and tolerance)"""
        return part_dim - self.tolerance <= stock_dim + self.tolerance + kerf
    
    def __str__(self):
        return f"{self.name} ({self.length}×{self.width}×{self.thickness}mm) qty:{self.total_quantity}"


@dataclass
class CuttingParameters:
    """Cutting parameters and constraints"""
    kerf: float = 3.0  # mm, saw blade gap
    min_offcut_to_keep: float = 100.0  # mm
    tolerance: float = 2.0  # mm, allowable deviation
    grain_direction: GrainDirection = GrainDirection.NONE
    optimization_priority: OptimizationPriority = OptimizationPriority.MAXIMIZE_EFFICIENCY
    allow_resawing: bool = True
    allow_planing: bool = True
    max_planing_depth: float = 5.0  # mm
    
    def __str__(self):
        return (f"Kerf: {self.kerf}mm, Min Offcut: {self.min_offcut_to_keep}mm, "
                f"Tolerance: {self.tolerance}mm")


@dataclass
class CutPiece:
    """Represents a cut piece with position on stock"""
    part: Part
    x: float  # Position in stock (mm)
    y: float
    z: float
    rotated: bool = False
    actual_length: float = 0.0  # Actual cut dimensions (may differ slightly from part)
    actual_width: float = 0.0
    actual_thickness: float = 0.0
    
    def __post_init__(self):
        if self.actual_length == 0.0:
            self.actual_length = self.part.length
        if self.actual_width == 0.0:
            self.actual_width = self.part.width
        if self.actual_thickness == 0.0:
            self.actual_thickness = self.part.thickness


@dataclass
class Offcut:
    """Represents a leftover piece of lumber"""
    length: float  # mm
    width: float
    thickness: float
    original_stock: str  # ID of original stock
    usable: bool = True
    
    @property
    def volume(self) -> float:
        """Calculate volume in cubic mm"""
        return self.length * self.width * self.thickness


@dataclass
class CuttingPlan:
    """Represents a cutting plan for a single stock piece"""
    stock: LumberStock
    stock_index: int  # Which piece of this stock type
    cuts: List[CutPiece] = field(default_factory=list)
    offcuts: List[Offcut] = field(default_factory=list)
    
    @property
    def material_utilized(self) -> float:
        """Calculate percentage of material utilized"""
        if self.stock.volume == 0:
            return 0.0
        used_volume = sum(cut.actual_length * cut.actual_width * cut.actual_thickness 
                         for cut in self.cuts)
        return (used_volume / self.stock.volume) * 100
    
    @property
    def waste_percentage(self) -> float:
        """Calculate waste percentage"""
        return 100 - self.material_utilized
    
    @property
    def total_cuts(self) -> int:
        """Count total number of cuts needed"""
        return len(self.cuts)


@dataclass
class OptimizationResult:
    """Complete optimization result"""
    cutting_plans: List[CuttingPlan] = field(default_factory=list)
    unassigned_parts: List[Tuple[Part, int]] = field(default_factory=list)  # (part, quantity)
    total_sticks_used: int = 0
    total_cuts: int = 0
    overall_efficiency: float = 0.0
    total_waste: float = 0.0
    total_cost: float = 0.0
    total_volume_used_cft: float = 0.0
    computation_time: float = 0.0
    
    @property
    def success(self) -> bool:
        """Check if optimization was successful (all parts assigned)"""
        return len(self.unassigned_parts) == 0
    
    def get_summary(self) -> dict:
        """Get summary statistics"""
        return {
            "total_sticks_used": self.total_sticks_used,
            "total_cuts": self.total_cuts,
            "overall_efficiency": f"{self.overall_efficiency:.2f}%",
            "total_waste": f"{self.total_waste:.2f}%",
            "total_cost": f"${self.total_cost:.2f}",
            "total_volume_cft": f"{self.total_volume_used_cft:.4f} cft",
            "computation_time": f"{self.computation_time:.3f}s",
            "success": self.success
        }
