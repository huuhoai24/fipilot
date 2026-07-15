import edge_tts
import io

class TTSService:
    def __init__(self):
        print("Initializing Edge TTS...")
        self.voice = "vi-VN-HoaiMyNeural" # Giọng nữ Việt Nam chất lượng cao (miễn phí)
        print(f"Edge TTS initialized with voice: {self.voice}")

    async def synthesize(self, text: str, language: str = "vi") -> bytes:
        """
        Synthesize text to speech using edge-tts.
        Returns the raw audio bytes.
        """
        voice = "en-US-AriaNeural" if language == "en" else "vi-VN-HoaiMyNeural"
        print(f"Synthesizing ({voice}): {text}")
        
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
                
        return audio_data

tts_service = TTSService()
