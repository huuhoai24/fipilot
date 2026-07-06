import React, { useEffect, useRef, useState } from 'react'
import { cn } from '@/lib/utils'

interface WaveformProps {
  active: boolean
  variant?: 'agent' | 'candidate'
  className?: string
}

/**
 * Signature hero element per spec 5.1:
 * "a waveform visualizer that mirrors the AI agent's voice in real-time —
 * pulsing indigo rings synchronized to speech amplitude."
 *
 * Since there's no real audio stream in this frontend-only build, amplitude
 * is simulated with smoothed pseudo-random values to approximate natural speech.
 */
export function WaveformVisualizer({ active, variant = 'agent', className }: WaveformProps) {
  const barCount = 24
  const [amplitudes, setAmplitudes] = useState<number[]>(Array(barCount).fill(0.15))
  const targetsRef = useRef<number[]>(Array(barCount).fill(0.15))

  useEffect(() => {
    if (!active) {
      setAmplitudes(Array(barCount).fill(0.08))
      return
    }
    let raf: number
    const tick = () => {
      targetsRef.current = targetsRef.current.map((t, i) => {
        if (Math.random() < 0.08) {
          return 0.15 + Math.random() * 0.85
        }
        return t
      })
      setAmplitudes((prev) =>
        prev.map((v, i) => v + (targetsRef.current[i] - v) * 0.15)
      )
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [active])

  const color = variant === 'agent' ? '#6366F1' : '#8385F5'

  return (
    <div className={cn('relative flex items-center justify-center', className)}>
      {/* pulsing rings, only when active */}
      {active && (
        <>
          <span
            className="absolute h-24 w-24 rounded-full border border-accent/40 animate-pulse-ring"
            style={{ animationDelay: '0s' }}
          />
          <span
            className="absolute h-24 w-24 rounded-full border border-accent/40 animate-pulse-ring"
            style={{ animationDelay: '0.6s' }}
          />
          <span
            className="absolute h-24 w-24 rounded-full border border-accent/40 animate-pulse-ring"
            style={{ animationDelay: '1.2s' }}
          />
        </>
      )}
      <div className="relative z-10 flex h-24 items-center gap-[3px] rounded-2xl bg-surface-raised border border-border px-4">
        {amplitudes.map((amp, i) => (
          <div
            key={i}
            className="w-[3px] rounded-full transition-[height] duration-100 ease-out"
            style={{
              height: `${Math.max(8, amp * 56)}px`,
              backgroundColor: color,
              opacity: active ? 0.55 + amp * 0.45 : 0.3,
            }}
          />
        ))}
      </div>
    </div>
  )
}
