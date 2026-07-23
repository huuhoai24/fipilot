import React, { useState } from 'react'
import { Save } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Input, Label, Select, Textarea } from '@/components/ui/Input'

export function SettingsPage() {
  const [language, setLanguage] = useState('vi')
  const [experienceLevel, setExperienceLevel] = useState('junior')
  const [durationMinutes, setDurationMinutes] = useState(30)
  const [questionCount, setQuestionCount] = useState(10)
  const [objective, setObjective] = useState('Evaluate technical knowledge and practical experience')

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
              <Label>Language</Label>
              <Select value={language} onChange={(event) => setLanguage(event.target.value)}>
                <option value="vi">Vietnamese</option>
                <option value="en">English</option>
              </Select>
            </div>
            <div>
              <Label>Experience Level</Label>
              <Select value={experienceLevel} onChange={(event) => setExperienceLevel(event.target.value)}>
                <option value="intern">Intern</option>
                <option value="junior">Junior</option>
                <option value="middle">Middle</option>
                <option value="senior">Senior</option>
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

          <div className="flex justify-end">
            <Button type="button">
              <Save className="h-4 w-4" />
              Save Locally
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
