import React from 'react'
import { cn } from '@/lib/utils'

interface VoiceWaveformPlaceholderProps {
  active?: boolean
  label?: string
}

const barHeights = [18, 34, 24, 46, 30, 52, 28, 42, 20, 36, 18]

export function VoiceWaveformPlaceholder({
  active = false,
  label = 'Voice activity',
}: VoiceWaveformPlaceholderProps) {
  return (
    <div
      className="flex h-16 items-center justify-center gap-1.5"
      role="img"
      aria-label={label}
    >
      {barHeights.map((height, index) => (
        <span
          key={`${height}-${index}`}
          className={cn(
            'w-1.5 rounded-full',
            active ? 'animate-pulse bg-accent' : 'bg-border'
          )}
          style={{
            height,
            animationDelay: active ? `${index * 70}ms` : undefined,
          }}
          aria-hidden="true"
        />
      ))}
    </div>
  )
}
