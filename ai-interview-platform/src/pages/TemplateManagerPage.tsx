import React, { useState } from 'react'
import {
  Plus,
  Search,
  Pencil,
  ChevronDown,
  ChevronUp,
  Upload,
  Save,
  Tag,
} from 'lucide-react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input, Select } from '@/components/ui/Input'
import { Badge, DifficultyBadge } from '@/components/ui/Badge'
import { mockTemplates } from '@/data/mockData'
import { formatDate } from '@/lib/utils'

export function TemplateManagerPage() {
  const [search, setSearch] = useState('')
  const [roleFilter, setRoleFilter] = useState('all')
  const [levelFilter, setLevelFilter] = useState('all')
  const [expandedId, setExpandedId] = useState<string | null>(mockTemplates[0]?.id ?? null)

  const filtered = mockTemplates.filter((t) => {
    if (roleFilter !== 'all' && t.role !== roleFilter) return false
    if (levelFilter !== 'all' && String(t.level) !== levelFilter) return false
    if (search && !t.title.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-bold tracking-tight-display text-text-primary">Bộ câu hỏi</h1>
          <p className="mt-1 text-sm text-text-muted">Quản lý bộ câu hỏi dùng cho AI interview agent.</p>
        </div>
        <Button>
          <Plus className="h-4 w-4" /> Bộ câu hỏi mới
        </Button>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <Select value={roleFilter} onChange={(e) => setRoleFilter(e.target.value)} className="w-44">
          <option value="all">Tất cả vai trò</option>
          <option value="data-ai">Data-AI</option>
          <option value="backend">Backend</option>
          <option value="frontend">Frontend</option>
        </Select>
        <Select value={levelFilter} onChange={(e) => setLevelFilter(e.target.value)} className="w-36">
          <option value="all">Tất cả level</option>
          <option value="2">Level 2</option>
          <option value="3">Level 3</option>
          <option value="4">Level 4</option>
        </Select>
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-faint" />
          <Input
            placeholder="Tìm bộ câu hỏi…"
            className="pl-9"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="space-y-3">
        {filtered.map((tpl) => (
          <Card key={tpl.id}>
            <button
              onClick={() => setExpandedId(expandedId === tpl.id ? null : tpl.id)}
              className="flex w-full items-center justify-between px-5 py-4 text-left"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-sm font-semibold text-text-primary">{tpl.title}</span>
                  <Badge variant="outline">v{tpl.version}</Badge>
                  <Badge variant="accent">{tpl.questions.length}Q</Badge>
                </div>
                <p className="mt-1 text-xs text-text-muted">
                  Role: {tpl.role} · Level {tpl.level} ·{' '}
                  {(() => {
                    const counts = tpl.questions.reduce(
                      (acc, q) => ({ ...acc, [q.difficulty]: (acc[q.difficulty] ?? 0) + 1 }),
                      {} as Record<string, number>
                    )
                    return `Dễ×${counts.easy ?? 0}/TB×${counts.medium ?? 0}/Khó×${counts.hard ?? 0}`
                  })()}
                </p>
                <p className="mt-0.5 text-xs text-text-faint">
                  Đã dùng {tpl.used_count} lần · Lần cuối: {tpl.last_used_at ? formatDate(tpl.last_used_at) : '—'}
                </p>
              </div>
              <div className="flex items-center gap-2 shrink-0 ml-4">
                <Button variant="ghost" size="sm" onClick={(e) => e.stopPropagation()}>
                  <Pencil className="h-3.5 w-3.5" /> Sửa
                </Button>
                {expandedId === tpl.id ? (
                  <ChevronUp className="h-4 w-4 text-text-faint" />
                ) : (
                  <ChevronDown className="h-4 w-4 text-text-faint" />
                )}
              </div>
            </button>

            {expandedId === tpl.id && (
              <div className="border-t border-border px-5 py-4 animate-fade-in">
                <div className="space-y-3">
                  {tpl.questions.map((q, idx) => (
                    <QuestionRow key={q.id} index={idx} question={q} />
                  ))}
                </div>
                <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-border pt-4">
                  <Button variant="secondary" size="sm">
                    <Plus className="h-3.5 w-3.5" /> Thêm câu hỏi
                  </Button>
                  <Button variant="secondary" size="sm">
                    <Upload className="h-3.5 w-3.5" /> Đăng lên từ Markdown
                  </Button>
                  <Button size="sm" className="ml-auto">
                    <Save className="h-3.5 w-3.5" /> Lưu v{(parseFloat(tpl.version) + 0.1).toFixed(1)}
                  </Button>
                </div>
              </div>
            )}
          </Card>
        ))}

        {filtered.length === 0 && (
          <Card>
            <CardContent className="text-center py-10 text-sm text-text-muted">
              Không tìm thấy bộ câu hỏi phù hợp với bộ lọc.
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

function QuestionRow({
  index,
  question,
}: {
  index: number
  question: (typeof mockTemplates)[0]['questions'][0]
}) {
  const [editing, setEditing] = useState(false)

  return (
    <div className="rounded-lg border border-border bg-surface-raised p-3">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2 flex-1">
          <DifficultyBadge difficulty={question.difficulty} />
          <div className="flex-1">
            <p className="text-sm text-text-primary">
              <span className="text-text-faint font-mono text-xs mr-1">Q{index + 1}</span>
              {question.question}
            </p>
            {editing && (
              <p className="mt-2 text-xs text-text-muted italic">{question.sample_answer}</p>
            )}
            <div className="mt-2 flex flex-wrap items-center gap-1.5">
              {question.tags.map((tag) => (
                <Badge key={tag} variant="default" className="gap-1">
                  <Tag className="h-2.5 w-2.5" /> {tag}
                </Badge>
              ))}
              <button className="text-xs text-text-faint hover:text-accent transition-colors duration-150">
                + thêm tag
              </button>
            </div>
          </div>
        </div>
        <button
          onClick={() => setEditing((e) => !e)}
          className="text-text-faint hover:text-accent transition-colors duration-150 shrink-0"
        >
          <Pencil className="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  )
}
