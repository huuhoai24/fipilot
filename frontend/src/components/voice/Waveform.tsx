import { cn } from '@/lib/utils'

interface WaveformProps {
  active?: boolean
  className?: string
}

/**
 * Radiating interview waveform used as the live voice-stage backdrop.
 * Mirrors the fipilot-v1 InterviewStage visual language.
 */
export function Waveform({ active = false, className }: WaveformProps) {
  const rays = Array.from({ length: 31 }, (_, index) => index)
  const contours = [0, 1, 2, 3, 4, 5]

  return (
    <svg
      className={cn('pointer-events-none absolute inset-0 h-full w-full', className)}
      viewBox="0 0 1440 190"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="voice-wave-fade" x1="0" x2="1">
          <stop offset="0" stopColor="#77f8f0" stopOpacity="0.16" />
          <stop offset="0.5" stopColor="#a1fff9" stopOpacity="0.75" />
          <stop offset="1" stopColor="#77f8f0" stopOpacity="0.16" />
        </linearGradient>
      </defs>
      <g
        className={cn(
          'origin-center transition-opacity duration-500',
          active ? 'opacity-100' : 'opacity-30',
        )}
        style={{ animation: active ? 'voiceWaveRays 3.2s ease-in-out infinite' : undefined }}
      >
        {rays.map((ray) => {
          const x = ray * 48
          return <path key={ray} d={`M720 82 L${x} 190`} stroke="url(#voice-wave-fade)" strokeWidth="1.5" fill="none" />
        })}
      </g>
      <g className={cn(active ? 'opacity-90' : 'opacity-30')}>
        {contours.map((contour) => {
          const y = 80 + contour * 18
          const arch = 20 + contour * 3
          return (
            <path
              key={contour}
              d={`M0 ${y + 52} Q360 ${y - arch} 720 ${y} T1440 ${y + 52}`}
              stroke="url(#voice-wave-fade)"
              strokeWidth="1.5"
              fill="none"
            />
          )
        })}
      </g>
      <path
        className={cn(active ? 'opacity-90' : 'opacity-40')}
        style={{ animation: active ? 'voiceWaveCrest 4s ease-in-out infinite' : undefined }}
        d="M0 126 C80 110 112 127 174 108 C232 91 287 112 351 93 C415 77 480 101 540 84 C606 64 649 91 708 73 C762 58 821 91 882 72 C945 58 1008 92 1062 79 C1125 65 1196 103 1262 91 C1324 82 1381 112 1440 104"
        stroke="url(#voice-wave-fade)"
        strokeWidth="2"
        fill="none"
      />
    </svg>
  )
}
