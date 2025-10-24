from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

from .models import (
    Dimension3D,
    Tolerance,
    InventoryItem,
    PartRequirement,
    CuttingParameters,
    CutPiece,
    Offcut,
)


PART_COLOR_MAP = {
    "plank": "#4CAF50",
    "stringer": "#2196F3",
    "block": "#FF9800",
    "runner": "#9C27B0",
}


@dataclass
class LengthSegmentPlan:
    start_mm: float
    end_mm: float
    cuts: List[CutPiece] = field(default_factory=list)
    offcuts: List[Offcut] = field(default_factory=list)


@dataclass
class StickPlan:
    inventory_name: str
    stick_index: int
    dims_mm: Dimension3D
    segments: List[LengthSegmentPlan] = field(default_factory=list)


@dataclass
class OptimizationResult:
    stick_plans: List[StickPlan]
    utilization_percent: float
    waste_percent: float
    total_cuts: int
    summary_by_part: Dict[str, Dict[str, float]]


def _fits(required: Dimension3D, available: Dimension3D, tol: Tolerance) -> bool:
    return tol.within(required, available)


def _choose_color(part: PartRequirement) -> str:
    return PART_COLOR_MAP.get(part.name.lower(), "#607D8B")


def optimize_cutting_plan(
    inventory: List[InventoryItem],
    required_parts: List[PartRequirement],
    params: CuttingParameters,
) -> OptimizationResult:
    # Simple greedy heuristic along length, then pack width, then thickness
    # Tracks kerf and offcuts; allows tolerance-based acceptance
    required_left: Dict[str, int] = {p.key: p.quantity_total for p in required_parts}
    part_by_key = {p.key: p for p in required_parts}

    stick_plans: List[StickPlan] = []

    total_stock_volume = 0.0
    total_cut_volume = 0.0
    total_cuts = 0

    for item in inventory:
        for i in range(item.quantity):
            stick = StickPlan(
                inventory_name=item.name,
                stick_index=i + 1,
                dims_mm=item.dimensions_mm,
                segments=[],
            )

            length_cursor = 0.0
            L = item.dimensions_mm.length_mm
            while length_cursor < L:
                remaining_length = L - length_cursor
                segment = LengthSegmentPlan(start_mm=length_cursor, end_mm=L)

                # Try to place parts that fit in remaining length
                placed_any = False
                for part in sorted(required_parts, key=lambda p: (-p.priority, p.name)):
                    qty_left = required_left.get(part.key, 0)
                    if qty_left <= 0:
                        continue

                    req = part.required_dimensions_mm
                    # Respect grain along length: default alignment along stock length
                    part_len = req.length_mm
                    part_w = req.width_mm
                    part_t = req.thickness_mm

                    # Consider simple rotations subject to grain and flags
                    def candidate_dims() -> List[Dimension3D]:
                        dims = [Dimension3D(part_len, part_w, part_t)]
                        if part.allow_rotation_width_thickness:
                            dims.append(Dimension3D(part_len, part_t, part_w))
                        if not part.enforce_grain_along_length:
                            if part.allow_rotation_length_width:
                                dims.append(Dimension3D(part_w, part_len, part_t))
                            if part.allow_rotation_length_thickness:
                                dims.append(Dimension3D(part_t, part_w, part_len))
                        # deduplicate
                        unique: List[Dimension3D] = []
                        seen = set()
                        for d in dims:
                            tup = (d.length_mm, d.width_mm, d.thickness_mm)
                            if tup not in seen:
                                unique.append(d)
                                seen.add(tup)
                        return unique

                    picked_dims: Optional[Dimension3D] = None
                    for cand in candidate_dims():
                        if remaining_length + params.kerf_mm < cand.length_mm:
                            continue
                        if _fits(cand, item.dimensions_mm, params.tolerance):
                            picked_dims = cand
                            break
                    if picked_dims is None:
                        continue

                    # Place one piece at current cursor
                    piece_pos = (length_cursor, 0.0, 0.0)
                    cut_piece = CutPiece(
                        part_key=part.key,
                        dims_mm=picked_dims,
                        position_mm=piece_pos,
                        color=_choose_color(part),
                    )
                    segment.cuts.append(cut_piece)
                    length_cursor += picked_dims.length_mm + params.kerf_mm
                    total_cut_volume += (
                        picked_dims.length_mm * picked_dims.width_mm * picked_dims.thickness_mm
                    )
                    required_left[part.key] = qty_left - 1
                    total_cuts += 1
                    placed_any = True

                    # If width leftover beyond keep threshold, track an offcut strip
                    width_offcut = item.dimensions_mm.width_mm - picked_dims.width_mm
                    if width_offcut >= params.min_offcut_keep_mm:
                        segment.offcuts.append(
                            Offcut(
                                dims_mm=Dimension3D(
                                    length_mm=picked_dims.length_mm,
                                    width_mm=width_offcut - params.kerf_mm,
                                    thickness_mm=picked_dims.thickness_mm,
                                ),
                                position_mm=(piece_pos[0], picked_dims.width_mm + params.kerf_mm, 0.0),
                            )
                        )

                    break  # place one piece at a time in greedy pass

                if not placed_any:
                    # If nothing fits, create an offcut for the rest if large enough and end segment
                    leftover_len = L - length_cursor
                    if leftover_len >= params.min_offcut_keep_mm:
                        segment.offcuts.append(
                            Offcut(
                                dims_mm=Dimension3D(
                                    length_mm=leftover_len,
                                    width_mm=item.dimensions_mm.width_mm,
                                    thickness_mm=item.dimensions_mm.thickness_mm,
                                ),
                                position_mm=(length_cursor, 0.0, 0.0),
                            )
                        )
                    # End stick
                    segment.end_mm = length_cursor
                    stick.segments.append(segment)
                    break
                else:
                    # Close the segment up to current cursor
                    segment.end_mm = length_cursor
                    stick.segments.append(segment)

                # Stop if nothing left to cut
                if all(qty <= 0 for qty in required_left.values()):
                    break

            stick_plans.append(stick)
            total_stock_volume += (
                item.dimensions_mm.length_mm
                * item.dimensions_mm.width_mm
                * item.dimensions_mm.thickness_mm
            )

        if all(qty <= 0 for qty in required_left.values()):
            break

    utilization_percent = (
        (total_cut_volume / total_stock_volume) * 100.0 if total_stock_volume > 0 else 0.0
    )
    waste_percent = 100.0 - utilization_percent if total_stock_volume > 0 else 0.0

    # Summary by part
    summary_by_part: Dict[str, Dict[str, float]] = {}
    for key, part in part_by_key.items():
        produced = part.quantity_total - required_left.get(key, 0)
        summary_by_part[key] = {
            "produced": float(produced),
            "requested": float(part.quantity_total),
        }

    return OptimizationResult(
        stick_plans=stick_plans,
        utilization_percent=utilization_percent,
        waste_percent=waste_percent,
        total_cuts=total_cuts,
        summary_by_part=summary_by_part,
    )
