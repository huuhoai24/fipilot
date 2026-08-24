import os
import subprocess
import tempfile
import threading
import wave
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk


def _convert_to_wav(audio: bytes) -> tuple[Path, tempfile.TemporaryDirectory]:
    directory = tempfile.TemporaryDirectory(prefix="fipilot-stt-")
    input_path = Path(directory.name) / "recording"
    output_path = Path(directory.name) / "recording.wav"
    input_path.write_bytes(audio)
    conversion = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-i",
            str(input_path),
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            str(output_path),
        ],
        capture_output=True,
        check=False,
    )
    if conversion.returncode != 0:
        directory.cleanup()
        details = conversion.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"Could not decode the recording: {details}")
    return output_path, directory


def recognize_vietnamese(audio: bytes) -> str:
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    if not speech_key or not speech_region:
        raise RuntimeError("Azure Speech is not configured")

    wav_path, directory = _convert_to_wav(audio)
    try:
        with wave.open(str(wav_path), "rb") as wav_file:
            duration = wav_file.getnframes() / wav_file.getframerate()

        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region,
        )
        speech_config.speech_recognition_language = "vi-VN"
        audio_config = speechsdk.audio.AudioConfig(filename=str(wav_path))
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )

        completed = threading.Event()
        transcript: list[str] = []
        cancellation_error: list[str] = []

        def recognized(event) -> None:
            if event.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                text = event.result.text.strip()
                if text:
                    transcript.append(text)

        def canceled(event) -> None:
            details = event.result.cancellation_details
            if details.error_details:
                cancellation_error.append(details.error_details)
            completed.set()

        recognizer.recognized.connect(recognized)
        recognizer.session_stopped.connect(lambda _: completed.set())
        recognizer.canceled.connect(canceled)
        recognizer.start_continuous_recognition_async().get()
        finished = completed.wait(timeout=max(30.0, duration + 20.0))
        recognizer.stop_continuous_recognition_async().get()

        if not finished:
            raise TimeoutError("Azure Speech recognition timed out")
        if cancellation_error and not transcript:
            raise RuntimeError(cancellation_error[0])
        return " ".join(transcript).strip()
    finally:
        directory.cleanup()
