import React from 'react'
import { cn } from '@/lib/utils'

type BadgeVariant = 'default' | 'accent' | 'success' | 'warning' | 'danger' | 'outline'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant
}

const variantClasses: Record<BadgeVariant, string> = {
  default: 'bg-surface-raised text-text-muted border border-border',
  accent: 'bg-accent-soft text-accent border border-accent/30',
  success: 'bg-success/10 text-success border border-success/30',
  warning: 'bg-warning/10 text-warning border border-warning/30',
  danger: 'bg-danger/10 text-danger border border-danger/30',
  outline: 'bg-transparent text-text-muted border border-border',
}

export function Badge({ className, variant = 'default', children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium leading-5',
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  )
}

export function DifficultyBadge({ difficulty }: { difficulty: 'easy' | 'medium' | 'hard' }) {
  const map = {
    easy: { label: 'Dễ', variant: 'success' as const },
    medium: { label: 'Trung bình', variant: 'warning' as const },
    hard: { label: 'Khó', variant: 'danger' as const },
  }
  const { label, variant } = map[difficulty]
  return <Badge variant={variant}>{label}</Badge>
}
