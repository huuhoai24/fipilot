"use client";

import { useState } from "react";
import { Clock3, Mic, MicOff, UserRound, Video, VideoOff } from "lucide-react";
import styles from "./landing.module.css";

export function PreviewHero() {
  const [microphoneEnabled, setMicrophoneEnabled] = useState(true);
  const [videoEnabled, setVideoEnabled] = useState(true);

  return (
    <aside className={styles.previewHero} aria-label="AI interview preview">
      <div className={styles.previewFrame}>
        <div className={styles.previewToolbar}>
          <span><Clock3 size={10} />30:00</span>
          <i aria-hidden="true" />
        </div>
        <div className={styles.previewStage}>
          <div className={styles.previewCandidate}>
            <span className={styles.previewUser}><UserRound size={20} /></span>
            <div className={styles.previewControls}>
              <button
                className={microphoneEnabled ? styles.previewControl : styles.previewControlOff}
                onClick={() => setMicrophoneEnabled((enabled) => !enabled)}
                aria-label={microphoneEnabled ? "Mute microphone" : "Unmute microphone"}
                type="button"
              >
                {microphoneEnabled ? <Mic size={16} /> : <MicOff size={16} />}
              </button>
              <button
                className={videoEnabled ? styles.previewControl : styles.previewControlOff}
                onClick={() => setVideoEnabled((enabled) => !enabled)}
                aria-label={videoEnabled ? "Disable video" : "Enable video"}
                type="button"
              >
                {videoEnabled ? <Video size={16} /> : <VideoOff size={16} />}
              </button>
            </div>
          </div>
          <div className={styles.previewAi}>
            <div className={styles.listeningPulse}>
              <span><Mic size={15} /></span>
            </div>
            <p>LISTENING...</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
