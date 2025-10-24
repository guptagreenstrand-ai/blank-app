from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import math
from datetime import datetime

app = FastAPI(title="Wooden Cutting Plan Optimizer API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LumberStock(BaseModel):
    name: str
    length: float  # mm
    width: float   # mm
    thickness: float  # mm
    quantity: int
    cost_per_unit: Optional[float] = None

class Part(BaseModel):
    name: str
    description: str
    length: float  # mm
    width: float   # mm
    thickness: float  # mm
    quantity_per_product: int
    total_units: int
    material_type: str
    allow_rotation: bool = True
    priority: float = 1.0  # 0.0 to 1.0

class CuttingParameters(BaseModel):
    kerf: float = 3.0  # mm
    min_offcut: float = 50.0  # mm
    tolerance: float = 2.0  # mm
    grain_direction_enforcement: bool = False
    optimization_priority: str = "efficiency"  # efficiency, cost, speed

class OptimizationRequest(BaseModel):
    lumber_stock: List[LumberStock]
    parts: List[Part]
    cutting_parameters: CuttingParameters

class CutAssignment(BaseModel):
    part_name: str
    part_id: int
    lumber_name: str
    lumber_id: int
    x_position: float
    y_position: float
    z_position: float
    rotation: float  # degrees
    length: float
    width: float
    thickness: float

class StickPlan(BaseModel):
    stick_id: int
    lumber_name: str
    lumber_id: int
    length: float
    width: float
    thickness: float
    cuts: List[CutAssignment]
    utilization_percentage: float
    waste_area: float
    total_cuts: int

class OptimizationResult(BaseModel):
    success: bool
    message: str
    stick_plans: List[StickPlan]
    total_material_used: float  # cubic feet
    total_waste: float  # cubic feet
    overall_utilization: float  # percentage
    total_cuts: int
    optimization_time: float  # seconds
    summary: Dict[str, Any]

# 3D Guillotine Cutting Algorithm Implementation
class CuttingOptimizer:
    def __init__(self, lumber_stock: List[LumberStock], parts: List[Part], params: CuttingParameters):
        self.lumber_stock = lumber_stock
        self.parts = parts
        self.params = params
        self.offcuts = []  # Track available offcuts
        
    def optimize(self) -> OptimizationResult:
        """Main optimization algorithm"""
        start_time = datetime.now()
        
        try:
            # Calculate total parts needed
            total_parts = []
            for part in self.parts:
                total_quantity = part.quantity_per_product * part.total_units
                for _ in range(total_quantity):
                    total_parts.append(part)
            
            # Sort parts by priority and size
            total_parts.sort(key=lambda p: (-p.priority, p.length * p.width * p.thickness))
            
            stick_plans = []
            part_assignments = []
            
            # Process each part
            for part in total_parts:
                assigned = False
                
                # Try to fit in existing stick plans first
                for stick_plan in stick_plans:
                    if self._can_fit_part(part, stick_plan):
                        assignment = self._assign_part_to_stick(part, stick_plan)
                        if assignment:
                            part_assignments.append(assignment)
                            assigned = True
                            break
                
                # If not assigned, create new stick
                if not assigned:
                    new_stick = self._create_new_stick_for_part(part)
                    if new_stick:
                        stick_plans.append(new_stick)
                        assignment = self._assign_part_to_stick(part, new_stick)
                        if assignment:
                            part_assignments.append(assignment)
            
            # Calculate results
            total_material = sum(stick.length * stick.width * stick.thickness for stick in stick_plans) / (25.4**3) / 1728  # Convert to cubic feet
            total_waste = sum(stick.waste_area for stick in stick_plans) / (25.4**2) / 144  # Convert to square feet
            overall_utilization = (1 - total_waste / total_material) * 100 if total_material > 0 else 0
            
            optimization_time = (datetime.now() - start_time).total_seconds()
            
            summary = {
                "total_sticks": len(stick_plans),
                "total_parts_cut": len(part_assignments),
                "average_utilization": sum(stick.utilization_percentage for stick in stick_plans) / len(stick_plans) if stick_plans else 0,
                "material_efficiency": f"{overall_utilization:.1f}%",
                "waste_percentage": f"{(total_waste / total_material * 100):.1f}%" if total_material > 0 else "0%"
            }
            
            return OptimizationResult(
                success=True,
                message="Optimization completed successfully",
                stick_plans=stick_plans,
                total_material_used=total_material,
                total_waste=total_waste,
                overall_utilization=overall_utilization,
                total_cuts=sum(stick.total_cuts for stick in stick_plans),
                optimization_time=optimization_time,
                summary=summary
            )
            
        except Exception as e:
            return OptimizationResult(
                success=False,
                message=f"Optimization failed: {str(e)}",
                stick_plans=[],
                total_material_used=0,
                total_waste=0,
                overall_utilization=0,
                total_cuts=0,
                optimization_time=(datetime.now() - start_time).total_seconds(),
                summary={}
            )
    
    def _can_fit_part(self, part: Part, stick_plan: StickPlan) -> bool:
        """Check if part can fit in existing stick plan"""
        # Simple 2D fitting check (can be enhanced for 3D)
        available_length = stick_plan.length
        available_width = stick_plan.width
        
        # Account for kerf
        kerf = self.params.kerf
        
        # Check both orientations
        fits_normal = (part.length + kerf <= available_length and 
                      part.width + kerf <= available_width)
        
        fits_rotated = (part.width + kerf <= available_length and 
                       part.length + kerf <= available_width)
        
        return fits_normal or (fits_rotated and part.allow_rotation)
    
    def _assign_part_to_stick(self, part: Part, stick_plan: StickPlan) -> Optional[CutAssignment]:
        """Assign part to stick plan"""
        # Find best position (simplified - can be enhanced)
        x_pos = 0
        y_pos = 0
        rotation = 0
        
        # Check if rotation is needed
        if (part.width + self.params.kerf <= stick_plan.length and 
            part.length + self.params.kerf <= stick_plan.width and 
            part.allow_rotation):
            rotation = 90
            length = part.width
            width = part.length
        else:
            length = part.length
            width = part.width
        
        # Create assignment
        assignment = CutAssignment(
            part_name=part.name,
            part_id=id(part),
            lumber_name=stick_plan.lumber_name,
            lumber_id=stick_plan.stick_id,
            x_position=x_pos,
            y_position=y_pos,
            z_position=0,
            rotation=rotation,
            length=length,
            width=width,
            thickness=part.thickness
        )
        
        # Update stick plan
        stick_plan.cuts.append(assignment)
        stick_plan.total_cuts += 1
        
        # Update utilization
        used_area = length * width
        total_area = stick_plan.length * stick_plan.width
        stick_plan.utilization_percentage = (used_area / total_area) * 100
        stick_plan.waste_area = total_area - used_area
        
        return assignment
    
    def _create_new_stick_for_part(self, part: Part) -> Optional[StickPlan]:
        """Create new stick plan for part"""
        # Find best lumber stock
        best_lumber = None
        best_waste = float('inf')
        
        for lumber in self.lumber_stock:
            if lumber.quantity > 0:
                # Check if part fits
                fits_normal = (part.length + self.params.kerf <= lumber.length and 
                              part.width + self.params.kerf <= lumber.width)
                
                fits_rotated = (part.width + self.params.kerf <= lumber.length and 
                               part.length + self.params.kerf <= lumber.width and 
                               part.allow_rotation)
                
                if fits_normal or fits_rotated:
                    # Calculate waste
                    if fits_normal:
                        waste = lumber.length * lumber.width - part.length * part.width
                    else:
                        waste = lumber.length * lumber.width - part.width * part.length
                    
                    if waste < best_waste:
                        best_waste = waste
                        best_lumber = lumber
        
        if best_lumber:
            # Create stick plan
            stick_plan = StickPlan(
                stick_id=len(self.lumber_stock) + 1,
                lumber_name=best_lumber.name,
                lumber_id=id(best_lumber),
                length=best_lumber.length,
                width=best_lumber.width,
                thickness=best_lumber.thickness,
                cuts=[],
                utilization_percentage=0,
                waste_area=best_lumber.length * best_lumber.width,
                total_cuts=0
            )
            
            # Reduce lumber quantity
            best_lumber.quantity -= 1
            
            return stick_plan
        
        return None

@app.get("/")
async def root():
    return {"message": "Wooden Cutting Plan Optimizer API", "version": "1.0.0"}

@app.post("/optimize", response_model=OptimizationResult)
async def optimize_cutting_plan(request: OptimizationRequest):
    """Optimize cutting plan based on input parameters"""
    try:
        optimizer = CuttingOptimizer(
            lumber_stock=request.lumber_stock,
            parts=request.parts,
            params=request.cutting_parameters
        )
        
        result = optimizer.optimize()
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sample-data")
async def get_sample_data():
    """Get sample data for testing"""
    sample_lumber = [
        LumberStock(
            name="Aus KD Pine 8'×7\"×3.5\"",
            length=2438.4,  # 8 feet in mm
            width=177.8,    # 7 inches in mm
            thickness=88.9, # 3.5 inches in mm
            quantity=10,
            cost_per_unit=25.50
        ),
        LumberStock(
            name="Douglas Fir 10'×6\"×2\"",
            length=3048.0,  # 10 feet in mm
            width=152.4,    # 6 inches in mm
            thickness=50.8, # 2 inches in mm
            quantity=15,
            cost_per_unit=18.75
        )
    ]
    
    sample_parts = [
        Part(
            name="Plank",
            description="Main structural plank",
            length=1200.0,
            width=100.0,
            thickness=25.0,
            quantity_per_product=4,
            total_units=10,
            material_type="Pine",
            allow_rotation=True,
            priority=1.0
        ),
        Part(
            name="Stringer",
            description="Support stringer",
            length=800.0,
            width=50.0,
            thickness=25.0,
            quantity_per_product=2,
            total_units=10,
            material_type="Pine",
            allow_rotation=True,
            priority=0.8
        ),
        Part(
            name="Block",
            description="Corner block",
            length=100.0,
            width=100.0,
            thickness=88.9,
            quantity_per_product=4,
            total_units=10,
            material_type="Pine",
            allow_rotation=False,
            priority=0.6
        )
    ]
    
    sample_params = CuttingParameters(
        kerf=3.0,
        min_offcut=50.0,
        tolerance=2.0,
        grain_direction_enforcement=False,
        optimization_priority="efficiency"
    )
    
    return {
        "lumber_stock": sample_lumber,
        "parts": sample_parts,
        "cutting_parameters": sample_params
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)