import {
  Captions,
  CaptionsOff,
  MessageSquare,
  Mic,
  MicOff,
  Video,
  VideoOff,
} from "lucide-react";
import styles from "./InterviewPage.module.css";

interface MediaControlsProps {
  microphoneActive: boolean;
  cameraActive: boolean;
  chatOpen: boolean;
  transcriptVisible: boolean;
  onToggleChat: () => void;
  onToggleMicrophone: () => void;
  onToggleCamera: () => void;
  onToggleTranscript: () => void;
}

export function MediaControls({
  microphoneActive,
  cameraActive,
  chatOpen,
  transcriptVisible,
  onToggleChat,
  onToggleMicrophone,
  onToggleCamera,
  onToggleTranscript,
}: MediaControlsProps) {
  const microphoneLabel = microphoneActive
    ? "Mute microphone"
    : "Unmute microphone";
  const cameraLabel = cameraActive ? "Hide self view" : "Show self view";
  const transcriptLabel = transcriptVisible
    ? "Hide transcript"
    : "Show transcript";

  return (
    <div className={styles.mediaTray} aria-label="Interview controls">
      <button
        className={`${styles.mediaButton} ${microphoneActive ? "" : styles.mediaButtonDisabled}`}
        type="button"
        onClick={onToggleMicrophone}
        aria-label={microphoneLabel}
        title={microphoneLabel}
        aria-pressed={!microphoneActive}
      >
        {microphoneActive ? <Mic aria-hidden="true" /> : <MicOff aria-hidden="true" />}
      </button>
      <button
        className={`${styles.mediaButton} ${cameraActive ? "" : styles.mediaButtonDisabled}`}
        type="button"
        onClick={onToggleCamera}
        aria-label={cameraLabel}
        title={cameraLabel}
        aria-pressed={!cameraActive}
      >
        {cameraActive ? <Video aria-hidden="true" /> : <VideoOff aria-hidden="true" />}
      </button>
      <button
        className={`${styles.mediaButton} ${styles.transcriptButton} ${transcriptVisible ? "" : styles.mediaButtonDisabled}`}
        type="button"
        onClick={onToggleTranscript}
        aria-label={transcriptLabel}
        title={transcriptLabel}
        aria-pressed={!transcriptVisible}
      >
        {transcriptVisible ? (
          <Captions aria-hidden="true" />
        ) : (
          <CaptionsOff aria-hidden="true" />
        )}
      </button>
      <button
        className={`${styles.mediaButton} ${styles.chatButton} ${chatOpen ? styles.mediaButtonActive : ""}`}
        type="button"
        onClick={onToggleChat}
        aria-label={chatOpen ? "Close text answer" : "Answer with text"}
        title={chatOpen ? "Close text answer" : "Answer with text"}
        aria-pressed={chatOpen}
      >
        <MessageSquare aria-hidden="true" />
      </button>
    </div>
  );
}
