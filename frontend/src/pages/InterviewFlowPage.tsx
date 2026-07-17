import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Loader2,
  Sparkles,
  ArrowLeft,
  ArrowRight,
  Pencil,
  CheckCircle2,
  Mic,
  Clock,
  Clock4,
  ListChecks,
  Zap,
  Plus,
  AlertTriangle,
  BrainCircuit,
  Workflow,
} from 'lucide-react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Select, Label, Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { StepIndicator } from '@/components/StepIndicator'
import { CvDropzone } from '@/components/CvDropzone'
import { useAuthStore } from '@/store/useAuthStore'
import { useScheduleStore } from '@/store/useScheduleStore'
import { useActiveSessionStore } from '@/store/useActiveSessionStore'
import type { CandidateProfile, TemplateMatch } from '@/types'
import { api } from '@/lib/api'

export function InterviewFlowPage() {
  const navigate = useNavigate()
  const { currentUser } = useAuthStore()
  const { addPending } = useScheduleStore()
  const startSession = useActiveSessionStore((s) => s.startSession)
  const [step, setStep] = useState(1)
  const [extracting, setExtracting] = useState(false)
  const [profile, setProfile] = useState<CandidateProfile | null>(null)
  const [editingProfile, setEditingProfile] = useState(false)
  const [selectedTemplateId, setSelectedTemplateId] = useState<string | null>(null)
  const [cvFile, setCvFile] = useState<File | null>(null)
  const [templateMatches, setTemplateMatches] = useState<TemplateMatch[]>([])
  const [extractError, setExtractError] = useState<string | null>(null)
  const [matchingTemplates, setMatchingTemplates] = useState(false)
  const [parserMode, setParserMode] = useState<'workflow' | 'llm'>('workflow')
  const [confirmStartOpen, setConfirmStartOpen] = useState(false)

  // Step 4: chọn giữa bắt đầu ngay hoặc để vào hàng đợi phỏng vấn sau
  const [startMode, setStartMode] = useState<'immediate' | 'later' | null>(null)
  const [queued, setQueued] = useState(false)
  const [starting, setStarting] = useState(false)

  const handleExtract = async () => {
    if (!cvFile) return
    setExtracting(true)
    setExtractError(null)
    try {
      const res = await api.extractCv(cvFile, parserMode)
      setProfile(res.profile)
      setTemplateMatches(res.matches)
      setSelectedTemplateId(res.matches?.[0]?.score >= 0.5 ? res.matches[0].template_id : null)
      setStep(2)
    } catch (e) {
      console.error(e)
      const message = e instanceof Error ? e.message : 'Không thể trích xuất CV.'
      setExtractError(message)
      alert(message)
    } finally {
      setExtracting(false)
    }
  }

  const handleStartNow = async () => {
    if (!profile || !selectedTemplateId) return
    setConfirmStartOpen(false)
    setStarting(true)
    try {
      const res = await api.createSession({
        name: profile.candidate_name,
        role: profile.role_fit,
        level: profile.inferred_level.toString(),
        language: 'vi',
        template_id: selectedTemplateId,
        skills: profile.skills,
        recent_role: profile.recent_role,
        years_experience: profile.years_experience,
        education: profile.education,
      })
      startSession({ sessionId: res.session_id.toString(), candidateName: profile.candidate_name })
      navigate(`/interview-flow/session/${res.session_id}`)
    } catch (error) {
      console.error('Failed to start session:', error)
      alert(error instanceof Error ? error.message : 'Không thể tạo phiên phỏng vấn.')
    } finally {
      setStarting(false)
    }
  }

  const handleMatchTemplates = async () => {
    if (!profile) return
    setMatchingTemplates(true)
    try {
      const res = await api.matchTemplates({
        role_fit: profile.role_fit,
        inferred_level: profile.inferred_level,
        skills: profile.skills,
        target_role: profile.role_fit,
      })
      const matches = res.matches ?? []
      setTemplateMatches(matches)
      setSelectedTemplateId(matches?.[0]?.score >= 0.5 ? matches[0].template_id : null)
      setStep(3)
    } catch (error) {
      console.error('Failed to match templates:', error)
      alert(error instanceof Error ? error.message : 'KhÃ´ng thá»ƒ khá»›p template.')
    } finally {
      setMatchingTemplates(false)
    }
  }

  const handleQueueForLater = async () => {
    if (!profile || !selectedTemplateId) return
    setStarting(true)
    try {
      const res = await api.createSession({
        name: profile.candidate_name,
        role: profile.role_fit,
        level: profile.inferred_level.toString(),
        language: 'vi',
        template_id: selectedTemplateId,
        skills: profile.skills,
        recent_role: profile.recent_role,
        years_experience: profile.years_experience,
        education: profile.education,
      })
      addPending({
        sessionId: res.session_id.toString(),
        candidate: profile.candidate_name,
        role: `${profile.role_fit} L${profile.inferred_level}`,
        interviewer_email: currentUser?.email ?? '',
        created_at: new Date().toISOString(),
      })
      setQueued(true)
    } catch (error) {
      console.error('Failed to queue session:', error)
      alert(error instanceof Error ? error.message : 'Không thể tạo phiên phỏng vấn.')
    } finally {
      setStarting(false)
    }
  }

  const handleCreateAnother = () => {
    setStep(1)
    setCvFile(null)
    setProfile(null)
    setEditingProfile(false)
    setSelectedTemplateId(null)
    setTemplateMatches([])
    setExtractError(null)
    setMatchingTemplates(false)
    setStartMode(null)
    setQueued(false)
    setConfirmStartOpen(false)
  }

  const runningSessions = useActiveSessionStore((s) => Object.values(s.sessions))

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-2xl font-bold tracking-tight-display text-text-primary">
          Tạo buổi phỏng vấn mới
        </h1>
        <p className="mt-1 text-sm text-text-muted">
          Tải CV, để AI trích xuất hồ sơ và gợi ý bộ câu hỏi phù hợp nhất.
        </p>
      </div>

      {runningSessions.length > 0 && (
        <div className="mx-auto max-w-2xl rounded-lg border border-accent/30 bg-accent-soft px-4 py-3 text-sm">
          <p className="mb-2 text-accent">
            Bạn đang có {runningSessions.length} buổi phỏng vấn diễn ra. Bạn vẫn có thể tạo thêm buổi mới.
          </p>
          <div className="flex flex-wrap gap-2">
            {runningSessions.map((s) => (
              <Button
                key={s.sessionId}
                size="sm"
                variant="secondary"
                onClick={() => navigate(`/interview-flow/session/${s.sessionId}`)}
              >
                Quay lại: {s.candidateName}
              </Button>
            ))}
          </div>
        </div>
      )}

      <div className="flex justify-center">
        <StepIndicator currentStep={step} />
      </div>

      <Card className="mx-auto max-w-2xl">
        <CardContent className="space-y-5">
          {/* STEP 1 */}
          {step === 1 && (
            <div className="space-y-5 animate-fade-in">
              <div>
                <Label>CV ứng viên</Label>
                <CvDropzone onFileAccepted={setCvFile} />
                {extractError && <p className="mt-2 text-sm text-danger">{extractError}</p>}
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>JD (tùy chọn)</Label>
                  <Select defaultValue="">
                    <option value="">Chọn từ thư viện…</option>
                    <option value="jd_ai_l3">AI Engineer L3 — JD chuẩn</option>
                    <option value="jd_ai_l2">AI Engineer L2 — JD chuẩn</option>
                  </Select>
                </div>
                <div>
                  <Label>Ngôn ngữ</Label>
                  <Select defaultValue="vi">
                    <option value="vi">Tiếng Việt</option>
                  </Select>
                </div>
              </div>
              <div>
                <Label>Chế độ track CV</Label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setParserMode('workflow')}
                    className={`rounded-lg border p-3 text-left transition-colors duration-150 ${
                      parserMode === 'workflow'
                        ? 'border-accent bg-accent-soft'
                        : 'border-border bg-surface-raised hover:border-accent/40'
                    }`}
                  >
                    <div className="mb-1 flex items-center gap-2 text-sm font-medium text-text-primary">
                      <Workflow className="h-4 w-4 text-accent" />
                      Workflow nhanh
                    </div>
                    <p className="text-xs text-text-muted">Tối ưu tốc độ, ổn định cho CV có text rõ.</p>
                  </button>
                  <button
                    type="button"
                    onClick={() => setParserMode('llm')}
                    className={`rounded-lg border p-3 text-left transition-colors duration-150 ${
                      parserMode === 'llm'
                        ? 'border-accent bg-accent-soft'
                        : 'border-border bg-surface-raised hover:border-accent/40'
                    }`}
                  >
                    <div className="mb-1 flex items-center gap-2 text-sm font-medium text-text-primary">
                      <BrainCircuit className="h-4 w-4 text-accent" />
                      LLM Gemma
                    </div>
                    <p className="text-xs text-text-muted">Dùng gemma4:e2b để phân tích CV linh hoạt hơn.</p>
                  </button>
                </div>
              </div>
              <div className="flex justify-end pt-2">
                <Button onClick={handleExtract} disabled={!cvFile || extracting}>
                  {extracting ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" /> Đang trích xuất…
                    </>
                  ) : (
                    <>
                      Trích xuất <ArrowRight className="h-4 w-4" />
                    </>
                  )}
                </Button>
              </div>
            </div>
          )}

          {/* STEP 2 */}
          {step === 2 && profile && (
            <div className="space-y-5 animate-fade-in">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-accent" />
                  <span className="text-sm font-medium text-text-primary">Hồ sơ đã trích xuất</span>
                </div>
                <Badge variant="success">Độ tin cậy {(profile.confidence * 100).toFixed(0)}%</Badge>
              </div>

              {profile.parser_warning && (
                <div className="rounded-lg border border-warning/30 bg-warning/10 p-3 text-sm text-warning">
                  {profile.parser_warning}
                </div>
              )}

              <div className="rounded-lg border border-border bg-surface-raised p-4 space-y-4">
                <div className="flex items-center justify-between">
                  <ProfileField
                    label="Họ tên"
                    value={profile.candidate_name}
                    editing={editingProfile}
                    onChange={(v) => setProfile({ ...profile, candidate_name: v })}
                  />
                  <button onClick={() => setEditingProfile((e) => !e)} className="text-text-faint hover:text-accent transition-colors duration-150">
                    <Pencil className="h-4 w-4" />
                  </button>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <ProfileField
                    label="Kinh nghiệm"
                    value={`${profile.years_experience} năm`}
                    editing={false}
                  />
                  <ProfileField
                    label="Level suy luận"
                    value={`${profile.inferred_level}`}
                    editing={editingProfile}
                    onChange={(v) => setProfile({ ...profile, inferred_level: Number(v) || profile.inferred_level })}
                  />
                  <ProfileField
                    label="Vai trò phù hợp"
                    value={profile.role_fit}
                    editing={editingProfile}
                    onChange={(v) => setProfile({ ...profile, role_fit: v as any })}
                  />
                  <ProfileField label="Học vấn" value={profile.education} editing={false} />
                </div>
                <div>
                  <Label>Kỹ năng</Label>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {profile.skills.map((s) => (
                      <Badge key={s} variant="accent">{s}</Badge>
                    ))}
                  </div>
                </div>
                <ProfileField label="Vai trò gần nhất" value={profile.recent_role} editing={false} />
              </div>

              <div className="flex justify-between pt-2">
                <Button variant="ghost" onClick={() => setStep(1)}>
                  <ArrowLeft className="h-4 w-4" /> Quay lại
                </Button>
                <Button onClick={handleMatchTemplates} disabled={matchingTemplates}>
                  Khớp template <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* STEP 3 */}
          {step === 3 && (
            <div className="space-y-4 animate-fade-in">
              <div className="text-sm font-medium text-text-primary">5 template phù hợp nhất</div>
              {templateMatches.length === 0 && (
                <div className="rounded-lg border border-warning/30 bg-warning/10 p-4 text-sm text-warning">
                  Không tìm thấy template phù hợp. Vui lòng import template hoặc kiểm tra lại role/level.
                </div>
              )}
              {templateMatches[0] && templateMatches[0].score < 0.5 && (
                <div className="rounded-lg border border-warning/30 bg-warning/10 p-4 text-sm text-warning">
                  Không có template match mạnh. Hãy chọn thủ công template gần nhất trước khi bắt đầu.
                </div>
              )}
              <div className="space-y-2">
                {templateMatches.map((m) => (
                  <button
                    key={m.template_id}
                    onClick={() => setSelectedTemplateId(m.template_id)}
                    className={`w-full rounded-lg border p-4 text-left transition-colors duration-150 ${
                      selectedTemplateId === m.template_id
                        ? 'border-accent bg-accent-soft'
                        : 'border-border bg-surface-raised hover:border-accent/40'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span
                          className={`h-3 w-3 rounded-full border-2 ${
                            selectedTemplateId === m.template_id ? 'border-accent bg-accent' : 'border-text-faint'
                          }`}
                        />
                        <span className="text-sm font-medium text-text-primary">{m.title}</span>
                      </div>
                      <Badge variant={m.score >= 0.9 ? 'success' : m.score >= 0.8 ? 'accent' : 'default'}>
                        Match: {(m.score * 100).toFixed(0)}%
                      </Badge>
                    </div>
                    <div className="mt-2 flex items-center gap-4 text-xs text-text-muted">
                      <span className="flex items-center gap-1"><ListChecks className="h-3.5 w-3.5" /> {m.question_count} câu</span>
                      <span>
                        Dễ×{m.difficulty_mix.easy} / TB×{m.difficulty_mix.medium} / Khó×{m.difficulty_mix.hard}
                      </span>
                      <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" /> {m.duration_minutes} phút</span>
                    </div>
                  </button>
                ))}
              </div>
              <div className="flex justify-between pt-2">
                <Button variant="ghost" onClick={() => setStep(2)}>
                  <ArrowLeft className="h-4 w-4" /> Quay lại
                </Button>
                <Button onClick={() => setStep(4)} disabled={!selectedTemplateId}>
                  Bắt đầu phỏng vấn <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* STEP 4 */}
          {step === 4 && selectedTemplateId && (
            <div className="space-y-5 animate-fade-in">
              {/* Trạng thái: đã đưa vào hàng đợi "đang chờ" thành công */}
              {queued ? (
                <div className="space-y-5 text-center">
                  <div className="flex justify-center">
                    <div className="flex h-14 w-14 items-center justify-center rounded-full bg-success/10">
                      <CheckCircle2 className="h-7 w-7 text-success" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-base font-semibold text-text-primary">Đã thêm vào danh sách chờ</h3>
                    <p className="mt-1 text-sm text-text-muted">
                      Buổi phỏng vấn với{' '}
                      <span className="text-text-primary font-medium">{profile?.candidate_name}</span> đã được
                      thêm vào "Buổi phỏng vấn đang chờ" trên Dashboard. Bạn có thể bắt đầu bất cứ lúc nào.
                    </p>
                  </div>
                  <div className="flex justify-center gap-2">
                    <Button variant="secondary" onClick={() => navigate('/')}>
                      Về Dashboard
                    </Button>
                    <Button onClick={handleCreateAnother}>
                      <Plus className="h-4 w-4" /> Tạo buổi phỏng vấn mới
                    </Button>
                  </div>
                </div>
              ) : (
                <>
                  <div className="text-center">
                    <div className="flex justify-center mb-3">
                      <div className="flex h-14 w-14 items-center justify-center rounded-full bg-success/10">
                        <CheckCircle2 className="h-7 w-7 text-success" />
                      </div>
                    </div>
                    <h3 className="text-base font-semibold text-text-primary">Sẵn sàng bắt đầu</h3>
                    <p className="mt-1 text-sm text-text-muted">
                      Template:{' '}
                      <span className="text-text-primary font-medium">
                        {templateMatches.find((m) => m.template_id === selectedTemplateId)?.title}
                      </span>
                    </p>
                  </div>

                  {/* Chọn chế độ: bắt đầu ngay hoặc để phỏng vấn sau */}
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      onClick={() => setStartMode('immediate')}
                      className={`rounded-lg border p-4 text-left transition-colors duration-150 ${
                        startMode === 'immediate'
                          ? 'border-accent bg-accent-soft'
                          : 'border-border bg-surface-raised hover:border-accent/40'
                      }`}
                    >
                      <div className="flex items-center gap-2 mb-1.5">
                        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-accent/15">
                          <Zap className="h-3.5 w-3.5 text-accent" />
                        </div>
                        <span className="text-sm font-medium text-text-primary">Bắt đầu ngay</span>
                      </div>
                      <p className="text-xs text-text-muted">Vào phòng phỏng vấn ngay bây giờ.</p>
                    </button>

                    <button
                      onClick={() => setStartMode('later')}
                      className={`rounded-lg border p-4 text-left transition-colors duration-150 ${
                        startMode === 'later'
                          ? 'border-accent bg-accent-soft'
                          : 'border-border bg-surface-raised hover:border-accent/40'
                      }`}
                    >
                      <div className="flex items-center gap-2 mb-1.5">
                        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-accent/15">
                          <Clock4 className="h-3.5 w-3.5 text-accent" />
                        </div>
                        <span className="text-sm font-medium text-text-primary">Phỏng vấn sau</span>
                      </div>
                      <p className="text-xs text-text-muted">Thêm vào danh sách chờ, bắt đầu khi sẵn sàng.</p>
                    </button>
                  </div>

                  <div className="flex justify-between pt-2">
                    <Button variant="ghost" onClick={() => setStep(3)}>
                      <ArrowLeft className="h-4 w-4" /> Quay lại
                    </Button>
                    {startMode === 'later' ? (
                      <Button onClick={handleQueueForLater} disabled={!selectedTemplateId || starting}>
                        <Clock4 className="h-4 w-4" /> Thêm vào danh sách chờ
                      </Button>
                    ) : (
                      <Button onClick={() => setConfirmStartOpen(true)} disabled={startMode !== 'immediate' || starting}>
                        {starting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Mic className="h-4 w-4" />}
                        {starting ? ' Đang kết nối...' : ' Vào phòng phỏng vấn'}
                      </Button>
                    )}
                  </div>
                </>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {confirmStartOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="w-full max-w-md rounded-lg border border-warning/30 bg-surface p-5 shadow-2xl">
            <div className="mb-3 flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-warning/10">
                <AlertTriangle className="h-5 w-5 text-warning" />
              </div>
              <h3 className="text-base font-semibold text-text-primary">Chuẩn bị trước khi phỏng vấn</h3>
            </div>
            <div className="space-y-2 text-sm leading-relaxed text-text-muted">
              <p>Hãy chuẩn bị thật kỹ trước khi bắt đầu. Trong lúc phỏng vấn, bạn không được chuyển tab, đổi cửa sổ, rời khỏi trang hoặc làm việc khác ngoài trả lời phỏng vấn.</p>
              <p>Hệ thống sẽ hiển thị cảnh báo ngay khi phát hiện bạn chuyển tab/cửa sổ và số lần vi phạm sẽ xuất hiện trong báo cáo đánh giá.</p>
            </div>
            <div className="mt-5 flex justify-end gap-2">
              <Button variant="secondary" onClick={() => setConfirmStartOpen(false)} disabled={starting}>
                Suy nghĩ lại
              </Button>
              <Button onClick={handleStartNow} disabled={starting}>
                {starting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Mic className="h-4 w-4" />}
                Bắt đầu ngay
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function ProfileField({
  label,
  value,
  editing,
  onChange,
}: {
  label: string
  value: string
  editing: boolean
  onChange?: (v: string) => void
}) {
  return (
    <div className="flex-1">
      <Label>{label}</Label>
      {editing && onChange ? (
        <Input value={value} onChange={(e) => onChange(e.target.value)} />
      ) : (
        <div className="text-sm text-text-primary capitalize">{value}</div>
      )}
    </div>
  )
}
