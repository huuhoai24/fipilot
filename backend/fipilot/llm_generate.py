import difflib
import json
import os
import random
import re
from datetime import datetime
from html import escape
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

from fipilot.knowledge_index import search_domain

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "Knowledge"

resume = {
    "role": "AI Engineer",
    "level": "Junior",
    "workExperience": [
        {
            "type": "Work",
            "name": "FPT Software",
            "position": "AI & Backend Developer (Intern)",
            "jobDescription": "FPT Software Project: Estimation Tool (05/2025 - 02/2026) An AI-powered tool that assists Project Managers in estimating task effort points by analyzing sprint in- puts through an LLM pipeline via Azure OpenAI. Role: AI & Backend Developer (Intern) Engineered an LLM pipeline via Azure OpenAI (GPT) to automate sprint effort estimation for Project Managers, reducing manual estimation effort in the delivery workflow. Designed and iterated prompt engineering strategies (system prompts, context formatting, output schema enforcement) through 25 evaluation cycles to improve output consistency and PM ac- ceptance rate. Processed and structured sprint input data into a clean context pipeline for the LLM, with output parsing and quality validation logic built in Python. Technologies Used: Python, C# Sklearn, Pandas, .Net Core, CosmosDB Azure AI Foundry, Azure OpenAI Gitlab, HAPI",
        },
        {
            "type": "Project",
            "name": "Fipilot — AI-Powered Resume Analysis Pipeline",
            "position": "AI Engineer",
            "jobDescription": "Project: Fipilot — AI-Powered Resume Analysis Pipeline (05/2026 – Present) An end-to-end document AI system that parses Vietnamese CVs using YOLO-based layout detection, PyMuPDF text extraction, and LLM-based structured data extraction via Qwen/Llama. Role: AI Engineer Responsibilities: Designed and trained YOLOv12s/YOLO26s models for CV layout detection, achieving best-in-class performance across 5 model iterations. Built a fine-tuned SLM extraction pipeline (Qwen3-0.6B via LoRA/SFT) using Jinja2 prompt tem- plates and Pydantic/BAML schema constraints to parse structured JSON from Vietnamese re- sume text. Developed a hybrid interview engine combining template-based questioning with LLM-driven adaptive paraphrasing — bot reads from a curated Q&A template (~60%) while contextualizing questions to the candidate's CV projects (~40%). Technologies Used: Python, PyTorch, YOLO (v12s, 26s), PyMuPDF Qwen(SLM), Jinja2, Pydantic Git, uv , NumPy, OpenCV",
        },
        {
            "type": "Project",
            "name": "Invoice OCR System",
            "position": "AI Engineer / Research Developer",
            "jobDescription": "Project: Invoice OCR System (01/2025 – 05/2025) Research project tackling Vietnamese invoice OCR — a domain with high complexity due to mixed fonts, layouts and handwriting — benchmarked against MC-OCR competition solutions. Role: AI Engineer / Research Developer Responsibilities: Reduced invoice OCR Character Error Rate by 22%, benchmarked against competition-tier base- lines. Engineered multi-model pipeline (YOLOv11 →VietOCR →PhoBERT) with controlled fine-tuning on Vietnamese invoice datasets. Built systematic evaluation framework with bounding-box visualization for iterative model com- parison. Technologies Used: Python, PyTorch, TensorFlow YOLOv11, PhoBERT, VietOCR NumPy, OpenCV",
        },
        {
            "type": "Project",
            "name": "Scene Text Recognition",
            "position": "AI Developer",
            "jobDescription": "Project: Scene Text Recognition (05/2024 – 11/2024) A computer vision system that automatically detects and recognizes text in natural scenes — such as street signs and advertisements — using deep learning. Role: AI Developer Responsibilities: Developed a scene text recognition system for natural environments (street signs, advertise- ments) using deep learning, delivering accurate text extraction via a web-based interface. Engineered a full-stack pipeline integrating YOLOv11 detection and ResNet + Bi-LSTM + CTC ar- chitecture, with OpenCV preprocessing to handle real-world noise (perspective distortion, lighting variance). Technologies Used: Python, TensorFlow, YOLOv11 OpenCV, NumPy, Scikit-learn",
        },
    ],
}

TOP_K_DOMAIN_FILES = 3
MAX_FOLLOW_UPS = 2
INTERVIEW_GREETING = (
    "Xin chào, rất vui được gặp bạn. Rất hoan nghênh bạn đã tham gia buổi phỏng vấn. "
    "Tôi là người phỏng vấn AI của bạn ngày hôm nay. Chúng ta sẽ lần lượt trao đổi "
    "qua từng câu hỏi một."
)
SPEECH_VOICE = "en-US-Harper:MAI-Voice-2-Flash"


class QuestionRubric(BaseModel):
    evaluation_goal: str
    critical_points: list[str] = Field(min_length=1, max_length=5)
    met: str
    partially_met: str
    not_met: str


class InterviewQuestion(BaseModel):
    company: str
    topic: str
    question: str
    rubric: QuestionRubric


class AnswerEvaluation(BaseModel):
    score: int = Field(ge=0, le=3)
    evidence_quote: str
    justification: str
    should_follow_up: bool
    next_direction: str
    matched_points: list[str] = Field(default_factory=list)
    missing_points: list[str] = Field(default_factory=list)
    technical_errors: list[str] = Field(default_factory=list)


QUESTION_SYSTEM_PROMPT = """
You are a professional technical interviewer.
Based ONLY on the candidate's project and the related knowledge topics provided,
generate one interview question and the private rubric used to evaluate that question.
Rules:
- Write all questions in Vietnamese.
- Keep each question SHORT: 1-2 sentences maximum. No long preambles.
- Each question must directly reference a specific claim, technology, or metric from the project description
  (e.g. "Trong pipeline OCR tại MB Bank, làm sao để đạt accuracy 94-95%/paper?").
- The related knowledge topics help you know what the role expects; use them to ask about the project
  at a reasonable technical depth. Do NOT ask about topics unrelated to the project.
- Do NOT fabricate details that are not in the project description.
- Use the candidate's real company names, positions, and project descriptions.
- Keep the spoken question natural. Do NOT reveal the rubric, expected answer, or a list of
  technical keywords in the question.
- The rubric must evaluate only the generated question. Its critical_points must be concrete,
  observable technical evidence rather than keyword matches.
Return one JSON object with:
  "company": the company name of the project,
  "topic": the knowledge topic this question targets,
  "question": the interview question itself (in Vietnamese),
  "rubric": {
    "evaluation_goal": the exact capability this question evaluates (in Vietnamese),
    "critical_points": 2-5 concrete points to look for in the answer,
    "met": evidence required for score 3,
    "partially_met": evidence required for score 2,
    "not_met": evidence required for score 1
  }
"""

ANSWER_EVALUATION_SYSTEM_PROMPT = """
You are a strict technical interview answer evaluator. Evaluate the candidate's answer
only against the saved rubric supplied inside the question. This is a provisional
per-turn evaluation used to decide whether a follow-up is useful. The final report is
produced separately after the interview.

Scoring rules:
- 3 / MET: the answer satisfies the saved `met` anchor and provides evidence for the
  important critical points.
- 2 / PARTIALLY_MET: the answer satisfies the saved `partially_met` anchor but is
  missing concrete depth or one or more important critical points.
- 1 / NOT_MET: the answer satisfies the saved `not_met` anchor, is technically wrong,
  evasive, or fails to answer the question.
- 0 / NOT_ASSESSED: the answer is empty, unusable, or contains no relevant statement
  that can be evaluated. Do not use 0 merely because the answer is weak.

Evidence rules:
- For scores 1-3, `evidence_quote` must be one exact, verbatim substring copied from
  the candidate's answer. Never paraphrase it.
- For score 0, `evidence_quote` must be empty.
- Judge meaning, not keyword overlap. Accept technically valid alternatives allowed by
  the question even when they use different terminology.

Follow-up rules:
- Set `should_follow_up` to true only when one focused follow-up can collect missing
  evidence from this rubric.
- Set it to false when the answer already meets the rubric or when no useful focused
  probe remains.
- When true, `next_direction` must describe exactly one missing detail in Vietnamese.
- When false, `next_direction` must be an empty string.

Return a JSON object with:
  "score": integer 0-3,
  "evidence_quote": exact quote from the candidate answer, or empty for score 0,
  "justification": concise explanation in Vietnamese tied to the saved rubric,
  "should_follow_up": boolean,
  "next_direction": one missing detail in Vietnamese, or empty when no follow-up,
  "matched_points": array containing critical points supported by the answer,
  "missing_points": array containing critical points not yet supported by the answer,
  "technical_errors": array of concrete technical errors found in the answer.
"""


def _normalize(name: str) -> str:
    return "".join(ch.lower() for ch in name if ch.isalnum())


def speak_text(text: str, rate: str | None = None) -> None:
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    if not speech_key or not speech_region:
        raise RuntimeError(
            "Thiếu AZURE_SPEECH_KEY hoặc AZURE_SPEECH_REGION trong biến môi trường."
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    spoken_text = escape(text)
    if rate:
        spoken_text = f"<prosody rate='{rate}'>{spoken_text}</prosody>"

    ssml = (
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
        "xmlns:mstts='http://www.w3.org/2001/mstts' "
        "xml:lang='vi-VN'>"
        f"<voice xml:lang='vi-VN' name='{SPEECH_VOICE}'>"
        f"{spoken_text}"
        "</voice>"
        "</speak>"
    )
    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        cancellation = result.cancellation_details
        raise RuntimeError(
            f"Azure Speech không thể phát nội dung: {cancellation.reason}. "
            f"{cancellation.error_details or ''}".strip()
        )


def load_level_file(role: str, level: str) -> str:
    candidates = sorted(
        d.name for d in (KNOWLEDGE_DIR / "Levels").iterdir() if d.is_dir()
    )
    norm_candidates = [_normalize(c) for c in candidates]
    match = difflib.get_close_matches(
        _normalize(role), norm_candidates, n=1, cutoff=0.7
    )
    if not match:
        raise ValueError(
            f"Cannot resolve role '{role}' to any Levels folder. Available: {candidates}"
        )
    level_dir = KNOWLEDGE_DIR / "Levels" / candidates[norm_candidates.index(match[0])]
    for f in level_dir.iterdir():
        if f.stem.lower() == level.lower():
            return f.read_text()
    raise ValueError(
        f"No level file for '{level}' in {level_dir}. Available: {[f.stem for f in level_dir.iterdir()]}"
    )


def extract_json_object(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in response: {text}")
    return json.loads(match.group(0))


def _parse_interview_question(text: str) -> dict:
    question = InterviewQuestion.model_validate(extract_json_object(text))
    return question.model_dump()


def _format_topics(domain_hits: list) -> str:
    return "\n\n".join(
        f"--- Topic {i + 1} (score {hit['score']}) ---\n{hit['path']}"
        for i, hit in enumerate(domain_hits)
    )


def generate_question(
    client: OpenAI, project: dict, role: str, domain_hits: list
) -> dict:
    related_topics = _format_topics(domain_hits)
    user_prompt = (
        f"Candidate project:\n{json.dumps(project, ensure_ascii=False, indent=2)}\n\n"
        f"Related knowledge topics (from the role's knowledge base):\n{related_topics}\n\n"
        f"Generate exactly 1 interview question closely based on this project. "
        f"Generate and return its evaluation rubric in the same JSON object."
    )
    response = client.responses.create(
        model="gpt41mini",
        input=[
            {"role": "system", "content": QUESTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return _parse_interview_question(response.output_text)


def generate_followup(
    client: OpenAI,
    project: dict,
    role: str,
    domain_hits: list,
    question: dict,
    answer: str,
    next_direction: str,
) -> dict:
    related_topics = _format_topics(domain_hits)
    user_prompt = (
        f"Candidate project:\n{json.dumps(project, ensure_ascii=False, indent=2)}\n\n"
        f"Related knowledge topics (from the role's knowledge base):\n{related_topics}\n\n"
        f"Previous question: {question['question']}\n"
        f"Candidate's answer: {answer}\n"
        f"Interviewer's direction for the follow-up: {next_direction}\n\n"
        f"Generate exactly 1 follow-up interview question in Vietnamese, SHORT (1-2 sentences), "
        f"more specific and guided than the previous one (e.g. ask for concrete pipeline steps, "
        f"mechanisms, or a method comparison). Do NOT repeat the previous question. "
        f"Generate a NEW rubric that evaluates only this follow-up question. Do not copy the "
        f"entire rubric of the previous question. Return the question and rubric in one JSON object."
    )
    response = client.responses.create(
        model="gpt41mini",
        input=[
            {"role": "system", "content": QUESTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return _parse_interview_question(response.output_text)


def evaluate_answer(client: OpenAI, question: dict, answer: str) -> dict:
    user_prompt = (
        f"Question asked:\n{json.dumps(question, ensure_ascii=False, indent=2)}\n\n"
        f"Candidate's answer:\n{answer}\n\n"
        "Evaluate this answer against the saved question rubric and return the JSON object."
    )
    response = client.responses.create(
        model="gpt41mini",
        input=[
            {"role": "system", "content": ANSWER_EVALUATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    evaluation = AnswerEvaluation.model_validate(
        extract_json_object(response.output_text)
    )
    result = evaluation.model_dump()

    evidence_quote = result["evidence_quote"].strip()
    if result["score"] > 0 and (
        not evidence_quote or evidence_quote not in answer
    ):
        result.update(
            score=0,
            status="NOT_ASSESSED",
            evidence_quote="",
            justification="Không tìm thấy bằng chứng nguyên văn hợp lệ trong câu trả lời.",
            should_follow_up=False,
            next_direction="",
        )
    elif result["score"] == 0:
        result["status"] = "NOT_ASSESSED"
        result["evidence_quote"] = ""
    else:
        result["status"] = {
            1: "NOT_MET",
            2: "PARTIALLY_MET",
            3: "MET",
        }[result["score"]]

    if result["score"] in (0, 3):
        result["should_follow_up"] = False

    if not result["should_follow_up"]:
        result["next_direction"] = ""

    return result


REPORT_SYSTEM_PROMPT = """
You are the Reporter Agent for a technical interview. Evaluate only the supplied
transcript against the saved rubric attached to each question. The level rubric is
background context only. Do not create new criteria after seeing the candidate's
answers, and do not infer knowledge that the candidate did not state.

For every asked question, return one expectation object with:
  "criterion": string in Vietnamese,
  "raw_score": integer 0-3,
  "status": one of "MET", "PARTIALLY_MET", "NOT_MET", "NOT_ASSESSED",
  "rationale": string in Vietnamese,
  "evidence": array of {"timestamp": string, "quote": string}.

Rules:
- Every score 1-3 requires at least one exact, verbatim quote from a candidate answer
  and its matching timestamp.
- 3: concrete mechanism, structured reasoning, project ownership, or a specific example.
- 2: relevant evidence but incomplete, generic, or missing depth/trade-offs.
- 1: evidence shows incorrect reasoning, evasion, or a vague answer to the criterion.
- 0 / NOT_ASSESSED: no relevant evidence exists. Its evidence array must be empty.
- Quotes must be copied exactly from the transcript. Never invent a quote or timestamp.
- Use the question's saved evaluation_goal as criterion and its met, partially_met,
  not_met, and critical_points as the scoring anchors.

Return a JSON object with:
  "expectations": array described above,
  "solutions_summary": string based only on the transcript,
  "overall_assessment": string based only on assessed expectations,
  "recommendations": string for the next round.
"""


def _build_interview_log(sessions: dict) -> tuple[str, dict[str, str]]:
    lines = []
    answers_by_timestamp = {}
    for name, s in sessions.items():
        lines.append(f"### Project: {name}")
        for i, (q, a, timestamp) in enumerate(
            zip(s["questions"], s["answers"], s["timestamps"]), start=1
        ):
            lines.append(
                f"[{timestamp}] Q{i}: {q['question']}\n"
                f"[{timestamp}] Saved rubric: "
                f"{json.dumps(q['rubric'], ensure_ascii=False)}\n"
                f"[{timestamp}] Candidate: {a}\n"
            )
            answers_by_timestamp[timestamp] = a
    return "\n".join(lines), answers_by_timestamp


def _validate_report_evidence(report: dict, answers_by_timestamp: dict[str, str]) -> dict:
    for expectation in report.get("expectations", []):
        valid_evidence = [
            evidence
            for evidence in expectation.get("evidence", [])
            if evidence.get("timestamp") in answers_by_timestamp
            and evidence.get("quote", "").strip()
            in answers_by_timestamp[evidence["timestamp"]]
        ]
        expectation["evidence"] = valid_evidence
        if not valid_evidence:
            expectation["raw_score"] = 0
            expectation["status"] = "NOT_ASSESSED"
            expectation["rationale"] = "Không có bằng chứng nguyên văn hợp lệ trong transcript."
        else:
            expectation["raw_score"] = max(1, min(3, int(expectation.get("raw_score", 1))))
    assessed_scores = [
        item["raw_score"]
        for item in report.get("expectations", [])
        if item["raw_score"] > 0
    ]
    report["normalized_score"] = round(
        sum(assessed_scores) / len(assessed_scores) * 5 / 3, 2
    ) if assessed_scores else 0.0
    return report


def generate_report(client: OpenAI, sessions: dict, level: str, rubric: str) -> dict:
    log, answers_by_timestamp = _build_interview_log(sessions)
    response = client.responses.create(
        model="gpt41mini",
        input=[
            {"role": "system", "content": REPORT_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Level rubric for {level}:\n{rubric}\n\nInterview transcript:\n{log}\n\nWrite the report and return the JSON object.",
            },
        ],
    )
    return _validate_report_evidence(
        extract_json_object(response.output_text), answers_by_timestamp
    )


load_dotenv()
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://hoai-openai-test-2026-55ac1.openai.azure.com/openai/v1/",
)

role = resume["role"]
level = resume["level"]
rubric = load_level_file(role, level)

print(INTERVIEW_GREETING)
speak_text(INTERVIEW_GREETING, rate="+8%")

try:
    n_total = int(input("Số câu hỏi muốn phỏng vấn: "))
except ValueError:
    n_total = 5

sessions = {}
asked = 0
current = None
follow_ups = 0
last_verdict = None
last_question = None
last_answer = None

while asked < n_total:
    if (
        current is None
        or (not last_verdict["should_follow_up"] if last_verdict else True)
        or follow_ups >= MAX_FOLLOW_UPS
    ):
        current = random.choice(resume["workExperience"])
        follow_ups = 0
        last_verdict = None
        if current["name"] not in sessions:
            sessions[current["name"]] = {
                "domain_hits": search_domain(
                    current["jobDescription"], role, TOP_K_DOMAIN_FILES
                ),
                "questions": [],
                "answers": [],
                "evaluations": [],
                "timestamps": [],
            }
        s = sessions[current["name"]]
        last_question = generate_question(client, current, role, s["domain_hits"])
        qtype = "HỎI MỚI"
    else:
        s = sessions[current["name"]]
        follow_ups += 1
        last_question = generate_followup(
            client,
            current,
            role,
            s["domain_hits"],
            last_question,
            last_answer,
            last_verdict["next_direction"],
        )
        qtype = f"FOLLOW-UP ({follow_ups}/{MAX_FOLLOW_UPS})"

    print(f"\n[{qtype}] [{current['name']}] ({last_question['topic']})")
    print(f"Q: {last_question['question']}\n")

    # Freeze the generated question and its rubric before the candidate answers.
    s = sessions[current["name"]]
    s["questions"].append(last_question)
    s["timestamps"].append(
        datetime.now().astimezone().isoformat(timespec="microseconds")
    )

    speak_text(last_question["question"])
    last_answer = input("Câu trả lời của bạn: ")

    last_verdict = evaluate_answer(client, last_question, last_answer)
    s["answers"].append(last_answer)
    s["evaluations"].append(last_verdict)

    if last_verdict["should_follow_up"]:
        print(f"Sẽ hỏi sâu thêm: {last_verdict['next_direction']}\n")
    asked += 1

report = generate_report(client, sessions, level, rubric)

print("\n=== BÁO CÁO EVIDENCE-ANCHORED ===")
print(f"Điểm chuẩn hóa: {report['normalized_score']}/5")
for expectation in report["expectations"]:
    print(
        f"\n[{expectation['raw_score']}/3 - {expectation['status']}] "
        f"{expectation['criterion']}"
    )
    print(f"Lý do: {expectation['rationale']}")
    for evidence in expectation["evidence"]:
        print(f"Bằng chứng [{evidence['timestamp']}]: \"{evidence['quote']}\"")

print("\n=== TỔNG HỢP CUỐI BUỔI ===")
print("--- Giải pháp ứng viên đã làm và cách làm ---")
print(report["solutions_summary"])
print("\n--- Đánh giá so với level ---")
print(report["overall_assessment"])
print(f"--- Khuyến nghị: {report['recommendations']} ---")
