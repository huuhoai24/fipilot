"use client";

import { useRouter } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";
import { createInterviewReport } from "../shared/interviewApi";
import { AI_FLUENCY_BASE_PATH } from "../shared/mockData";
import type { InterviewPhase } from "../shared/types";
import { EndInterviewDialog } from "./EndInterviewDialog";
import { InterviewHeader } from "./InterviewHeader";
import styles from "./InterviewPage.module.css";
import { InterviewStage } from "./InterviewStage";

interface InterviewPageProps {
  sessionId: string;
}

const INTERVIEW_SECONDS = 30 * 60;
const MICROPHONE_STORAGE_KEY = "interview_microphone_id";

import { getAuthUser } from "@/lib/auth";

export function InterviewPage({ sessionId }: InterviewPageProps) {
  const router = useRouter();
  const [phase, setPhase] = useState<InterviewPhase>("connecting");
  const [remainingSeconds, setRemainingSeconds] = useState(INTERVIEW_SECONDS);
  const [microphoneActive, setMicrophoneActive] = useState(false);
  const [speechTranscript, setSpeechTranscript] = useState("");
  const [speechStatus, setSpeechStatus] = useState<"idle" | "transcribing" | "error">("idle");
  const [speechError, setSpeechError] = useState("");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const startMicrophoneRef = useRef<() => void>(() => undefined);
  const [cameraActive, setCameraActive] = useState(true);
  const [transcriptVisible, setTranscriptVisible] = useState(true);
  const [chatOpen, setChatOpen] = useState(false);
  const [endDialogOpen, setEndDialogOpen] = useState(false);

  useEffect(() => {
    const user = getAuthUser();
    if (user === null) {
      router.replace(AI_FLUENCY_BASE_PATH);
      return;
    }
    const setupTimer = window.setTimeout(() => setPhase("live"), 900);

    return () => window.clearTimeout(setupTimer);
  }, [router]);

  useEffect(() => {
    if (phase !== "live" && phase !== "question-transition") {
      return;
    }

    const countdown = window.setInterval(() => {
      setRemainingSeconds((seconds) => Math.max(0, seconds - 1));
    }, 1000);

    return () => window.clearInterval(countdown);
  }, [phase]);

  useEffect(() => () => {
    const recorder = mediaRecorderRef.current;
    if (recorder !== null && recorder.state !== "inactive") recorder.stop();
    mediaStreamRef.current?.getTracks().forEach((track) => track.stop());
  }, []);

  async function transcribeRecording(blob: Blob) {
    setSpeechError("");
    setSpeechStatus("transcribing");
    try {
      const formData = new FormData();
      formData.append("audio", blob, "answer.webm");
      const response = await fetch("/api/speech/recognize", {
        method: "POST",
        body: formData,
      });
      const body = (await response.json().catch(() => null)) as { detail?: string; text?: string } | null;
      if (!response.ok || !body?.text) {
        throw new Error(body?.detail ?? "Không thể nhận diện giọng nói");
      }
      setSpeechTranscript(body.text);
      setTranscriptVisible(true);
      setSpeechStatus("idle");
    } catch (error) {
      console.error("Vietnamese speech recognition failed", error);
      setSpeechError(error instanceof Error ? error.message : "Không thể nhận diện giọng nói.");
      setSpeechStatus("error");
    }
  }

  async function startMicrophone() {
    const currentRecorder = mediaRecorderRef.current;
    if (currentRecorder !== null && currentRecorder.state === "recording") return;

    try {
      if (!window.isSecureContext || navigator.mediaDevices?.getUserMedia === undefined) {
        throw new DOMException(
          "Microphone chỉ hoạt động trên localhost hoặc HTTPS. Hãy mở web bằng http://localhost:3000 thay vì địa chỉ 192.168.x.x.",
          "SecurityError",
        );
      }
      if (typeof MediaRecorder === "undefined") {
        throw new DOMException("Trình duyệt này không hỗ trợ ghi âm.", "NotSupportedError");
      }
      const microphoneId = sessionStorage.getItem(MICROPHONE_STORAGE_KEY) ?? "";
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          ...(microphoneId ? { deviceId: { exact: microphoneId } } : {}),
        },
      });
      const chunks: Blob[] = [];
      const recorder = new MediaRecorder(stream);
      const audioContext = new AudioContext();
      const source = audioContext.createMediaStreamSource(stream);
      const analyser = audioContext.createAnalyser();
      const samples = new Uint8Array(analyser.fftSize);
      let animationFrame: number | undefined;
      let heardSpeech = false;
      let lastSpeechAt = performance.now();
      const recordingStartedAt = performance.now();
      source.connect(analyser);
      if (audioContext.state === "suspended") await audioContext.resume();
      mediaStreamRef.current = stream;
      mediaRecorderRef.current = recorder;
      recorder.addEventListener("dataavailable", (event) => {
        if (event.data.size > 0) chunks.push(event.data);
      });
      recorder.addEventListener("stop", () => {
        if (animationFrame !== undefined) window.cancelAnimationFrame(animationFrame);
        source.disconnect();
        void audioContext.close();
        stream.getTracks().forEach((track) => track.stop());
        mediaStreamRef.current = null;
        mediaRecorderRef.current = null;
        const blob = new Blob(chunks, { type: recorder.mimeType || "audio/webm" });
        if (blob.size > 0) void transcribeRecording(blob);
      }, { once: true });
      setChatOpen(false);
      setSpeechTranscript("");
      setSpeechError("");
      setSpeechStatus("idle");
      setMicrophoneActive(true);
      recorder.start(250);

      function monitorSilence() {
        if (recorder.state !== "recording") return;
        analyser.getByteTimeDomainData(samples);
        let signalEnergy = 0;
        for (const sample of samples) {
          const normalized = (sample - 128) / 128;
          signalEnergy += normalized * normalized;
        }
        const volume = Math.sqrt(signalEnergy / samples.length);
        const now = performance.now();
        if (volume > 0.018) {
          heardSpeech = true;
          lastSpeechAt = now;
        }
        const finishedSpeaking = heardSpeech && now - lastSpeechAt > 4_000;
        const maximumDurationReached = now - recordingStartedAt > 90_000;
        if (finishedSpeaking || maximumDurationReached) {
          recorder.stop();
          setMicrophoneActive(false);
          return;
        }
        animationFrame = window.requestAnimationFrame(monitorSilence);
      }

      animationFrame = window.requestAnimationFrame(monitorSilence);
    } catch (error) {
      console.error("Could not access the microphone", error);
      setMicrophoneActive(false);
      const errorName = error instanceof DOMException ? error.name : "";
      const message = errorName === "NotAllowedError"
        ? "Quyền microphone đang bị chặn. Nhấn biểu tượng ổ khóa trên thanh địa chỉ, cho phép Microphone rồi tải lại trang."
        : errorName === "NotFoundError"
          ? "Không tìm thấy microphone. Hãy kiểm tra thiết bị đầu vào trong cài đặt âm thanh của máy."
          : errorName === "NotReadableError"
            ? "Microphone đang bị hệ điều hành hoặc ứng dụng khác chiếm dụng. Hãy đóng ứng dụng đang dùng mic rồi thử lại."
            : error instanceof Error
              ? error.message
              : "Không thể truy cập microphone.";
      setSpeechError(message);
      setSpeechStatus("error");
    }
  }

  startMicrophoneRef.current = () => void startMicrophone();
  const beginListening = useCallback(() => startMicrophoneRef.current(), []);
  const consumeSpeechTranscript = useCallback(() => setSpeechTranscript(""), []);

  function toggleMicrophone() {
    const recorder = mediaRecorderRef.current;
    if (recorder !== null && recorder.state === "recording") {
      recorder.stop();
      setMicrophoneActive(false);
      return;
    }
    void startMicrophone();
  }

  useEffect(() => {
    if (phase !== "live") {
      return;
    }

    const transitionTimer = window.setTimeout(
      () => setPhase("question-transition"),
      5200,
    );

    return () => window.clearTimeout(transitionTimer);
  }, [phase]);

  async function finishInterview() {
    setEndDialogOpen(false);
    setPhase("processing");
    try {
      await createInterviewReport(sessionId);
    } catch (error) {
      console.error("Could not create the interview report", error);
    } finally {
      router.push(`${AI_FLUENCY_BASE_PATH}/${sessionId}/feedback`);
    }
  }

  function toggleChat() {
    const openingChat = !chatOpen;
    setChatOpen(openingChat);
    if (openingChat) {
      setTranscriptVisible(true);
      const recorder = mediaRecorderRef.current;
      if (recorder !== null && recorder.state === "recording") recorder.stop();
      setMicrophoneActive(false);
    }
  }

  return (
    <div className={styles.interviewPage} data-session-id={sessionId}>
      <InterviewHeader
        remainingSeconds={remainingSeconds}
        onEndInterview={() => setEndDialogOpen(true)}
      />
      <InterviewStage
        sessionId={sessionId}
        phase={phase}
        microphoneActive={microphoneActive}
        cameraActive={cameraActive}
        chatOpen={chatOpen}
        speechStatus={speechStatus}
        speechError={speechError}
        speechTranscript={speechTranscript}
        transcriptVisible={transcriptVisible}
        onReadyForAnswer={beginListening}
        onSpeechTranscriptConsumed={consumeSpeechTranscript}
        onToggleChat={toggleChat}
        onToggleMicrophone={toggleMicrophone}
        onToggleCamera={() => setCameraActive((active) => !active)}
        onToggleTranscript={() => setTranscriptVisible((visible) => !visible)}
      />
      {endDialogOpen ? (
        <EndInterviewDialog
          remainingMinutes={Math.ceil(remainingSeconds / 60)}
          onContinue={() => setEndDialogOpen(false)}
          onEnd={() => void finishInterview()}
        />
      ) : null}
    </div>
  );
}
