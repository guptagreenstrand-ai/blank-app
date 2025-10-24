from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict
import io
import csv

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from .guillotine import OptimizationResult
from .svg import render_stick_svg


def export_csv(result: OptimizationResult) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["metric", "value"])
    writer.writerow(["utilization_percent", f"{result.utilization_percent:.2f}"])
    writer.writerow(["waste_percent", f"{result.waste_percent:.2f}"])
    writer.writerow(["total_cuts", result.total_cuts])

    writer.writerow([])
    writer.writerow(["part_key", "produced", "requested"])
    for k, v in result.summary_by_part.items():
        writer.writerow([k, v.get("produced", 0), v.get("requested", 0)])

    return output.getvalue()


def export_pdf(result: OptimizationResult) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, (height - 20 * mm), "Cutting Plan Report")
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, (height - 27 * mm), f"Utilization: {result.utilization_percent:.2f}%  Waste: {result.waste_percent:.2f}%  Cuts: {result.total_cuts}")

    y = height - 40 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "Summary by Part")
    y -= 6 * mm
    c.setFont("Helvetica", 10)
    for k, v in result.summary_by_part.items():
        c.drawString(22 * mm, y, f"{k}: produced {int(v.get('produced',0))} / requested {int(v.get('requested',0))}")
        y -= 5 * mm
        if y < 40 * mm:
            c.showPage()
            y = height - 20 * mm

    # Simple per-stick sketches: embed rasterized SVG is non-trivial without extra deps.
    # We'll just list sticks for now.
    c.showPage()
    y = height - 20 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "Stick Plans")
    y -= 8 * mm
    c.setFont("Helvetica", 10)
    for stick in result.stick_plans:
        c.drawString(22 * mm, y, f"{stick.inventory_name} #{stick.stick_index}: L{stick.dims_mm.length_mm} x W{stick.dims_mm.width_mm} x T{stick.dims_mm.thickness_mm} mm")
        y -= 5 * mm
        for seg in stick.segments:
            for cut in seg.cuts:
                c.drawString(26 * mm, y, f"- {cut.part_key} at {cut.position_mm[0]:.1f}mm length; {cut.dims_mm.length_mm}x{cut.dims_mm.width_mm}x{cut.dims_mm.thickness_mm}")
                y -= 4 * mm
                if y < 20 * mm:
                    c.showPage()
                    y = height - 20 * mm
        y -= 3 * mm

    c.save()
    return buffer.getvalue()
