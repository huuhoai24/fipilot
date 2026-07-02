import React from 'react'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

const steps = [
  { n: 1, label: 'Tải CV' },
  { n: 2, label: 'Xem hồ sơ' },
  { n: 3, label: 'Chọn template' },
  { n: 4, label: 'Bắt đầu' },
]

export function StepIndicator({ currentStep }: { currentStep: number }) {
  return (
    <div className="flex items-center">
      {steps.map((step, idx) => (
        <React.Fragment key={step.n}>
          <div className="flex flex-col items-center gap-2">
            <div
              className={cn(
                'flex h-9 w-9 items-center justify-center rounded-full border text-sm font-semibold transition-colors duration-150',
                currentStep > step.n
                  ? 'border-accent bg-accent text-white'
                  : currentStep === step.n
                  ? 'border-accent bg-accent-soft text-accent'
                  : 'border-border bg-surface text-text-faint'
              )}
            >
              {currentStep > step.n ? <Check className="h-4 w-4" /> : step.n}
            </div>
            <span
              className={cn(
                'text-xs font-medium',
                currentStep >= step.n ? 'text-text-primary' : 'text-text-faint'
              )}
            >
              {step.label}
            </span>
          </div>
          {idx < steps.length - 1 && (
            <div
              className={cn(
                'mx-3 mb-5 h-px w-12 sm:w-24 transition-colors duration-150',
                currentStep > step.n ? 'bg-accent' : 'bg-border'
              )}
            />
          )}
        </React.Fragment>
      ))}
    </div>
  )
}
