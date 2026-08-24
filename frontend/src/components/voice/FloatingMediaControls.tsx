import React from 'react'
import {
  Camera,
  CameraOff,
  MessageSquare,
  Mic,
  MicOff,
  Subtitles,
} from 'lucide-react'

interface FloatingMediaControlsProps {
  microphoneActive: boolean
  cameraActive: boolean
  captionsActive: boolean
  chatActive: boolean
  disabled?: boolean
  onToggleMicrophone: () => void
  onToggleCamera: () => void
  onToggleCaptions: () => void
  onToggleChat: () => void
}

export function FloatingMediaControls({
  microphoneActive,
  cameraActive,
  captionsActive,
  chatActive,
  disabled = false,
  onToggleMicrophone,
  onToggleCamera,
  onToggleCaptions,
  onToggleChat,
}: FloatingMediaControlsProps) {
  return (
    <div
      className="inline-flex items-center gap-2 rounded-2xl border border-white/10 bg-[#16181e]/90 p-2 shadow-2xl backdrop-blur-md"
      role="toolbar"
      aria-label="Media controls"
    >
      {/* Microphone toggle */}
      <button
        type="button"
        disabled={disabled}
        onClick={onToggleMicrophone}
        aria-label={microphoneActive ? 'Mute microphone' : 'Unmute microphone'}
        className={`flex h-11 w-11 items-center justify-center rounded-xl transition-all duration-200 ${
          microphoneActive
            ? 'bg-accent text-slate-950 shadow-md shadow-accent/20 hover:bg-accent-hover'
            : 'border border-red-500/30 bg-red-500/10 text-red-400 hover:bg-red-500/20'
        } disabled:cursor-not-allowed disabled:opacity-50`}
      >
        {microphoneActive ? <Mic className="h-5 w-5" /> : <MicOff className="h-5 w-5" />}
      </button>

      {/* Camera toggle */}
      <button
        type="button"
        disabled={disabled}
        onClick={onToggleCamera}
        aria-label={cameraActive ? 'Turn off camera' : 'Turn on camera'}
        className={`flex h-11 w-11 items-center justify-center rounded-xl transition-all duration-200 ${
          cameraActive
            ? 'bg-white/15 text-white hover:bg-white/25'
            : 'border border-red-500/30 bg-red-500/10 text-red-400 hover:bg-red-500/20'
        } disabled:cursor-not-allowed disabled:opacity-50`}
      >
        {cameraActive ? <Camera className="h-5 w-5" /> : <CameraOff className="h-5 w-5" />}
      </button>

      <div className="mx-1 h-6 w-px bg-white/10" aria-hidden="true" />

      {/* Subtitles toggle */}
      <button
        type="button"
        onClick={onToggleCaptions}
        aria-label={captionsActive ? 'Hide captions' : 'Show captions'}
        className={`flex h-11 w-11 items-center justify-center rounded-xl transition-all duration-200 ${
          captionsActive
            ? 'bg-white/20 text-white shadow-sm'
            : 'text-white/60 hover:bg-white/10 hover:text-white'
        }`}
      >
        <Subtitles className="h-5 w-5" />
      </button>

      {/* Chat toggle */}
      <button
        type="button"
        onClick={onToggleChat}
        aria-label={chatActive ? 'Close chat' : 'Open chat'}
        className={`flex h-11 w-11 items-center justify-center rounded-xl transition-all duration-200 ${
          chatActive
            ? 'bg-accent/20 text-accent shadow-sm'
            : 'text-white/60 hover:bg-white/10 hover:text-white'
        }`}
      >
        <MessageSquare className="h-5 w-5" />
      </button>
    </div>
  )
}
