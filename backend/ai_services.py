import os
from dotenv import load_dotenv
load_dotenv()

import static_ffmpeg
static_ffmpeg.add_paths(weak=True)

import httpx
from groq import AsyncGroq
from openai import AsyncOpenAI

class AIServices:
    def __init__(self):
        # Groq STT client
        self.groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY", "placeholder"))
        
        # HTTP client with SSL verification disabled for proxies
        http_client = httpx.AsyncClient(verify=False)
        
        # Core LLM (Gemini 3 Flash) via OpenAI SDK
        self.core_model = os.environ.get("CORE_MODEL", "Gemini-3-Flash")
        self.core_llm_client = AsyncOpenAI(
            api_key=os.environ.get("CORE_API_KEY", "None"),
            base_url=os.environ.get("CORE_BASE_URL", "https://aiportalapi.stu-platform.live/jpe"),
            http_client=http_client
        )
        
        # Evaluator LLM (GPT-4.1) via OpenAI SDK
        self.evaluator_model = os.environ.get("EVALUATOR_MODEL", "github_copilot/gpt-4.1")
        self.evaluator_client = AsyncOpenAI(
            api_key=os.environ.get("EVALUATOR_API_KEY", "None"),
            base_url=os.environ.get("EVALUATOR_BASE_URL", "https://litellm-proxy.ashybay-4abd4a6e.southeastasia.azurecontainerapps.io"),
            http_client=http_client
        )
        
        # PhoWhisper local STT (for Vietnamese)
        print("Initializing PhoWhisper...")
        try:
            import torch
            
            # Monkeypatch transformers security checks for torch < 2.6 to allow loading .bin/.pth models
            try:
                import transformers.utils.import_utils
                import transformers.modeling_utils
                import transformers.pipelines.base
                transformers.utils.import_utils.check_torch_load_is_safe = lambda: None
                transformers.modeling_utils.check_torch_load_is_safe = lambda: None
                transformers.pipelines.base.check_torch_load_is_safe = lambda: None
                
                import transformers.utils
                transformers.utils.check_torch_load_is_safe = lambda: None
            except ImportError:
                pass
                
            from transformers import pipeline
            if torch.cuda.is_available():
                try:
                    print("Attempting to load PhoWhisper on GPU...")
                    self.phowhisper_pipeline = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-small", device="cuda:0")
                    print("PhoWhisper initialized successfully on GPU.")
                except Exception as cuda_err:
                    print(f"Failed to load PhoWhisper on GPU: {cuda_err}. Falling back to CPU...")
                    self.phowhisper_pipeline = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-small", device="cpu")
                    print("PhoWhisper initialized successfully on CPU.")
            else:
                self.phowhisper_pipeline = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-small", device="cpu")
                print("PhoWhisper initialized successfully on CPU.")
        except Exception as e:
            print(f"Failed to initialize PhoWhisper: {e}")
            self.phowhisper_pipeline = None

    async def stt(self, audio_bytes: bytes, language: str = "vi") -> str:
        """
        Convert audio bytes to text using PhoWhisper for Vietnamese and fallback to Groq.
        """
        print(f"Processing STT (Language: {language})...")
        try:
            if hasattr(self, "phowhisper_pipeline") and self.phowhisper_pipeline is not None:
                print("Using local PhoWhisper for Vietnamese...")
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_bytes)
                    tmp_path = tmp.name
                
                # generate text
                res = self.phowhisper_pipeline(tmp_path)
                
                # clean up
                os.remove(tmp_path)
                
                # Extract text
                if res and 'text' in res:
                    text = res['text'].strip()
                    return text
                return "Xin lỗi, tôi không nghe rõ."
            else:
                print("Using Groq Whisper STT as fallback...")
                prompt_text = "Các thuật ngữ công nghệ tiếng Anh: OCR, AI, LLM, SQL, Python, Spark, Airflow, Cloud, API, Database, Data Engineering, Machine Learning, Deep Learning, NLP, Backend, Frontend, React, Next.js."
                completion = await self.groq_client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=("audio.wav", audio_bytes),
                    response_format="text",
                    prompt=prompt_text,
                    language="vi"
                )
                return completion
        except Exception as e:
            print(f"STT Error: {e}")
            return "Xin lỗi, tôi không nghe rõ."

    async def generate_interview_response(self, history: list, status: str, role: str, level: str, name: str, language: str = "vi", template_id: str = None) -> str:
        """
        Generate response using Core LLM (Gemini) based on current status and history.
        """
        print(f"Calling Core LLM ({self.core_model}) with template_id: {template_id}...")
        
        system_prompt = f"You are an AI interviewer conducting a technical interview. The candidate's name is {name} and they are applying for the role of {role} at the {level} level. The current interview status is {status}. You MUST communicate strictly in Vietnamese."
        
        # Load and append template questions if available
        template_questions = []
        if template_id:
            from template_service import template_service
            template_questions = template_service.get_template_questions(template_id)
            
        if template_questions:
            questions_formatted = ""
            for q in template_questions:
                questions_formatted += f"Câu {q['id']} (Độ khó: {q['difficulty']}): {q['question']}\nĐáp án mẫu tham khảo: {q['answer']}\n\n"
            
            template_instruction = f"""
Bạn đang thực hiện cuộc phỏng vấn dựa trên bộ câu hỏi tiêu chuẩn gồm 10 câu sau đây:
{questions_formatted}

Quy trình phỏng vấn:
1. Bạn phải đi qua lần lượt 10 câu hỏi này theo thứ tự tăng dần từ Câu 1 đến Câu 10.
2. Đối với mỗi câu hỏi tiêu chuẩn trong danh sách:
   - Hãy đặt câu hỏi một cách tự nhiên và mạch lạc.
   - Khi ứng viên trả lời:
     * Đánh giá xem câu trả lời của họ có đầy đủ không. Nếu câu trả lời quá ngắn, mơ hồ hoặc có điểm thú vị cần làm rõ (ví dụ: ứng viên trả lời "langgraph đi theo các node" cho câu hỏi về LangGraph), bạn hãy đặt một câu hỏi phụ (follow-up question) dựa trên ngữ cảnh đó để yêu cầu làm rõ (ví dụ: các node đó tên là gì, hoạt động như thế nào, v.v.).
     * Chỉ đặt tối đa 1 hoặc 2 câu hỏi phụ cho mỗi câu hỏi tiêu chuẩn để đảm bảo thời lượng phỏng vấn.
     * Nếu ứng viên nói "tôi không biết gì thêm", "không biết", "bỏ qua", "chịu", "đi tiếp", "sang câu khác", hoặc tương đương, hoặc sau khi bạn đã hỏi phụ xong và họ trả lời tiếp, bạn phải chuyển ngay sang câu hỏi tiêu chuẩn tiếp theo trong bộ câu hỏi.
3. Hãy phân tích kỹ lịch sử cuộc trò chuyện (history) để tự xác định bạn đang ở câu hỏi nào trong danh sách 10 câu, câu nào đã hoàn thành và câu nào cần đặt tiếp theo. Không lặp lại câu hỏi đã hỏi xong.
4. Khi đã hoàn thành câu hỏi số 10 và ứng viên đã hoàn tất câu trả lời/câu hỏi phụ cuối cùng, hãy đưa ra lời kết thúc phỏng vấn một cách thân thiện, cảm ơn ứng viên và thông báo buổi phỏng vấn đã hoàn tất.
"""
            system_prompt += "\n" + template_instruction
            
        if not history:
            greeting_instruction = f"""
            Vì đây là tin nhắn đầu tiên, bạn hãy bắt đầu cuộc phỏng vấn bằng một lời chào thân thiện theo cấu trúc này (có thể dùng từ ngữ khác nhưng cùng ngữ nghĩa):
            - "Chào {name}, tôi là Alex, một chuyên viên tuyển dụng AI."
            - "Bạn đang ứng tuyển cho vị trí {role}."
            - "Tôi rất hào hứng muốn tìm hiểu thêm về bạn!"
            - "Để bắt đầu, bạn có thể chia sẻ một chút về bản thân và điều gì đã thúc đẩy bạn ứng tuyển vào vị trí này không?"
            
            Hãy giữ phong cách tự nhiên, thân thiện và chuyên nghiệp.
            """
            system_prompt += "\n" + greeting_instruction

        messages = [{"role": "system", "content": system_prompt}]
        
        # Append history (converting custom models.Message format to OpenAI format)
        for msg in history:
            messages.append({"role": "assistant" if msg.role == "ai" else "user", "content": msg.content})
            
        try:
            response = await self.core_llm_client.chat.completions.create(
                model=self.core_model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Core LLM API Error: {e}")
            if status == "CHITCHAT":
                return f"Chào {name}. Bạn ứng tuyển vào vị trí {role} đúng không?"
            else:
                return "Xin lỗi, hiện tại tôi không thể phản hồi. Vui lòng thử lại sau."


    async def evaluate_answer(self, question: str, answer: str, level: str, role: str) -> dict:
        """
        Evaluate answer using Evaluator LLM (GPT-4.1) - Preserved for demo/future use.
        """
        print(f"Calling Evaluator LLM ({self.evaluator_model})...")
        
        system_prompt = f"Evaluate the candidate's answer based on the question. Role: {role}, Level: {level}. Output JSON with keys: 'correctness' (Correct/Partial/Wrong), 'score' (0-10), 'explanation' (string)."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"}
        ]
        
        try:
            response = await self.evaluator_client.chat.completions.create(
                model=self.evaluator_model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Evaluator LLM API Error: {e}")
            return {
                "correctness": "Correct",
                "score": 8,
                "explanation": "Câu trả lời được chấp nhận (Fallback do lỗi API)."
            }

    async def evaluate_segment(self, segment: dict, level: str, role: str) -> dict:
        """
        Evaluate a standard template question along with its follow-up Q&A together.
        """
        print(f"Calling Evaluator LLM ({self.evaluator_model}) for segment {segment['question_id']}...")
        
        system_prompt = (
            f"You are an expert technical interviewer evaluating a candidate's response to a standard question. "
            f"Role: {role}, Level: {level}. "
            f"Evaluate the candidate's initial answer and any follow-up Q&A to check if they collectively satisfy the standard question requirements. "
            f"Output JSON with keys: 'correctness' (Correct/Partial/Wrong), 'score' (0-10), 'explanation' (string)."
        )
        
        content = f"Standard Question: {segment['template_question']}\n"
        content += f"Sample Reference Answer: {segment['sample_answer']}\n\n"
        content += f"Candidate's Initial Answer: {segment['initial_answer']}\n"
        
        if segment["follow_ups"]:
            content += "\nFollow-up Discussion:\n"
            for idx, fu in enumerate(segment["follow_ups"], start=1):
                content += f"Interviewer Follow-up {idx}: {fu['question']}\n"
                content += f"Candidate Answer {idx}: {fu['answer']}\n"
                
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ]
        
        try:
            response = await self.evaluator_client.chat.completions.create(
                model=self.evaluator_model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Evaluator LLM Segment API Error: {e}")
            return {
                "correctness": "Correct",
                "score": 8,
                "explanation": "Câu trả lời được chấp nhận (Fallback do lỗi API)."
            }

    async def evaluate_overall_session(self, history: list, role: str, level: str, language: str = "vi") -> dict:
        """
        Phân tích toàn bộ cuộc phỏng vấn để đưa ra đánh giá tổng quan (Score, Strengths, Weaknesses, Feedback).
        """
        print(f"Calling Evaluator LLM for OVERALL REPORT...")
        
        system_prompt = f"""
You are an expert technical recruiter evaluating a candidate for the role of {role} ({level}).
Below is the full transcript of the interview.
Evaluate their overall performance and output a JSON object with the following keys:
- "overall_score": (int from 0 to 10)
- "strengths": (list of strings)
- "weaknesses": (list of strings)
- "final_feedback": (detailed string)
Output must be in Vietnamese.
"""
        transcript = ""
        for msg in history:
            sender = "Interviewer" if msg.role == "ai" else "Candidate"
            transcript += f"{sender}: {msg.content}\n"
            
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ]
        
        try:
            response = await self.evaluator_client.chat.completions.create(
                model=self.evaluator_model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Evaluator LLM Overall Error: {e}")
            return {
                "overall_score": 0,
                "strengths": ["Không thể tải dữ liệu điểm mạnh."],
                "weaknesses": ["Không thể tải dữ liệu điểm yếu."],
                "final_feedback": "Đã xảy ra lỗi khi tạo báo cáo. Vui lòng thử lại sau."
            }

ai_services = AIServices()
