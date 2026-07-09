import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(iso: string, withTime = false): string {
  const d = new Date(iso)
  const date = d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
  if (!withTime) return date
  const time = d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
  return `${date} ${time}`
}

export function formatDuration(ms: number): string {
  const totalSec = Math.floor(ms / 1000)
  const m = Math.floor(totalSec / 60)
  const s = totalSec % 60
  return `${m}:${s.toString().padStart(2, '0')}`
}

export function formatElapsed(startedAt: string): string {
  const diff = Date.now() - new Date(startedAt).getTime()
  const totalSec = Math.max(0, Math.floor(diff / 1000))
  const h = Math.floor(totalSec / 3600)
  const m = Math.floor((totalSec % 3600) / 60)
  const s = totalSec % 60
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

export function scoreColor(score: number, max = 10): string {
  const pct = score / max
  if (pct >= 0.75) return 'text-success'
  if (pct >= 0.5) return 'text-warning'
  return 'text-danger'
}

export function scoreBarColor(score: number, max = 10): string {
  const pct = score / max
  if (pct >= 0.75) return 'bg-success'
  if (pct >= 0.5) return 'bg-warning'
  return 'bg-danger'
}

export function difficultyLabel(d: 'easy' | 'medium' | 'hard'): string {
  return { easy: 'Dễ', medium: 'Trung bình', hard: 'Khó' }[d]
}

export function recommendationLabel(r: string): string {
  const map: Record<string, string> = {
    strong_hire: 'Rất nên tuyển',
    hire: 'Nên tuyển',
    consider: 'Xem xét',
    reject: 'Không phù hợp',
  }
  return map[r] ?? r
}
