import React, { useMemo, useState } from 'react'
import { X } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Label, Textarea } from '@/components/ui/Input'
import {
  calculateRoleMatches,
  INTERVIEW_ROLES,
} from '@/lib/roleMatching'
import type { CandidateProfile, ExperienceLevel } from '@/types'

interface InterviewFocusModalProps {
  isOpen: boolean
  profile: CandidateProfile | null
  onBack: () => void
  onClose: () => void
  onContinue: (config: {
    roleTitle: string
    roleId: string
    experienceLevel: ExperienceLevel
    objective?: string
    durationMinutes: number
    questionCount: number
  }) => void
}

const EXPERIENCE_OPTIONS: { id: ExperienceLevel; label: string; sub: string }[] = [
  { id: 'junior', label: 'Junior', sub: '0 – 2 years of experience' },
  { id: 'middle', label: 'Mid-level', sub: '3 – 5 years of experience' },
  { id: 'senior', label: 'Senior', sub: '5+ years of experience' },
]

export function InterviewFocusModal({
  isOpen,
  profile,
  onBack,
  onClose,
  onContinue,
}: InterviewFocusModalProps) {
  const roleMatches = useMemo(() => calculateRoleMatches(profile), [profile])

  const initialRole = roleMatches[0]?.id || 'ai-engineer'
  const initialYears = profile?.years_experience ?? 1
  const initialLevel: ExperienceLevel =
    initialYears > 5 ? 'senior' : initialYears > 2 ? 'middle' : 'junior'

  const [selectedRoleId, setSelectedRoleId] = useState<string>(initialRole)
  const [selectedLevel, setSelectedLevel] = useState<ExperienceLevel>(initialLevel)
  const [objective, setObjective] = useState('')
  const [durationMinutes] = useState(30)
  const [questionCount] = useState(5)

  if (!isOpen) return null

  const selectedRoleMatch = roleMatches.find((r) => r.id === selectedRoleId) || roleMatches[0]
  const selectedRoleDef = INTERVIEW_ROLES.find((r) => r.id === selectedRoleId)

  const handleProceed = () => {
    onContinue({
      roleTitle: selectedRoleMatch?.title || selectedRoleDef?.title || 'AI Interview',
      roleId: selectedRoleId,
      experienceLevel: selectedLevel,
      objective: objective.trim() || undefined,
      durationMinutes,
      questionCount,
    })
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-150">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="focus-title"
        className="relative w-full max-w-3xl max-h-[90vh] flex flex-col rounded-2xl border border-border bg-surface shadow-2xl overflow-hidden transition-colors"
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border px-6 py-4">
          <div>
            <h2 id="focus-title" className="text-lg font-bold text-text-primary">
              Step 2: Choose your interview focus
            </h2>
            <p className="text-xs text-text-muted mt-0.5">
              These percentages show how your CV evidence is distributed across roles.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-text-muted hover:bg-surface-raised hover:text-text-primary transition-colors"
            aria-label="Close"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Body Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Role Matching Cards Grid */}
          <div className="space-y-3">
            <Label className="text-xs font-bold uppercase tracking-wider text-text-muted">
              Select Role Focus
            </Label>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
              {roleMatches.map((match) => {
                const isSelected = selectedRoleId === match.id
                return (
                  <div
                    key={match.id}
                    onClick={() => setSelectedRoleId(match.id)}
                    className={`relative p-4 rounded-xl border cursor-pointer transition-all ${
                      isSelected
                        ? 'border-accent bg-accent/10 shadow-sm ring-1 ring-accent'
                        : 'border-border bg-surface-raised hover:border-border/80 hover:bg-surface-raised/80'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2 mb-1.5">
                      <h3 className="text-sm font-bold text-text-primary leading-tight">
                        {match.title}
                      </h3>
                      <span className="text-sm font-extrabold text-emerald-600 dark:text-emerald-400">
                        {match.score}%
                      </span>
                    </div>
                    <p className="text-xs text-text-muted line-clamp-2 leading-relaxed">
                      {match.summary}
                    </p>
                    {match.matchedSkills.length > 0 && (
                      <div className="mt-2.5 pt-2 border-t border-border/50 text-[11px] text-text-muted leading-relaxed">
                        <span className="font-semibold text-text-primary">Skills: </span>
                        <span>
                          {match.matchedSkills.slice(0, 4).join(' • ')}
                          {match.matchedSkills.length > 4 ? ' • ...' : ''}
                        </span>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>

          {/* Experience Level Selector */}
          <div className="space-y-3">
            <Label className="text-xs font-bold uppercase tracking-wider text-text-muted">
              Select Experience Level
            </Label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {EXPERIENCE_OPTIONS.map((opt) => {
                const isSelected = selectedLevel === opt.id
                return (
                  <div
                    key={opt.id}
                    onClick={() => setSelectedLevel(opt.id)}
                    className={`p-3.5 rounded-xl border cursor-pointer text-center transition-all ${
                      isSelected
                        ? 'border-accent bg-accent/10 shadow-sm ring-1 ring-accent'
                        : 'border-border bg-surface-raised hover:border-border/80'
                    }`}
                  >
                    <strong className="text-sm font-bold block text-text-primary">
                      {opt.label}
                    </strong>
                    <span className="text-xs text-text-muted block mt-0.5">{opt.sub}</span>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Optional Objective / Note */}
          <div className="space-y-2">
            <Label htmlFor="custom-objective" className="text-xs font-bold text-text-primary">
              Custom Focus / Objective (Optional)
            </Label>
            <Textarea
              id="custom-objective"
              rows={2}
              placeholder="e.g. Focus on PyTorch distributed training and system design questions..."
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              className="text-xs"
            />
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-border px-6 py-4 bg-surface-raised/50">
          <Button type="button" variant="ghost" onClick={onBack}>
            Back to Step 1
          </Button>
          <Button
            type="button"
            onClick={handleProceed}
            className="bg-[#13813a] hover:bg-[#0e612c] text-white font-bold px-6"
          >
            Continue
          </Button>
        </div>
      </div>
    </div>
  )
}
