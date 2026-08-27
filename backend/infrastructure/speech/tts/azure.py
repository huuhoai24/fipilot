from __future__ import annotations

import asyncio
import subprocess
from collections.abc import AsyncIterator
from typing import Any

from core.logging import get_logger
from infrastructure.speech.tts.base import AudioChunk, StreamingTTS


logger = get_logger(__name__)


try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:  # pragma: no cover - imported only when provider is selected
    speechsdk = None


SAMPLE_RATE = 24000
# ~100 ms mono PCM16 frames: 24000 * 2 bytes * 0.1 s.
_FRAME_BYTES = SAMPLE_RATE * 2 * 100 // 1000


class AzureTTSError(RuntimeError):
    pass


class AzureStreamingTTS(StreamingTTS):
    """Azure Text-to-Speech adapter that emits mono PCM16 @ 24 kHz frames.

    Azure returns MP3, which we decode to raw PCM16 little-endian with ffmpeg
    (the same dependency VieNeu relies on) and chunk into ~100 ms frames.
    """

    def __init__(
        self,
        *,
        speech_key: str,
        speech_region: str,
        speech_endpoint: str | None = None,
        voice: str = "vi-VN-HoaiMyNeural",
        sample_rate: int = SAMPLE_RATE,
        frame_duration_ms: int = 100,
    ) -> None:
        if not speech_key or not (speech_region or speech_endpoint):
            raise AzureTTSError(
                "Azure Speech TTS requires AZURE_SPEECH_KEY and "
                "AZURE_SPEECH_REGION (or AZURE_SPEECH_ENDPOINT)."
            )
        if speechsdk is None:
            raise AzureTTSError(
                "Install azure-cognitiveservices-speech to use Azure TTS."
            )
        self._speech_key = speech_key
        self._speech_region = speech_region
        self._speech_endpoint = speech_endpoint
        self.voice = voice
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self._frame_bytes = max(
            1, sample_rate * 2 * frame_duration_ms // 1000
        )
        self._synthesizer: Any | None = None

    def _get_synthesizer(self):
        if self._synthesizer is not None:
            return self._synthesizer
        if self._speech_endpoint:
            config = speechsdk.SpeechConfig(
                endpoint=self._speech_endpoint,
                subscription=self._speech_key,
            )
        else:
            config = speechsdk.SpeechConfig(
                subscription=self._speech_key,
                region=self._speech_region,
            )
        config.speech_synthesis_voice_name = self.voice
        # Ensure it does not play on the host speaker by setting audio_config=None
        audio_config = None
        self._synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=config, audio_config=audio_config
        )
        return self._synthesizer

    async def synthesize_stream(self, text: str) -> AsyncIterator[AudioChunk]:
        normalized_text = text.strip()
        if not normalized_text:
            return
        mp3_bytes = await asyncio.to_thread(self._synthesize_mp3, normalized_text)
        pcm = await asyncio.to_thread(self._decode_mp3, mp3_bytes)
        for offset in range(0, len(pcm), self._frame_bytes):
            frame = pcm[offset : offset + self._frame_bytes]
            if frame:
                yield AudioChunk(
                    bytes=frame,
                    sample_rate=self.sample_rate,
                    format="pcm",
                )

    def _synthesize_mp3(self, text: str) -> bytes:
        import html
        synthesizer = self._get_synthesizer()
        
        ssml = (
            "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
            "xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='vi-VN'>"
            f"<voice xml:lang='vi-VN' name='{html.escape(self.voice)}'>"
            f"<prosody rate='+0%'>{html.escape(text)}</prosody>"
            "</voice>"
            "</speak>"
        )
        
        result = synthesizer.speak_ssml_async(ssml).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            reason = getattr(result, "reason", "unknown")
            raise AzureTTSError(
                f"Azure Speech synthesis failed (reason={reason})."
            )
        return result.audio_data

    def _decode_mp3(self, mp3_bytes: bytes) -> bytes:
        conversion = subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-i",
                "-",
                "-f",
                "s16le",
                "-ac",
                "1",
                "-ar",
                str(self.sample_rate),
                "-",
            ],
            input=mp3_bytes,
            capture_output=True,
            check=False,
        )
        if conversion.returncode != 0:
            details = conversion.stderr.decode("utf-8", errors="replace").strip()
            raise AzureTTSError(f"Could not decode Azure TTS audio: {details}")
        return conversion.stdout

    async def warm_up(self) -> None:
        async for _ in self.synthesize_stream("Xin chao."):
            pass

    def close(self) -> None:
        if self._synthesizer is not None:
            try:
                self._synthesizer = None
            except Exception:
                pass
