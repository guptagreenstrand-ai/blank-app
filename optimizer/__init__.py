"""
Optimizer package for wooden cutting plan generation.

Modules:
- models: Core dataclasses and types
- guillotine: Heuristic 3D guillotine cutting algorithm (length -> width -> thickness)
- svg: SVG diagram generation for per-stick plans
- reports: CSV and PDF report generation
"""

from .models import (
    Dimension3D,
    Tolerance,
    InventoryItem,
    PartRequirement,
    CuttingParameters,
)
from .guillotine import optimize_cutting_plan, OptimizationResult, StickPlan, LengthSegmentPlan
