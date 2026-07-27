import React, { useState } from 'react'
import { Check, Save, SlidersHorizontal } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Input, Label, Select, Textarea } from '@/components/ui/Input'
import {
  loadInterviewPreferences,
  saveInterviewPreferences,
} from '@/lib/interviewPreferences'
import type { ExperienceLevel, InterviewLanguage, InterviewStyle } from '@/types'

export function SettingsPage() {
  const preferences = loadInterviewPreferences()
  const [language, setLanguage] = useState<InterviewLanguage>(preferences.language)
  const [experienceLevel, setExperienceLevel] = useState<ExperienceLevel>(preferences.experienceLevel)
  const [interviewStyle, setInterviewStyle] = useState<InterviewStyle>(preferences.interviewStyle)
  const [durationMinutes, setDurationMinutes] = useState(preferences.durationMinutes)
  const [questionCount, setQuestionCount] = useState(preferences.questionCount)
  const [objective, setObjective] = useState(preferences.objective)
  const [saved, setSaved] = useState(false)

  const handleSave = () => {
    saveInterviewPreferences({
      language,
      experienceLevel,
      interviewStyle,
      durationMinutes,
      questionCount,
      objective,
    })
    setSaved(true)
    window.setTimeout(() => setSaved(false), 2200)
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-4xl font-semibold tracking-tight-display text-text-primary sm:text-5xl">Practice preferences</h1>
        <p className="mt-3 max-w-2xl text-base leading-7 text-text-muted">Choose the defaults used whenever you prepare a new text or voice interview.</p>
      </div>

      <Card className="max-w-4xl overflow-hidden">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent-soft">
              <SlidersHorizontal className="h-5 w-5 text-accent" />
            </div>
            <div>
              <CardTitle>Interview defaults</CardTitle>
              <p className="mt-1 text-xs text-text-faint">Stored only on this browser.</p>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <Label>Language</Label>
              <Select value={language} onChange={(event) => setLanguage(event.target.value as InterviewLanguage)}>
                <option value="vi">Vietnamese</option>
                <option value="en">English</option>
              </Select>
            </div>
            <div>
              <Label>Experience Level</Label>
              <Select value={experienceLevel} onChange={(event) => setExperienceLevel(event.target.value as ExperienceLevel)}>
                <option value="intern">Intern</option>
                <option value="junior">Junior</option>
                <option value="middle">Middle</option>
                <option value="senior">Senior</option>
              </Select>
            </div>
            <div>
              <Label>Interview Style</Label>
              <Select value={interviewStyle} onChange={(event) => setInterviewStyle(event.target.value as InterviewStyle)}>
                <option value="technical">Technical</option>
                <option value="behavioral">Behavioral</option>
                <option value="mixed">Mixed</option>
              </Select>
            </div>
            <div>
              <Label>Duration</Label>
              <Input
                type="number"
                min={5}
                max={180}
                value={durationMinutes}
                onChange={(event) => setDurationMinutes(Number(event.target.value) || 30)}
              />
            </div>
            <div>
              <Label>Question Count</Label>
              <Input
                type="number"
                min={1}
                value={questionCount}
                onChange={(event) => setQuestionCount(Number(event.target.value) || 10)}
              />
            </div>
          </div>

          <div>
            <Label>Objective</Label>
            <Textarea rows={4} value={objective} onChange={(event) => setObjective(event.target.value)} />
          </div>

          <div className="flex items-center justify-end gap-3 border-t border-border pt-5">
            <span className="text-xs text-text-faint" role="status" aria-live="polite">
              {saved ? 'Preferences saved on this device.' : 'Changes apply to new interviews.'}
            </span>
            <Button type="button" onClick={handleSave}>
              {saved ? <Check className="h-4 w-4" /> : <Save className="h-4 w-4" />}
              {saved ? 'Saved' : 'Save preferences'}
            </Button>
          </div>
        </CardContent>
      </Card>

    </div>
  )
}
