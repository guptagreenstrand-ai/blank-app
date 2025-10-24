'use client'

import { useState } from 'react'
import { Plus, Trash2, Package, Scissors } from 'lucide-react'

interface LumberStock {
  name: string
  length: number
  width: number
  thickness: number
  quantity: number
  costPerUnit?: number
}

interface Part {
  name: string
  description: string
  length: number
  width: number
  thickness: number
  quantityPerProduct: number
  totalUnits: number
  materialType: string
  allowRotation: boolean
  priority: number
}

interface InputData {
  lumberStock: LumberStock[]
  parts: Part[]
  cuttingParameters: {
    kerf: number
    minOffcut: number
    tolerance: number
    grainDirectionEnforcement: boolean
    optimizationPriority: string
  }
}

interface InputFormsProps {
  data: InputData
  onChange: (data: InputData) => void
  onNext: () => void
}

export function InputForms({ data, onChange, onNext }: InputFormsProps) {
  const [activeTab, setActiveTab] = useState<'lumber' | 'parts'>('lumber')

  const addLumberStock = () => {
    const newLumber: LumberStock = {
      name: '',
      length: 0,
      width: 0,
      thickness: 0,
      quantity: 1,
      costPerUnit: 0
    }
    onChange({
      ...data,
      lumberStock: [...data.lumberStock, newLumber]
    })
  }

  const updateLumberStock = (index: number, field: keyof LumberStock, value: any) => {
    const updated = [...data.lumberStock]
    updated[index] = { ...updated[index], [field]: value }
    onChange({ ...data, lumberStock: updated })
  }

  const removeLumberStock = (index: number) => {
    const updated = data.lumberStock.filter((_, i) => i !== index)
    onChange({ ...data, lumberStock: updated })
  }

  const addPart = () => {
    const newPart: Part = {
      name: '',
      description: '',
      length: 0,
      width: 0,
      thickness: 0,
      quantityPerProduct: 1,
      totalUnits: 1,
      materialType: '',
      allowRotation: true,
      priority: 1.0
    }
    onChange({
      ...data,
      parts: [...data.parts, newPart]
    })
  }

  const updatePart = (index: number, field: keyof Part, value: any) => {
    const updated = [...data.parts]
    updated[index] = { ...updated[index], [field]: value }
    onChange({ ...data, parts: updated })
  }

  const removePart = (index: number) => {
    const updated = data.parts.filter((_, i) => i !== index)
    onChange({ ...data, parts: updated })
  }

  const loadSampleData = () => {
    const sampleLumber: LumberStock[] = [
      {
        name: "Aus KD Pine 8'×7\"×3.5\"",
        length: 2438.4,
        width: 177.8,
        thickness: 88.9,
        quantity: 10,
        costPerUnit: 25.50
      },
      {
        name: "Douglas Fir 10'×6\"×2\"",
        length: 3048.0,
        width: 152.4,
        thickness: 50.8,
        quantity: 15,
        costPerUnit: 18.75
      }
    ]

    const sampleParts: Part[] = [
      {
        name: "Plank",
        description: "Main structural plank",
        length: 1200.0,
        width: 100.0,
        thickness: 25.0,
        quantityPerProduct: 4,
        totalUnits: 10,
        materialType: "Pine",
        allowRotation: true,
        priority: 1.0
      },
      {
        name: "Stringer",
        description: "Support stringer",
        length: 800.0,
        width: 50.0,
        thickness: 25.0,
        quantityPerProduct: 2,
        totalUnits: 10,
        materialType: "Pine",
        allowRotation: true,
        priority: 0.8
      },
      {
        name: "Block",
        description: "Corner block",
        length: 100.0,
        width: 100.0,
        thickness: 88.9,
        quantityPerProduct: 4,
        totalUnits: 10,
        materialType: "Pine",
        allowRotation: false,
        priority: 0.6
      }
    ]

    onChange({
      ...data,
      lumberStock: sampleLumber,
      parts: sampleParts
    })
  }

  return (
    <div className="p-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Input Data
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Enter your lumber stock and required parts to generate optimized cutting plans.
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('lumber')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'lumber'
                ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
            }`}
          >
            <Package className="w-4 h-4 inline mr-2" />
            Lumber Stock
          </button>
          <button
            onClick={() => setActiveTab('parts')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'parts'
                ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
            }`}
          >
            <Scissors className="w-4 h-4 inline mr-2" />
            Parts List
          </button>
        </nav>
      </div>

      {/* Lumber Stock Tab */}
      {activeTab === 'lumber' && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Available Lumber Stock
            </h3>
            <div className="space-x-2">
              <button
                onClick={loadSampleData}
                className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600"
              >
                Load Sample Data
              </button>
              <button
                onClick={addLumberStock}
                className="px-3 py-1 text-sm bg-primary-600 text-white rounded-md hover:bg-primary-700 flex items-center"
              >
                <Plus className="w-4 h-4 mr-1" />
                Add Lumber
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {data.lumberStock.map((lumber, index) => (
              <div key={index} className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Name
                    </label>
                    <input
                      type="text"
                      value={lumber.name}
                      onChange={(e) => updateLumberStock(index, 'name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                      placeholder="e.g., Aus KD Pine 8'×7\"×3.5\""
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Length (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={lumber.length}
                      onChange={(e) => updateLumberStock(index, 'length', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Width (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={lumber.width}
                      onChange={(e) => updateLumberStock(index, 'width', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Thickness (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={lumber.thickness}
                      onChange={(e) => updateLumberStock(index, 'thickness', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Quantity
                    </label>
                    <input
                      type="number"
                      value={lumber.quantity}
                      onChange={(e) => updateLumberStock(index, 'quantity', parseInt(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div className="flex items-end">
                    <button
                      onClick={() => removeLumberStock(index)}
                      className="p-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
            
            {data.lumberStock.length === 0 && (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                <Package className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No lumber stock added yet. Click "Add Lumber" to get started.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Parts Tab */}
      {activeTab === 'parts' && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Required Parts
            </h3>
            <button
              onClick={addPart}
              className="px-3 py-1 text-sm bg-primary-600 text-white rounded-md hover:bg-primary-700 flex items-center"
            >
              <Plus className="w-4 h-4 mr-1" />
              Add Part
            </button>
          </div>

          <div className="space-y-4">
            {data.parts.map((part, index) => (
              <div key={index} className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Part Name
                    </label>
                    <input
                      type="text"
                      value={part.name}
                      onChange={(e) => updatePart(index, 'name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                      placeholder="e.g., Plank"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Description
                    </label>
                    <input
                      type="text"
                      value={part.description}
                      onChange={(e) => updatePart(index, 'description', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                      placeholder="e.g., Main structural plank"
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Length (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={part.length}
                      onChange={(e) => updatePart(index, 'length', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Width (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={part.width}
                      onChange={(e) => updatePart(index, 'width', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Thickness (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={part.thickness}
                      onChange={(e) => updatePart(index, 'thickness', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Material Type
                    </label>
                    <input
                      type="text"
                      value={part.materialType}
                      onChange={(e) => updatePart(index, 'materialType', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                      placeholder="e.g., Pine"
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Qty per Product
                    </label>
                    <input
                      type="number"
                      value={part.quantityPerProduct}
                      onChange={(e) => updatePart(index, 'quantityPerProduct', parseInt(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Total Units
                    </label>
                    <input
                      type="number"
                      value={part.totalUnits}
                      onChange={(e) => updatePart(index, 'totalUnits', parseInt(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Priority (0-1)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="1"
                      value={part.priority}
                      onChange={(e) => updatePart(index, 'priority', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 dark:text-white text-sm"
                    />
                  </div>
                  
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id={`allowRotation-${index}`}
                      checked={part.allowRotation}
                      onChange={(e) => updatePart(index, 'allowRotation', e.target.checked)}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600 rounded"
                    />
                    <label htmlFor={`allowRotation-${index}`} className="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                      Allow Rotation
                    </label>
                  </div>
                </div>
                
                <div className="flex justify-end">
                  <button
                    onClick={() => removePart(index)}
                    className="p-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
            
            {data.parts.length === 0 && (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                <Scissors className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No parts added yet. Click "Add Part" to get started.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Navigation */}
      <div className="mt-8 flex justify-end">
        <button
          onClick={onNext}
          disabled={data.lumberStock.length === 0 || data.parts.length === 0}
          className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          Next: Parameters
        </button>
      </div>
    </div>
  )
}