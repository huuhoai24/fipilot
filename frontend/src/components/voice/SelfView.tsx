import { forwardRef } from 'react'
import { User } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SelfViewProps {
  active: boolean
  name?: string
  className?: string
}

function SignalBars() {
  return (
    <span className="flex items-end gap-[2px]" aria-hidden="true">
      <span className="h-[5px] w-[2px] rounded-sm bg-emerald-400" />
      <span className="h-[8px] w-[2px] rounded-sm bg-emerald-400" />
      <span className="h-[11px] w-[2px] rounded-sm bg-emerald-400" />
      <span className="h-[15px] w-[2px] rounded-sm bg-emerald-400" />
    </span>
  )
}

export const SelfView = forwardRef<HTMLVideoElement, SelfViewProps>(function SelfView(
  { active, name, className },
  ref,
) {
  return (
    <div
      className={cn(
        'relative h-[340px] w-[487px] max-w-full overflow-hidden rounded-2xl border border-white/10 bg-zinc-900',
        className,
      )}
    >
      {active ? (
        <video
          ref={ref}
          autoPlay
          playsInline
          muted
          className="h-full w-full scale-x-[-1] object-cover"
        />
      ) : (
        <div className="flex h-full w-full flex-col items-center justify-center gap-3 text-center p-6">
          <div className="flex h-20 w-20 items-center justify-center rounded-full border border-white/10 bg-white/10 text-white/80 shadow-inner">
            <User className="h-10 w-10" />
          </div>
          <span className="text-sm font-semibold text-white/90">{name || 'Ứng viên'}</span>
          <span className="text-xs text-white/40">Camera đã tắt</span>
        </div>
      )}

      <div className="absolute bottom-3 left-3 z-10 flex items-center gap-1.5 rounded-lg border border-white/15 bg-black/70 px-2.5 py-1">
        <SignalBars />
        <span className="text-[10px] font-mono font-semibold text-emerald-400">Trực tiếp</span>
      </div>
    </div>
  )
})
