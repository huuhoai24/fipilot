import {
  Camera,
  CameraOff,
  Captions,
  CaptionsOff,
  MessageSquare,
  Mic,
  MicOff,
} from 'lucide-react'
import styles from './FloatingMediaControls.module.css'

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
    <div className={styles.mediaTray} role="toolbar" aria-label="Điều khiển phỏng vấn">
      {/* Microphone toggle - v1: active = base, inactive = mediaButtonDisabled (red) */}
      <button
        type="button"
        disabled={disabled}
        onClick={onToggleMicrophone}
        aria-label={microphoneActive ? 'Tắt microphone' : 'Bật microphone'}
        aria-pressed={!microphoneActive}
        className={`${styles.mediaButton} ${!microphoneActive ? styles.mediaButtonDisabled : ''}`}
      >
        {microphoneActive ? <Mic aria-hidden="true" /> : <MicOff aria-hidden="true" />}
      </button>

      {/* Camera toggle - v1: same as microphone */}
      <button
        type="button"
        disabled={disabled}
        onClick={onToggleCamera}
        aria-label={cameraActive ? 'Tắt camera' : 'Bật camera'}
        aria-pressed={!cameraActive}
        className={`${styles.mediaButton} ${!cameraActive ? styles.mediaButtonDisabled : ''}`}
      >
        {cameraActive ? <Camera aria-hidden="true" /> : <CameraOff aria-hidden="true" />}
      </button>

      <div className={styles.separator} aria-hidden="true" />

      {/* Captions toggle - v1: transcriptButton + Disabled when off, base when on */}
      <button
        type="button"
        disabled={disabled}
        onClick={onToggleCaptions}
        aria-label={captionsActive ? 'Ẩn phụ đề' : 'Hiện phụ đề'}
        aria-pressed={!captionsActive}
        className={`${styles.mediaButton} ${styles.transcriptButton} ${!captionsActive ? styles.mediaButtonDisabled : ''}`}
      >
        {captionsActive ? <Captions aria-hidden="true" /> : <CaptionsOff aria-hidden="true" />}
      </button>

      {/* Chat toggle - v1: chatButton + Active when on (blue #5154d9) */}
      <button
        type="button"
        disabled={disabled}
        onClick={onToggleChat}
        aria-label={chatActive ? 'Đóng trả lời văn bản' : 'Trả lời bằng văn bản'}
        aria-pressed={chatActive}
        className={`${styles.mediaButton} ${styles.chatButton} ${chatActive ? styles.mediaButtonActive : ''}`}
      >
        <MessageSquare aria-hidden="true" />
      </button>
    </div>
  )
}
