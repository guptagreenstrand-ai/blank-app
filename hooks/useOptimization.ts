import { useState } from 'react'
import axios from 'axios'

interface OptimizationResult {
  success: boolean
  message: string
  stickPlans: Array<{
    stickId: number
    lumberName: string
    lumberId: number
    length: number
    width: number
    thickness: number
    cuts: Array<{
      partName: string
      partId: number
      lumberName: string
      lumberId: number
      xPosition: number
      yPosition: number
      zPosition: number
      rotation: number
      length: number
      width: number
      thickness: number
    }>
    utilizationPercentage: number
    wasteArea: number
    totalCuts: number
  }>
  totalMaterialUsed: number
  totalWaste: number
  overallUtilization: number
  totalCuts: number
  optimizationTime: number
  summary: {
    totalSticks: number
    totalPartsCut: number
    averageUtilization: number
    materialEfficiency: string
    wastePercentage: string
  }
}

interface InputData {
  lumberStock: Array<{
    name: string
    length: number
    width: number
    thickness: number
    quantity: number
    costPerUnit?: number
  }>
  parts: Array<{
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
  }>
  cuttingParameters: {
    kerf: number
    minOffcut: number
    tolerance: number
    grainDirectionEnforcement: boolean
    optimizationPriority: string
  }
}

export function useOptimization() {
  const [result, setResult] = useState<OptimizationResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const optimize = async (inputData: InputData) => {
    setLoading(true)
    setError(null)
    
    try {
      // Transform data to match API format
      const apiData = {
        lumber_stock: inputData.lumberStock.map(lumber => ({
          name: lumber.name,
          length: lumber.length,
          width: lumber.width,
          thickness: lumber.thickness,
          quantity: lumber.quantity,
          cost_per_unit: lumber.costPerUnit
        })),
        parts: inputData.parts.map(part => ({
          name: part.name,
          description: part.description,
          length: part.length,
          width: part.width,
          thickness: part.thickness,
          quantity_per_product: part.quantityPerProduct,
          total_units: part.totalUnits,
          material_type: part.materialType,
          allow_rotation: part.allowRotation,
          priority: part.priority
        })),
        cutting_parameters: {
          kerf: inputData.cuttingParameters.kerf,
          min_offcut: inputData.cuttingParameters.minOffcut,
          tolerance: inputData.cuttingParameters.tolerance,
          grain_direction_enforcement: inputData.cuttingParameters.grainDirectionEnforcement,
          optimization_priority: inputData.cuttingParameters.optimizationPriority
        }
      }

      const response = await axios.post('/api/optimize', apiData)
      setResult(response.data)
    } catch (err) {
      console.error('Optimization error:', err)
      setError(err instanceof Error ? err.message : 'Optimization failed')
    } finally {
      setLoading(false)
    }
  }

  const loadSampleData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.get('/api/sample-data')
      return response.data
    } catch (err) {
      console.error('Error loading sample data:', err)
      setError(err instanceof Error ? err.message : 'Failed to load sample data')
      return null
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setResult(null)
    setError(null)
    setLoading(false)
  }

  return {
    result,
    loading,
    error,
    optimize,
    loadSampleData,
    reset
  }
}