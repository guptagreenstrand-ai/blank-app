from __future__ import annotations
from typing import List, TextIO
import csv

from .models import Dimension3D, InventoryItem, PartRequirement, CuttingParameters, Tolerance


def load_inventory_csv(path: str) -> List[InventoryItem]:
    items: List[InventoryItem] = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(
                InventoryItem(
                    name=row["name"],
                    dimensions_mm=Dimension3D(
                        length_mm=float(row["length_mm"]),
                        width_mm=float(row["width_mm"]),
                        thickness_mm=float(row["thickness_mm"]),
                    ),
                    quantity=int(row["quantity"]),
                    cost_per_unit=float(row["cost_per_unit"]) if row.get("cost_per_unit") else None,
                    material=row.get("material") or None,
                )
            )
    return items


def load_parts_csv(path: str) -> List[PartRequirement]:
    parts: List[PartRequirement] = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parts.append(
                PartRequirement(
                    key=row["key"],
                    name=row["name"],
                    material=row["material"],
                    required_dimensions_mm=Dimension3D(
                        length_mm=float(row["length_mm"]),
                        width_mm=float(row["width_mm"]),
                        thickness_mm=float(row["thickness_mm"]),
                    ),
                    quantity_total=int(row["quantity_total"]),
                    allow_rotation_length_width=row["allow_rotation_length_width"].lower() == "true",
                    allow_rotation_width_thickness=row["allow_rotation_width_thickness"].lower() == "true",
                    allow_rotation_length_thickness=row["allow_rotation_length_thickness"].lower() == "true",
                    enforce_grain_along_length=row["enforce_grain_along_length"].lower() == "true",
                    priority=int(row.get("priority", 0)),
                )
            )
    return parts


def load_inventory_filelike(file_obj: TextIO) -> List[InventoryItem]:
    items: List[InventoryItem] = []
    reader = csv.DictReader(file_obj)
    for row in reader:
        items.append(
            InventoryItem(
                name=row["name"],
                dimensions_mm=Dimension3D(
                    length_mm=float(row["length_mm"]),
                    width_mm=float(row["width_mm"]),
                    thickness_mm=float(row["thickness_mm"]),
                ),
                quantity=int(row["quantity"]),
                cost_per_unit=float(row["cost_per_unit"]) if row.get("cost_per_unit") else None,
                material=row.get("material") or None,
            )
        )
    return items


def load_parts_filelike(file_obj: TextIO) -> List[PartRequirement]:
    parts: List[PartRequirement] = []
    reader = csv.DictReader(file_obj)
    for row in reader:
        parts.append(
            PartRequirement(
                key=row["key"],
                name=row["name"],
                material=row["material"],
                required_dimensions_mm=Dimension3D(
                    length_mm=float(row["length_mm"]),
                    width_mm=float(row["width_mm"]),
                    thickness_mm=float(row["thickness_mm"]),
                ),
                quantity_total=int(row["quantity_total"]),
                allow_rotation_length_width=row["allow_rotation_length_width"].lower() == "true",
                allow_rotation_width_thickness=row["allow_rotation_width_thickness"].lower() == "true",
                allow_rotation_length_thickness=row["allow_rotation_length_thickness"].lower() == "true",
                enforce_grain_along_length=row["enforce_grain_along_length"].lower() == "true",
                priority=int(row.get("priority", 0)),
            )
        )
    return parts


def default_parameters() -> CuttingParameters:
    return CuttingParameters(
        kerf_mm=3.2,
        min_offcut_keep_mm=80.0,
        tolerance=Tolerance(length_mm=2.0, width_mm=1.0, thickness_mm=1.0),
        optimization_priority="efficiency",
    )
