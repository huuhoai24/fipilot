import React, { useCallback, useEffect, useRef, useState } from 'react'
import {
  AlertTriangle,
  Camera,
  Check,
  ChevronDown,
  Loader2,
  Mic,
  Volume2,
  X,
} from 'lucide-react'

interface DeviceSettingsModalProps {
  isOpen: boolean
  onClose: () => void
  onStart: (settings: {
    audioDeviceId?: string
    videoDeviceId?: string
    cameraEnabled: boolean
  }) => void
}

type DeviceKind = 'audioinput' | 'audiooutput' | 'videoinput'

export function DeviceSettingsModal({
  isOpen,
  onClose,
  onStart,
}: DeviceSettingsModalProps) {
  const [permissionState, setPermissionState] = useState<'checking' | 'ready' | 'denied' | 'error'>('checking')
  const [errorMessage, setErrorMessage] = useState('')
  const [devices, setDevices] = useState<MediaDeviceInfo[]>([])
  const [selectedMicrophone, setSelectedMicrophone] = useState('')
  const [selectedSpeaker, setSelectedSpeaker] = useState('')
  const [selectedCamera, setSelectedCamera] = useState('')
  const [cameraEnabled, setCameraEnabled] = useState(true)
  const [microphoneLevel, setMicrophoneLevel] = useState(0)
  const [testingSpeakers, setTestingSpeakers] = useState(false)
  const [openDropdown, setOpenDropdown] = useState<DeviceKind | null>(null)

  const mountedRef = useRef(false)
  const streamRef = useRef<MediaStream | null>(null)
  const videoPreviewRef = useRef<HTMLVideoElement>(null)
  const audioContextRef = useRef<AudioContext | null>(null)

  const refreshDevices = useCallback(async () => {
    try {
      const list = await navigator.mediaDevices.enumerateDevices()
      if (!mountedRef.current) return
      setDevices(list)

      const audioInputs = list.filter((d) => d.kind === 'audioinput')
      const audioOutputs = list.filter((d) => d.kind === 'audiooutput')
      const videoInputs = list.filter((d) => d.kind === 'videoinput')

      if (audioInputs.length > 0 && !selectedMicrophone) {
        setSelectedMicrophone(audioInputs[0].deviceId)
      }
      if (audioOutputs.length > 0 && !selectedSpeaker) {
        setSelectedSpeaker(audioOutputs[0].deviceId)
      }
      if (videoInputs.length > 0 && !selectedCamera) {
        setSelectedCamera(videoInputs[0].deviceId)
      }
    } catch {
      // ignore
    }
  }, [selectedMicrophone, selectedSpeaker, selectedCamera])

  const setupStreams = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setPermissionState('error')
      setErrorMessage('Microphone access is not supported by your browser.')
      return
    }

    setPermissionState('checking')
    setErrorMessage('')

    // Stop existing stream
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }

    try {
      const audioConstraint = selectedMicrophone
        ? { deviceId: { exact: selectedMicrophone } }
        : true

      const videoConstraint = cameraEnabled
        ? (selectedCamera ? { deviceId: { exact: selectedCamera } } : { width: { ideal: 640 }, height: { ideal: 480 } })
        : false

      const mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: audioConstraint,
        video: videoConstraint,
      })

      if (!mountedRef.current) {
        mediaStream.getTracks().forEach((t) => t.stop())
        return
      }

      streamRef.current = mediaStream
      setPermissionState('ready')

      if (videoPreviewRef.current && cameraEnabled) {
        videoPreviewRef.current.srcObject = mediaStream
      }

      await refreshDevices()
    } catch (err: unknown) {
      if (!mountedRef.current) return
      if (err instanceof DOMException && (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError')) {
        setPermissionState('denied')
        setErrorMessage('Microphone or Camera permission was denied. Please allow access in your browser.')
      } else {
        setPermissionState('error')
        setErrorMessage('Could not connect to audio/video devices.')
      }
    }
  }, [selectedMicrophone, selectedCamera, cameraEnabled, refreshDevices])

  useEffect(() => {
    if (!isOpen) return
    mountedRef.current = true
    void setupStreams()

    return () => {
      mountedRef.current = false
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop())
        streamRef.current = null
      }
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        void audioContextRef.current.close()
      }
    }
  }, [isOpen, setupStreams])

  // Mic level meter
  useEffect(() => {
    if (permissionState !== 'ready' || !streamRef.current) return
    const audioTracks = streamRef.current.getAudioTracks()
    if (audioTracks.length === 0) return

    let animFrame = 0
    try {
      const audioCtx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)()
      audioContextRef.current = audioCtx
      const analyser = audioCtx.createAnalyser()
      analyser.fftSize = 256
      const source = audioCtx.createMediaStreamSource(new MediaStream(audioTracks))
      source.connect(analyser)

      const buffer = new Uint8Array(analyser.frequencyBinCount)

      const updateMeter = () => {
        if (!mountedRef.current) return
        analyser.getByteFrequencyData(buffer)
        let sum = 0
        for (let i = 0; i < buffer.length; i++) {
          sum += buffer[i]
        }
        const avg = sum / buffer.length
        // Scale to 0-7 bars
        const bars = Math.min(7, Math.round((avg / 128) * 7))
        setMicrophoneLevel(bars)
        animFrame = requestAnimationFrame(updateMeter)
      }
      animFrame = requestAnimationFrame(updateMeter)
    } catch {
      // AudioContext may be blocked or not supported
    }

    return () => {
      cancelAnimationFrame(animFrame)
    }
  }, [permissionState, selectedMicrophone])

  const testSpeakers = async () => {
    if (testingSpeakers) return
    setTestingSpeakers(true)
    try {
      const ctx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)()
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.type = 'sine'
      osc.frequency.setValueAtTime(440, ctx.currentTime)
      gain.gain.setValueAtTime(0.01, ctx.currentTime)
      gain.gain.exponentialRampToValueAtTime(0.3, ctx.currentTime + 0.05)
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6)
      osc.connect(gain)
      gain.connect(ctx.destination)
      osc.start()
      osc.stop(ctx.currentTime + 0.6)
      setTimeout(() => {
        setTestingSpeakers(false)
        void ctx.close()
      }, 700)
    } catch {
      setTestingSpeakers(false)
    }
  }

  const handleStart = () => {
    // Release streams here so SpeechInterviewPage can acquire cleanly
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop())
      streamRef.current = null
    }
    onStart({
      audioDeviceId: selectedMicrophone,
      videoDeviceId: selectedCamera,
      cameraEnabled,
    })
  }

  if (!isOpen) return null

  const micDevices = devices.filter((d) => d.kind === 'audioinput')
  const speakerDevices = devices.filter((d) => d.kind === 'audiooutput')
  const cameraDevices = devices.filter((d) => d.kind === 'videoinput')

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm">
      <div
        className="w-full max-w-xl rounded-2xl border border-white/10 bg-[#16181e] p-6 shadow-2xl text-white animate-fade-in"
        role="dialog"
        aria-modal="true"
        aria-labelledby="audio-settings-title"
      >
        <div className="flex items-center justify-between pb-4 border-b border-white/10">
          <h2 id="audio-settings-title" className="text-xl font-semibold tracking-tight text-white">
            Audio & Camera Settings
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="rounded-lg p-1 text-white/50 hover:bg-white/10 hover:text-white"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Video preview box */}
        <div className="mt-4 relative h-48 w-full overflow-hidden rounded-xl bg-[#0e1014] border border-white/10 flex items-center justify-center">
          {cameraEnabled && permissionState === 'ready' ? (
            <video
              ref={videoPreviewRef}
              autoPlay
              playsInline
              muted
              className="h-full w-full object-cover scale-x-[-1]"
            />
          ) : (
            <div className="flex flex-col items-center gap-2 text-white/40">
              <Camera className="h-10 w-10 stroke-[1.5]" />
              <p className="text-sm">Camera preview inactive</p>
            </div>
          )}
        </div>

        {errorMessage && (
          <div className="mt-3 flex items-start gap-2.5 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-300">
            <AlertTriangle className="h-4 w-4 shrink-0 text-red-400 mt-0.5" />
            <p>{errorMessage}</p>
          </div>
        )}

        <div className="mt-5 space-y-4 text-sm">
          {/* Microphone device selection */}
          <div>
            <label className="text-xs font-medium text-white/70 block mb-1.5">Microphone</label>
            <div className="flex items-center gap-3">
              <div className="relative flex-1">
                <button
                  type="button"
                  onClick={() => setOpenDropdown(openDropdown === 'audioinput' ? null : 'audioinput')}
                  className="flex h-10 w-full items-center justify-between rounded-lg border border-white/10 bg-[#1f222a] px-3 text-left text-sm text-white hover:border-white/20"
                >
                  <span className="flex items-center gap-2 truncate">
                    <Mic className="h-4 w-4 text-accent shrink-0" />
                    {micDevices.find((d) => d.deviceId === selectedMicrophone)?.label || 'Default Microphone'}
                  </span>
                  <ChevronDown className="h-4 w-4 text-white/50 shrink-0" />
                </button>

                {openDropdown === 'audioinput' && (
                  <div className="absolute left-0 top-full z-20 mt-1 max-h-48 w-full overflow-auto rounded-lg border border-white/10 bg-[#1f222a] py-1 shadow-xl">
                    {micDevices.map((device, idx) => (
                      <button
                        key={device.deviceId || idx}
                        type="button"
                        onClick={() => {
                          setSelectedMicrophone(device.deviceId)
                          setOpenDropdown(null)
                        }}
                        className="flex w-full items-center justify-between px-3 py-2 text-left text-xs text-white hover:bg-white/10"
                      >
                        <span className="truncate">{device.label || `Microphone ${idx + 1}`}</span>
                        {selectedMicrophone === device.deviceId && <Check className="h-3.5 w-3.5 text-accent" />}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Mic level bars */}
              <div className="flex items-center gap-0.5 rounded-lg border border-white/10 bg-[#1f222a] px-2.5 h-10" title="Microphone Level">
                {Array.from({ length: 7 }).map((_, i) => (
                  <div
                    key={i}
                    className={`h-4 w-1.5 rounded-sm transition-colors duration-75 ${
                      i < microphoneLevel ? 'bg-accent shadow-sm shadow-accent/50' : 'bg-white/10'
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Speaker selection & test */}
          <div>
            <label className="text-xs font-medium text-white/70 block mb-1.5">Speakers</label>
            <div className="flex items-center gap-3">
              <div className="relative flex-1">
                <button
                  type="button"
                  onClick={() => setOpenDropdown(openDropdown === 'audiooutput' ? null : 'audiooutput')}
                  className="flex h-10 w-full items-center justify-between rounded-lg border border-white/10 bg-[#1f222a] px-3 text-left text-sm text-white hover:border-white/20"
                >
                  <span className="flex items-center gap-2 truncate">
                    <Volume2 className="h-4 w-4 text-white/60 shrink-0" />
                    {speakerDevices.find((d) => d.deviceId === selectedSpeaker)?.label || 'Default Speakers'}
                  </span>
                  <ChevronDown className="h-4 w-4 text-white/50 shrink-0" />
                </button>

                {openDropdown === 'audiooutput' && (
                  <div className="absolute left-0 top-full z-20 mt-1 max-h-48 w-full overflow-auto rounded-lg border border-white/10 bg-[#1f222a] py-1 shadow-xl">
                    {speakerDevices.map((device, idx) => (
                      <button
                        key={device.deviceId || idx}
                        type="button"
                        onClick={() => {
                          setSelectedSpeaker(device.deviceId)
                          setOpenDropdown(null)
                        }}
                        className="flex w-full items-center justify-between px-3 py-2 text-left text-xs text-white hover:bg-white/10"
                      >
                        <span className="truncate">{device.label || `Speaker ${idx + 1}`}</span>
                        {selectedSpeaker === device.deviceId && <Check className="h-3.5 w-3.5 text-accent" />}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <button
                type="button"
                onClick={testSpeakers}
                disabled={testingSpeakers}
                className="h-10 rounded-lg border border-white/10 bg-[#1f222a] px-3 text-xs font-medium text-white hover:bg-white/10 transition-colors shrink-0 disabled:opacity-50"
              >
                {testingSpeakers ? 'Testing...' : 'Test Speakers'}
              </button>
            </div>
          </div>

          {/* Camera selection */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-medium text-white/70 block">Camera</label>
              <button
                type="button"
                onClick={() => setCameraEnabled(!cameraEnabled)}
                className="text-xs text-accent hover:underline font-medium"
              >
                {cameraEnabled ? 'Disable Camera' : 'Enable Camera'}
              </button>
            </div>
            <div className="relative">
              <button
                type="button"
                onClick={() => setOpenDropdown(openDropdown === 'videoinput' ? null : 'videoinput')}
                className="flex h-10 w-full items-center justify-between rounded-lg border border-white/10 bg-[#1f222a] px-3 text-left text-sm text-white hover:border-white/20"
              >
                <span className="flex items-center gap-2 truncate">
                  <Camera className="h-4 w-4 text-white/60 shrink-0" />
                  {cameraDevices.find((d) => d.deviceId === selectedCamera)?.label || 'Default Camera'}
                </span>
                <ChevronDown className="h-4 w-4 text-white/50 shrink-0" />
              </button>

              {openDropdown === 'videoinput' && (
                <div className="absolute left-0 top-full z-20 mt-1 max-h-48 w-full overflow-auto rounded-lg border border-white/10 bg-[#1f222a] py-1 shadow-xl">
                  {cameraDevices.map((device, idx) => (
                    <button
                      key={device.deviceId || idx}
                      type="button"
                      onClick={() => {
                        setSelectedCamera(device.deviceId)
                        setOpenDropdown(null)
                      }}
                      className="flex w-full items-center justify-between px-3 py-2 text-left text-xs text-white hover:bg-white/10"
                    >
                      <span className="truncate">{device.label || `Camera ${idx + 1}`}</span>
                      {selectedCamera === device.deviceId && <Check className="h-3.5 w-3.5 text-accent" />}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Action buttons */}
        <div className="mt-8 flex items-center justify-end gap-3 pt-4 border-t border-white/10">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg px-4 py-2 text-sm font-medium text-white/70 hover:bg-white/10 hover:text-white transition-colors"
          >
            Back
          </button>
          <button
            type="button"
            onClick={handleStart}
            disabled={permissionState === 'checking'}
            className="flex items-center gap-2 rounded-lg bg-accent px-5 py-2 text-sm font-semibold text-slate-950 hover:bg-accent-hover transition-all shadow-md shadow-accent/20 disabled:opacity-50"
          >
            {permissionState === 'checking' && <Loader2 className="h-4 w-4 animate-spin" />}
            Start Interview
          </button>
        </div>
      </div>
    </div>
  )
}
