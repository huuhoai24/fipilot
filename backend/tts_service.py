import io
import os
import asyncio
import tempfile
import httpx
from dotenv import load_dotenv
from vieneu import Vieneu

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class TTSService:
    def __init__(self):
        self.model = None
        self.provider = os.environ.get("TTS_PROVIDER", "local").lower()
        self.remote_model_url = os.environ.get("REMOTE_MODEL_URL", "").rstrip("/")
        self.remote_model_token = os.environ.get("REMOTE_MODEL_TOKEN", "")
        self.local_device = os.environ.get("LOCAL_TTS_DEVICE", "auto").lower()
        self.preload_enabled = os.environ.get("LOCAL_TTS_PRELOAD", "true").lower() in {"1", "true", "yes"}
        if self.provider == "local" and self.preload_enabled:
            self._ensure_loaded()

    def _ensure_loaded(self):
        if self.model is None:
            devices = ["cuda", "cpu"] if self.local_device == "auto" else [self.local_device]
            if self.local_device not in {"auto", "cuda", "cpu"}:
                devices = ["cpu"]

            for device in devices:
                try:
                    print(f"Attempting to load VieNeu-TTS on {device.upper()}...")
                    self.model = Vieneu(device=device)
                    print(f"VieNeu-TTS loaded successfully on {device.upper()}.")
                    return
                except Exception as err:
                    print(f"Failed to load VieNeu-TTS on {device.upper()}: {err}")
            self.model = None

    async def preload(self):
        if self.provider == "local":
            await asyncio.to_thread(self._ensure_loaded)

    async def synthesize(self, text: str, language: str = "vi") -> bytes:
        """
        Synthesize text to speech using VieNeu-TTS.
        Returns the raw audio bytes (WAV format).
        """
        if self.provider == "remote":
            if not self.remote_model_url:
                raise RuntimeError("REMOTE_MODEL_URL is not configured")
            headers = {}
            if self.remote_model_token:
                headers["Authorization"] = f"Bearer {self.remote_model_token}"
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    f"{self.remote_model_url}/tts",
                    json={"text": text, "language": language},
                    headers=headers,
                )
                response.raise_for_status()
                return response.content

        if self.model is None:
            self._ensure_loaded()
        if self.model is None:
            raise RuntimeError("VieNeu-TTS model is not loaded")

        try:
            print(f"Synthesizing using VieNeu-TTS: {text.encode('ascii', 'replace').decode('ascii')}")
        except Exception:
            print("Synthesizing using VieNeu-TTS...")
        
        # Run inference in a separate thread to avoid blocking the asyncio event loop
        audio = await asyncio.to_thread(self.model.infer, text)
        
        # Save to a temporary file, then read wav bytes
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            await asyncio.to_thread(self.model.save, audio, tmp_path)
            with open(tmp_path, "rb") as f:
                wav_bytes = f.read()
            return wav_bytes
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

tts_service = TTSService()
