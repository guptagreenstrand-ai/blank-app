import React from 'react';
import { CuttingPlan } from '../types';

interface CuttingPlanVisualizationProps {
  plan: CuttingPlan;
}

const CuttingPlanVisualization: React.FC<CuttingPlanVisualizationProps> = ({ plan }) => {
  const { cutting_layout } = plan;
  const { lumber_dimensions, part_dimensions, parts_per_layer, layers, kerf } = cutting_layout;

  // Calculate layout dimensions
  const lumberLength = lumber_dimensions[0];
  const lumberWidth = lumber_dimensions[1];
  const lumberThickness = lumber_dimensions[2];
  
  const partLength = part_dimensions[0];
  const partWidth = part_dimensions[1];
  const partThickness = part_dimensions[2];

  // Calculate how many parts fit in each direction
  const partsX = Math.floor(lumberLength / (partLength + kerf));
  const partsY = Math.floor(lumberWidth / (partWidth + kerf));
  const actualPartsPerLayer = partsX * partsY;

  // Scale factor for visualization (fit in 400px width)
  const scale = 400 / Math.max(lumberLength, lumberWidth);

  const scaledLumberLength = lumberLength * scale;
  const scaledLumberWidth = lumberWidth * scale;
  const scaledPartLength = partLength * scale;
  const scaledPartWidth = partWidth * scale;
  const scaledKerf = kerf * scale;

  return (
    <div className="space-y-6">
      {/* 2D Top View */}
      <div>
        <h4 className="text-lg font-semibold mb-4">2D Top View (Length × Width)</h4>
        <div className="flex justify-center">
          <svg
            width={scaledLumberLength + 20}
            height={scaledLumberWidth + 20}
            className="border border-color"
          >
            {/* Lumber outline */}
            <rect
              x="10"
              y="10"
              width={scaledLumberLength}
              height={scaledLumberWidth}
              fill="none"
              stroke="#4a5568"
              strokeWidth="2"
            />
            
            {/* Parts grid */}
            {Array.from({ length: partsY }, (_, y) =>
              Array.from({ length: partsX }, (_, x) => (
                <g key={`${x}-${y}`}>
                  {/* Part rectangle */}
                  <rect
                    x={10 + x * (scaledPartLength + scaledKerf)}
                    y={10 + y * (scaledPartWidth + scaledKerf)}
                    width={scaledPartLength}
                    height={scaledPartWidth}
                    fill="#3182ce"
                    fillOpacity="0.7"
                    stroke="#2b6cb0"
                    strokeWidth="1"
                  />
                  
                  {/* Kerf lines */}
                  {x < partsX - 1 && (
                    <line
                      x1={10 + (x + 1) * scaledPartLength + x * scaledKerf + scaledKerf / 2}
                      y1={10 + y * (scaledPartWidth + scaledKerf)}
                      x2={10 + (x + 1) * scaledPartLength + x * scaledKerf + scaledKerf / 2}
                      y2={10 + (y + 1) * (scaledPartWidth + scaledKerf)}
                      stroke="#e53e3e"
                      strokeWidth="1"
                    />
                  )}
                  {y < partsY - 1 && (
                    <line
                      x1={10 + x * (scaledPartLength + scaledKerf)}
                      y1={10 + (y + 1) * scaledPartWidth + y * scaledKerf + scaledKerf / 2}
                      x2={10 + (x + 1) * (scaledPartLength + scaledKerf)}
                      y2={10 + (y + 1) * scaledPartWidth + y * scaledKerf + scaledKerf / 2}
                      stroke="#e53e3e"
                      strokeWidth="1"
                    />
                  )}
                </g>
              ))
            )}
            
            {/* Labels */}
            <text
              x={scaledLumberLength / 2 + 10}
              y={scaledLumberWidth + 35}
              textAnchor="middle"
              className="text-sm fill-current"
            >
              Lumber: {lumberLength} × {lumberWidth} mm
            </text>
            <text
              x={scaledLumberLength / 2 + 10}
              y={scaledLumberWidth + 50}
              textAnchor="middle"
              className="text-sm fill-current"
            >
              Parts: {partLength} × {partWidth} mm ({actualPartsPerLayer} per layer)
            </text>
          </svg>
        </div>
      </div>

      {/* 3D Side View */}
      <div>
        <h4 className="text-lg font-semibold mb-4">3D Side View (Length × Thickness)</h4>
        <div className="flex justify-center">
          <svg
            width={scaledLumberLength + 20}
            height={lumberThickness * scale + 20}
            className="border border-color"
          >
            {/* Lumber outline */}
            <rect
              x="10"
              y="10"
              width={scaledLumberLength}
              height={lumberThickness * scale}
              fill="none"
              stroke="#4a5568"
              strokeWidth="2"
            />
            
            {/* Layers */}
            {Array.from({ length: layers }, (_, layer) => (
              <g key={layer}>
                {/* Layer rectangle */}
                <rect
                  x="10"
                  y={10 + layer * (partThickness * scale + kerf * scale)}
                  width={scaledLumberLength}
                  height={partThickness * scale}
                  fill="#3182ce"
                  fillOpacity="0.3"
                  stroke="#2b6cb0"
                  strokeWidth="1"
                />
                
                {/* Parts within layer */}
                {Array.from({ length: partsX }, (_, x) => (
                  <rect
                    key={x}
                    x={10 + x * (scaledPartLength + scaledKerf)}
                    y={10 + layer * (partThickness * scale + kerf * scale)}
                    width={scaledPartLength}
                    height={partThickness * scale}
                    fill="#3182ce"
                    fillOpacity="0.7"
                    stroke="#2b6cb0"
                    strokeWidth="1"
                  />
                ))}
                
                {/* Layer separation lines */}
                {layer < layers - 1 && (
                  <line
                    x1="10"
                    y1={10 + (layer + 1) * partThickness * scale + layer * kerf * scale + kerf * scale / 2}
                    x2={scaledLumberLength + 10}
                    y2={10 + (layer + 1) * partThickness * scale + layer * kerf * scale + kerf * scale / 2}
                    stroke="#e53e3e"
                    strokeWidth="1"
                  />
                )}
              </g>
            ))}
            
            {/* Labels */}
            <text
              x={scaledLumberLength / 2 + 10}
              y={lumberThickness * scale + 35}
              textAnchor="middle"
              className="text-sm fill-current"
            >
              Thickness: {lumberThickness} mm ({layers} layers)
            </text>
          </svg>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card text-center">
          <div className="text-2xl font-bold text-accent-primary">
            {actualPartsPerLayer * layers}
          </div>
          <div className="text-sm text-muted">Total Parts</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-warning">
            {((actualPartsPerLayer * layers * partLength * partWidth * partThickness) / (lumberLength * lumberWidth * lumberThickness) * 100).toFixed(1)}%
          </div>
          <div className="text-sm text-muted">Utilization</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-secondary">
            {plan.cuts}
          </div>
          <div className="text-sm text-muted">Cuts Required</div>
        </div>
      </div>

      {/* Cutting Instructions */}
      <div className="card">
        <h4 className="text-lg font-semibold mb-4">Cutting Instructions</h4>
        <div className="space-y-2 text-sm">
          <div>
            <strong>1. Horizontal Cuts (between layers):</strong> {layers - 1} cuts
          </div>
          <div>
            <strong>2. Vertical Cuts (within each layer):</strong> {(partsX - 1) * layers} length cuts, {(partsY - 1) * layers} width cuts
          </div>
          <div>
            <strong>3. Total Cuts:</strong> {plan.cuts} cuts
          </div>
          <div>
            <strong>4. Kerf Width:</strong> {kerf}mm per cut
          </div>
          <div>
            <strong>5. Waste:</strong> {((plan.waste / 1000000) * 1000).toFixed(2)} liters
          </div>
        </div>
      </div>
    </div>
  );
};

export default CuttingPlanVisualization;