import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { getInterviewGreetingAudio } from "../shared/greetingAudio";
import {
  getPreparedInterviewQuestions,
  requestNextInterviewQuestion,
  saveInterviewTurn,
  type InterviewQuestion,
} from "../shared/interviewApi";
import { MOCK_TRANSCRIPT } from "../shared/mockData";
import type { InterviewPhase } from "../shared/types";
import { MediaControls } from "./MediaControls";
import styles from "./InterviewPage.module.css";

const CAMERA_STORAGE_KEY = "interview_camera_id";

interface InterviewStageProps {
  sessionId: string;
  phase: InterviewPhase;
  microphoneActive: boolean;
  cameraActive: boolean;
  chatOpen: boolean;
  speechError: string;
  speechStatus: "idle" | "transcribing" | "error";
  speechTranscript: string;
  transcriptVisible: boolean;
  onReadyForAnswer: () => void;
  onSpeechTranscriptConsumed: () => void;
  onToggleChat: () => void;
  onToggleMicrophone: () => void;
  onToggleCamera: () => void;
  onToggleTranscript: () => void;
}

function Waveform({ active }: { active: boolean }) {
  const rays = Array.from({ length: 31 }, (_, index) => index);
  const contours = [0, 1, 2, 3, 4, 5];

  return (
    <svg
      className={`${styles.waveform} ${active ? styles.waveformActive : ""}`}
      viewBox="0 0 1440 190"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="ai-wave-fade" x1="0" x2="1">
          <stop offset="0" stopColor="#77f8f0" stopOpacity=".16" />
          <stop offset=".5" stopColor="#a1fff9" stopOpacity=".75" />
          <stop offset="1" stopColor="#77f8f0" stopOpacity=".16" />
        </linearGradient>
      </defs>
      <g className={styles.waveRays}>
        {rays.map((ray) => {
          const x = ray * 48;
          return <path key={ray} d={`M720 82 L${x} 190`} />;
        })}
      </g>
      <g className={styles.waveContours}>
        {contours.map((contour) => {
          const y = 80 + contour * 18;
          const arch = 20 + contour * 3;
          return (
            <path
              key={contour}
              d={`M0 ${y + 52} Q360 ${y - arch} 720 ${y} T1440 ${y + 52}`}
            />
          );
        })}
      </g>
      <path
        className={styles.waveCrest}
        d="M0 126 C80 110 112 127 174 108 C232 91 287 112 351 93 C415 77 480 101 540 84 C606 64 649 91 708 73 C762 58 821 91 882 72 C945 58 1008 92 1062 79 C1125 65 1196 103 1262 91 C1324 82 1381 112 1440 104"
      />
    </svg>
  );
}

interface SpokenTextProps {
  audio: HTMLAudioElement;
  onEnded?: () => void;
  text: string;
}

function SpokenText({ audio, onEnded, text }: SpokenTextProps) {
  const [visibleText, setVisibleText] = useState("");
  const [playbackBlocked, setPlaybackBlocked] = useState(false);

  async function continuePlayback() {
    try {
      await audio.play();
      setPlaybackBlocked(false);
    } catch {
      setPlaybackBlocked(true);
    }
  }

  useEffect(() => {
    let timer: number | undefined;
    let animationFrame: number | undefined;
    let cancelled = false;

    function revealText(characterDelayMs: number) {
      let characterIndex = 0;
      timer = window.setInterval(() => {
        characterIndex += 1;
        setVisibleText(text.slice(0, characterIndex));
        if (characterIndex === text.length) {
          window.clearInterval(timer);
          onEnded?.();
        }
      }, characterDelayMs);
    }

    function syncTextToAudio() {
      if (cancelled || audio === null) return;

      if (!Number.isFinite(audio.duration) || audio.duration <= 0) {
        revealText(40);
        return;
      }

      const progress = Math.min(1, audio.currentTime / audio.duration);
      const characterIndex = Math.max(1, Math.floor(progress * text.length));
      setVisibleText(text.slice(0, characterIndex));

      if (audio.ended) {
        setVisibleText(text);
        return;
      }
      animationFrame = window.requestAnimationFrame(syncTextToAudio);
    }

    function finishText() {
      setVisibleText(text);
      onEnded?.();
    }

    function startTextSync() {
      setPlaybackBlocked(false);
      syncTextToAudio();
    }

    audio.addEventListener("ended", finishText);
    audio.addEventListener("playing", startTextSync);
    if (!audio.paused) {
      syncTextToAudio();
    } else if (!audio.ended && audio.currentTime === 0) {
      void audio.play().catch(() => {
        if (!cancelled) setPlaybackBlocked(true);
      });
    } else if (audio.ended || audio.currentTime > 0) {
      setVisibleText(text);
    }

    return () => {
      cancelled = true;
      if (timer !== undefined) window.clearInterval(timer);
      if (animationFrame !== undefined) window.cancelAnimationFrame(animationFrame);
      audio.removeEventListener("ended", finishText);
      audio.removeEventListener("playing", startTextSync);
    };
  }, [audio, onEnded, text]);

  return (
    <>
      {visibleText}
      {playbackBlocked ? (
        <button className={styles.continuePlaybackButton} onClick={continuePlayback} type="button">
          Tiếp tục phỏng vấn
        </button>
      ) : null}
    </>
  );
}

function SpeakerGlyph() {
  return (
    <span className={styles.speakerGlyph} aria-hidden="true">
      <i />
      <i />
      <i />
      <i />
      <i />
      <i />
    </span>
  );
}

interface TranscriptMessage {
  audio: HTMLAudioElement | null;
  expectsAnswer?: boolean;
  id: string;
  onEnded?: () => void;
  text: string;
}

async function prepareQuestionAudio(text: string) {
  const response = await fetch("/api/speech", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Question speech request failed");
  const url = URL.createObjectURL(await response.blob());
  const audio = new Audio(url);
  audio.preload = "auto";
  audio.volume = 1;
  await new Promise<void>((resolve, reject) => {
    audio.addEventListener("loadedmetadata", () => resolve(), { once: true });
    audio.addEventListener("error", () => reject(new Error("Question audio failed to load")), {
      once: true,
    });
  });
  return { audio, url };
}

function Transcript({
  sessionId,
  chatOpen,
  microphoneActive,
  speechError,
  speechStatus,
  speechTranscript,
  onReadyForAnswer,
  onSpeechTranscriptConsumed,
}: {
  sessionId: string;
  chatOpen: boolean;
  microphoneActive: boolean;
  speechError: string;
  speechStatus: "idle" | "transcribing" | "error";
  speechTranscript: string;
  onReadyForAnswer: () => void;
  onSpeechTranscriptConsumed: () => void;
}) {
  const [greetingAudio, setGreetingAudio] = useState<HTMLAudioElement | null>(null);
  const [greetingFinished, setGreetingFinished] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState<InterviewQuestion | null>(null);
  const [interviewMessages, setInterviewMessages] = useState<TranscriptMessage[]>([]);
  const [followUpCount, setFollowUpCount] = useState(0);
  const [usedProjectNames, setUsedProjectNames] = useState<string[]>([]);
  const [usedQuestionTexts, setUsedQuestionTexts] = useState<string[]>([]);
  const [answerPending, setAnswerPending] = useState(false);
  const [draftAnswer, setDraftAnswer] = useState("");
  const audioAssets = useRef<Array<{ audio: HTMLAudioElement; url: string }>>([]);

  useEffect(() => {
    setGreetingAudio(getInterviewGreetingAudio());
  }, []);

  useEffect(() => {
    let cancelled = false;
    async function prepareFirstQuestion() {
      try {
        const result = await getPreparedInterviewQuestions(sessionId);
        const firstQuestion = result.questions[0];
        if (firstQuestion === undefined || cancelled) return;
        const asset = await prepareQuestionAudio(firstQuestion.question);
        if (cancelled) {
          asset.audio.pause();
          URL.revokeObjectURL(asset.url);
          return;
        }
        audioAssets.current.push(asset);
        setCurrentQuestion(firstQuestion);
        setUsedProjectNames([firstQuestion.project]);
        setUsedQuestionTexts([firstQuestion.question]);
        setInterviewMessages([{
          audio: asset.audio,
          expectsAnswer: true,
          id: `question-${Date.now().toString(36)}`,
          text: firstQuestion.question,
        }]);
      } catch (error) {
        console.error("Could not prepare the first interview question", error);
      }
    }

    void prepareFirstQuestion();
    return () => {
      cancelled = true;
      audioAssets.current.forEach(({ audio, url }) => {
        audio.pause();
        URL.revokeObjectURL(url);
      });
      audioAssets.current = [];
    };
  }, [sessionId]);

  const finishGreeting = useCallback(() => setGreetingFinished(true), []);
  const showQuestion = greetingFinished && currentQuestion !== null;
  const transcriptMessages = greetingAudio === null
    ? []
    : [
        {
          audio: greetingAudio,
          id: "greeting",
          onEnded: finishGreeting,
          text: MOCK_TRANSCRIPT[0].text,
        },
        ...(greetingFinished ? interviewMessages : []),
      ].slice(-2);

  const submitAnswer = useCallback(async (providedAnswer?: string) => {
    const answer = (providedAnswer ?? draftAnswer).trim();
    if (!answer || !showQuestion || currentQuestion === null || answerPending) return;
    const answerId = `answer-${Date.now().toString(36)}`;
    setInterviewMessages((messages) => [
      ...messages,
      { audio: null, id: answerId, text: answer },
    ]);
    setDraftAnswer("");
    setAnswerPending(true);
    try {
      const result = await requestNextInterviewQuestion(
        sessionId,
        currentQuestion,
        answer,
        followUpCount,
        usedProjectNames,
        usedQuestionTexts,
      );
      saveInterviewTurn(sessionId, currentQuestion, answer);
      let audio: HTMLAudioElement | null = null;
      try {
        const asset = await prepareQuestionAudio(result.question.question);
        audioAssets.current.push(asset);
        audio = asset.audio;
      } catch (error) {
        console.error("Could not prepare next question audio", error);
      }
      setCurrentQuestion(result.question);
      setFollowUpCount(result.follow_up_count);
      setUsedProjectNames((names) => (
        names.includes(result.question.project) ? names : [...names, result.question.project]
      ));
      setUsedQuestionTexts((questions) => (
        questions.includes(result.question.question)
          ? questions
          : [...questions, result.question.question]
      ));
      setInterviewMessages((messages) => [
        ...messages,
        {
          audio,
          expectsAnswer: true,
          id: `question-${Date.now().toString(36)}`,
          text: result.question.question,
        },
      ]);
      if (audio === null && !chatOpen) {
        window.setTimeout(onReadyForAnswer, 0);
      }
    } catch (error) {
      console.error("Could not prepare the next interview question", error);
      setInterviewMessages((messages) => messages.filter((message) => message.id !== answerId));
      setDraftAnswer(answer);
    } finally {
      setAnswerPending(false);
    }
  }, [
    answerPending,
    chatOpen,
    currentQuestion,
    draftAnswer,
    followUpCount,
    onReadyForAnswer,
    sessionId,
    showQuestion,
    usedProjectNames,
    usedQuestionTexts,
  ]);

  useEffect(() => {
    if (!speechTranscript || !showQuestion || currentQuestion === null || answerPending) return;
    const recognizedAnswer = speechTranscript;
    onSpeechTranscriptConsumed();
    void submitAnswer(recognizedAnswer);
  }, [
    answerPending,
    currentQuestion,
    onSpeechTranscriptConsumed,
    showQuestion,
    speechTranscript,
    submitAnswer,
  ]);

  return (
    <div className={styles.transcript} aria-live="polite">
      <div className={styles.transcriptStack}>
        {transcriptMessages.map((message, index) => {
          const isCurrent = index === transcriptMessages.length - 1;
          return (
            <div
              className={`${styles.transcriptMessage} ${isCurrent ? styles.currentMessage : styles.olderMessage}`}
              key={message.id}
            >
              <SpeakerGlyph />
              <p>
                {isCurrent && message.audio !== null ? (
                  <SpokenText
                    audio={message.audio}
                    key={message.id}
                    onEnded={message.onEnded ?? (
                      message.expectsAnswer && !chatOpen ? onReadyForAnswer : undefined
                    )}
                    text={message.text}
                  />
                ) : message.text}
              </p>
            </div>
          );
        })}
      </div>
      {microphoneActive ? (
        <div className={styles.listeningStatus}>
          <span aria-hidden="true" />
          Đang nghe... nói xong và im lặng để gửi
        </div>
      ) : null}
      {speechStatus === "transcribing" ? (
        <div className={styles.listeningStatus} role="status">
          <span aria-hidden="true" />
          Đang chuyển giọng nói thành văn bản...
        </div>
      ) : null}
      {speechStatus === "error" ? (
        <div className={styles.listeningStatus} role="alert">
          {speechError || "Không thể nhận diện giọng nói. Hãy thử lại."}
        </div>
      ) : null}
      {chatOpen && typeof document !== "undefined"
        ? createPortal(
            <form
              className={styles.chatComposer}
              onSubmit={(event) => {
                event.preventDefault();
                void submitAnswer();
              }}
            >
              <textarea
                aria-label="Nhập câu trả lời"
                autoFocus
                disabled={!showQuestion || answerPending}
                onChange={(event) => setDraftAnswer(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    event.currentTarget.form?.requestSubmit();
                  }
                }}
                placeholder={answerPending
                  ? "Đang chuẩn bị câu hỏi tiếp theo..."
                  : showQuestion ? "Nhập câu trả lời của bạn..." : "Đang chờ câu hỏi..."}
                rows={3}
                value={draftAnswer}
              />
              <span>Enter để gửi · Shift + Enter để xuống dòng</span>
            </form>,
            document.body,
          )
        : null}
    </div>
  );
}

function SelfView() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [videoReady, setVideoReady] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function startCamera() {
      if (typeof navigator === "undefined" || !navigator.mediaDevices?.getUserMedia) {
        return;
      }
      const selectedCameraId = sessionStorage.getItem(CAMERA_STORAGE_KEY) ?? "";
      let useSelectedCamera = Boolean(selectedCameraId);

      for (let attempt = 0; attempt < 3 && !cancelled; attempt += 1) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            audio: false,
            video: {
              width: { ideal: 1280 },
              height: { ideal: 720 },
              ...(useSelectedCamera ? { deviceId: { exact: selectedCameraId } } : {}),
            },
          });
          if (cancelled) {
            stream.getTracks().forEach((track) => track.stop());
            return;
          }
          streamRef.current = stream;
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            await videoRef.current.play().catch(() => undefined);
          }
          return;
        } catch (error) {
          if (cancelled) return;
          if (
            useSelectedCamera
            && error instanceof DOMException
            && (error.name === "NotFoundError" || error.name === "OverconstrainedError")
          ) {
            useSelectedCamera = false;
            continue;
          }
          if (
            attempt < 2
            && error instanceof DOMException
            && (error.name === "NotReadableError" || error.name === "AbortError")
          ) {
            await waitForCamera(300 * (attempt + 1));
            continue;
          }
          return;
        }
      }
    }

    void startCamera();
    return () => {
      cancelled = true;
      streamRef.current?.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    };
  }, []);

  return (
    <div className={styles.selfView} aria-label="Self view">
      <video
        ref={videoRef}
        className={styles.selfViewVideo}
        autoPlay
        muted
        onPlaying={() => setVideoReady(true)}
        playsInline
      />
      {!videoReady ? <div className={styles.selfViewGlow} /> : null}
      <div className={styles.signalBadge} aria-label="Strong connection">
        <i />
        <i />
        <i />
        <i />
      </div>
    </div>
  );
}

function waitForCamera(milliseconds: number) {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}

function StatusScreen({ processing }: { processing: boolean }) {
  return (
    <div className={styles.statusScreen} role="status">
      <span className={styles.spinner} aria-hidden="true" />
      <strong>
        {processing ? "Preparing your feedback" : "Setting up your interview"}
      </strong>
      <span>
        {processing
          ? "Your interview has ended."
          : "Connecting to your interviewer..."}
      </span>
    </div>
  );
}

export function InterviewStage({
  sessionId,
  phase,
  microphoneActive,
  cameraActive,
  chatOpen,
  speechError,
  speechStatus,
  speechTranscript,
  transcriptVisible,
  onReadyForAnswer,
  onSpeechTranscriptConsumed,
  onToggleChat,
  onToggleMicrophone,
  onToggleCamera,
  onToggleTranscript,
}: InterviewStageProps) {
  const isLive = phase === "live" || phase === "question-transition";

  if (!isLive) {
    return (
      <main className={styles.stage}>
        <StatusScreen processing={phase === "processing"} />
      </main>
    );
  }

  const onlyTranscript = transcriptVisible && !cameraActive;
  const onlyCamera = cameraActive && !transcriptVisible;

  return (
    <main className={styles.stage}>
      <Waveform active={microphoneActive} />
      <div
        className={`${styles.conversation} ${onlyTranscript ? styles.onlyTranscript : ""} ${onlyCamera ? styles.onlyCamera : ""}`}
      >
        {transcriptVisible ? (
          <Transcript
            sessionId={sessionId}
            chatOpen={chatOpen}
            microphoneActive={microphoneActive}
            speechError={speechError}
            speechStatus={speechStatus}
            speechTranscript={speechTranscript}
            onReadyForAnswer={onReadyForAnswer}
            onSpeechTranscriptConsumed={onSpeechTranscriptConsumed}
          />
        ) : null}
        {cameraActive ? <SelfView /> : null}
      </div>
      <MediaControls
        microphoneActive={microphoneActive}
        cameraActive={cameraActive}
        transcriptVisible={transcriptVisible}
        chatOpen={chatOpen}
        onToggleChat={onToggleChat}
        onToggleMicrophone={onToggleMicrophone}
        onToggleCamera={onToggleCamera}
        onToggleTranscript={onToggleTranscript}
      />
    </main>
  );
}
