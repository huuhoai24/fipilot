import React from 'react'
import { FileText } from 'lucide-react'

interface TranscriptPreviewProps {
  transcript?: string
  editable?: boolean
  onChange?: (value: string) => void
}

export function TranscriptPreview({
  transcript = '',
  editable = false,
  onChange,
}: TranscriptPreviewProps) {
  return (
    <section aria-labelledby="transcript-preview-title">
      <div className="mb-3 flex items-center gap-2">
        <FileText className="h-4 w-4 text-accent" aria-hidden="true" />
        <h2 id="transcript-preview-title" className="text-sm font-semibold text-text-primary">
          Transcript Preview
        </h2>
      </div>
      <textarea
        value={transcript}
        onChange={(event) => onChange?.(event.target.value)}
        readOnly={!editable}
        rows={5}
        placeholder="Your speech transcript will appear here."
        className="min-h-28 w-full resize-y rounded-lg border border-border bg-surface-raised p-4 text-sm leading-6 text-text-primary placeholder:text-text-faint read-only:cursor-default read-only:text-text-muted"
        aria-live="polite"
        aria-atomic="true"
        aria-label="Interview answer transcript"
      />
    </section>
  )
}
