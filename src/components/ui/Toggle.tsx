import React from 'react'
import { cn } from '@/lib/utils'

interface ToggleProps {
  checked: boolean
  onChange: (checked: boolean) => void
  label?: string
  description?: string
  disabled?: boolean
}

export function Toggle({ checked, onChange, label, description, disabled }: ToggleProps) {
  return (
    <div className="flex items-center justify-between gap-4 py-1">
      {(label || description) && (
        <div>
          {label && <div className="text-sm text-text-primary">{label}</div>}
          {description && <div className="text-xs text-text-muted mt-0.5">{description}</div>}
        </div>
      )}
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        disabled={disabled}
        onClick={() => onChange(!checked)}
        className={cn(
          'relative h-6 w-11 shrink-0 rounded-full transition-colors duration-150 disabled:opacity-40',
          checked ? 'bg-accent' : 'bg-surface-raised border border-border'
        )}
      >
        <span
          className={cn(
            'absolute top-0.5 left-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform duration-150',
            checked && 'translate-x-5'
          )}
        />
      </button>
    </div>
  )
}
