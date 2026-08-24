import React from 'react'

interface SpeechWaveformProps {
  active?: boolean
  mode?: 'ai' | 'user' | 'idle'
}

export function SpeechWaveform({ active = false, mode = 'idle' }: SpeechWaveformProps) {
  const rays = Array.from({ length: 31 }, (_, index) => index)
  const contours = [0, 1, 2, 3, 4, 5]

  const strokeColor = mode === 'ai'
    ? 'rgba(42, 199, 174, 0.45)'
    : mode === 'user'
      ? 'rgba(96, 165, 250, 0.45)'
      : 'rgba(255, 255, 255, 0.12)'

  const rayColor = mode === 'ai'
    ? 'rgba(42, 199, 174, 0.18)'
    : mode === 'user'
      ? 'rgba(96, 165, 250, 0.18)'
      : 'rgba(255, 255, 255, 0.05)'

  return (
    <div className="pointer-events-none absolute inset-x-0 bottom-0 flex h-48 w-full items-end justify-center overflow-hidden">
      <svg
        className={`h-full w-full transition-opacity duration-500 ${
          active ? 'opacity-100' : 'opacity-40'
        }`}
        viewBox="0 0 1440 190"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="ai-wave-glow" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#2ac7ae" stopOpacity="0.05" />
            <stop offset="50%" stopColor={mode === 'user' ? '#60a5fa' : '#2ac7ae'} stopOpacity={active ? "0.8" : "0.25"} />
            <stop offset="100%" stopColor="#2ac7ae" stopOpacity="0.05" />
          </linearGradient>
        </defs>

        <g className="transition-all duration-700">
          {rays.map((ray) => {
            const x = ray * 48
            return (
              <path
                key={ray}
                d={`M720 82 L${x} 190`}
                stroke={rayColor}
                strokeWidth="1"
                className={active ? 'animate-pulse' : ''}
                style={{ animationDelay: `${(ray % 7) * 120}ms` }}
              />
            )
          })}
        </g>

        <g>
          {contours.map((contour) => {
            const y = 80 + contour * 18
            const arch = 20 + contour * 3 + (active ? (contour % 2 === 0 ? 10 : -6) : 0)
            return (
              <path
                key={contour}
                d={`M0 ${y + 52} Q360 ${y - arch} 720 ${y} T1440 ${y + 52}`}
                fill="none"
                stroke={strokeColor}
                strokeWidth="1.2"
                className="transition-all duration-500"
              />
            )
          })}
        </g>

        <path
          d="M0 126 C80 110 112 127 174 108 C232 91 287 112 351 93 C415 77 480 101 540 84 C606 64 649 91 708 73 C762 58 821 91 882 72 C945 58 1008 92 1062 79 C1125 65 1196 103 1262 91 C1324 82 1381 112 1440 104"
          fill="none"
          stroke="url(#ai-wave-glow)"
          strokeWidth={active ? "2.5" : "1.5"}
          className={`transition-all duration-300 ${active ? 'animate-pulse' : ''}`}
        />
      </svg>
    </div>
  )
}
