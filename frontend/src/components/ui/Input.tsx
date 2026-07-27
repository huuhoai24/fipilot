import React from 'react'
import { cn } from '@/lib/utils'

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        'h-12 w-full rounded-xl border border-border bg-surface-raised px-4 text-sm text-text-primary placeholder:text-text-faint outline-none transition-all duration-200 focus:border-accent focus:ring-4 focus:ring-accent/10',
        className
      )}
      {...props}
    />
  )
)
Input.displayName = 'Input'

export const Select = React.forwardRef<HTMLSelectElement, React.SelectHTMLAttributes<HTMLSelectElement>>(
  ({ className, children, ...props }, ref) => (
    <select
      ref={ref}
      className={cn(
        'h-12 w-full rounded-xl border border-border bg-surface-raised px-4 text-sm text-text-primary outline-none transition-all duration-200 focus:border-accent focus:ring-4 focus:ring-accent/10 appearance-none cursor-pointer',
        className
      )}
      {...props}
    >
      {children}
    </select>
  )
)
Select.displayName = 'Select'

export const Label = ({ className, children, ...props }: React.LabelHTMLAttributes<HTMLLabelElement>) => (
  <label className={cn('mb-2 block text-xs font-semibold text-text-muted', className)} {...props}>
    {children}
  </label>
)

export const Textarea = React.forwardRef<HTMLTextAreaElement, React.TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ className, ...props }, ref) => (
    <textarea
      ref={ref}
      className={cn(
        'w-full rounded-xl border border-border bg-surface-raised px-4 py-3 text-sm leading-6 text-text-primary placeholder:text-text-faint outline-none transition-all duration-200 focus:border-accent focus:ring-4 focus:ring-accent/10 resize-none',
        className
      )}
      {...props}
    />
  )
)
Textarea.displayName = 'Textarea'
