import React from 'react'
import { Link, type LinkProps } from 'react-router-dom'
import { cn } from '@/lib/utils'

type Variant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline'
type Size = 'sm' | 'md' | 'lg' | 'icon'
type Treatment = 'legacy' | 'restrained'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
  treatment?: Treatment
}

const variantClasses: Record<Variant, string> = {
  primary: 'bg-accent text-accent-contrast hover:bg-accent-hover shadow-[0_0_0_1px_var(--color-accent)]',
  secondary: 'bg-surface-raised text-text-primary border border-border hover:border-accent/50',
  ghost: 'bg-transparent text-text-muted hover:text-text-primary hover:bg-surface-raised',
  danger: 'bg-danger/10 text-danger border border-danger/30 hover:bg-danger/20',
  outline: 'bg-transparent border border-border text-text-primary hover:border-accent hover:text-accent',
}

const sizeClasses: Record<Size, string> = {
  sm: 'h-8 px-3 text-xs gap-1.5',
  md: 'h-10 px-4 text-sm gap-2',
  lg: 'h-12 px-6 text-sm gap-2',
  icon: 'h-9 w-9 p-0 justify-center',
}

const treatmentClasses: Record<Treatment, string> = {
  legacy: 'rounded-md transition-colors duration-150',
  restrained: 'rounded-lg transition-colors duration-150',
}

function buttonClassName(
  variant: Variant,
  size: Size,
  treatment: Treatment,
  className?: string,
) {
  return cn(
    'inline-flex items-center justify-center font-medium disabled:opacity-40 disabled:cursor-not-allowed whitespace-nowrap',
    variantClasses[variant],
    sizeClasses[size],
    treatmentClasses[treatment],
    className,
  )
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    className,
    variant = 'primary',
    size = 'md',
    treatment = 'legacy',
    children,
    ...props
  }, ref) => {
    return (
      <button
        ref={ref}
        className={buttonClassName(variant, size, treatment, className)}
        {...props}
      >
        {children}
      </button>
    )
  }
)
Button.displayName = 'Button'

interface ButtonLinkProps extends LinkProps {
  variant?: Variant
  size?: Size
  treatment?: Treatment
}

export const ButtonLink = React.forwardRef<HTMLAnchorElement, ButtonLinkProps>(
  ({
    className,
    variant = 'primary',
    size = 'md',
    treatment = 'legacy',
    children,
    ...props
  }, ref) => (
    <Link
      ref={ref}
      className={buttonClassName(variant, size, treatment, className)}
      {...props}
    >
      {children}
    </Link>
  ),
)
ButtonLink.displayName = 'ButtonLink'
