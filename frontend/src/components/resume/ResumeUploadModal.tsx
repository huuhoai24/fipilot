import React, { useRef, useState } from 'react'
import {
  AlertCircle,
  Briefcase,
  CheckCircle2,
  Eye,
  FileText,
  FileUp,
  FolderGit2,
  Loader2,
  Sparkles,
  Type,
  X,
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Textarea } from '@/components/ui/Input'
import { api } from '@/lib/api'
import { getUserFacingError } from '@/lib/userFacingError'
import type { CandidateProfile } from '@/types'

interface ResumeUploadModalProps {
  isOpen: boolean
  onClose: () => void
  onContinue: (profile: CandidateProfile, file: File | null) => void
}

export function ResumeUploadModal({
  isOpen,
  onClose,
  onContinue,
}: ResumeUploadModalProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [activeTab, setActiveTab] = useState<'upload' | 'manual'>('upload')
  const [file, setFile] = useState<File | null>(null)
  const [profile, setProfile] = useState<CandidateProfile | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)

  // Manual input fields
  const [manualText, setManualText] = useState('')

  if (!isOpen) return null

  const handleFileSelect = async (selectedFile: File | null) => {
    if (!selectedFile) return
    const isPdf = selectedFile.name.toLowerCase().endsWith('.pdf')
    const isDocx = selectedFile.name.toLowerCase().endsWith('.docx')
    if (!isPdf && !isDocx) {
      setError('Unsupported file format. Please upload a PDF or DOCX file.')
      return
    }
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size exceeds 10MB limit.')
      return
    }

    setError('')
    setFile(selectedFile)
    setPreviewUrl(URL.createObjectURL(selectedFile))
    setUploading(true)

    try {
      const uploadRes = await api.uploadResume(selectedFile)
      const profileRes = await api.getCandidateProfile(uploadRes.candidate_id)
      setProfile(profileRes.profile)
    } catch (err) {
      setError(getUserFacingError(err, 'Failed to analyze resume. Please try again.'))
      setFile(null)
      setProfile(null)
    } finally {
      setUploading(false)
    }
  }

  const handleManualSubmit = () => {
    if (!manualText.trim() || manualText.trim().length < 20) {
      setError('Please provide at least 20 characters of your CV or experience summary.')
      return
    }

    // Extract skills and lines from manual text
    const lines = manualText.split('\n').map((l) => l.trim()).filter(Boolean)
    const manualProfile: CandidateProfile = {
      name: 'Candidate',
      skills: lines.slice(0, 8),
      skill_evidence: [],
      projects: [
        {
          name: 'Provided Experience Summary',
          description: manualText.trim(),
          technologies: [],
        },
      ],
      experiences: [],
      confidence: 1,
      confidence_score: 1,
    }

    setProfile(manualProfile)
    setError('')
  }

  const handleRemove = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl)
      setPreviewUrl(null)
    }
    setFile(null)
    setProfile(null)
    setError('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handlePreview = () => {
    if (previewUrl) {
      window.open(previewUrl, '_blank', 'noopener,noreferrer')
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-150">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="upload-resume-title"
        className="relative w-full max-w-2xl max-h-[90vh] flex flex-col rounded-2xl border border-border bg-surface shadow-2xl overflow-hidden transition-colors"
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border px-6 py-4">
          <div>
            <h2 id="upload-resume-title" className="text-lg font-bold text-text-primary">
              Step 1: Upload / Input Resume
            </h2>
            <p className="text-xs text-text-muted mt-0.5">
              Add your CV so our AI interviewer can tailor questions to your real background.
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

        {/* Tab switch (Upload vs Manual Text) */}
        {!profile && (
          <div className="flex border-b border-border bg-surface-raised/50 px-6 pt-2">
            <button
              type="button"
              onClick={() => {
                setActiveTab('upload')
                setError('')
              }}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-all ${
                activeTab === 'upload'
                  ? 'border-accent text-accent'
                  : 'border-transparent text-text-muted hover:text-text-primary'
              }`}
            >
              <FileUp className="h-4 w-4" />
              Upload PDF / DOCX
            </button>
            <button
              type="button"
              onClick={() => {
                setActiveTab('manual')
                setError('')
              }}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition-all ${
                activeTab === 'manual'
                  ? 'border-accent text-accent'
                  : 'border-transparent text-text-muted hover:text-text-primary'
              }`}
            >
              <Type className="h-4 w-4" />
              Paste Text / CV Summary
            </button>
          </div>
        )}

        {/* Body Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5">
          {error && (
            <div role="alert" className="flex items-center gap-2.5 rounded-xl border border-danger/30 bg-danger/10 p-3.5 text-xs text-danger">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* If Analyzed Profile Exists */}
          {profile ? (
            <div className="space-y-4 animate-in fade-in duration-200">
              {/* Success Banner */}
              <div className="flex items-center gap-3 rounded-xl border border-success/30 bg-success/10 p-3.5 text-sm text-success">
                <CheckCircle2 className="h-5 w-5 shrink-0" />
                <div>
                  <strong className="font-semibold block text-text-primary">
                    Your resume has been analyzed!
                  </strong>
                  <span className="text-xs text-text-muted">
                    Review the extracted details below before selecting your interview focus.
                  </span>
                </div>
              </div>

              {/* File Meta Bar */}
              <div className="flex items-center justify-between rounded-xl border border-border bg-surface-raised p-3">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-surface border border-border text-accent shrink-0">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div className="min-w-0">
                    <span className="text-sm font-semibold text-text-primary truncate block">
                      {file?.name || `${profile.name || 'Candidate'}_Resume`}
                    </span>
                    <span className="text-xs text-text-muted">
                      Candidate: {profile.name || 'Extracted Profile'}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {previewUrl && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={handlePreview}
                      title="Preview Resume"
                      className="h-8 w-8 p-0"
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                  )}
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={handleRemove}
                    title="Remove and re-upload"
                    className="h-8 w-8 p-0 text-danger hover:bg-danger/10 hover:text-danger"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Metrics Summary */}
              <div className="grid grid-cols-3 gap-3">
                <div className="rounded-xl border border-border bg-surface-raised/60 p-3 text-center">
                  <span className="text-xs text-text-muted block">Work Experience</span>
                  <strong className="text-lg font-bold text-text-primary">
                    {profile.experiences?.length || 0}
                  </strong>
                </div>
                <div className="rounded-xl border border-border bg-surface-raised/60 p-3 text-center">
                  <span className="text-xs text-text-muted block">Projects</span>
                  <strong className="text-lg font-bold text-text-primary">
                    {profile.projects?.length || 0}
                  </strong>
                </div>
                <div className="rounded-xl border border-border bg-surface-raised/60 p-3 text-center">
                  <span className="text-xs text-text-muted block">Skills Found</span>
                  <strong className="text-lg font-bold text-text-primary">
                    {profile.skills?.length || 0}
                  </strong>
                </div>
              </div>

              {/* Skills Tags */}
              {profile.skills && profile.skills.length > 0 && (
                <div className="rounded-xl border border-border bg-surface-raised/40 p-3.5 space-y-2">
                  <div className="flex items-center gap-1.5 text-xs font-semibold text-text-primary">
                    <Sparkles className="h-3.5 w-3.5 text-accent" />
                    <span>Extracted Technical Skills</span>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {profile.skills.slice(0, 15).map((skill, idx) => (
                      <span
                        key={idx}
                        className="inline-flex items-center rounded-md border border-border bg-surface px-2 py-0.5 text-xs font-medium text-text-primary"
                      >
                        {skill}
                      </span>
                    ))}
                    {profile.skills.length > 15 && (
                      <span className="text-xs text-text-muted self-center">
                        +{profile.skills.length - 15} more
                      </span>
                    )}
                  </div>
                </div>
              )}

              {/* Experience and Project Preview Cards */}
              <div className="space-y-3">
                <span className="text-xs font-semibold text-text-muted uppercase tracking-wider block">
                  Extracted Experiences & Projects
                </span>

                {profile.experiences && profile.experiences.map((exp, idx) => (
                  <div
                    key={`exp-${idx}`}
                    className="rounded-xl border border-border bg-surface-raised/50 p-3.5 space-y-1.5"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Briefcase className="h-4 w-4 text-accent shrink-0" />
                        <span className="text-xs font-bold text-text-primary">
                          {exp.title}
                        </span>
                        <span className="text-xs text-text-muted">· {exp.company}</span>
                      </div>
                      <span className="text-[11px] rounded bg-accent/10 px-1.5 py-0.5 text-accent font-medium">
                        Work
                      </span>
                    </div>
                    {exp.description && (
                      <p className="text-xs text-text-muted line-clamp-2 leading-relaxed">
                        {exp.description}
                      </p>
                    )}
                  </div>
                ))}

                {profile.projects && profile.projects.map((proj, idx) => (
                  <div
                    key={`proj-${idx}`}
                    className="rounded-xl border border-border bg-surface-raised/50 p-3.5 space-y-1.5"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <FolderGit2 className="h-4 w-4 text-emerald-500 shrink-0" />
                        <span className="text-xs font-bold text-text-primary">
                          {proj.name}
                        </span>
                        {proj.role && (
                          <span className="text-xs text-text-muted">· {proj.role}</span>
                        )}
                      </div>
                      <span className="text-[11px] rounded bg-emerald-500/10 px-1.5 py-0.5 text-emerald-600 dark:text-emerald-400 font-medium">
                        Project
                      </span>
                    </div>
                    {proj.description && (
                      <p className="text-xs text-text-muted line-clamp-2 leading-relaxed">
                        {proj.description}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ) : activeTab === 'manual' ? (
            /* Manual Text Input Tab */
            <div className="space-y-4">
              <div>
                <label htmlFor="manual-cv-input" className="block text-xs font-bold text-text-primary mb-1.5">
                  Paste your CV content or skills summary
                </label>
                <Textarea
                  id="manual-cv-input"
                  rows={8}
                  placeholder="Paste your CV text, skills (e.g. Python, PyTorch, React), and recent projects here..."
                  value={manualText}
                  onChange={(e) => setManualText(e.target.value)}
                  className="font-mono text-xs leading-relaxed"
                />
              </div>
              <Button
                type="button"
                onClick={handleManualSubmit}
                disabled={!manualText.trim()}
                className="w-full sm:w-auto bg-accent text-white"
              >
                Use this CV content
              </Button>
            </div>
          ) : (
            /* Upload Dropzone Tab */
            <div
              onClick={() => !uploading && fileInputRef.current?.click()}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault()
                if (!uploading && e.dataTransfer.files[0]) {
                  void handleFileSelect(e.dataTransfer.files[0])
                }
              }}
              className={`flex flex-col items-center justify-center p-10 border-2 border-dashed rounded-2xl cursor-pointer transition-all ${
                uploading
                  ? 'border-accent bg-accent/5 cursor-wait'
                  : 'border-border hover:border-accent hover:bg-surface-raised'
              }`}
            >
              {uploading ? (
                <div className="flex flex-col items-center gap-3 text-center">
                  <Loader2 className="h-10 w-10 text-accent animate-spin" />
                  <strong className="text-sm font-semibold text-text-primary">
                    Analyzing your resume with AI...
                  </strong>
                  <span className="text-xs text-text-muted">
                    Extracting skills, projects, and work history. This takes ~10-20 seconds.
                  </span>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-2.5 text-center">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-surface-raised border border-border text-accent mb-1 shadow-sm">
                    <FileUp className="h-7 w-7" />
                  </div>
                  <strong className="text-base font-bold text-text-primary">
                    Drag and drop your resume here
                  </strong>
                  <span className="text-xs text-text-muted">
                    Supported formats: PDF, DOCX (Max size: 10 MB)
                  </span>
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="mt-2"
                    onClick={(e) => {
                      e.stopPropagation()
                      fileInputRef.current?.click()
                    }}
                  >
                    Browse files
                  </Button>
                </div>
              )}
            </div>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            className="hidden"
            onChange={(e) => void handleFileSelect(e.target.files?.[0] || null)}
          />
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-border px-6 py-4 bg-surface-raised/50">
          <Button type="button" variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="button"
            disabled={!profile || uploading}
            onClick={() => profile && onContinue(profile, file)}
            className="bg-[#13813a] hover:bg-[#0e612c] text-white font-bold px-6"
          >
            Continue to Step 2
          </Button>
        </div>
      </div>
    </div>
  )
}
