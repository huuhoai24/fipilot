import { cn } from '@/lib/utils'

interface SpeakerGlyphProps {
  className?: string
}

/** Small animated voice glyph shown next to interviewer messages (fipilot-v1 style). */
export function SpeakerGlyph({ className }: SpeakerGlyphProps) {
  return (
    <span
      className={cn('inline-flex items-end gap-[2px] h-4', className)}
      aria-hidden="true"
    >
      {[0, 1, 2, 3, 4].map((bar) => (
        <i
          key={bar}
          className="w-[2px] rounded-full bg-accent"
          style={{
            height: '100%',
            transformOrigin: 'bottom',
            animation: `voiceBar 0.9s ease-in-out ${bar * 0.12}s infinite`,
          }}
        />
      ))}
    </span>
  )
}
