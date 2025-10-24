import React from 'react';
import { CuttingParameters } from '../types';

interface ParametersFormProps {
  parameters: CuttingParameters;
  onUpdate: (parameters: CuttingParameters) => void;
  onNext: () => void;
  onPrevious: () => void;
}

const ParametersForm: React.FC<ParametersFormProps> = ({ parameters, onUpdate, onPrevious, onNext }) => {
  const handleParameterChange = (field: keyof CuttingParameters, value: any) => {
    onUpdate({ ...parameters, [field]: value });
  };

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6">Cutting Parameters</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Basic Parameters */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Basic Parameters</h3>
          
          <div className="form-group">
            <label className="form-label">Kerf (Saw Blade Gap) - mm</label>
            <input
              type="number"
              step="0.1"
              className="form-input"
              value={parameters.kerf}
              onChange={(e) => handleParameterChange('kerf', parseFloat(e.target.value) || 0)}
              placeholder="3.0"
            />
            <p className="text-sm text-muted">Width of the saw blade cut</p>
          </div>

          <div className="form-group">
            <label className="form-label">Minimum Offcut to Keep - mm</label>
            <input
              type="number"
              step="0.1"
              className="form-input"
              value={parameters.minOffcut}
              onChange={(e) => handleParameterChange('minOffcut', parseFloat(e.target.value) || 0)}
              placeholder="50.0"
            />
            <p className="text-sm text-muted">Minimum size of leftover pieces to track for reuse</p>
          </div>

          <div className="form-group">
            <label className="form-label">Tolerance - mm</label>
            <input
              type="number"
              step="0.1"
              className="form-input"
              value={parameters.tolerance}
              onChange={(e) => handleParameterChange('tolerance', parseFloat(e.target.value) || 0)}
              placeholder="1.0"
            />
            <p className="text-sm text-muted">Allowable deviation from exact dimensions</p>
          </div>
        </div>

        {/* Advanced Parameters */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Advanced Parameters</h3>
          
          <div className="form-group">
            <label className="form-label">Grain Direction Enforcement</label>
            <div className="flex items-center">
              <input
                type="checkbox"
                id="grain-direction"
                className="mr-2"
                checked={parameters.grainDirectionEnforcement}
                onChange={(e) => handleParameterChange('grainDirectionEnforcement', e.target.checked)}
              />
              <label htmlFor="grain-direction" className="form-label mb-0">
                Enforce grain direction constraints
              </label>
            </div>
            <p className="text-sm text-muted">Prevent rotation that would violate wood grain requirements</p>
          </div>

          <div className="form-group">
            <label className="form-label">Optimization Priority</label>
            <select
              className="form-select"
              value={parameters.optimizationPriority}
              onChange={(e) => handleParameterChange('optimizationPriority', e.target.value)}
            >
              <option value="efficiency">Maximize Material Efficiency</option>
              <option value="cost">Minimize Cost</option>
              <option value="speed">Fastest Cutting (Fewest Cuts)</option>
            </select>
            <p className="text-sm text-muted">Primary goal for optimization algorithm</p>
          </div>
        </div>
      </div>

      {/* Parameter Descriptions */}
      <div className="mt-8 p-4 bg-tertiary rounded">
        <h3 className="text-lg font-semibold mb-4">Parameter Guidelines</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <h4 className="font-semibold mb-2">Kerf Width</h4>
            <ul className="space-y-1 text-muted">
              <li>• Table saw: 3-4mm</li>
              <li>• Circular saw: 2-3mm</li>
              <li>• Band saw: 1-2mm</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Tolerance</h4>
            <ul className="space-y-1 text-muted">
              <li>• High precision: 0.5mm</li>
              <li>• Standard: 1-2mm</li>
              <li>• Rough cuts: 3-5mm</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Minimum Offcut</h4>
            <ul className="space-y-1 text-muted">
              <li>• Small parts: 25-50mm</li>
              <li>• Medium parts: 50-100mm</li>
              <li>• Large parts: 100-200mm</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Grain Direction</h4>
            <ul className="space-y-1 text-muted">
              <li>• Structural parts: Enforce</li>
              <li>• Decorative parts: Optional</li>
              <li>• Small parts: Usually flexible</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Current Settings Summary */}
      <div className="mt-6 p-4 bg-secondary rounded">
        <h3 className="text-lg font-semibold mb-4">Current Settings Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="font-semibold">Kerf:</span> {parameters.kerf}mm
          </div>
          <div>
            <span className="font-semibold">Min Offcut:</span> {parameters.minOffcut}mm
          </div>
          <div>
            <span className="font-semibold">Tolerance:</span> {parameters.tolerance}mm
          </div>
          <div>
            <span className="font-semibold">Grain:</span> {parameters.grainDirectionEnforcement ? 'Enforced' : 'Flexible'}
          </div>
          <div className="col-span-2">
            <span className="font-semibold">Priority:</span> {
              parameters.optimizationPriority === 'efficiency' ? 'Maximize Efficiency' :
              parameters.optimizationPriority === 'cost' ? 'Minimize Cost' :
              'Fastest Cutting'
            }
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        <button
          onClick={onPrevious}
          className="btn btn-secondary"
        >
          Previous: Parts
        </button>
        <button
          onClick={onNext}
          className="btn btn-primary"
        >
          Next: Optimize
        </button>
      </div>
    </div>
  );
};

export default ParametersForm;