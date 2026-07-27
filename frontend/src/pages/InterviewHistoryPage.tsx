import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, ArrowRight, FileText, History, Loader2, MessageSquareText, RefreshCw } from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Card, CardContent } from '@/components/ui/Card'
import { api } from '@/lib/api'
import type { InterviewHistoryResponse, InterviewSessionSummary, InterviewStatus } from '@/types'

const PAGE_SIZE = 10

const statusLabels: Record<InterviewStatus, string> = {
  created: 'Created',
  in_progress: 'In Progress',
  completed: 'Completed',
  report_generated: 'Report Ready',
}

function statusVariant(status: InterviewStatus) {
  if (status === 'report_generated') return 'success' as const
  if (status === 'completed') return 'accent' as const
  if (status === 'in_progress') return 'warning' as const
  return 'default' as const
}

function SessionAction({ session }: { session: InterviewSessionSummary }) {
  const navigate = useNavigate()
  if (session.status === 'in_progress') {
    return (
      <Button size="sm" onClick={() => navigate(`/text-interview/${session.session_id}`)}>
        <MessageSquareText className="h-4 w-4" />
        Continue Interview
      </Button>
    )
  }
  if (session.status === 'completed' || session.status === 'report_generated') {
    return (
      <Button size="sm" variant="secondary" onClick={() => navigate(`/text-interview/${session.session_id}/report`)}>
        <FileText className="h-4 w-4" />
        {session.status === 'completed' ? 'Generate Report' : 'View Report'}
      </Button>
    )
  }
  return null
}

export function InterviewHistoryPage() {
  const [data, setData] = useState<InterviewHistoryResponse | null>(null)
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = async () => {
    setLoading(true)
    setError('')
    try {
      setData(await api.listInterviewSessions({ limit: PAGE_SIZE, offset }))
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : 'Failed to load interview history')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void load()
  }, [offset])

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-bold text-text-primary">Interview History</h1>
          <p className="mt-1 text-sm text-text-muted">{data ? `${data.total} interview sessions` : 'Previous interview sessions'}</p>
        </div>
        <Button variant="secondary" size="icon" title="Refresh history" onClick={() => void load()} disabled={loading}>
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
        </Button>
      </div>

      {error && (
        <div className="rounded-lg border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">{error}</div>
      )}

      {loading && !data ? (
        <div className="flex min-h-64 items-center justify-center"><Loader2 className="h-7 w-7 animate-spin text-accent" /></div>
      ) : data?.items.length ? (
        <div className="space-y-3">
          {data.items.map((session) => {
            const progress = session.question_count
              ? Math.round((session.answered_question_count / session.question_count) * 100)
              : 0
            return (
              <Card key={session.session_id}>
                <CardContent className="grid gap-4 p-4 md:grid-cols-[minmax(150px,1.2fr)_100px_120px_minmax(160px,1fr)_90px_auto] md:items-center">
                  <div>
                    <div className="text-sm font-medium text-text-primary">
                      {new Date(session.started_at).toLocaleDateString(undefined, { dateStyle: 'medium' })}
                    </div>
                    <div className="mt-1 text-xs text-text-faint">Session {session.session_id}</div>
                  </div>
                  <div>
                    <div className="text-xs text-text-faint">Language</div>
                    <div className="mt-1 text-sm font-medium uppercase text-text-primary">{session.language}</div>
                  </div>
                  <div>
                    <div className="text-xs text-text-faint">Level</div>
                    <div className="mt-1 text-sm font-medium capitalize text-text-primary">{session.experience_level}</div>
                  </div>
                  <div>
                    <div className="mb-2 flex justify-between text-xs text-text-faint">
                      <span>Progress</span>
                      <span>{session.answered_question_count}/{session.question_count}</span>
                    </div>
                    <div className="h-1.5 overflow-hidden rounded-full bg-surface-raised">
                      <div className="h-full bg-accent" style={{ width: `${Math.min(progress, 100)}%` }} />
                    </div>
                  </div>
                  <div className="flex md:justify-center">
                    {session.overall_score == null ? (
                      <span className="text-sm text-text-faint">No score</span>
                    ) : (
                      <span className="text-sm font-semibold text-text-primary">{session.overall_score.toFixed(1)}/10</span>
                    )}
                  </div>
                  <div className="flex flex-wrap items-center gap-2 md:justify-end">
                    <Badge variant={statusVariant(session.status)}>{statusLabels[session.status]}</Badge>
                    <SessionAction session={session} />
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      ) : (
        <div className="flex min-h-64 flex-col items-center justify-center rounded-lg border border-border bg-surface text-center">
          <History className="h-7 w-7 text-text-faint" />
          <h2 className="mt-3 text-sm font-semibold text-text-primary">No interview sessions</h2>
          <p className="mt-1 text-sm text-text-muted">Completed and active interviews will appear here.</p>
        </div>
      )}

      {data && data.total > PAGE_SIZE && (
        <div className="flex items-center justify-between border-t border-border pt-4">
          <span className="text-xs text-text-faint">
            {offset + 1}-{Math.min(offset + PAGE_SIZE, data.total)} of {data.total}
          </span>
          <div className="flex gap-2">
            <Button variant="secondary" size="sm" disabled={offset === 0 || loading} onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}>
              <ArrowLeft className="h-4 w-4" /> Previous
            </Button>
            <Button variant="secondary" size="sm" disabled={offset + PAGE_SIZE >= data.total || loading} onClick={() => setOffset(offset + PAGE_SIZE)}>
              Next <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
