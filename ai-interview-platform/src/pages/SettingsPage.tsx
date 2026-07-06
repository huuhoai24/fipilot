import React, { useState } from 'react'
import { Plus, Save, Trash2 } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input, Select, Label } from '@/components/ui/Input'
import { Slider } from '@/components/ui/Slider'
import { Toggle } from '@/components/ui/Toggle'
import { Badge } from '@/components/ui/Badge'
import { mockConfigs } from '@/data/mockData'

export function SettingsPage() {
  const [configs] = useState(mockConfigs)
  const [activeId, setActiveId] = useState(configs[0]?.id)
  const active = configs.find((c) => c.id === activeId) ?? configs[0]

  const [name, setName] = useState(active.name)
  const [duration, setDuration] = useState(active.duration_minutes)
  const [easy, setEasy] = useState(active.difficulty_mix.easy)
  const [medium, setMedium] = useState(active.difficulty_mix.medium)
  const [hard, setHard] = useState(active.difficulty_mix.hard)
  const [voiceEnabled, setVoiceEnabled] = useState(active.voice_enabled)
  const [avatarEnabled, setAvatarEnabled] = useState(active.avatar_enabled)
  const [autoEvaluate, setAutoEvaluate] = useState(active.auto_evaluate)

  const selectConfig = (id: string) => {
    const cfg = configs.find((c) => c.id === id)
    if (!cfg) return
    setActiveId(id)
    setName(cfg.name)
    setDuration(cfg.duration_minutes)
    setEasy(cfg.difficulty_mix.easy)
    setMedium(cfg.difficulty_mix.medium)
    setHard(cfg.difficulty_mix.hard)
    setVoiceEnabled(cfg.voice_enabled)
    setAvatarEnabled(cfg.avatar_enabled)
    setAutoEvaluate(cfg.auto_evaluate)
  }

  const totalQuestions = easy + medium + hard

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-bold tracking-tight-display text-text-primary">Interview Settings</h1>
          <p className="mt-1 text-sm text-text-muted">Cấu hình các profile dùng để tạo phiên phỏng vấn.</p>
        </div>
        <Button variant="secondary">
          <Plus className="h-4 w-4" /> Config mới
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[280px_1fr]">
        <Card>
          <div className="border-b border-border px-4 py-3">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-text-muted">Configs</h3>
          </div>
          <div className="divide-y divide-border">
            {configs.map((c) => (
              <button
                key={c.id}
                onClick={() => selectConfig(c.id)}
                className={`block w-full px-4 py-3 text-left transition-colors duration-150 ${
                  activeId === c.id ? 'bg-accent-soft' : 'hover:bg-surface-raised'
                }`}
              >
                <div className={`text-sm font-medium ${activeId === c.id ? 'text-accent' : 'text-text-primary'}`}>
                  {c.name}
                </div>
                <div className="mt-0.5 text-xs text-text-muted">
                  L{c.level} · {c.duration_minutes} phút
                </div>
              </button>
            ))}
          </div>
        </Card>

        <Card>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="sm:col-span-1">
                <Label>Tên config</Label>
                <Input value={name} onChange={(e) => setName(e.target.value)} />
              </div>
              <div>
                <Label>Vai trò</Label>
                <Select defaultValue={active.role}>
                  <option value="data-ai">Data-AI</option>
                  <option value="backend">Backend</option>
                  <option value="frontend">Frontend</option>
                </Select>
              </div>
              <div>
                <Label>Level</Label>
                <Select defaultValue={String(active.level)}>
                  <option value="2">Level 2</option>
                  <option value="3">Level 3</option>
                  <option value="4">Level 4</option>
                </Select>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <Label className="mb-0">Thời lượng phỏng vấn</Label>
                <span className="font-mono text-sm text-text-primary">{duration} phút</span>
              </div>
              <Slider value={duration} min={15} max={120} step={5} onChange={setDuration} />
              <div className="flex justify-between text-xs text-text-faint mt-1">
                <span>15</span>
                <span>120</span>
              </div>
            </div>

            <div className="rounded-lg border border-border bg-surface-raised p-4 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-text-primary">Phân bổ độ khó</span>
                <Badge variant="accent">{totalQuestions} câu hỏi</Badge>
              </div>
              <DifficultyRow label="Dễ" color="#22C55E" value={easy} onChange={setEasy} />
              <DifficultyRow label="Trung bình" color="#F59E0B" value={medium} onChange={setMedium} />
              <DifficultyRow label="Khó" color="#EF4444" value={hard} onChange={setHard} />
            </div>

            <div className="rounded-lg border border-border bg-surface-raised p-4 divide-y divide-border">
              <Toggle
                checked={voiceEnabled}
                onChange={setVoiceEnabled}
                label="Voice Interview"
                description="Cho phép phỏng vấn bằng giọng nói thời gian thực"
              />
              <Toggle
                checked={avatarEnabled}
                onChange={setAvatarEnabled}
                label="Avatar"
                description="Hiển thị avatar động cho AI interviewer"
              />
              <Toggle
                checked={autoEvaluate}
                onChange={setAutoEvaluate}
                label="Auto-Evaluate"
                description="Tự động chạy đánh giá khi phiên kết thúc"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Scoring Rubric</Label>
                <Select defaultValue={active.scoring_rubric}>
                  <option value="default_l3">default_l3</option>
                  <option value="default_l2">default_l2</option>
                  <option value="llm_focus_l4">llm_focus_l4</option>
                </Select>
              </div>
              <div>
                <Label>Ngôn ngữ</Label>
                <Select defaultValue={active.language}>
                  <option value="vi">Tiếng Việt</option>
                  <option value="en">English</option>
                </Select>
              </div>
            </div>

            <div className="flex justify-between border-t border-border pt-4">
              <Button variant="danger" size="sm">
                <Trash2 className="h-3.5 w-3.5" /> Xóa config
              </Button>
              <Button>
                <Save className="h-4 w-4" /> Lưu làm template
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function DifficultyRow({
  label,
  color,
  value,
  onChange,
}: {
  label: string
  color: string
  value: number
  onChange: (v: number) => void
}) {
  return (
    <div className="flex items-center gap-3">
      <span className="w-24 shrink-0 text-sm text-text-muted">{label}</span>
      <div className="flex-1">
        <Slider value={value} min={0} max={10} onChange={onChange} accentColor={color} />
      </div>
      <span className="w-6 shrink-0 text-right font-mono text-sm text-text-primary">{value}</span>
    </div>
  )
}
