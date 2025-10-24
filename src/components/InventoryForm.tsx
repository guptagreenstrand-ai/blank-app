import React, { useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import { LumberStock } from '../types';

interface InventoryFormProps {
  lumberStock: LumberStock[];
  onUpdate: (lumberStock: LumberStock[]) => void;
  onNext: () => void;
}

const InventoryForm: React.FC<InventoryFormProps> = ({ lumberStock, onUpdate, onNext }) => {
  const [newStock, setNewStock] = useState<LumberStock>({
    name: '',
    length: 0,
    width: 0,
    thickness: 0,
    quantity: 0,
    cost_per_unit: 0
  });

  const handleAddStock = () => {
    if (newStock.name && newStock.length > 0 && newStock.width > 0 && newStock.thickness > 0 && newStock.quantity > 0) {
      onUpdate([...lumberStock, { ...newStock }]);
      setNewStock({
        name: '',
        length: 0,
        width: 0,
        thickness: 0,
        quantity: 0,
        cost_per_unit: 0
      });
    }
  };

  const handleRemoveStock = (index: number) => {
    const updatedStock = lumberStock.filter((_, i) => i !== index);
    onUpdate(updatedStock);
  };

  const handleUpdateStock = (index: number, field: keyof LumberStock, value: any) => {
    const updatedStock = lumberStock.map((stock, i) => 
      i === index ? { ...stock, [field]: value } : stock
    );
    onUpdate(updatedStock);
  };

  const canProceed = lumberStock.length > 0;

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6">Lumber Stock Inventory</h2>
      
      {/* Add new stock form */}
      <div className="bg-tertiary p-4 rounded mb-6">
        <h3 className="text-lg font-semibold mb-4">Add New Lumber Stock</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="form-group">
            <label className="form-label">Name</label>
            <input
              type="text"
              className="form-input"
              value={newStock.name}
              onChange={(e) => setNewStock({ ...newStock, name: e.target.value })}
              placeholder="e.g., Aus KD Pine 8'×7\"×3.5\""
            />
          </div>
          <div className="form-group">
            <label className="form-label">Length (mm)</label>
            <input
              type="number"
              className="form-input"
              value={newStock.length || ''}
              onChange={(e) => setNewStock({ ...newStock, length: parseFloat(e.target.value) || 0 })}
              placeholder="2438.4"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Width (mm)</label>
            <input
              type="number"
              className="form-input"
              value={newStock.width || ''}
              onChange={(e) => setNewStock({ ...newStock, width: parseFloat(e.target.value) || 0 })}
              placeholder="177.8"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Thickness (mm)</label>
            <input
              type="number"
              className="form-input"
              value={newStock.thickness || ''}
              onChange={(e) => setNewStock({ ...newStock, thickness: parseFloat(e.target.value) || 0 })}
              placeholder="88.9"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Quantity</label>
            <input
              type="number"
              className="form-input"
              value={newStock.quantity || ''}
              onChange={(e) => setNewStock({ ...newStock, quantity: parseInt(e.target.value) || 0 })}
              placeholder="50"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Cost per Unit ($)</label>
            <input
              type="number"
              step="0.01"
              className="form-input"
              value={newStock.cost_per_unit || ''}
              onChange={(e) => setNewStock({ ...newStock, cost_per_unit: parseFloat(e.target.value) || 0 })}
              placeholder="25.50"
            />
          </div>
        </div>
        <button
          onClick={handleAddStock}
          className="btn btn-primary mt-4"
          disabled={!newStock.name || newStock.length <= 0 || newStock.width <= 0 || newStock.thickness <= 0 || newStock.quantity <= 0}
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Stock
        </button>
      </div>

      {/* Current stock list */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4">Current Stock ({lumberStock.length} types)</h3>
        {lumberStock.length === 0 ? (
          <p className="text-muted text-center py-8">No lumber stock added yet. Add some stock to continue.</p>
        ) : (
          <div className="space-y-4">
            {lumberStock.map((stock, index) => (
              <div key={index} className="bg-secondary p-4 rounded border">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
                  <div className="form-group">
                    <label className="form-label">Name</label>
                    <input
                      type="text"
                      className="form-input"
                      value={stock.name}
                      onChange={(e) => handleUpdateStock(index, 'name', e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Length (mm)</label>
                    <input
                      type="number"
                      className="form-input"
                      value={stock.length}
                      onChange={(e) => handleUpdateStock(index, 'length', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Width (mm)</label>
                    <input
                      type="number"
                      className="form-input"
                      value={stock.width}
                      onChange={(e) => handleUpdateStock(index, 'width', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Thickness (mm)</label>
                    <input
                      type="number"
                      className="form-input"
                      value={stock.thickness}
                      onChange={(e) => handleUpdateStock(index, 'thickness', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Quantity</label>
                    <input
                      type="number"
                      className="form-input"
                      value={stock.quantity}
                      onChange={(e) => handleUpdateStock(index, 'quantity', parseInt(e.target.value) || 0)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Cost ($)</label>
                    <input
                      type="number"
                      step="0.01"
                      className="form-input"
                      value={stock.cost_per_unit || ''}
                      onChange={(e) => handleUpdateStock(index, 'cost_per_unit', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                </div>
                <div className="flex justify-end mt-4">
                  <button
                    onClick={() => handleRemoveStock(index)}
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
      <div className="flex justify-end">
        <button
          onClick={onNext}
          disabled={!canProceed}
          className="btn btn-primary"
        >
          Next: Define Parts
        </button>
      </div>
    </div>
  );
};

export default InventoryForm;