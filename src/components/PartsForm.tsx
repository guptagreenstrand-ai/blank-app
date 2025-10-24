import React, { useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import { Part } from '../types';

interface PartsFormProps {
  parts: Part[];
  onUpdate: (parts: Part[]) => void;
  onNext: () => void;
  onPrevious: () => void;
}

const PartsForm: React.FC<PartsFormProps> = ({ parts, onUpdate, onNext, onPrevious }) => {
  const [newPart, setNewPart] = useState<Part>({
    name: '',
    description: '',
    length: 0,
    width: 0,
    thickness: 0,
    quantity_per_product: 1,
    total_units: 0,
    material_type: 'pine',
    allow_rotation: true,
    priority: 1.0
  });

  const handleAddPart = () => {
    if (newPart.name && newPart.length > 0 && newPart.width > 0 && newPart.thickness > 0 && newPart.total_units > 0) {
      onUpdate([...parts, { ...newPart }]);
      setNewPart({
        name: '',
        description: '',
        length: 0,
        width: 0,
        thickness: 0,
        quantity_per_product: 1,
        total_units: 0,
        material_type: 'pine',
        allow_rotation: true,
        priority: 1.0
      });
    }
  };

  const handleRemovePart = (index: number) => {
    const updatedParts = parts.filter((_, i) => i !== index);
    onUpdate(updatedParts);
  };

  const handleUpdatePart = (index: number, field: keyof Part, value: any) => {
    const updatedParts = parts.map((part, i) => 
      i === index ? { ...part, [field]: value } : part
    );
    onUpdate(updatedParts);
  };

  const canProceed = parts.length > 0;
  const totalUnits = parts.reduce((sum, part) => sum + part.total_units, 0);

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6">Parts List</h2>
      
      {/* Add new part form */}
      <div className="bg-tertiary p-4 rounded mb-6">
        <h3 className="text-lg font-semibold mb-4">Add New Part</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="form-group">
            <label className="form-label">Name</label>
            <input
              type="text"
              className="form-input"
              value={newPart.name}
              onChange={(e) => setNewPart({ ...newPart, name: e.target.value })}
              placeholder="e.g., Pallet Deck Board"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Description</label>
            <input
              type="text"
              className="form-input"
              value={newPart.description}
              onChange={(e) => setNewPart({ ...newPart, description: e.target.value })}
              placeholder="e.g., Main deck board for pallet"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Length (mm)</label>
            <input
              type="number"
              className="form-input"
              value={newPart.length || ''}
              onChange={(e) => setNewPart({ ...newPart, length: parseFloat(e.target.value) || 0 })}
              placeholder="1200.0"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Width (mm)</label>
            <input
              type="number"
              className="form-input"
              value={newPart.width || ''}
              onChange={(e) => setNewPart({ ...newPart, width: parseFloat(e.target.value) || 0 })}
              placeholder="100.0"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Thickness (mm)</label>
            <input
              type="number"
              className="form-input"
              value={newPart.thickness || ''}
              onChange={(e) => setNewPart({ ...newPart, thickness: parseFloat(e.target.value) || 0 })}
              placeholder="25.0"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Quantity per Product</label>
            <input
              type="number"
              className="form-input"
              value={newPart.quantity_per_product || ''}
              onChange={(e) => setNewPart({ ...newPart, quantity_per_product: parseInt(e.target.value) || 1 })}
              placeholder="5"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Total Units</label>
            <input
              type="number"
              className="form-input"
              value={newPart.total_units || ''}
              onChange={(e) => setNewPart({ ...newPart, total_units: parseInt(e.target.value) || 0 })}
              placeholder="250"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Material Type</label>
            <select
              className="form-select"
              value={newPart.material_type}
              onChange={(e) => setNewPart({ ...newPart, material_type: e.target.value })}
            >
              <option value="pine">Pine</option>
              <option value="oak">Oak</option>
              <option value="maple">Maple</option>
              <option value="birch">Birch</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Priority (0.0 - 1.0)</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              className="form-input"
              value={newPart.priority}
              onChange={(e) => setNewPart({ ...newPart, priority: parseFloat(e.target.value) })}
            />
            <div className="text-sm text-muted">{newPart.priority}</div>
          </div>
          <div className="form-group flex items-center">
            <input
              type="checkbox"
              id="allow-rotation"
              className="mr-2"
              checked={newPart.allow_rotation}
              onChange={(e) => setNewPart({ ...newPart, allow_rotation: e.target.checked })}
            />
            <label htmlFor="allow-rotation" className="form-label mb-0">Allow Rotation</label>
          </div>
        </div>
        <button
          onClick={handleAddPart}
          className="btn btn-primary mt-4"
          disabled={!newPart.name || newPart.length <= 0 || newPart.width <= 0 || newPart.thickness <= 0 || newPart.total_units <= 0}
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Part
        </button>
      </div>

      {/* Current parts list */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4">
          Current Parts ({parts.length} types, {totalUnits} total units)
        </h3>
        {parts.length === 0 ? (
          <p className="text-muted text-center py-8">No parts added yet. Add some parts to continue.</p>
        ) : (
          <div className="space-y-4">
            {parts.map((part, index) => (
              <div key={index} className="bg-secondary p-4 rounded border">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
                  <div className="form-group">
                    <label className="form-label">Name</label>
                    <input
                      type="text"
                      className="form-input"
                      value={part.name}
                      onChange={(e) => handleUpdatePart(index, 'name', e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Description</label>
                    <input
                      type="text"
                      className="form-input"
                      value={part.description}
                      onChange={(e) => handleUpdatePart(index, 'description', e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Dimensions (L×W×T mm)</label>
                    <div className="grid grid-cols-3 gap-2">
                      <input
                        type="number"
                        className="form-input"
                        value={part.length}
                        onChange={(e) => handleUpdatePart(index, 'length', parseFloat(e.target.value) || 0)}
                        placeholder="L"
                      />
                      <input
                        type="number"
                        className="form-input"
                        value={part.width}
                        onChange={(e) => handleUpdatePart(index, 'width', parseFloat(e.target.value) || 0)}
                        placeholder="W"
                      />
                      <input
                        type="number"
                        className="form-input"
                        value={part.thickness}
                        onChange={(e) => handleUpdatePart(index, 'thickness', parseFloat(e.target.value) || 0)}
                        placeholder="T"
                      />
                    </div>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Quantity per Product</label>
                    <input
                      type="number"
                      className="form-input"
                      value={part.quantity_per_product}
                      onChange={(e) => handleUpdatePart(index, 'quantity_per_product', parseInt(e.target.value) || 1)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Total Units</label>
                    <input
                      type="number"
                      className="form-input"
                      value={part.total_units}
                      onChange={(e) => handleUpdatePart(index, 'total_units', parseInt(e.target.value) || 0)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Material & Priority</label>
                    <select
                      className="form-select mb-2"
                      value={part.material_type}
                      onChange={(e) => handleUpdatePart(index, 'material_type', e.target.value)}
                    >
                      <option value="pine">Pine</option>
                      <option value="oak">Oak</option>
                      <option value="maple">Maple</option>
                      <option value="birch">Birch</option>
                      <option value="other">Other</option>
                    </select>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      className="form-input"
                      value={part.priority}
                      onChange={(e) => handleUpdatePart(index, 'priority', parseFloat(e.target.value))}
                    />
                    <div className="text-xs text-muted">{part.priority}</div>
                  </div>
                </div>
                <div className="flex justify-between items-center mt-4">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id={`allow-rotation-${index}`}
                      className="mr-2"
                      checked={part.allow_rotation}
                      onChange={(e) => handleUpdatePart(index, 'allow_rotation', e.target.checked)}
                    />
                    <label htmlFor={`allow-rotation-${index}`} className="text-sm">Allow Rotation</label>
                  </div>
                  <button
                    onClick={() => handleRemovePart(index)}
                    className="btn btn-secondary text-error"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={onPrevious}
          className="btn btn-secondary"
        >
          Previous: Inventory
        </button>
        <button
          onClick={onNext}
          disabled={!canProceed}
          className="btn btn-primary"
        >
          Next: Parameters
        </button>
      </div>
    </div>
  );
};

export default PartsForm;