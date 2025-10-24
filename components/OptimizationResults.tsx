'use client'

import { TrendingUp, Package, Scissors, DollarSign, Clock } from 'lucide-react'

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

interface OptimizationResultsProps {
  result: OptimizationResult
}

export function OptimizationResults({ result }: OptimizationResultsProps) {
  if (!result.success) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-red-800 dark:text-red-200 mb-2">
          Optimization Failed
        </h3>
        <p className="text-red-600 dark:text-red-400">{result.message}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Package className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Sticks</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                {result.summary.totalSticks}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Scissors className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Parts Cut</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                {result.summary.totalPartsCut}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Efficiency</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                {result.summary.materialEfficiency}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Clock className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Optimization Time</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                {result.optimizationTime.toFixed(2)}s
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Results */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Optimization Summary
          </h3>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                Material Usage
              </h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Total Material Used:</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {result.totalMaterialUsed.toFixed(2)} cubic feet
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Total Waste:</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {result.totalWaste.toFixed(2)} square feet
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Waste Percentage:</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {result.summary.wastePercentage}
                  </span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                Cutting Statistics
              </h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Total Cuts:</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {result.totalCuts}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Average Utilization:</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {result.summary.averageUtilization.toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Overall Utilization:</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {result.overallUtilization.toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stick Plans Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Stick-by-Stick Breakdown
          </h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Stick ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Lumber Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Dimensions (mm)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Parts Cut
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Utilization
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Waste Area
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {result.stickPlans.map((stick) => (
                <tr key={stick.stickId} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    #{stick.stickId}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                    {stick.lumberName}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                    {stick.length.toFixed(0)} × {stick.width.toFixed(0)} × {stick.thickness.toFixed(0)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                    {stick.totalCuts}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                    <div className="flex items-center">
                      <div className="w-16 bg-gray-200 dark:bg-gray-600 rounded-full h-2 mr-2">
                        <div 
                          className="bg-primary-600 h-2 rounded-full" 
                          style={{ width: `${Math.min(stick.utilizationPercentage, 100)}%` }}
                        ></div>
                      </div>
                      <span>{stick.utilizationPercentage.toFixed(1)}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                    {stick.wasteArea.toFixed(0)} mm²
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}