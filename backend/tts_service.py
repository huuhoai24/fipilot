import io
import os
import asyncio
import tempfile
from vieneu import Vieneu

class TTSService:
    def __init__(self):
        self.model = None
        self._ensure_loaded()

    def _ensure_loaded(self):
        if self.model is None:
            # Attempt to load VieNeu-TTS on GPU first
            try:
                print("Attempting to load VieNeu-TTS on GPU...")
                self.model = Vieneu(device="cuda")
                print("VieNeu-TTS loaded successfully on GPU.")
            except Exception as cuda_err:
                print(f"Failed to load VieNeu-TTS on GPU: {cuda_err}. Falling back to CPU...")
                try:
                    self.model = Vieneu(device="cpu")
                    print("VieNeu-TTS loaded successfully on CPU.")
                except Exception as cpu_err:
                    print(f"Failed to load VieNeu-TTS on CPU: {cpu_err}")
                    self.model = None

    async def preload(self):
        pass

    async def synthesize(self, text: str, language: str = "vi") -> bytes:
        """
        Synthesize text to speech using VieNeu-TTS (GPU first, CPU fallback).
        Returns the raw audio bytes (WAV format).
        """
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
