from __future__ import annotations

import asyncio
import subprocess
import tempfile
import urllib.error
import urllib.request
from html import escape
from pathlib import Path

from core.logging import get_logger
from infrastructure.speech.tts.base import AudioChunk, StreamingTTS


logger = get_logger(__name__)

# Same voice and output format the minimal deployment proved working.
DEFAULT_AZURE_VOICE = "en-US-Harper:MAI-Voice-2"
_AZURE_OUTPUT_FORMAT = "audio-24khz-160kbitrate-mono-mp3"
_REQUEST_TIMEOUT_S = 30.0


class AzureTTSError(RuntimeError):
    pass


def _http_post_ssml(endpoint: str, data: bytes, headers: dict[str, str]) -> bytes:
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=_REQUEST_TIMEOUT_S) as response:
            audio = response.read()
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace").strip()
        raise AzureTTSError(
            f"Azure Speech REST failed ({error.code}): {details}"
        ) from error
    except urllib.error.URLError as error:
        raise AzureTTSError(
            f"Azure Speech REST connection failed: {error.reason}"
        ) from error
    if not audio:
        raise AzureTTSError("Azure Speech REST returned empty audio")
    return audio


def _convert_mp3_to_pcm(audio: bytes, sample_rate: int) -> bytes:
    """Decode Azure's MP3 reply into raw mono PCM16 at the pipeline rate."""
    with tempfile.TemporaryDirectory(prefix="fipilot-azure-tts-") as directory:
        input_path = Path(directory) / "speech.mp3"
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
                str(sample_rate),
                "-ac",
                "1",
                "-f",
                "s16le",
                "pipe:1",
            ],
            capture_output=True,
            check=False,
        )
        if conversion.returncode != 0:
            details = conversion.stderr.decode("utf-8", errors="replace").strip()
            raise AzureTTSError(f"Could not convert Azure speech audio: {details}")
        pcm = conversion.stdout
    if not pcm:
        raise AzureTTSError("Azure speech audio converted to empty PCM")
    return pcm


class AzureStreamingTTS(StreamingTTS):
    """Azure Speech synthesis behind the streaming TTS seam.

    The minimal deployment proved the REST SSML flow; this adapter reuses it
    verbatim and slices the decoded PCM into fixed frames so the existing
    question-speech streamer can push them over the playback WebSocket.
    """

    def __init__(
        self,
        *,
        speech_key: str,
        speech_region: str,
        voice: str | None = None,
        sample_rate: int = 24000,
        frame_duration_ms: int = 100,
    ) -> None:
        if not speech_key or not speech_region:
            raise AzureTTSError("Azure Speech key and region are required.")
        if sample_rate <= 0 or frame_duration_ms <= 0:
            raise AzureTTSError("Sample rate and frame duration must be positive.")
        self._speech_key = speech_key
        self._speech_region = speech_region
        self._voice = voice or DEFAULT_AZURE_VOICE
        self._sample_rate = sample_rate
        self._frame_bytes = max(2, int(sample_rate * frame_duration_ms / 1000) * 2)

    async def synthesize_stream(self, text: str):
        payload = (text or "").strip()
        if not payload:
            return
        pcm = await asyncio.to_thread(self._synthesize_pcm, payload)
        for offset in range(0, len(pcm), self._frame_bytes):
            yield AudioChunk(
                bytes=pcm[offset : offset + self._frame_bytes],
                sample_rate=self._sample_rate,
            )

    def _synthesize_pcm(self, text: str) -> bytes:
        ssml = (
            "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
            "xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='vi-VN'>"
            f"<voice xml:lang='vi-VN' name='{escape(self._voice)}'>"
            f"<prosody rate='+0%'>{escape(text)}</prosody>"
            "</voice>"
            "</speak>"
        ).encode("utf-8")
        endpoint = (
            f"https://{self._speech_region}.tts.speech.microsoft.com"
            "/cognitiveservices/v1"
        )
        mp3 = _http_post_ssml(
            endpoint,
            ssml,
            {
                "Ocp-Apim-Subscription-Key": self._speech_key,
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": _AZURE_OUTPUT_FORMAT,
                "User-Agent": "fipilot",
            },
        )
        return _convert_mp3_to_pcm(mp3, self._sample_rate)
