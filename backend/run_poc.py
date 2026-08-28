import os
import sys
import hashlib
from pathlib import Path
import fitz  # pymupdf

# Thêm root path để import được các module từ backend
backend_dir = "/home/hoai/user/resource/fipilot/backend"
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from fipilot.model.llm_client import LLMClient
from pydantic import BaseModel, Field
from typing import List, Optional
import dotenv

dotenv.load_dotenv(Path(backend_dir) / ".env")

TEST_PDF_PATH = Path(backend_dir) / "test" / "CV_hoainh.docx"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

print(f"Test file exists: {TEST_PDF_PATH.exists()}")

def validate_file(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError("File not found")
    
    size = file_path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes")
        
    with open(file_path, "rb") as f:
        header = f.read(4)
        if header.startswith(b"%PDF"):
            file_type = "PDF"
        elif header.startswith(b"PK\x03\x04"):
            file_type = "DOCX"
        else:
            raise ValueError("Unsupported file type. Must be PDF or DOCX.")
            
    print(f"Validation passed: {file_type}, {size} bytes")
    return file_type, size

file_type, file_size = validate_file(TEST_PDF_PATH)

# def extract_text(file_path: Path):
#     text = ""
#     with fitz.open(file_path) as doc:
#         for page in doc:
#             text += page.get_text() + "\n"
#     return text.strip()

import pymupdf4llm

def extract_text(file_path: Path):
    md_text = pymupdf4llm.to_markdown(str(file_path))
    return md_text.strip()

def compute_hash(file_path: Path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

file_hash = compute_hash(TEST_PDF_PATH)
print(f"File Hash: {file_hash}")

resume_text = extract_text(TEST_PDF_PATH)
print(f"Extracted {len(resume_text)} characters")
print("-- Preview --\n" + resume_text[:] + "...")

MOCK_CACHE = {}

def check_cache(file_hash: str):
    if file_hash in MOCK_CACHE:
        print("Cache hit!")
        return MOCK_CACHE[file_hash]
    print("Cache miss! Need to process.")
    return None

cached_result = check_cache(file_hash)



class SkillEvidence(BaseModel):
    skill: str
    evidence: str

class CandidateProfile(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    years_experience: Optional[int] = Field(None, description="Total years of experience")
    recent_role: Optional[str] = Field(None, description="Most recent job title")
    skills: List[str] = Field(default_factory=list, description="List of technical and soft skills")
    skill_evidence: List[SkillEvidence] = Field(default_factory=list, description="Evidence for extracted skills")
    is_resume: bool = Field(..., description="True if the document is a resume, False otherwise")

def extract_profile_with_llm(text: str) -> CandidateProfile:
    llm = LLMClient()
    
    system_prompt = """
    You are an expert HR extraction system.
    Extract the candidate profile from the user's document.
    Return ONLY a valid JSON object matching this schema:
    {
      "name": "string",
      "years_experience": "integer or null",
      "recent_role": "string or null",
      "skills": ["string"],
      "skill_evidence": [{"skill": "string", "evidence": "string"}],
      "is_resume": "boolean"
    }
    If the document does not appear to be a resume/CV, set is_resume to false.
    Do NOT return markdown formatting (no ```json ... ```).
    """
    
    user_prompt = f"Document Text:\n{text[:5000]}"
    
    print("Calling LLM...")
    response_text = llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=2048)
    
    try:
        import json_repair
        parsed_json = json_repair.loads(response_text)
        return CandidateProfile(**parsed_json)
    except Exception as e:
        print(f"Error parsing LLM response: {response_text}")
        raise e

if not cached_result:
    profile = extract_profile_with_llm(resume_text)
    print(f"Extracted Name: {profile.name}")
    print(f"Is Resume: {profile.is_resume}")
    print(f"Skills: {profile.skills}")
    
    # Save to cache
    MOCK_CACHE[file_hash] = profile


import uuid

def mock_save_to_repository(candidate_profile, raw_text, file_hash):
    candidate_id = str(uuid.uuid4())
    print(f"\n[Mock Repo] Saved Candidate ID: {candidate_id}")
    print(f"[Mock Repo] Linked Profile: {candidate_profile.name}")
    print(f"[Mock Repo] Linked File Hash: {file_hash}")
    
    return {
        "candidate_id": candidate_id,
        "profile": candidate_profile.model_dump(),
        "extraction_metadata": {
            "file_hash": file_hash,
            "status": "completed"
        }
    }

final_result = mock_save_to_repository(profile, resume_text, file_hash)
print("\n--- FINAL API RESPONSE MOCK ---")
import pprint
pprint.pprint(final_result)



class InterviewConfig(BaseModel):
    role: str = Field(..., description="Role to interview for")
    level: str = Field(..., description="Seniority level (e.g., Junior, Mid, Senior)")
    duration_minutes: int = Field(30, description="Expected interview duration")

class InterviewRound(BaseModel):
    round_id: int = Field(..., description="Order of the round")
    topic: str = Field(..., description="Main topic of this round")
    target_skills: List[str] = Field(..., description="Skills to evaluate from the candidate profile")
    difficulty: str = Field(..., description="Difficulty level (e.g., Easy, Medium, Hard)")
    weight_percentage: int = Field(..., description="Importance weight out of 100%")

class InterviewPlan(BaseModel):
    rounds: List[InterviewRound] = Field(..., description="List of interview rounds")
    focus_areas: List[str] = Field(..., description="Key areas the interviewer should focus on")

def generate_interview_plan(profile: CandidateProfile, config: InterviewConfig) -> InterviewPlan:
    llm = LLMClient()
    
    system_prompt = """
    You are an expert Technical Interview Planner.
    Based on the candidate's profile and the interview configuration, generate a structured interview plan.
    The plan should be divided into logical rounds, progressing from general experience to deep technical dives.
    Only target skills that the candidate claims to have in their profile.
    
    Return ONLY a valid JSON object matching this schema:
    {
      "rounds": [
        {
          "round_id": 1,
          "topic": "string",
          "target_skills": ["string"],
          "difficulty": "string",
          "weight_percentage": 20
        }
      ],
      "focus_areas": ["string"]
    }
    Do NOT return markdown formatting (no ```json ... ```).
    """
    
    user_prompt = f"""
    Interview Config:
    Role: {config.role}
    Level: {config.level}
    Duration: {config.duration_minutes} minutes

    Candidate Profile:
    Name: {profile.name}
    Skills: {', '.join(profile.skills)}
    Recent Role: {profile.recent_role}
    Experience: {profile.years_experience} years
    """
    
    print(f"Planning interview for {config.role} ({config.level})...")
    response_text = llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=2048)
    
    import json_repair
    parsed_json = json_repair.loads(response_text)
    return InterviewPlan(**parsed_json)


# Khởi tạo cấu hình phỏng vấn
interview_config = InterviewConfig(
    role="AI Engineer (Computer Vision & LLM)",
    level="Mid-level",
    duration_minutes=45
)

# Gọi LLM tạo kịch bản dựa trên profile đã có từ phần trước
interview_blueprint = generate_interview_plan(profile, interview_config)

print("\n=== INTERVIEW BLUEPRINT ===\n")
print(f"Focus Areas: {', '.join(interview_blueprint.focus_areas)}\n")
for r in interview_blueprint.rounds:
    print(f"Round {r.round_id}: {r.topic} ({r.difficulty} - {r.weight_percentage}%)")
    print(f"  -> Target Skills: {', '.join(r.target_skills)}\n")

print("[Mock Repo] Blueprint saved to cache & DB.")
print("[Mock Repo] Response: profile_version = v1")





class QuestionGenerationResult(BaseModel):
    question_text: str = Field(..., description="The actual question to ask the candidate")
    expected_key_points: List[str] = Field(..., description="Key points expected in a good answer")

def generate_first_question(profile: CandidateProfile, first_round: InterviewRound) -> QuestionGenerationResult:
    llm = LLMClient()
    
    system_prompt = """
    You are a technical interviewer for an AI Engineering role.
    Your task is to generate the VERY FIRST technical question for the candidate based on their profile and the current interview round.
    
    IMPORTANT RULES:
    1. DO NOT include any greetings, pleasantries, or opening messages (e.g., no "Hello", no "Welcome").
    2. Get straight to the technical question.
    3. Ask exactly ONE clear, concise question related to the Target Skills.
    4. Base the context of the question on the candidate's actual experience if possible.
    5. The question_text and expected_key_points MUST be written in VIETNAMESE.
    
    Return ONLY a valid JSON object matching this schema:
    {
      "question_text": "string",
      "expected_key_points": ["string"]
    }
    Do NOT return markdown formatting (no ```json ... ```).
    """
    
    user_prompt = f"""
    Candidate Name: {profile.name}
    Candidate Experience/Skills: {', '.join(profile.skills)}
    
    Current Round Topic: {first_round.topic}
    Target Skills for this Round: {', '.join(first_round.target_skills)}
    Difficulty: {first_round.difficulty}
    """
    
    print("Calling QuestionGeneratorAgent...")
    response_text = llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=1024)
    
    import json_repair
    parsed_json = json_repair.loads(response_text)
    return QuestionGenerationResult(**parsed_json)


import uuid

# 1. Lấy Round đầu tiên từ Blueprint
first_round = interview_blueprint.rounds[0]
print(f"[Orchestrator] Starting Round 1: {first_round.topic}")

# 2. QuestionGeneratorAgent tạo câu hỏi đầu tiên (Không có Opening Message)
first_question_result = generate_first_question(profile, first_round)

# 3. Tạo Session và State
session_id = str(uuid.uuid4())
session_state = {
    "session_id": session_id,
    "status": "IN_PROGRESS",
    "current_round_id": first_round.round_id,
    "turn_count": 1
}

print("\n=== API RESPONSE (Interview Start) ===")
print(f"Session ID: {session_id}")
print("\n[AI Interviewer Asks]:")
print(f"> {first_question_result.question_text}")
print("\n[Expected Key Points (Hidden from Candidate)]:")
for pt in first_question_result.expected_key_points:
    print(f"- {pt}")



from enum import Enum

class ExpectationStatus(str, Enum):
    MET = "MET"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"

class EvidenceEvaluation(BaseModel):
    key_point: str = Field(..., description="The expected key point being evaluated")
    status: ExpectationStatus = Field(..., description="Status of the evaluation (MET, PARTIAL, MISSING)")
    evidence: Optional[str] = Field(None, description="Direct quote or proof from the answer, if any")
    reasoning: str = Field(..., description="Brief explanation of why this status was given")

class AnswerEvaluationResult(BaseModel):
    evaluations: List[EvidenceEvaluation] = Field(..., description="Evaluation for each expected key point")
    overall_assessment: str = Field(..., description="Short summary of the candidate's performance on this question")


def evaluate_answer(question: str, expected_points: List[str], candidate_answer: str) -> AnswerEvaluationResult:
    llm = LLMClient()
    system_prompt = """
    You are a strict, evidence-based technical interviewer.
    Evaluate the candidate's answer against the Expected Key Points.
    For EACH key point, you must assign a status:
    - MET: The candidate clearly and accurately addressed this with specificity.
    - PARTIAL: The candidate touched on this, but lacked depth, specificity, or examples.
    - MISSING: The candidate completely failed to address this or was incorrect.
    
    You MUST extract a direct quote (`evidence`) from the candidate's answer if the status is MET or PARTIAL.
    Do NOT guess or assume. If it's not explicitly in the answer, it's MISSING.
    
    Return ONLY a valid JSON object matching exactly this schema:
    {
      "evaluations": [
        {
          "key_point": "string (the expected key point)",
          "status": "MET" | "PARTIAL" | "MISSING",
          "evidence": "string (direct quote) or null",
          "reasoning": "string (why you gave this status)"
        }
      ],
      "overall_assessment": "string (short summary)"
    }
    Do NOT return markdown formatting.
    """
    
    user_prompt = f"""
    Question Asked: {question}
    Expected Key Points: {expected_points}
    Candidate's Answer: {candidate_answer}
    """
    
    response_text = llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=1500)
    
    import json_repair
    parsed_json = json_repair.loads(response_text)
    return AnswerEvaluationResult(**parsed_json)

def generate_followup_question(original_question: str, candidate_answer: str, missing_point: str) -> str:
    llm = LLMClient()
    system_prompt = """
    You are an adaptive AI interviewer for a Middle-level AI Engineer.\n    Here is the Knowledge Base and Evaluation Focus for this level:\n    \n    # AI Engineer - Middle Level Knowledge Depth & Evaluation

### Knowledge Depth

The candidate should:

- Deeply understand the operating mechanisms of AI algorithms and architectures.
- Analyze assumptions and limitations of each method.
- Analyze failure modes and root causes.
- Compare multiple methods under different constraints.
- Evaluate trade-offs among accuracy, latency, memory, compute and data.
- Understand the relationships among data, training, evaluation, inference and deployment.
- Analyze the impact of data quality and distribution on models.
- Understand data drift, concept drift, train-serving skew and model degradation.
- Understand calibration, uncertainty and model confidence at a theoretical level.
- Assess when a method is no longer appropriate.
- Distinguish symptoms from root causes.

### Evaluation Focus

- Analysis.
- Assumptions.
- Failure modes.
- Root causes.
- Trade-offs.
- Evaluation.
- Conditions for method selection.

---
\n\n    You must enforce these standards.
    The candidate missed or was superficial about a specific expectation in their previous answer.
    Generate a SINGLE, sharp follow-up question to probe the candidate specifically on this missing expectation.
    DO NOT repeat the original question. Just ask the follow-up directly.
    The question MUST be written in VIETNAMESE.
    Return ONLY the string of the question (no JSON, no markdown).
    """
    user_prompt = f"""
    Original Question: {original_question}
    Candidate Answer: {candidate_answer}
    Missing/Partial Expectation to Probe: {missing_point}
    """
    return llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=256).strip()


def process_answer(question_text: str, expected_points: List[str], candidate_answer: str):
    print("\n===============================================")
    print("[Ứng viên trả lời]:")
    print(f"> {candidate_answer}\n")
    
    print("--- 1. EVALUATOR AGENT CHẤM ĐIỂM (EVIDENCE-BASED) ---")
    global global_evaluation_mock
    global_evaluation_mock = evaluate_answer(question_text, expected_points, candidate_answer)
    evaluation = global_evaluation_mock
    
    missing_gaps = []
    for ev in evaluation.evaluations:
        status_map = {"MET": "[3 - Met]", "PARTIAL": "[2 - Partially Met]", "MISSING": "[1 - Not Met]"}
        status_display = status_map.get(ev.status, "[0 - Not Assessed]")
        print(f"{status_display} Tiêu chí: {ev.key_point}")
        if ev.evidence:
            print(f"    Lý do: {ev.reasoning} (Bằng chứng: '{ev.evidence}')")
        else:
            print(f"    Lý do: {ev.reasoning}")
        
        # Phân loại gap để tính toán Belief State
        if ev.status in ["MISSING", "PARTIAL"]:
            missing_gaps.append(ev.key_point)
            
    print(f"\nĐánh giá chung: {evaluation.overall_assessment}")
    
    print("\n--- 2. DECISION CONTROLLER (FOLLOW-UP) ---")
    if missing_gaps:
        # Thuật toán Information Gain: Chọn gap đầu tiên (hoặc lớn nhất) để đào sâu
        target_gap = missing_gaps[0] 
        print(f"[Policy] Phát hiện lỗ hổng. Trigger cờ FOLLOW_UP cho tiêu chí: '{target_gap}'")
        
        follow_up_q = generate_followup_question(question_text, candidate_answer, target_gap)
        print("\n[AI Interviewer Hỏi Xoáy]:")
        print(f"> {follow_up_q}")
    else:
        print("[Policy] Ứng viên đạt đủ kỳ vọng. Trigger cờ NEXT_QUESTION (Chuyển câu tiếp theo).")


# Chạy giả lập (Mock Simulation)
# Tình huống: Ứng viên trả lời rất hời hợt, thiếu chiều sâu so với câu hỏi kỹ thuật ở Bước 8

mock_candidate_answer = "Trong dự án phân tích hóa đơn, tôi đã sử dụng YOLOv12 thay vì YOLOv8 cũ vì kiến trúc mới của nó cho kết quả nhận diện Layout nhanh hơn hẳn."

process_answer(
    first_question_result.question_text, 
    first_question_result.expected_key_points, 
    mock_candidate_answer
)





def generate_coaching_feedback(evaluations: List[EvidenceEvaluation]) -> str:
    llm = LLMClient()
    
    # Lọc ra các lỗ hổng
    gaps = [ev for ev in evaluations if ev.status in [ExpectationStatus.MISSING, ExpectationStatus.PARTIAL]]
    if not gaps:
        return "Tuyệt vời! Bạn đã trả lời xuất sắc tất cả các tiêu chí."
        
    gap_descriptions = "\n".join([f"- {ev.key_point} (Lý do: {ev.reasoning})" for ev in gaps])
    
    system_prompt = """
    You are an expert AI Interview Coach.
    Based on the candidate's missing or partial gaps during the interview, write a short, constructive, and highly actionable coaching feedback block in VIETNAMESE.
    Tell the candidate exactly what they missed and how they can improve their answers in actual job interviews.
    Return ONLY the raw string of the feedback (no markdown formatting, no JSON).
    """
    
    user_prompt = f"Candidate Gaps:\n{gap_descriptions}"
    
    return llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=500).strip()


# Giả lập việc gom toàn bộ đánh giá của phiên phỏng vấn (Trong thực tế sẽ lấy từ Database)
# Ở đây ta dùng lại biến `evaluation` từ Bước 9

def generate_final_report(all_evaluations: List[EvidenceEvaluation]):
    print("===============================================")
    print("       HACKERRANK CHAKRA-STYLE SCORECARD       ")
    print("===============================================\n")
    
    # 1. Tính toán điểm số
    score_map = {"MET": 3, "PARTIAL": 2, "MISSING": 1}
    total_possible = len(all_evaluations) * 3
    total_earned = sum([score_map[ev.status] for ev in all_evaluations])
    
    # Chuẩn hóa về thang 5.0
    normalized_score = (total_earned / total_possible) * 5.0 if total_possible > 0 else 0
    
    print(f"⭐ OVERALL SCORE: {normalized_score:.1f} / 5.0\n")
    
    # 2. Báo cáo Bằng chứng (Evidence-Anchored Breakdown)
    print("🔍 EVIDENCE-ANCHORED BREAKDOWN:")
    for idx, ev in enumerate(all_evaluations, 1):
        status_map = {"MET": "[3 - Met]", "PARTIAL": "[2 - Partially Met]", "MISSING": "[1 - Not Met]"}
        status_display = status_map.get(ev.status, "[0 - Not Assessed]")
        print(f"  {idx}. {ev.key_point} {status_display}")
        if ev.evidence:
            print(f"     > Bằng chứng (Trích xuất từ Transcript): \"{ev.evidence}\"")
        else:
            print(f"     > Bằng chứng: [Không tìm thấy bằng chứng trong Transcript]")
        print(f"     > Đánh giá: {ev.reasoning}\n")
        
    # 3. Lời khuyên (Coaching Feedback)
    print("💡 ACTIONABLE COACHING FEEDBACK:")
    print("Đang phân tích lỗ hổng để sinh lời khuyên...")
    coaching_advice = generate_coaching_feedback(all_evaluations)
    print(f"> {coaching_advice}")

# Chạy hàm sinh Report với kết quả từ Câu hỏi 1 (Giả sử ta chỉ hỏi 1 câu)
# Vì ở Bước 9 ta lưu kết quả vào biến local, ta cần gọi lại hàm evaluate_answer để lấy data, 
# hoặc bạn có thể pass trực tiếp data nếu đang lưu global. Ở đây ta giả sử đã có data:
# evaluation = evaluate_answer(first_question_result.question_text, first_question_result.expected_key_points, mock_candidate_answer)
print("Bắt đầu xuất Report...\n")
if 'global_evaluation_mock' in globals():
    generate_final_report(global_evaluation_mock.evaluations)
else:
    print('Vui lòng chạy lại Cell 9 để lưu dữ liệu trước khi xuất Report!')



