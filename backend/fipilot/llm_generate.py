import difflib
import json
import os
import random
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

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
PASS_THRESHOLD = 6

QUESTION_SYSTEM_PROMPT = """
You are a professional technical interviewer.
Based ONLY on the candidate's project and the related knowledge topics provided, generate interview questions.
Rules:
- Write all questions in Vietnamese.
- Keep each question SHORT: 1-2 sentences maximum. No long preambles.
- Each question must directly reference a specific claim, technology, or metric from the project description
  (e.g. "Trong pipeline OCR tại MB Bank, làm sao để đạt accuracy 94-95%/paper?").
- The related knowledge topics help you know what the role expects; use them to ask about the project
  at a reasonable technical depth. Do NOT ask about topics unrelated to the project.
- Do NOT fabricate details that are not in the project description.
- Use the candidate's real company names, positions, and project descriptions.
Return a JSON array of objects, each with:
  "company": the company name of the project,
  "topic": the knowledge topic this question targets,
  "question": the interview question itself (in Vietnamese).
"""

JUDGE_SYSTEM_PROMPT = """
You are an experienced technical interviewer evaluating a candidate's answer.
Use this rubric for the candidate's level ({level}) — it defines exactly what depth
and which evaluation dimensions to judge:

{rubric}

Evaluate the answer using these criteria:
1. Technical correctness: is the answer technically accurate? Does it show real understanding, or is it vague/fabricated?
2. Depth vs rubric: does the answer meet the depth and evaluation focus defined by the rubric above for level {level}?
   Award full depth points if the answer meets that bar; do NOT require higher-level analysis.
3. Grounding: does the answer directly address the question and the candidate's own project claims, without rambling?

Score 0-10, where:
- 0-3: wrong, fabricated, or completely off-topic
- 4-5: vague, shallow, partially correct
- 6-7: correct and reasonably deep for the level
- 8-10: excellent, precise, clearly above the level bar

Be strict but fair. Do not inflate scores.
Return a JSON object with:
  "score": integer 0-10,
  "strengths": string in Vietnamese (1-2 sentences),
  "weaknesses": string in Vietnamese (1-2 sentences),
  "next_direction": string in Vietnamese, what to ask next (deeper on same topic, or move to another project).
"""


def _normalize(name: str) -> str:
    return "".join(ch.lower() for ch in name if ch.isalnum())


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


def extract_json_array(text: str):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON array found in response: {text}")
    return json.loads(match.group(0))


def extract_json_object(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in response: {text}")
    return json.loads(match.group(0))


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
        f"Return a JSON array of objects."
    )
    response = client.responses.create(
        model="gpt41mini",
        input=[
            {"role": "system", "content": QUESTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return extract_json_array(response.output_text)[0]


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
        f"Return a JSON array of objects."
    )
    response = client.responses.create(
        model="gpt41mini",
        input=[
            {"role": "system", "content": QUESTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return extract_json_array(response.output_text)[0]


def evaluate_answer(
    client: OpenAI, question: dict, answer: str, project: dict, level: str, rubric: str
) -> dict:
    user_prompt = (
        f"Question asked:\n{json.dumps(question, ensure_ascii=False, indent=2)}\n\n"
        f"Candidate's project (for grounding context):\n{json.dumps(project, ensure_ascii=False, indent=2)}\n\n"
        f"Candidate's answer:\n{answer}\n\n"
        f"Evaluate this answer and return the JSON object."
    )
    response = client.responses.create(
        model="gpt41mini",
        input=[
            {
                "role": "system",
                "content": JUDGE_SYSTEM_PROMPT.format(level=level, rubric=rubric),
            },
            {"role": "user", "content": user_prompt},
        ],
    )
    verdict = extract_json_object(response.output_text)
    verdict["pass"] = verdict["score"] >= PASS_THRESHOLD
    return verdict


REPORT_SYSTEM_PROMPT = """
You are a senior hiring manager writing the final interview report.
Input: the full interview log (each question, the candidate's answer, the judge's
score and feedback) and the level rubric. Produce the report in Vietnamese.
Return a JSON object with:
  "solutions_summary": string. For each project that was discussed, summarize the
    technical solutions the candidate actually implemented and HOW they implemented
    them (mechanisms, pipeline steps, tools). Base this ONLY on the interview log;
    do not invent details.
  "overall_assessment": string. Assess the candidate against the level rubric:
    demonstrated strengths and weaknesses during this interview.
  "verdict": string "PASS" or "FAIL" for the {level} level, with a brief justification.
  "recommendations": string. What should be probed in a next interview round, if any.
"""


def _build_interview_log(sessions: dict) -> str:
    lines = []
    for name, s in sessions.items():
        lines.append(f"### Project: {name}")
        for i, (q, a, v) in enumerate(
            zip(s["questions"], s["answers"], s["verdicts"]), start=1
        ):
            lines.append(
                f"Q{i}: {q['question']}\n"
                f"A{i}: {a}\n"
                f"Score: {v['score']}/10 ({'PASS' if v['pass'] else 'FAIL'})\n"
                f"Strengths: {v['strengths']}\n"
                f"Weaknesses: {v['weaknesses']}\n"
            )
    return "\n".join(lines)


def generate_report(client: OpenAI, sessions: dict, level: str, rubric: str) -> dict:
    log = _build_interview_log(sessions)
    response = client.responses.create(
        model="gpt41mini",
        input=[
            {"role": "system", "content": REPORT_SYSTEM_PROMPT.format(level=level)},
            {
                "role": "user",
                "content": f"Level rubric:\n{rubric}\n\nInterview log:\n{log}\n\nWrite the report and return the JSON object.",
            },
        ],
    )
    return extract_json_object(response.output_text)


load_dotenv()
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://hoai-openai-test-2026-55ac1.openai.azure.com/openai/v1/",
)

role = resume["role"]
level = resume["level"]
rubric = load_level_file(role, level)

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
        or (last_verdict["pass"] if last_verdict else True)
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
                "verdicts": [],
                "questions": [],
                "answers": [],
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
    last_answer = input("Câu trả lời của bạn: ")

    last_verdict = evaluate_answer(
        client, last_question, last_answer, current, level, rubric
    )
    s = sessions[current["name"]]
    s["verdicts"].append(last_verdict)
    s["questions"].append(last_question)
    s["answers"].append(last_answer)

    print(
        f"Score: {last_verdict['score']}/10 -> {'PASS' if last_verdict['pass'] else 'FAIL'}"
    )
    print(f"Yếu: {last_verdict['weaknesses']}\n")
    asked += 1

report = generate_report(client, sessions, level, rubric)

print("\n=== BÁO CÁO CHI TIẾT TỪNG CÂU ===")
for name, s in sessions.items():
    for i, (q, a, v) in enumerate(
        zip(s["questions"], s["answers"], s["verdicts"]), start=1
    ):
        print(f"[{name}] Q{i} ({q['topic']})")
        print(f"Q: {q['question']}")
        print(f"A: {a}")
        print(f"Score: {v['score']}/10 -> {'PASS' if v['pass'] else 'FAIL'}")
        print(f"Mạnh: {v['strengths']}")
        print(f"Yếu: {v['weaknesses']}\n")

print("=== TỔNG HỢP CUỐI BUỔI ===")
print("--- Giải pháp ứng viên đã làm và cách làm ---")
print(report["solutions_summary"])
print("\n--- Đánh giá so với level ---")
print(report["overall_assessment"])
print(f"\n--- Kết luận: {report['verdict']} ---")
print(f"--- Khuyến nghị: {report['recommendations']} ---")
