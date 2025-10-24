'use client'

import { useState } from 'react'
import { Download, FileText, Table, Printer, Share2 } from 'lucide-react'

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

interface ExportPanelProps {
  result: OptimizationResult
}

export function ExportPanel({ result }: ExportPanelProps) {
  const [isExporting, setIsExporting] = useState(false)

  const generateCSV = () => {
    const csvData = []
    
    // Header
    csvData.push([
      'Stick ID',
      'Lumber Type',
      'Length (mm)',
      'Width (mm)',
      'Thickness (mm)',
      'Part Name',
      'Part Length (mm)',
      'Part Width (mm)',
      'Part Thickness (mm)',
      'X Position (mm)',
      'Y Position (mm)',
      'Rotation (deg)',
      'Utilization (%)',
      'Waste Area (mm²)'
    ])
    
    // Data rows
    result.stickPlans.forEach(stick => {
      if (stick.cuts.length === 0) {
        csvData.push([
          stick.stickId.toString(),
          stick.lumberName,
          stick.length.toString(),
          stick.width.toString(),
          stick.thickness.toString(),
          'No cuts',
          '',
          '',
          '',
          '',
          '',
          '',
          stick.utilizationPercentage.toString(),
          stick.wasteArea.toString()
        ])
      } else {
        stick.cuts.forEach(cut => {
          csvData.push([
            stick.stickId.toString(),
            stick.lumberName,
            stick.length.toString(),
            stick.width.toString(),
            stick.thickness.toString(),
            cut.partName,
            cut.length.toString(),
            cut.width.toString(),
            cut.thickness.toString(),
            cut.xPosition.toString(),
            cut.yPosition.toString(),
            cut.rotation.toString(),
            stick.utilizationPercentage.toString(),
            stick.wasteArea.toString()
          ])
        })
      }
    })
    
    return csvData.map(row => row.join(',')).join('\n')
  }

  const generateSummaryCSV = () => {
    const csvData = []
    
    // Header
    csvData.push([
      'Metric',
      'Value',
      'Unit'
    ])
    
    // Summary data
    csvData.push(['Total Sticks', result.summary.totalSticks.toString(), 'count'])
    csvData.push(['Total Parts Cut', result.summary.totalPartsCut.toString(), 'count'])
    csvData.push(['Total Material Used', result.totalMaterialUsed.toFixed(2), 'cubic feet'])
    csvData.push(['Total Waste', result.totalWaste.toFixed(2), 'square feet'])
    csvData.push(['Overall Utilization', result.overallUtilization.toFixed(1), 'percent'])
    csvData.push(['Average Utilization', result.summary.averageUtilization.toFixed(1), 'percent'])
    csvData.push(['Waste Percentage', result.summary.wastePercentage, 'percent'])
    csvData.push(['Total Cuts', result.totalCuts.toString(), 'count'])
    csvData.push(['Optimization Time', result.optimizationTime.toFixed(2), 'seconds'])
    
    return csvData.map(row => row.join(',')).join('\n')
  }

  const downloadCSV = (data: string, filename: string) => {
    const blob = new Blob([data], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  const downloadDetailedCSV = () => {
    setIsExporting(true)
    try {
      const csvData = generateCSV()
      downloadCSV(csvData, 'cutting-plan-detailed.csv')
    } catch (error) {
      console.error('Error generating CSV:', error)
    } finally {
      setIsExporting(false)
    }
  }

  const downloadSummaryCSV = () => {
    setIsExporting(true)
    try {
      const csvData = generateSummaryCSV()
      downloadCSV(csvData, 'cutting-plan-summary.csv')
    } catch (error) {
      console.error('Error generating summary CSV:', error)
    } finally {
      setIsExporting(false)
    }
  }

  const generatePDF = () => {
    setIsExporting(true)
    // PDF generation would be implemented here using jsPDF
    // For now, we'll just show a placeholder
    setTimeout(() => {
      alert('PDF generation feature coming soon!')
      setIsExporting(false)
    }, 1000)
  }

  const printReport = () => {
    window.print()
  }

  const shareResults = () => {
    if (navigator.share) {
      navigator.share({
        title: 'Wooden Cutting Plan Optimization Results',
        text: `Optimized cutting plan with ${result.summary.totalSticks} sticks and ${result.summary.materialEfficiency} efficiency`,
        url: window.location.href
      })
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(
        `Wooden Cutting Plan Optimization Results\n` +
        `Total Sticks: ${result.summary.totalSticks}\n` +
        `Material Efficiency: ${result.summary.materialEfficiency}\n` +
        `Total Parts Cut: ${result.summary.totalPartsCut}\n` +
        `Overall Utilization: ${result.overallUtilization.toFixed(1)}%`
      ).then(() => {
        alert('Results copied to clipboard!')
      })
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">
          Export & Reports
        </h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Download cutting plans, generate reports, and share results
        </p>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Detailed CSV Export */}
          <button
            onClick={downloadDetailedCSV}
            disabled={isExporting}
            className="flex flex-col items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Table className="w-8 h-8 text-blue-600 mb-2" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">Detailed CSV</span>
            <span className="text-xs text-gray-500 dark:text-gray-400 text-center">
              Complete cutting data
            </span>
          </button>

          {/* Summary CSV Export */}
          <button
            onClick={downloadSummaryCSV}
            disabled={isExporting}
            className="flex flex-col items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <FileText className="w-8 h-8 text-green-600 mb-2" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">Summary CSV</span>
            <span className="text-xs text-gray-500 dark:text-gray-400 text-center">
              Key metrics only
            </span>
          </button>

          {/* PDF Report */}
          <button
            onClick={generatePDF}
            disabled={isExporting}
            className="flex flex-col items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <FileText className="w-8 h-8 text-red-600 mb-2" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">PDF Report</span>
            <span className="text-xs text-gray-500 dark:text-gray-400 text-center">
              Professional report
            </span>
          </button>

          {/* Print */}
          <button
            onClick={printReport}
            className="flex flex-col items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            <Printer className="w-8 h-8 text-purple-600 mb-2" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">Print</span>
            <span className="text-xs text-gray-500 dark:text-gray-400 text-center">
              Print cutting plans
            </span>
          </button>
        </div>

        {/* Additional Actions */}
        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-wrap gap-3">
            <button
              onClick={shareResults}
              className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
            >
              <Share2 className="w-4 h-4 mr-2" />
              Share Results
            </button>
            
            <button
              onClick={() => window.location.reload()}
              className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              <Download className="w-4 h-4 mr-2" />
              New Optimization
            </button>
          </div>
        </div>

        {/* Export Status */}
        {isExporting && (
          <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-md">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-3"></div>
              <span className="text-sm text-blue-800 dark:text-blue-200">
                Generating export file...
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}