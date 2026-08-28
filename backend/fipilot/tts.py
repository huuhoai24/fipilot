import os
import subprocess
import tempfile
import urllib.error
import urllib.request
from html import escape
from pathlib import Path


SPEECH_VOICE = "en-US-Harper:MAI-Voice-2"
SPEECH_OUTPUT_FORMAT = "audio-24khz-160kbitrate-mono-mp3"


def _convert_mp3_to_wav(audio: bytes) -> bytes:
    with tempfile.TemporaryDirectory(prefix="fipilot-tts-") as directory:
        input_path = Path(directory) / "speech.mp3"
        output_path = Path(directory) / "speech.wav"
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
                "24000",
                "-ac",
                "1",
                str(output_path),
            ],
            capture_output=True,
            check=False,
        )
        if conversion.returncode != 0:
            details = conversion.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"Could not convert Azure speech audio: {details}")
        return output_path.read_bytes()


def synthesize_speech(text: str, rate: str = "+0%") -> bytes:
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    if not speech_key or not speech_region:
        raise RuntimeError("Azure Speech is not configured")

    voice = os.getenv("AZURE_SPEECH_VOICE", SPEECH_VOICE)
    ssml = (
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
        "xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='vi-VN'>"
        f"<voice xml:lang='vi-VN' name='{escape(voice)}'>"
        f"<prosody rate='{escape(rate)}'>{escape(text)}</prosody>"
        "</voice>"
        "</speak>"
    ).encode("utf-8")
    endpoint = f"https://{speech_region}.tts.speech.microsoft.com/cognitiveservices/v1"
    request = urllib.request.Request(
        endpoint,
        data=ssml,
        headers={
            "Ocp-Apim-Subscription-Key": speech_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": SPEECH_OUTPUT_FORMAT,
            "User-Agent": "fipilot",
        },
        method="POST",
    )

    import http.client
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            audio = response.read()
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Azure Speech REST failed ({error.code}): {details}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Azure Speech REST connection failed: {error.reason}") from error
    except http.client.IncompleteRead as error:
        raise RuntimeError("Azure Speech REST connection interrupted") from error

    if not audio:
        raise RuntimeError("Azure Speech REST returned empty audio")
    return _convert_mp3_to_wav(audio)
