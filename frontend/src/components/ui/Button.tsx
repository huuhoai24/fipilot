import React from 'react'
import { cn } from '@/lib/utils'

type Variant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline'
type Size = 'sm' | 'md' | 'lg' | 'icon'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
}

const variantClasses: Record<Variant, string> = {
  primary: 'bg-accent text-[#07110d] hover:bg-accent-hover shadow-[0_0_0_1px_var(--color-accent),0_12px_32px_rgba(0,0,0,0.14)]',
  secondary: 'bg-surface-raised text-text-primary border border-border hover:border-accent/50 hover:bg-accent-soft',
  ghost: 'bg-transparent text-text-muted hover:text-text-primary hover:bg-surface-raised',
  danger: 'bg-danger/10 text-danger border border-danger/30 hover:bg-danger/20',
  outline: 'bg-transparent border border-border text-text-primary hover:border-accent hover:bg-accent-soft',
}

const sizeClasses: Record<Size, string> = {
  sm: 'h-9 px-3.5 text-xs gap-1.5',
  md: 'h-11 px-5 text-sm gap-2',
  lg: 'h-[52px] px-7 text-sm gap-2.5',
  icon: 'h-10 w-10 p-0 justify-center',
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center rounded-xl font-semibold transition-all duration-300 ease-out hover:-translate-y-0.5 active:translate-y-0 disabled:translate-y-0 disabled:opacity-40 disabled:cursor-not-allowed whitespace-nowrap',
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        {...props}
      >
        {children}
      </button>
    )
  }
)
Button.displayName = 'Button'
