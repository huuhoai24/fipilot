import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { UploadCloud, FileText, X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface CvDropzoneProps {
  onFileAccepted: (file: File) => void
}

export function CvDropzone({ onFileAccepted }: CvDropzoneProps) {
  const [file, setFile] = useState<File | null>(null)

  const onDrop = useCallback(
    (accepted: File[]) => {
      if (accepted.length > 0) {
        setFile(accepted[0])
        onFileAccepted(accepted[0])
      }
    },
    [onFileAccepted]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
  })

  if (file) {
    return (
      <div className="flex items-center justify-between rounded-lg border border-border bg-surface-raised px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent-soft">
            <FileText className="h-4 w-4 text-accent" />
          </div>
          <div>
            <div className="text-sm font-medium text-text-primary">{file.name}</div>
            <div className="text-xs text-text-muted">{(file.size / 1024).toFixed(0)} KB</div>
          </div>
        </div>
        <button
          onClick={() => setFile(null)}
          className="text-text-faint hover:text-danger transition-colors duration-150"
          aria-label="Xóa file"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    )
  }

  return (
    <div
      {...getRootProps()}
      className={cn(
        'flex cursor-pointer flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed border-border bg-surface-raised px-6 py-12 text-center transition-colors duration-150',
        isDragActive && 'border-accent bg-accent-soft'
      )}
    >
      <input {...getInputProps()} />
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent-soft">
        <UploadCloud className="h-6 w-6 text-accent" />
      </div>
      <div>
        <p className="text-sm font-medium text-text-primary">Kéo thả CV vào đây (PDF / DOCX)</p>
        <p className="mt-0.5 text-xs text-text-muted">hoặc bấm để chọn file từ máy</p>
      </div>
    </div>
  )
}
