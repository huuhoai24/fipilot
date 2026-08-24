"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  AlertTriangle,
  Camera,
  CameraOff,
  Check,
  ChevronDown,
  ChevronUp,
  LoaderCircle,
  Mic,
  Volume2,
} from "lucide-react";
import type { DevicePermissionState } from "../shared/types";
import styles from "./landing.module.css";

interface DeviceSettingsDialogProps {
  onBack: () => void;
  onStart: () => void;
}

type DeviceKind = "audioinput" | "audiooutput" | "videoinput";
type OpenMenu = "microphone" | "speaker" | "camera" | null;

const DEFAULT_LABELS: Record<DeviceKind, string> = {
  audioinput: "Default microphone",
  audiooutput: "Default speakers",
  videoinput: "Default camera",
};
const MICROPHONE_STORAGE_KEY = "interview_microphone_id";
const CAMERA_STORAGE_KEY = "interview_camera_id";

export function DeviceSettingsDialog({ onBack, onStart }: DeviceSettingsDialogProps) {
  const [permission, setPermission] = useState<DevicePermissionState>("checking");
  const [permissionError, setPermissionError] = useState("");
  const [cameraError, setCameraError] = useState("");
  const [devices, setDevices] = useState<MediaDeviceInfo[]>([]);
  const [selectedMicrophone, setSelectedMicrophone] = useState("");
  const [selectedSpeaker, setSelectedSpeaker] = useState("");
  const [selectedCamera, setSelectedCamera] = useState("");
  const [openMenu, setOpenMenu] = useState<OpenMenu>(null);
  const [microphoneLevel, setMicrophoneLevel] = useState(0);
  const [testingSpeakers, setTestingSpeakers] = useState(false);
  const mountedRef = useRef(false);
  const requestIdRef = useRef(0);
  const streamRef = useRef<MediaStream | null>(null);
  const previewRef = useRef<HTMLVideoElement>(null);
  const testAudioRef = useRef<HTMLAudioElement>(null);

  const refreshDevices = useCallback(async () => {
    const availableDevices = await navigator.mediaDevices.enumerateDevices();
    if (!mountedRef.current) return;
    setDevices(availableDevices);

    setSelectedMicrophone((current) => (
      deviceStillExists(availableDevices, "audioinput", current)
        ? current
        : firstDeviceId(availableDevices, "audioinput")
    ));
    setSelectedSpeaker((current) => (
      deviceStillExists(availableDevices, "audiooutput", current)
        ? current
        : firstDeviceId(availableDevices, "audiooutput")
    ));
    setSelectedCamera((current) => (
      deviceStillExists(availableDevices, "videoinput", current)
        ? current
        : firstDeviceId(availableDevices, "videoinput")
    ));
  }, []);

  const connectDevices = useCallback(async (
    microphoneId = "",
    cameraId = "",
  ) => {
    const requestId = ++requestIdRef.current;
    if (!navigator.mediaDevices?.getUserMedia) {
      setPermission("required");
      setPermissionError("Microphone access is not supported by this browser.");
      return;
    }

    setPermission("checking");
    setPermissionError("");

    let audioStream: MediaStream;
    try {
      audioStream = await navigator.mediaDevices.getUserMedia({
        audio: microphoneId ? { deviceId: { exact: microphoneId } } : true,
        video: false,
      });
    } catch (error) {
      if (!mountedRef.current || requestId !== requestIdRef.current) return;
      setPermission("required");
      setPermissionError(getMicrophoneErrorMessage(error));
      return;
    }

    if (!mountedRef.current || requestId !== requestIdRef.current) {
      audioStream.getTracks().forEach((track) => track.stop());
      return;
    }

    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = audioStream;
    const microphoneDeviceId = audioStream.getAudioTracks()[0]?.getSettings().deviceId;
    if (microphoneDeviceId) setSelectedMicrophone(microphoneDeviceId);
    setPermission("ready");
    void refreshDevices().catch(() => undefined);

    try {
      const videoStream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: cameraId
          ? { deviceId: { exact: cameraId } }
          : { width: { ideal: 1280 }, height: { ideal: 720 } },
      });
      if (!mountedRef.current || requestId !== requestIdRef.current) {
        videoStream.getTracks().forEach((track) => track.stop());
        return;
      }

      const nextStream = new MediaStream([
        ...audioStream.getAudioTracks(),
        ...videoStream.getVideoTracks(),
      ]);
      streamRef.current = nextStream;
      if (previewRef.current) previewRef.current.srcObject = nextStream;

      const cameraDeviceId = nextStream.getVideoTracks()[0]?.getSettings().deviceId;
      if (cameraDeviceId) setSelectedCamera(cameraDeviceId);
      setCameraError("");
    } catch (error) {
      if (mountedRef.current && requestId === requestIdRef.current) {
        setCameraError(getCameraErrorMessage(error));
      }
    }
  }, [refreshDevices]);

  useEffect(() => {
    mountedRef.current = true;
    const frame = window.requestAnimationFrame(() => void connectDevices());

    return () => {
      mountedRef.current = false;
      requestIdRef.current += 1;
      window.cancelAnimationFrame(frame);
      streamRef.current?.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    };
  }, [connectDevices]);

  useEffect(() => {
    if (!navigator.mediaDevices) return;

    const handleDeviceChange = () => void refreshDevices();
    navigator.mediaDevices.addEventListener("devicechange", handleDeviceChange);
    return () => navigator.mediaDevices.removeEventListener("devicechange", handleDeviceChange);
  }, [refreshDevices]);

  useEffect(() => {
    if (permission === "ready" && previewRef.current) {
      previewRef.current.srcObject = streamRef.current;
    }
  }, [cameraError, permission, selectedCamera]);

  useEffect(() => {
    const stream = streamRef.current;
    if (permission !== "ready" || !stream?.getAudioTracks().length) {
      return;
    }

    const audioContext = new AudioContext();
    const analyser = audioContext.createAnalyser();
    const source = audioContext.createMediaStreamSource(
      new MediaStream(stream.getAudioTracks()),
    );
    const samples = new Uint8Array(analyser.fftSize);
    let frame = 0;

    source.connect(analyser);
    void audioContext.resume();
    const measure = () => {
      analyser.getByteTimeDomainData(samples);
      let energy = 0;
      for (const sample of samples) {
        const amplitude = (sample - 128) / 128;
        energy += amplitude * amplitude;
      }
      const rms = Math.sqrt(energy / samples.length);
      setMicrophoneLevel(Math.min(7, Math.ceil(rms * 32)));
      frame = window.requestAnimationFrame(measure);
    };
    measure();

    return () => {
      window.cancelAnimationFrame(frame);
      source.disconnect();
      void audioContext.close();
    };
  }, [permission, selectedMicrophone]);

  const ready = permission === "ready";
  const microphoneDevices = devices.filter(({ kind }) => kind === "audioinput");
  const speakerDevices = devices.filter(({ kind }) => kind === "audiooutput");
  const cameraDevices = devices.filter(({ kind }) => kind === "videoinput");

  async function selectMicrophone(deviceId: string) {
    setSelectedMicrophone(deviceId);
    setOpenMenu(null);
    await connectDevices(deviceId, selectedCamera);
  }

  async function selectCamera(deviceId: string) {
    setSelectedCamera(deviceId);
    setOpenMenu(null);
    await connectDevices(selectedMicrophone, deviceId);
  }

  async function selectSpeaker(deviceId: string) {
    setSelectedSpeaker(deviceId);
    setOpenMenu(null);
    const audio = testAudioRef.current;
    if (audio && "setSinkId" in audio) {
      await audio.setSinkId(deviceId).catch(() => undefined);
    }
  }

  async function testSpeakers() {
    if (testingSpeakers) return;
    setTestingSpeakers(true);

    const audioContext = new AudioContext();
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    const output = audioContext.createMediaStreamDestination();
    const audio = testAudioRef.current;

    await audioContext.resume();

    oscillator.type = "sine";
    oscillator.frequency.value = 440;
    gain.gain.setValueAtTime(0.0001, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.16, audioContext.currentTime + 0.04);
    gain.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + 0.55);
    oscillator.connect(gain).connect(output);

    if (audio) {
      audio.srcObject = output.stream;
      if (selectedSpeaker && "setSinkId" in audio) {
        await audio.setSinkId(selectedSpeaker).catch(() => undefined);
      }
      await audio.play().catch(() => undefined);
    }

    oscillator.start();
    oscillator.stop(audioContext.currentTime + 0.6);
    window.setTimeout(() => {
      audio?.pause();
      if (audio) audio.srcObject = null;
      void audioContext.close();
      setTestingSpeakers(false);
    }, 700);
  }

  function startInterview() {
    sessionStorage.setItem(MICROPHONE_STORAGE_KEY, selectedMicrophone);
    sessionStorage.setItem(CAMERA_STORAGE_KEY, selectedCamera);
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    onStart();
  }

  return (
    <div className={styles.dialogBackdrop}>
      <section
        className={styles.deviceDialog}
        role="dialog"
        aria-modal="true"
        aria-labelledby="device-settings-title"
      >
        <h2 id="device-settings-title">Audio &amp; Camera Settings</h2>

        {ready ? (
          <ReadyPreview cameraError={cameraError} previewRef={previewRef} />
        ) : (
          <AccessRequiredPreview
            checking={permission === "checking"}
            error={permissionError}
            onRetry={() => void connectDevices(selectedMicrophone, selectedCamera)}
          />
        )}

        <div className={styles.deviceSettings} data-ready={ready || undefined}>
          {ready ? (
            <>
              <DeviceRow
                devices={microphoneDevices}
                fallbackLabel={DEFAULT_LABELS.audioinput}
                Icon={Mic}
                isOpen={openMenu === "microphone"}
                level={<LevelMeter level={microphoneLevel} />}
                onSelect={(deviceId) => void selectMicrophone(deviceId)}
                onToggle={() => setOpenMenu((menu) => menu === "microphone" ? null : "microphone")}
                selectedDeviceId={selectedMicrophone}
              />
              <DeviceRow
                devices={speakerDevices}
                fallbackLabel={DEFAULT_LABELS.audiooutput}
                Icon={Volume2}
                isOpen={openMenu === "speaker"}
                level={(
                  <button className={styles.testSpeakers} onClick={() => void testSpeakers()} type="button">
                    {testingSpeakers ? "Playing..." : "Test Speakers"}
                  </button>
                )}
                onSelect={(deviceId) => void selectSpeaker(deviceId)}
                onToggle={() => setOpenMenu((menu) => menu === "speaker" ? null : "speaker")}
                selectedDeviceId={selectedSpeaker}
              />
              <DeviceRow
                devices={cameraDevices}
                fallbackLabel={DEFAULT_LABELS.videoinput}
                Icon={Camera}
                isOpen={openMenu === "camera"}
                onSelect={(deviceId) => void selectCamera(deviceId)}
                onToggle={() => setOpenMenu((menu) => menu === "camera" ? null : "camera")}
                selectedDeviceId={selectedCamera}
              />
            </>
          ) : (
            <>
              <AccessRow Icon={Mic} label="Microphone" />
              <AccessRow Icon={Volume2} label="Sound" />
              <AccessRow Icon={Camera} label="Camera" />
            </>
          )}
        </div>

        <audio ref={testAudioRef} className={styles.testAudio} />
        <footer className={styles.dialogFooter}>
          <button className={styles.cancelButton} onClick={onBack} type="button">Back</button>
          <button className={styles.startButton} disabled={!ready} onClick={startInterview} type="button">
            Start Interview
          </button>
        </footer>
      </section>
    </div>
  );
}

function AccessRequiredPreview({
  checking,
  error,
  onRetry,
}: {
  checking: boolean;
  error: string;
  onRetry: () => void;
}) {
  return (
    <div className={`${styles.cameraPreview} ${styles.accessPreview}`}>
      {checking ? <LoaderCircle className={styles.permissionSpinner} size={31} /> : <CameraOff size={31} />}
      <strong>{checking ? "Checking your microphone" : "Microphone Access Required"}</strong>
      <p>{checking ? "Allow microphone access in your browser." : error}</p>
      {!checking ? (
        <>
          <div className={styles.permissionHelp}>
            <b>How to allow microphone access:</b>
            <ol>
              <li>Click the microphone or lock icon in the address bar</li>
              <li>Set Microphone to Allow</li>
              <li>Click Try Again</li>
            </ol>
          </div>
          <button className={styles.retryPermission} onClick={onRetry} type="button">Try Again</button>
        </>
      ) : null}
    </div>
  );
}

function ReadyPreview({
  cameraError,
  previewRef,
}: {
  cameraError: string;
  previewRef: React.RefObject<HTMLVideoElement | null>;
}) {
  return (
    <div className={`${styles.cameraPreview} ${cameraError ? styles.accessPreview : styles.readyPreview}`}>
      {cameraError ? (
        <>
          <CameraOff size={31} />
          <strong>Camera unavailable</strong>
          <p>{cameraError} You can still continue with your microphone.</p>
        </>
      ) : (
        <video ref={previewRef} autoPlay muted playsInline aria-label="Camera preview" />
      )}
    </div>
  );
}

function DeviceRow({
  devices,
  fallbackLabel,
  Icon,
  isOpen,
  level,
  onSelect,
  onToggle,
  selectedDeviceId,
}: {
  devices: MediaDeviceInfo[];
  fallbackLabel: string;
  Icon: typeof Mic;
  isOpen: boolean;
  level?: React.ReactNode;
  onSelect: (deviceId: string) => void;
  onToggle: () => void;
  selectedDeviceId: string;
}) {
  const selectedDevice = devices.find(({ deviceId }) => deviceId === selectedDeviceId);

  return (
    <div className={styles.deviceRow}>
      <button
        className={styles.deviceSelect}
        onClick={onToggle}
        aria-expanded={isOpen}
        type="button"
      >
        <Icon size={15} />
        <span>{selectedDevice?.label || fallbackLabel}</span>
        {isOpen ? <ChevronUp size={17} /> : <ChevronDown size={17} />}
      </button>
      {level}
      {isOpen ? (
        <div className={styles.microphoneMenu}>
          {devices.length ? devices.map((device) => (
            <button
              data-selected={device.deviceId === selectedDeviceId || undefined}
              key={`${device.kind}-${device.deviceId}`}
              onClick={() => onSelect(device.deviceId)}
              type="button"
            >
              <Icon size={15} />
              <span>{device.label || fallbackLabel}</span>
              {device.deviceId === selectedDeviceId ? <Check size={15} /> : null}
            </button>
          )) : (
            <span className={styles.noDevices}>No devices found</span>
          )}
        </div>
      ) : null}
    </div>
  );
}

function AccessRow({ Icon, label }: { Icon: typeof Mic; label: string }) {
  return (
    <div className={styles.deviceRow}>
      <span className={styles.accessLabel}><Icon size={15} />{label}</span>
      <span className={styles.accessBadge}><AlertTriangle size={15} />Access Required</span>
    </div>
  );
}

function LevelMeter({ level }: { level: number }) {
  return (
    <span className={styles.levelMeter} aria-label="Microphone input level">
      {Array.from({ length: 7 }, (_, index) => <i data-on={index < level || undefined} key={index} />)}
    </span>
  );
}

function firstDeviceId(devices: MediaDeviceInfo[], kind: DeviceKind) {
  return devices.find((device) => device.kind === kind)?.deviceId ?? "";
}

function deviceStillExists(devices: MediaDeviceInfo[], kind: DeviceKind, deviceId: string) {
  return Boolean(deviceId && devices.some((device) => device.kind === kind && device.deviceId === deviceId));
}

function getMicrophoneErrorMessage(error: unknown) {
  if (error instanceof DOMException) {
    if (error.name === "NotAllowedError" || error.name === "SecurityError") {
      return "Microphone permission was denied.";
    }
    if (error.name === "NotFoundError") {
      return "No microphone was found.";
    }
    if (error.name === "NotReadableError") {
      return "Your microphone is already in use by another application.";
    }
  }
  return "We could not connect to your microphone.";
}

function getCameraErrorMessage(error: unknown) {
  if (error instanceof DOMException) {
    if (error.name === "NotAllowedError" || error.name === "SecurityError") {
      return "Camera permission was denied.";
    }
    if (error.name === "NotFoundError" || error.name === "OverconstrainedError") {
      return "No available camera was found.";
    }
    if (error.name === "NotReadableError") {
      return "Your camera is already in use by another application.";
    }
  }
  return "We could not connect to your camera.";
}
