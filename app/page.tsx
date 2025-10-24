'use client'

import { useState } from 'react'
import { Header } from '@/components/Header'
import { InputForms } from '@/components/InputForms'
import { OptimizationResults } from '@/components/OptimizationResults'
import { Visualization } from '@/components/Visualization'
import { ExportPanel } from '@/components/ExportPanel'
import { useOptimization } from '@/hooks/useOptimization'

export default function Home() {
  const [currentStep, setCurrentStep] = useState(1)
  const [inputData, setInputData] = useState({
    lumberStock: [],
    parts: [],
    cuttingParameters: {
      kerf: 3.0,
      minOffcut: 50.0,
      tolerance: 2.0,
      grainDirectionEnforcement: false,
      optimizationPriority: 'efficiency'
    }
  })

  const { 
    optimize, 
    result, 
    loading, 
    error 
  } = useOptimization()

  const handleOptimize = async () => {
    await optimize(inputData)
    setCurrentStep(4) // Go to results
  }

  const steps = [
    { id: 1, name: 'Input Data', description: 'Enter lumber stock and parts' },
    { id: 2, name: 'Parameters', description: 'Set cutting parameters' },
    { id: 3, name: 'Optimize', description: 'Run optimization algorithm' },
    { id: 4, name: 'Results', description: 'View cutting plans and export' }
  ]

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Steps */}
        <div className="mb-8">
          <nav aria-label="Progress">
            <ol className="flex items-center justify-center space-x-8">
              {steps.map((step, stepIdx) => (
                <li key={step.name} className={`relative ${stepIdx !== steps.length - 1 ? 'pr-8 sm:pr-20' : ''}`}>
                  {currentStep > step.id ? (
                    <div className="absolute inset-0 flex items-center" aria-hidden="true">
                      <div className="h-0.5 w-full bg-primary-600" />
                    </div>
                  ) : currentStep === step.id ? (
                    <div className="absolute inset-0 flex items-center" aria-hidden="true">
                      <div className="h-0.5 w-full bg-gray-200 dark:bg-gray-700" />
                    </div>
                  ) : (
                    <div className="absolute inset-0 flex items-center" aria-hidden="true">
                      <div className="h-0.5 w-full bg-gray-200 dark:bg-gray-700" />
                    </div>
                  )}
                  <div className={`relative flex h-8 w-8 items-center justify-center rounded-full ${
                    currentStep >= step.id 
                      ? 'bg-primary-600 text-white' 
                      : 'bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400'
                  }`}>
                    <span className="text-sm font-medium">{step.id}</span>
                  </div>
                  <div className="mt-2 text-center">
                    <p className={`text-sm font-medium ${
                      currentStep >= step.id ? 'text-primary-600' : 'text-gray-500 dark:text-gray-400'
                    }`}>
                      {step.name}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{step.description}</p>
                  </div>
                </li>
              ))}
            </ol>
          </nav>
        </div>

        {/* Main Content */}
        <div className="bg-white dark:bg-gray-800 shadow-xl rounded-lg">
          {currentStep === 1 && (
            <InputForms 
              data={inputData} 
              onChange={setInputData}
              onNext={() => setCurrentStep(2)}
            />
          )}
          
          {currentStep === 2 && (
            <div className="p-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                Cutting Parameters
              </h2>
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Kerf (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={inputData.cuttingParameters.kerf}
                      onChange={(e) => setInputData({
                        ...inputData,
                        cuttingParameters: {
                          ...inputData.cuttingParameters,
                          kerf: parseFloat(e.target.value) || 0
                        }
                      })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Minimum Offcut (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={inputData.cuttingParameters.minOffcut}
                      onChange={(e) => setInputData({
                        ...inputData,
                        cuttingParameters: {
                          ...inputData.cuttingParameters,
                          minOffcut: parseFloat(e.target.value) || 0
                        }
                      })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Tolerance (mm)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={inputData.cuttingParameters.tolerance}
                      onChange={(e) => setInputData({
                        ...inputData,
                        cuttingParameters: {
                          ...inputData.cuttingParameters,
                          tolerance: parseFloat(e.target.value) || 0
                        }
                      })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Optimization Priority
                    </label>
                    <select
                      value={inputData.cuttingParameters.optimizationPriority}
                      onChange={(e) => setInputData({
                        ...inputData,
                        cuttingParameters: {
                          ...inputData.cuttingParameters,
                          optimizationPriority: e.target.value
                        }
                      })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                    >
                      <option value="efficiency">Maximize Efficiency</option>
                      <option value="cost">Minimize Cost</option>
                      <option value="speed">Fastest Cut</option>
                    </select>
                  </div>
                </div>
                
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="grainDirection"
                    checked={inputData.cuttingParameters.grainDirectionEnforcement}
                    onChange={(e) => setInputData({
                      ...inputData,
                      cuttingParameters: {
                        ...inputData.cuttingParameters,
                        grainDirectionEnforcement: e.target.checked
                      }
                    })}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600 rounded"
                  />
                  <label htmlFor="grainDirection" className="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                    Enforce grain direction
                  </label>
                </div>
              </div>
              
              <div className="mt-8 flex justify-between">
                <button
                  onClick={() => setCurrentStep(1)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                >
                  Previous
                </button>
                <button
                  onClick={() => setCurrentStep(3)}
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
                >
                  Next
                </button>
              </div>
            </div>
          )}
          
          {currentStep === 3 && (
            <div className="p-8 text-center">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                Ready to Optimize
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-8">
                Click the button below to run the optimization algorithm and generate cutting plans.
              </p>
              
              <div className="space-y-4">
                <button
                  onClick={handleOptimize}
                  disabled={loading}
                  className="px-8 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-medium rounded-lg shadow-lg transition-colors"
                >
                  {loading ? 'Optimizing...' : 'Start Optimization'}
                </button>
                
                {error && (
                  <div className="text-red-600 dark:text-red-400 text-sm">
                    {error}
                  </div>
                )}
              </div>
              
              <div className="mt-8 flex justify-between">
                <button
                  onClick={() => setCurrentStep(2)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                >
                  Previous
                </button>
              </div>
            </div>
          )}
          
          {currentStep === 4 && result && (
            <div className="p-8">
              <OptimizationResults result={result} />
              <Visualization result={result} />
              <ExportPanel result={result} />
              
              <div className="mt-8 flex justify-between">
                <button
                  onClick={() => setCurrentStep(1)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                >
                  Start Over
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}