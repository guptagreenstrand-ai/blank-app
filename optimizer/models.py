from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple


@dataclass(frozen=True)
class Dimension3D:
    length_mm: float
    width_mm: float
    thickness_mm: float

    def sorted_tuple(self) -> Tuple[float, float, float]:
        return (self.length_mm, self.width_mm, self.thickness_mm)


@dataclass(frozen=True)
class Tolerance:
    length_mm: float = 0.0
    width_mm: float = 0.0
    thickness_mm: float = 0.0

    def within(self, required: Dimension3D, actual: Dimension3D) -> bool:
        return (
            actual.length_mm >= required.length_mm - self.length_mm
            and actual.width_mm >= required.width_mm - self.width_mm
            and actual.thickness_mm >= required.thickness_mm - self.thickness_mm
        )


@dataclass
class InventoryItem:
    name: str
    dimensions_mm: Dimension3D
    quantity: int
    cost_per_unit: Optional[float] = None
    material: Optional[str] = None


@dataclass
class PartRequirement:
    key: str
    name: str
    material: str
    required_dimensions_mm: Dimension3D
    quantity_total: int
    allow_rotation_length_width: bool = False
    allow_rotation_width_thickness: bool = False
    allow_rotation_length_thickness: bool = False
    enforce_grain_along_length: bool = True
    priority: int = 0


@dataclass
class CuttingParameters:
    kerf_mm: float
    min_offcut_keep_mm: float = 0.0
    tolerance: Tolerance = field(default_factory=Tolerance)
    optimization_priority: str = "efficiency"  # efficiency | cost | speed


@dataclass
class CutPiece:
    part_key: str
    dims_mm: Dimension3D
    position_mm: Tuple[float, float, float]
    color: str


@dataclass
class Offcut:
    dims_mm: Dimension3D
    position_mm: Tuple[float, float, float]
