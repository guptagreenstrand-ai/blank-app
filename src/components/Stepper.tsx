import React from 'react';
import { Check } from 'lucide-react';

interface Step {
  id: number;
  title: string;
  description: string;
}

interface StepperProps {
  steps: Step[];
  currentStep: number;
  onStepClick: (step: number) => void;
}

const Stepper: React.FC<StepperProps> = ({ steps, currentStep, onStepClick }) => {
  return (
    <div className="w-full">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-center">
            <div className="flex flex-col items-center">
              <button
                onClick={() => onStepClick(step.id)}
                className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-colors ${
                  step.id < currentStep
                    ? 'bg-success text-white'
                    : step.id === currentStep
                    ? 'bg-accent-primary text-white'
                    : 'bg-tertiary text-muted'
                }`}
                disabled={step.id > currentStep}
              >
                {step.id < currentStep ? (
                  <Check className="w-5 h-5" />
                ) : (
                  step.id
                )}
              </button>
              <div className="mt-2 text-center">
                <div className={`text-sm font-medium ${
                  step.id <= currentStep ? 'text-primary' : 'text-muted'
                }`}>
                  {step.title}
                </div>
                <div className="text-xs text-secondary">
                  {step.description}
                </div>
              </div>
            </div>
            {index < steps.length - 1 && (
              <div className={`flex-1 h-0.5 mx-4 ${
                step.id < currentStep ? 'bg-success' : 'bg-tertiary'
              }`} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Stepper;