export interface LumberStock {
  name: string;
  length: number; // mm
  width: number;  // mm
  thickness: number; // mm
  quantity: number;
  cost_per_unit?: number;
}

export interface Part {
  name: string;
  description: string;
  length: number; // mm
  width: number;  // mm
  thickness: number; // mm
  quantity_per_product: number;
  total_units: number;
  material_type: string;
  allow_rotation: boolean;
  priority: number; // 0.0 to 1.0
}

export interface CuttingParameters {
  kerf: number; // mm
  minOffcut: number; // mm
  tolerance: number; // mm
  grainDirectionEnforcement: boolean;
  optimizationPriority: 'efficiency' | 'cost' | 'speed';
}

export interface OptimizationData {
  lumberStock: LumberStock[];
  parts: Part[];
  cuttingParameters: CuttingParameters;
}

export interface CuttingPlan {
  lumber_name: string;
  lumber_dimensions: number[];
  part_name: string;
  part_dimensions: number[];
  quantity: number;
  utilization: number;
  waste: number;
  cuts: number;
  cutting_layout: {
    lumber_dimensions: number[];
    part_dimensions: number[];
    parts_per_layer: number;
    layers: number;
    kerf: number;
    cuts: number;
    utilization: number;
    waste: number;
  };
}

export interface OptimizationResults {
  success: boolean;
  message: string;
  results?: {
    cutting_plans: CuttingPlan[];
    utilization_percentage: number;
    total_waste: number;
    total_cuts: number;
    used_lumber: Record<string, number>;
    remaining_offcuts: any[];
  };
  utilization_percentage?: number;
  total_waste?: number;
  total_cuts?: number;
  cutting_plans?: CuttingPlan[];
}