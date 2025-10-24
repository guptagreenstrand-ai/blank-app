'use client'

import { useState } from 'react'
import { Eye, Download, RotateCcw, Maximize2 } from 'lucide-react'

interface CutAssignment {
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
}

interface StickPlan {
  stickId: number
  lumberName: string
  lumberId: number
  length: number
  width: number
  thickness: number
  cuts: CutAssignment[]
  utilizationPercentage: number
  wasteArea: number
  totalCuts: number
}

interface OptimizationResult {
  stickPlans: StickPlan[]
  [key: string]: any
}

interface VisualizationProps {
  result: OptimizationResult
}

const PART_COLORS = {
  'Plank': '#3B82F6',
  'Stringer': '#10B981',
  'Block': '#F59E0B',
  'Runner': '#EF4444',
  'default': '#6B7280'
}

export function Visualization({ result }: VisualizationProps) {
  const [selectedStick, setSelectedStick] = useState<number | null>(null)
  const [viewMode, setViewMode] = useState<'2d' | '3d'>('2d')
  const [showOffcuts, setShowOffcuts] = useState(false)

  const getPartColor = (partName: string) => {
    return PART_COLORS[partName as keyof typeof PART_COLORS] || PART_COLORS.default
  }

  const renderStick2D = (stick: StickPlan) => {
    const scale = 0.3 // Scale factor for visualization
    const scaledLength = stick.length * scale
    const scaledWidth = stick.width * scale

    return (
      <div className="relative border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 rounded-lg p-4">
        <div className="text-center mb-4">
          <h4 className="font-medium text-gray-900 dark:text-white">
            Stick #{stick.stickId} - {stick.lumberName}
          </h4>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {stick.length.toFixed(0)} × {stick.width.toFixed(0)} × {stick.thickness.toFixed(0)} mm
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Utilization: {stick.utilizationPercentage.toFixed(1)}% | Parts: {stick.totalCuts}
          </p>
        </div>
        
        <div className="relative mx-auto" style={{ width: scaledLength, height: scaledWidth }}>
          {/* Lumber outline */}
          <div 
            className="absolute border-2 border-gray-400 dark:border-gray-500 bg-gray-50 dark:bg-gray-700"
            style={{ 
              width: scaledLength, 
              height: scaledWidth,
              borderRadius: '4px'
            }}
          />
          
          {/* Parts */}
          {stick.cuts.map((cut, index) => {
            const scaledPartLength = cut.length * scale
            const scaledPartWidth = cut.width * scale
            const scaledX = cut.xPosition * scale
            const scaledY = cut.yPosition * scale
            
            return (
              <div
                key={index}
                className="absolute border border-gray-600 dark:border-gray-400 rounded-sm flex items-center justify-center text-xs font-medium text-white"
                style={{
                  left: scaledX,
                  top: scaledY,
                  width: scaledPartLength,
                  height: scaledPartWidth,
                  backgroundColor: getPartColor(cut.partName),
                  transform: cut.rotation ? `rotate(${cut.rotation}deg)` : 'none',
                  transformOrigin: 'center'
                }}
                title={`${cut.partName} (${cut.length}×${cut.width}×${cut.thickness}mm)`}
              >
                <span className="text-center leading-tight">
                  {cut.partName}
                </span>
              </div>
            )
          })}
          
          {/* Kerf lines */}
          {stick.cuts.map((cut, index) => {
            const scaledPartLength = cut.length * scale
            const scaledPartWidth = cut.width * scale
            const scaledX = cut.xPosition * scale
            const scaledY = cut.yPosition * scale
            
            return (
              <div key={`kerf-${index}`}>
                {/* Horizontal kerf lines */}
                <div 
                  className="absolute bg-red-500 opacity-60"
                  style={{
                    left: scaledX,
                    top: scaledY + scaledPartWidth,
                    width: scaledPartLength,
                    height: 1
                  }}
                />
                {/* Vertical kerf lines */}
                <div 
                  className="absolute bg-red-500 opacity-60"
                  style={{
                    left: scaledX + scaledPartLength,
                    top: scaledY,
                    width: 1,
                    height: scaledPartWidth
                  }}
                />
              </div>
            )
          })}
        </div>
        
        {/* Legend */}
        <div className="mt-4 flex flex-wrap gap-2 justify-center">
          {Array.from(new Set(stick.cuts.map(cut => cut.partName))).map(partName => (
            <div key={partName} className="flex items-center space-x-1">
              <div 
                className="w-3 h-3 rounded-sm"
                style={{ backgroundColor: getPartColor(partName) }}
              />
              <span className="text-xs text-gray-600 dark:text-gray-400">{partName}</span>
            </div>
          ))}
        </div>
      </div>
    )
  }

  const renderStick3D = (stick: StickPlan) => {
    // Simplified 3D representation using CSS transforms
    return (
      <div className="relative border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 rounded-lg p-4">
        <div className="text-center mb-4">
          <h4 className="font-medium text-gray-900 dark:text-white">
            Stick #{stick.stickId} - {stick.lumberName} (3D View)
          </h4>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {stick.length.toFixed(0)} × {stick.width.toFixed(0)} × {stick.thickness.toFixed(0)} mm
          </p>
        </div>
        
        <div className="relative mx-auto" style={{ perspective: '1000px' }}>
          <div 
            className="relative mx-auto border-2 border-gray-400 dark:border-gray-500 bg-gradient-to-br from-wood-200 to-wood-400 dark:from-wood-600 dark:to-wood-800"
            style={{ 
              width: '200px', 
              height: '150px',
              transform: 'rotateX(15deg) rotateY(15deg)',
              borderRadius: '4px',
              boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
            }}
          >
            {/* 3D parts would be rendered here */}
            <div className="absolute inset-0 flex items-center justify-center text-gray-500 dark:text-gray-400">
              <span className="text-sm">3D View Coming Soon</span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const exportSVG = () => {
    // SVG export functionality would be implemented here
    console.log('Exporting SVG...')
  }

  const exportPNG = () => {
    // PNG export functionality would be implemented here
    console.log('Exporting PNG...')
  }

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Cutting Plan Visualization
            </h3>
            
            <div className="flex items-center space-x-4">
              {/* View Mode Toggle */}
              <div className="flex bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('2d')}
                  className={`px-3 py-1 text-sm rounded-md transition-colors ${
                    viewMode === '2d'
                      ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  2D
                </button>
                <button
                  onClick={() => setViewMode('3d')}
                  className={`px-3 py-1 text-sm rounded-md transition-colors ${
                    viewMode === '3d'
                      ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  3D
                </button>
              </div>
              
              {/* Export Buttons */}
              <div className="flex space-x-2">
                <button
                  onClick={exportSVG}
                  className="px-3 py-1 text-sm bg-primary-600 text-white rounded-md hover:bg-primary-700 flex items-center"
                >
                  <Download className="w-4 h-4 mr-1" />
                  SVG
                </button>
                <button
                  onClick={exportPNG}
                  className="px-3 py-1 text-sm bg-primary-600 text-white rounded-md hover:bg-primary-700 flex items-center"
                >
                  <Download className="w-4 h-4 mr-1" />
                  PNG
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div className="p-6">
          {/* Stick Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Select Stick to Visualize
            </label>
            <select
              value={selectedStick || ''}
              onChange={(e) => setSelectedStick(e.target.value ? parseInt(e.target.value) : null)}
              className="w-full max-w-xs px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="">All Sticks</option>
              {result.stickPlans.map((stick) => (
                <option key={stick.stickId} value={stick.stickId}>
                  Stick #{stick.stickId} - {stick.lumberName}
                </option>
              ))}
            </select>
          </div>
          
          {/* Visualization Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {result.stickPlans
              .filter(stick => !selectedStick || stick.stickId === selectedStick)
              .map((stick) => (
                <div key={stick.stickId}>
                  {viewMode === '2d' ? renderStick2D(stick) : renderStick3D(stick)}
                </div>
              ))}
          </div>
          
          {result.stickPlans.length === 0 && (
            <div className="text-center py-12 text-gray-500 dark:text-gray-400">
              <Eye className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>No cutting plans to visualize</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}