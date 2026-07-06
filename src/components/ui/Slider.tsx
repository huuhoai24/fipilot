import React from 'react'
import { cn } from '@/lib/utils'

interface SliderProps {
  value: number
  min: number
  max: number
  step?: number
  onChange: (value: number) => void
  className?: string
  accentColor?: string
}

export function Slider({ value, min, max, step = 1, onChange, className, accentColor = '#6366F1' }: SliderProps) {
  const pct = ((value - min) / (max - min)) * 100
  return (
    <input
      type="range"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      className={cn('w-full h-1.5 rounded-full appearance-none cursor-pointer slider-thumb', className)}
      style={{
        background: `linear-gradient(to right, ${accentColor} 0%, ${accentColor} ${pct}%, #2A2D3E ${pct}%, #2A2D3E 100%)`,
      }}
    />
  )
}
