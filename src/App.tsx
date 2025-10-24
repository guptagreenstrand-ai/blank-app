import React, { useState, useEffect } from 'react';
import { ThemeProvider } from './contexts/ThemeContext';
import Header from './components/Header';
import Stepper from './components/Stepper';
import InventoryForm from './components/InventoryForm';
import PartsForm from './components/PartsForm';
import ParametersForm from './components/ParametersForm';
import OptimizationResults from './components/OptimizationResults';
import { OptimizationData, LumberStock, Part, CuttingParameters } from './types';

const App: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [optimizationData, setOptimizationData] = useState<OptimizationData>({
    lumberStock: [],
    parts: [],
    cuttingParameters: {
      kerf: 3.0,
      minOffcut: 50.0,
      tolerance: 1.0,
      grainDirectionEnforcement: true,
      optimizationPriority: 'efficiency'
    }
  });
  const [optimizationResults, setOptimizationResults] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const steps = [
    { id: 1, title: 'Inventory', description: 'Enter lumber stock' },
    { id: 2, title: 'Parts', description: 'Define cut parts' },
    { id: 3, title: 'Parameters', description: 'Set cutting parameters' },
    { id: 4, title: 'Optimize', description: 'Run optimization' },
    { id: 5, title: 'Results', description: 'View results' }
  ];

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleLumberStockUpdate = (lumberStock: LumberStock[]) => {
    setOptimizationData(prev => ({ ...prev, lumberStock }));
  };

  const handlePartsUpdate = (parts: Part[]) => {
    setOptimizationData(prev => ({ ...prev, parts }));
  };

  const handleParametersUpdate = (cuttingParameters: CuttingParameters) => {
    setOptimizationData(prev => ({ ...prev, cuttingParameters }));
  };

  const handleOptimize = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(optimizationData),
      });

      if (!response.ok) {
        throw new Error('Optimization failed');
      }

      const results = await response.json();
      setOptimizationResults(results);
      setCurrentStep(5);
    } catch (error) {
      console.error('Optimization error:', error);
      alert('Optimization failed. Please check your inputs and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const loadSampleData = async () => {
    try {
      const response = await fetch('http://localhost:8000/sample-data');
      const data = await response.json();
      
      setOptimizationData({
        lumberStock: data.lumber_stock,
        parts: data.parts,
        cuttingParameters: data.cutting_parameters
      });
    } catch (error) {
      console.error('Failed to load sample data:', error);
    }
  };

  useEffect(() => {
    loadSampleData();
  }, []);

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <InventoryForm
            lumberStock={optimizationData.lumberStock}
            onUpdate={handleLumberStockUpdate}
            onNext={handleNext}
          />
        );
      case 2:
        return (
          <PartsForm
            parts={optimizationData.parts}
            onUpdate={handlePartsUpdate}
            onNext={handleNext}
            onPrevious={handlePrevious}
          />
        );
      case 3:
        return (
          <ParametersForm
            parameters={optimizationData.cuttingParameters}
            onUpdate={handleParametersUpdate}
            onNext={handleNext}
            onPrevious={handlePrevious}
          />
        );
      case 4:
        return (
          <div className="card text-center">
            <h2 className="text-2xl font-bold mb-6">Ready to Optimize</h2>
            <div className="mb-6">
              <p className="text-lg mb-4">Review your inputs and click optimize to generate the best cutting plan.</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <strong>Lumber Stock:</strong> {optimizationData.lumberStock.length} types
                </div>
                <div>
                  <strong>Parts:</strong> {optimizationData.parts.length} types
                </div>
                <div>
                  <strong>Total Parts:</strong> {optimizationData.parts.reduce((sum, part) => sum + part.total_units, 0)}
                </div>
              </div>
            </div>
            <div className="flex gap-4 justify-center">
              <button
                onClick={handlePrevious}
                className="btn btn-secondary"
              >
                Previous
              </button>
              <button
                onClick={handleOptimize}
                disabled={isLoading}
                className="btn btn-primary"
              >
                {isLoading ? 'Optimizing...' : 'Optimize Cutting Plan'}
              </button>
            </div>
          </div>
        );
      case 5:
        return (
          <OptimizationResults
            results={optimizationResults}
            onRestart={() => setCurrentStep(1)}
          />
        );
      default:
        return null;
    }
  };

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-primary">
        <Header />
        <main className="container py-8">
          <Stepper
            steps={steps}
            currentStep={currentStep}
            onStepClick={setCurrentStep}
          />
          <div className="mt-8">
            {renderStepContent()}
          </div>
        </main>
      </div>
    </ThemeProvider>
  );
};

export default App;