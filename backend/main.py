from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np
from optimization_algorithm import CuttingOptimizer
import json

app = FastAPI(title="Wooden Cutting Plan Optimizer API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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
    tolerance: float = 1.0  # mm
    grain_direction_enforcement: bool = True
    optimization_priority: str = "efficiency"  # efficiency, cost, speed

class OptimizationRequest(BaseModel):
    lumber_stock: List[LumberStock]
    parts: List[Part]
    cutting_parameters: CuttingParameters

class OptimizationResult(BaseModel):
    success: bool
    message: str
    results: Optional[Dict[str, Any]] = None
    utilization_percentage: Optional[float] = None
    total_waste: Optional[float] = None
    total_cuts: Optional[int] = None
    cutting_plans: Optional[List[Dict[str, Any]]] = None

@app.get("/")
async def root():
    return {"message": "Wooden Cutting Plan Optimizer API"}

@app.post("/optimize", response_model=OptimizationResult)
async def optimize_cutting_plan(request: OptimizationRequest):
    try:
        optimizer = CuttingOptimizer()
        
        # Convert request to optimizer format
        lumber_data = []
        for stock in request.lumber_stock:
            lumber_data.append({
                'name': stock.name,
                'dimensions': [stock.length, stock.width, stock.thickness],
                'quantity': stock.quantity,
                'cost': stock.cost_per_unit or 0
            })
        
        parts_data = []
        for part in request.parts:
            parts_data.append({
                'name': part.name,
                'description': part.description,
                'dimensions': [part.length, part.width, part.thickness],
                'quantity': part.total_units,
                'material_type': part.material_type,
                'allow_rotation': part.allow_rotation,
                'priority': part.priority
            })
        
        params = {
            'kerf': request.cutting_parameters.kerf,
            'min_offcut': request.cutting_parameters.min_offcut,
            'tolerance': request.cutting_parameters.tolerance,
            'grain_direction_enforcement': request.cutting_parameters.grain_direction_enforcement,
            'optimization_priority': request.cutting_parameters.optimization_priority
        }
        
        # Run optimization
        result = optimizer.optimize(lumber_data, parts_data, params)
        
        return OptimizationResult(
            success=True,
            message="Optimization completed successfully",
            results=result,
            utilization_percentage=result.get('utilization_percentage', 0),
            total_waste=result.get('total_waste', 0),
            total_cuts=result.get('total_cuts', 0),
            cutting_plans=result.get('cutting_plans', [])
        )
        
    except Exception as e:
        return OptimizationResult(
            success=False,
            message=f"Optimization failed: {str(e)}"
        )

@app.get("/sample-data")
async def get_sample_data():
    """Return sample data for testing"""
    return {
        "lumber_stock": [
            {
                "name": "Aus KD Pine 8'×7\"×3.5\"",
                "length": 2438.4,  # 8 feet in mm
                "width": 177.8,    # 7 inches in mm
                "thickness": 88.9,  # 3.5 inches in mm
                "quantity": 50,
                "cost_per_unit": 25.50
            },
            {
                "name": "Standard 2×4×8'",
                "length": 2438.4,
                "width": 88.9,
                "thickness": 38.1,
                "quantity": 100,
                "cost_per_unit": 8.75
            }
        ],
        "parts": [
            {
                "name": "Pallet Deck Board",
                "description": "Main deck board for pallet construction",
                "length": 1200.0,
                "width": 100.0,
                "thickness": 25.0,
                "quantity_per_product": 5,
                "total_units": 250,
                "material_type": "pine",
                "allow_rotation": True,
                "priority": 1.0
            },
            {
                "name": "Pallet Stringer",
                "description": "Support stringer for pallet",
                "length": 1000.0,
                "width": 100.0,
                "thickness": 25.0,
                "quantity_per_product": 3,
                "total_units": 150,
                "material_type": "pine",
                "allow_rotation": False,
                "priority": 0.9
            },
            {
                "name": "Pallet Block",
                "description": "Corner block for pallet assembly",
                "length": 100.0,
                "width": 100.0,
                "thickness": 90.0,
                "quantity_per_product": 9,
                "total_units": 450,
                "material_type": "pine",
                "allow_rotation": True,
                "priority": 0.8
            }
        ],
        "cutting_parameters": {
            "kerf": 3.0,
            "min_offcut": 50.0,
            "tolerance": 1.0,
            "grain_direction_enforcement": True,
            "optimization_priority": "efficiency"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)