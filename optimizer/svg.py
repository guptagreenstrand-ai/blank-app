from __future__ import annotations
from typing import List

from .guillotine import StickPlan


def render_stick_svg(stick: StickPlan, px_per_mm: float = 0.5) -> str:
    L = stick.dims_mm.length_mm * px_per_mm
    W = stick.dims_mm.width_mm * px_per_mm

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{W}" viewBox="0 0 {L} {W}">',
        f'<rect x="0" y="0" width="{L}" height="{W}" fill="#f5f5f5" stroke="#999"/>',
        f'<text x="5" y="15" font-size="12" fill="#333">{stick.inventory_name} #{stick.stick_index}</text>',
    ]

    for seg in stick.segments:
        for cut in seg.cuts:
            x = cut.position_mm[0] * px_per_mm
            y = cut.position_mm[1] * px_per_mm
            w = cut.dims_mm.length_mm * px_per_mm
            h = cut.dims_mm.width_mm * px_per_mm
            svg_parts.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{cut.color}" opacity="0.8" stroke="#222"/>'
            )
            svg_parts.append(
                f'<text x="{x + 2}" y="{y + 12}" font-size="10" fill="#000">{cut.part_key}</text>'
            )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def render_composite_svg(sticks: List[StickPlan], px_per_mm: float = 0.3, gap_px: int = 20) -> str:
    if not sticks:
        return "<svg xmlns='http://www.w3.org/2000/svg' width='100' height='40'></svg>"

    widths = [s.dims_mm.width_mm * px_per_mm for s in sticks]
    heights = [s.dims_mm.length_mm * px_per_mm for s in sticks]

    total_w = int(max(widths) + 40)
    total_h = int(sum(heights) + gap_px * (len(sticks) - 1) + 40)

    y_cursor = 20
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}">'
    ]

    for stick in sticks:
        # rotate to show length along x for consistency
        sub = render_stick_svg(stick, px_per_mm)
        # embed using foreignObject is complex; simplest is concatenate with translate
        svg_parts.append(f'<g transform="translate(20,{y_cursor})">')
        svg_parts.append(sub.replace("<svg", "<g").replace("</svg>", "</g>"))
        svg_parts.append("</g>")
        y_cursor += stick.dims_mm.width_mm * px_per_mm + gap_px

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)
