import React, { useState } from 'react';
import { Download, RotateCcw, Eye, EyeOff } from 'lucide-react';
import { OptimizationResults as OptimizationResultsType, CuttingPlan } from '../types';
import CuttingPlanVisualization from './CuttingPlanVisualization';
import { exportToPDF, exportToCSV } from '../utils/exportUtils';

interface OptimizationResultsProps {
  results: OptimizationResultsType | null;
  onRestart: () => void;
}

const OptimizationResults: React.FC<OptimizationResultsProps> = ({ results, onRestart }) => {
  const [selectedPlan, setSelectedPlan] = useState<CuttingPlan | null>(null);
  const [showVisualization, setShowVisualization] = useState(false);

  if (!results || !results.success) {
    return (
      <div className="card text-center">
        <h2 className="text-2xl font-bold mb-4 text-error">Optimization Failed</h2>
        <p className="text-muted mb-6">{results?.message || 'Unknown error occurred'}</p>
        <button onClick={onRestart} className="btn btn-primary">
          <RotateCcw className="w-4 h-4 mr-2" />
          Start Over
        </button>
      </div>
    );
  }

  const cuttingPlans = results.cutting_plans || [];
  const utilization = results.utilization_percentage || 0;
  const totalWaste = results.total_waste || 0;
  const totalCuts = results.total_cuts || 0;

  const handleExportPDF = () => {
    exportToPDF(results);
  };

  const handleExportCSV = () => {
    exportToCSV(results);
  };

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <div className="text-2xl font-bold text-accent-primary">{utilization.toFixed(1)}%</div>
          <div className="text-sm text-muted">Material Utilization</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-warning">{(totalWaste / 1000000).toFixed(2)}</div>
          <div className="text-sm text-muted">Waste (m³)</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-secondary">{totalCuts}</div>
          <div className="text-sm text-muted">Total Cuts</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-success">{cuttingPlans.length}</div>
          <div className="text-sm text-muted">Cutting Plans</div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-4 justify-center">
        <button onClick={handleExportPDF} className="btn btn-primary">
          <Download className="w-4 h-4 mr-2" />
          Export PDF Report
        </button>
        <button onClick={handleExportCSV} className="btn btn-secondary">
          <Download className="w-4 h-4 mr-2" />
          Export CSV Data
        </button>
        <button onClick={onRestart} className="btn btn-secondary">
          <RotateCcw className="w-4 h-4 mr-2" />
          Start New Optimization
        </button>
      </div>

      {/* Cutting Plans List */}
      <div className="card">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Cutting Plans</h2>
          <button
            onClick={() => setShowVisualization(!showVisualization)}
            className="btn btn-secondary"
          >
            {showVisualization ? (
              <>
                <EyeOff className="w-4 h-4 mr-2" />
                Hide Visualization
              </>
            ) : (
              <>
                <Eye className="w-4 h-4 mr-2" />
                Show Visualization
              </>
            )}
          </button>
        </div>

        {cuttingPlans.length === 0 ? (
          <p className="text-muted text-center py-8">No cutting plans generated</p>
        ) : (
          <div className="space-y-4">
            {cuttingPlans.map((plan, index) => (
              <div key={index} className="bg-secondary p-4 rounded border">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                  <div>
                    <h3 className="font-semibold text-lg">{plan.part_name}</h3>
                    <p className="text-sm text-muted">from {plan.lumber_name}</p>
                  </div>
                  <div>
                    <div className="text-sm text-muted">Quantity</div>
                    <div className="font-semibold">{plan.quantity} parts</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted">Utilization</div>
                    <div className="font-semibold text-accent-primary">{(plan.utilization * 100).toFixed(1)}%</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted">Cuts Required</div>
                    <div className="font-semibold">{plan.cuts}</div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="font-semibold mb-2">Lumber Dimensions (mm)</div>
                    <div>L: {plan.lumber_dimensions[0]} × W: {plan.lumber_dimensions[1]} × T: {plan.lumber_dimensions[2]}</div>
                  </div>
                  <div>
                    <div className="font-semibold mb-2">Part Dimensions (mm)</div>
                    <div>L: {plan.part_dimensions[0]} × W: {plan.part_dimensions[1]} × T: {plan.part_dimensions[2]}</div>
                  </div>
                </div>

                <div className="mt-4 flex justify-between items-center">
                  <div className="text-sm">
                    <span className="text-muted">Waste: </span>
                    <span className="font-semibold">{(plan.waste / 1000000).toFixed(3)} m³</span>
                  </div>
                  <button
                    onClick={() => setSelectedPlan(plan)}
                    className="btn btn-secondary text-sm"
                  >
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Visualization Modal */}
      {showVisualization && selectedPlan && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-primary rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold">Cutting Plan Visualization</h3>
                <button
                  onClick={() => setShowVisualization(false)}
                  className="btn btn-secondary"
                >
                  Close
                </button>
              </div>
              <CuttingPlanVisualization plan={selectedPlan} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default OptimizationResults;