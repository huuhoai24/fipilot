import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { PhoneOff, MoreHorizontal } from 'lucide-react';
import { api } from '@/lib/api';
import { useActiveSessionStore } from '@/store/useActiveSessionStore';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'

export function InterviewSessionPage() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const startSession = useActiveSessionStore((s) => s.startSession);
  const endActiveSession = useActiveSessionStore((s) => s.endSession);

  const role = 'Candidate';
  const name = 'Bạn';

  const [status, setStatus] = useState<string>('Connecting...');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [messages, setMessages] = useState<{sender: string, text: string}[]>([]);
  
  const wsRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const audioSourceRef = useRef<AudioBufferSourceNode | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const playbackIdRef = useRef<number>(0);

  // Đăng ký phiên này vào danh sách "đang mở" để Sidebar hiển thị sublist quay
  // lại nhanh. Không tự gỡ khi unmount — nếu người dùng điều hướng sang trang
  // khác mà chưa bấm "Kết thúc", phiên vẫn cần hiện trong sublist để quay lại
  // được; gỡ khỏi danh sách chỉ xảy ra trong endInterview() khi họ chủ động
  // kết thúc phỏng vấn.
  useEffect(() => {
    if (!sessionId) return;
    startSession({ sessionId, candidateName: name });
  }, [sessionId]);

  useEffect(() => {
    const startVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing webcam", err);
      }
    };
    startVideo();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const playAudio = async (arrayBuffer: ArrayBuffer) => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
    const ctx = audioContextRef.current;
    if (ctx.state === 'suspended') {
      await ctx.resume();
    }

    try {
      const currentPlaybackId = ++playbackIdRef.current;
      const bufferCopy = arrayBuffer.slice(0);
      const decodedData = await ctx.decodeAudioData(bufferCopy);
      
      if (currentPlaybackId !== playbackIdRef.current) return;

      const source = ctx.createBufferSource();
      source.buffer = decodedData;

      if (audioSourceRef.current) {
        try { audioSourceRef.current.stop(); } catch (e) { }
      }
      audioSourceRef.current = source;

      source.connect(ctx.destination);
      source.onended = () => {
        setIsSpeaking(false);
      };
      source.start(0);
    } catch (e) {
      console.error("Audio playback error:", e);
      setIsSpeaking(false);
    }
  };

  useEffect(() => {
    if (!sessionId) {
      setStatus('Error: Missing Session ID.');
      return;
    }
    const ws = new WebSocket(`${WS_URL}/interview/${sessionId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus('Connected');
    };

    ws.onmessage = async (event) => {
      if (typeof event.data === "string") {
        try {
          const data = JSON.parse(event.data);
          if (data.text) {
            setMessages(prev => [...prev, { sender: data.sender || 'AI', text: data.text }]);
            setTimeout(() => {
              messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
          }
          if (data.status) {
            setStatus(data.status);
            if (data.status === "ENDED") {
              if (sessionId) endActiveSession(sessionId);
              setTimeout(() => navigate(`/history/${sessionId}`), 3000);
            }
          }
        } catch (e) {
          console.error("Failed to parse text message", e);
        }
      } else {
        setIsSpeaking(true);
        const arrayBuffer = await event.data.arrayBuffer();
        playAudio(arrayBuffer);
      }
    };

    ws.onclose = () => {
      setStatus('Disconnected');
    };

    return () => {
      ws.close();
      if (audioSourceRef.current) {
        try { audioSourceRef.current.stop(); } catch (e) { }
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, [navigate, sessionId]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      
      const audioChunks: BlobPart[] = [];
      
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunks.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(audioBlob);
        }
      };

      mediaRecorder.start();
      setIsListening(true);
    } catch (err) {
      console.error("Microphone access denied or error:", err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
      setIsListening(false);
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const [isEnding, setIsEnding] = useState(false);

  const endInterview = async () => {
    if (!sessionId) return;
    setIsEnding(true);
    try {
      await api.endSession(sessionId);
      endActiveSession(sessionId);
      navigate(`/history/${sessionId}`);
    } catch (err) {
      console.error(err);
      alert("Lỗi kết nối khi đánh giá.");
      setIsEnding(false);
    }
  };

  return (
    <div className="relative h-[calc(100vh-6rem)] w-full bg-slate-900 flex overflow-hidden font-sans rounded-[1.5rem]">
      
      {/* Top Header */}
      <div className="absolute top-0 left-0 right-0 p-4 flex justify-between items-center z-10 text-white">
        <div className="text-sm font-medium opacity-70">
           {new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} | {role} Interview
        </div>
        <div className="flex space-x-3 text-sm items-center">
           <span className={`w-2 h-2 rounded-full ${status === 'Connected' || status === 'INTERVIEWING' ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
           <span className="opacity-70">{status}</span>
        </div>
      </div>

      {/* Main Video Area */}
      <div className="flex-grow relative bg-gray-900 rounded-[2rem] m-6 mt-12 overflow-hidden border border-gray-800 shadow-2xl flex items-center justify-center">
        
        {/* User Camera */}
        <video 
          ref={videoRef} 
          autoPlay 
          playsInline 
          muted 
          className="absolute inset-0 w-full h-full object-cover transform scale-x-[-1]"
        />
        
        {/* Name Overlay */}
        <div className="absolute bottom-8 left-8 flex items-center space-x-2 bg-black/30 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 shadow-lg z-10">
          <span className="text-white font-medium drop-shadow-md text-sm">
            {name} 
          </span>
          <span className="flex space-x-1 opacity-80">
             <span className="w-1 h-3 bg-white rounded-full animate-pulse"></span>
             <span className="w-1 h-4 bg-white rounded-full animate-pulse delay-75"></span>
             <span className="w-1 h-2 bg-white rounded-full animate-pulse delay-150"></span>
          </span>
        </div>

        {/* AI Avatar PiP */}
        <div className="absolute bottom-8 right-8 w-56 h-56 bg-[#2d2f33] rounded-[2rem] overflow-hidden shadow-2xl border border-gray-700 flex flex-col items-center justify-center z-10">
           <div className="w-24 h-24 rounded-full overflow-hidden border-[3px] border-gray-600 mb-3 relative bg-slate-800">
             <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex&backgroundColor=b6e3f4" alt="AI Avatar" className="w-full h-full object-cover" />
             {isSpeaking && (
               <div className="absolute inset-0 bg-indigo-500/20 animate-pulse rounded-full"></div>
             )}
           </div>
           <div className="text-white font-medium text-sm flex items-center space-x-1">
             <span>Alex</span>
             {isSpeaking && (
                <span className="flex space-x-0.5 ml-1">
                   <span className="w-1 h-1 bg-white rounded-full animate-bounce"></span>
                   <span className="w-1 h-1 bg-white rounded-full animate-bounce delay-75"></span>
                   <span className="w-1 h-1 bg-white rounded-full animate-bounce delay-150"></span>
                </span>
             )}
           </div>
           {!isSpeaking && <MoreHorizontal className="w-4 h-4 text-white/50 mt-1" />}
        </div>

        {/* Bottom Controls */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex items-center space-x-4 z-10">
           <button
              onMouseDown={startRecording}
              onMouseUp={stopRecording}
              onTouchStart={startRecording}
              onTouchEnd={stopRecording}
              className={`flex items-center space-x-2 px-6 py-3 rounded-full text-white font-medium text-sm transition-all shadow-lg backdrop-blur-md ${
                isListening ? 'bg-red-500/90 border border-red-400' : 'bg-indigo-500/90 hover:bg-indigo-500 border border-indigo-400/50'
              }`}
            >
              <span>{isListening ? 'Đang ghi âm...' : 'Giữ để Trả lời'}</span>
              <div className="w-6 h-3 bg-white/20 rounded-full ml-2 flex items-center justify-center">
                 <div className="w-1.5 h-1.5 bg-white rounded-full"></div>
              </div>
           </button>
           
           <button 
             onClick={endInterview}
             disabled={isEnding}
             className="bg-black/40 backdrop-blur-md hover:bg-red-500/90 text-white p-3 rounded-full transition-all border border-white/10 shadow-lg disabled:opacity-50"
             title="Kết thúc phỏng vấn"
           >
             <PhoneOff className="w-4 h-4" />
           </button>
        </div>
      </div>

      {/* Right Sidebar - Transcript */}
      <div className="w-[400px] bg-white m-6 ml-0 mt-12 rounded-[2rem] shadow-xl flex flex-col overflow-hidden relative">
        <div className="p-5 flex justify-center items-center">
          <h2 className="font-semibold text-gray-800 text-sm">Live Transcript</h2>
        </div>
        
        <div className="flex-grow p-6 overflow-y-auto space-y-6 flex flex-col pb-20">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-gray-400 text-sm text-center px-4">
              Nội dung hội thoại sẽ hiển thị ở đây...
            </div>
          ) : (
            messages.map((msg, idx) => {
              const isAI = msg.sender === 'AI' || msg.sender === 'Alex';
              return (
                <div key={idx} className="flex flex-col">
                  <div className="text-xs text-gray-500 mb-1.5 ml-1">
                    {isAI ? 'Alex' : name}
                  </div>
                  <div className={`p-4 rounded-[1.25rem] text-[15px] leading-relaxed max-w-[90%] ${
                    isAI 
                      ? 'bg-[#f4f4f5] text-gray-800 self-start rounded-tl-sm' 
                      : 'bg-indigo-500 text-white self-end rounded-tr-sm shadow-sm'
                  }`}>
                    <ReactMarkdown 
                      components={{
                        p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                        strong: ({node, ...props}) => <strong className="font-semibold" {...props} />
                      }}
                    >
                      {msg.text}
                    </ReactMarkdown>
                  </div>
                </div>
              );
            })
          )}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="absolute top-0 right-0 bg-yellow-400 text-black text-xs font-bold px-2 py-1 rounded-bl-lg">
           α
        </div>
      </div>
    </div>
  );
}
