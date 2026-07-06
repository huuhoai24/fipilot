# Hướng dẫn triển khai Streaming Audio (Tùy chọn)

Tài liệu này phác thảo cách nâng cấp hệ thống AI Interview Chatbot lên một mức độ "Real-time" cao hơn thông qua kỹ thuật **Streaming TTS** (Text-to-Speech).

## 1. Giới thiệu Streaming TTS là gì?

Hiện tại, hệ thống sử dụng quy trình tuần tự theo từng câu:
`STT (Hoàn tất) -> LLM (Sinh ra toàn bộ câu) -> TTS (Đọc toàn bộ câu) -> Gửi cho User`

Nếu câu trả lời của AI rất dài (ví dụ: 100 chữ), LLM có thể mất 3-4 giây để viết xong toàn bộ câu, và TTS mất thêm 2 giây để tổng hợp giọng nói. Tổng độ trễ (latency) lên tới 5-6 giây.

**Streaming TTS** phá vỡ quy trình này:
- Khi LLM đang suy nghĩ, nó sẽ "nhả" ra từng đoạn ngắn (Token/Chunk) ví dụ: *"Chào bạn,"*
- Ngay khi nhận được đoạn *"Chào bạn,"*, Backend gửi ngay cho TTS để tổng hợp âm thanh ngắn.
- Âm thanh được gửi ngay lập tức qua WebSocket cho Frontend phát lên.
- Trong lúc âm thanh đang phát, LLM tiếp tục nghĩ ra *"Hôm nay bạn thế nào?"* và quá trình lặp lại.

**Kết quả:** Độ trễ giảm xuống dưới 1 giây. Giống như bạn đang gọi điện thoại trực tiếp.

## 2. Kiến trúc Backend cho Streaming

Thay đổi luồng xử lý AI trong `ai_processing_task` (`backend/main.py`) và `ai_services.py`:

```python
# Ví dụ logic Streaming
async for chunk_text in ai_services.generate_interview_response_stream(history):
    # Gửi từng đoạn text nhỏ về Frontend (để hiển thị hiệu ứng đánh chữ - typing effect)
    await websocket.send_json({"text_chunk": chunk_text})
    
    # Tổng hợp đoạn âm thanh ngắn và gửi về Frontend
    audio_chunk = await tts_service.synthesize_stream(chunk_text)
    await websocket.send_bytes(audio_chunk)
```

## 3. Cập nhật Frontend để hỗ trợ Streaming

Frontend (`frontend/src/app/interview/page.tsx`) cũng cần thay đổi để xử lý hàng đợi âm thanh liên tiếp:

### Frontend Audio Queue (Hàng đợi phát âm thanh)

Web Audio API không thể phát nhiều đoạn âm thanh cùng lúc đè lên nhau. Cần có một Audio Queue ở Frontend:

```javascript
const audioQueue = useRef([]);
const isPlaying = useRef(false);

const playNextAudio = async () => {
  if (audioQueue.current.length === 0) {
    isPlaying.current = false;
    return;
  }
  
  isPlaying.current = true;
  const arrayBuffer = audioQueue.current.shift();
  
  const ctx = audioContextRef.current;
  const audioBuffer = await ctx.decodeAudioData(arrayBuffer);
  const source = ctx.createBufferSource();
  source.buffer = audioBuffer;
  source.connect(ctx.destination);
  
  // Khi đoạn âm thanh này kết thúc, lập tức phát đoạn tiếp theo trong Queue
  source.onended = () => playNextAudio(); 
  source.start(0);
};

// Trong ws.onmessage:
if (isBinary) {
   audioQueue.current.push(arrayBuffer);
   if (!isPlaying.current) {
       playNextAudio();
   }
}
```

## 4. Thư viện TTS hỗ trợ Streaming
Thư viện `edge-tts` mà chúng ta đang sử dụng **không hỗ trợ Streaming thực thụ (Text Streaming)** vì kiến trúc của Microsoft Edge API yêu cầu toàn bộ cụm từ hoàn chỉnh.

Để làm được Streaming TTS, bạn cần cân nhắc sử dụng:
- **Kokoro TTS (Local)**: Hỗ trợ streaming cực kỳ tốt. Pipeline trả về generator, rất dễ tích hợp.
- **ElevenLabs API**: Chuyên gia về Streaming TTS qua WebSocket.
- **OpenAI TTS API**: Hỗ trợ streaming mp3.

## 5. Kết luận
Triển khai Streaming TTS sẽ tăng độ phức tạp của code lên rất nhiều (cả Backend lẫn Frontend), nhưng mang lại trải nghiệm 5 sao (Zero-Latency). Hãy áp dụng nó ở Giai đoạn (Phase) 2 hoặc 3 của dự án khi mọi tính năng cơ bản đã chạy mượt mà.
