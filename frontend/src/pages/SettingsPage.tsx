import React, { useState } from 'react'
import { Save } from 'lucide-react'
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
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-2xl font-bold tracking-tight-display text-text-primary">Settings</h1>
        <p className="mt-1 text-sm text-text-muted">Default controls for the V2 text interview experience.</p>
      </div>

      <Card className="max-w-3xl">
        <CardHeader>
          <CardTitle>Interview Defaults</CardTitle>
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <Label htmlFor="settings-language">Language</Label>
              <Select id="settings-language" value={language} onChange={(event) => setLanguage(event.target.value as InterviewLanguage)}>
                <option value="vi">Vietnamese</option>
                <option value="en">English</option>
              </Select>
            </div>
            <div>
              <Label htmlFor="settings-experience-level">Experience Level</Label>
              <Select id="settings-experience-level" value={experienceLevel} onChange={(event) => setExperienceLevel(event.target.value as ExperienceLevel)}>
                <option value="intern">Intern</option>
                <option value="junior">Junior</option>
                <option value="middle">Middle</option>
                <option value="senior">Senior</option>
              </Select>
            </div>
            <div>
              <Label htmlFor="settings-interview-style">Interview Style</Label>
              <Select id="settings-interview-style" value={interviewStyle} onChange={(event) => setInterviewStyle(event.target.value as InterviewStyle)}>
                <option value="technical">Technical</option>
                <option value="behavioral">Behavioral</option>
                <option value="mixed">Mixed</option>
              </Select>
            </div>
            <div>
              <Label htmlFor="settings-duration">Duration</Label>
              <Input
                id="settings-duration"
                type="number"
                min={5}
                max={180}
                value={durationMinutes}
                onChange={(event) => setDurationMinutes(Number(event.target.value) || 30)}
              />
            </div>
            <div>
              <Label htmlFor="settings-question-count">Question Count</Label>
              <Input
                id="settings-question-count"
                type="number"
                min={1}
                value={questionCount}
                onChange={(event) => setQuestionCount(Number(event.target.value) || 10)}
              />
            </div>
          </div>

          <div>
            <Label htmlFor="settings-objective">Objective</Label>
            <Textarea id="settings-objective" rows={4} value={objective} onChange={(event) => setObjective(event.target.value)} />
          </div>

          <div className="flex items-center justify-end gap-3 border-t border-border pt-5">
            <span className="text-xs text-text-faint" role="status" aria-live="polite">
              {saved ? 'Preferences saved on this device.' : 'Changes apply to new interviews.'}
            </span>
            <Button type="button" onClick={handleSave}>
              <Save className="h-4 w-4" />
              {saved ? 'Saved' : 'Save preferences'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
