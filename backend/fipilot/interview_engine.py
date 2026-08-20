import json

import json_repair
from pydantic import BaseModel, Field


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


class ReportEvidence(BaseModel):
    timestamp: str
    quote: str


class ReportAssessment(BaseModel):
    turn_index: int = Field(ge=0)
    raw_score: int = Field(ge=0, le=3)
    rationale: str
    evidence: list[ReportEvidence] = Field(default_factory=list)


class TechnicalReport(BaseModel):
    assessments: list[ReportAssessment]
    solutions_summary: str
    overall_assessment: str
    recommendations: str


QUESTION_SYSTEM_PROMPT = """
You are a professional technical interviewer.
Based ONLY on the candidate's project and the related knowledge topics provided,
generate one interview question and the private rubric used to evaluate that question.
Rules:
- Write all questions in Vietnamese.
- Keep each question SHORT: 1-2 sentences maximum. No long preambles.
- Adapt the technical depth to the candidate's requested experience level.
- Each question must directly reference a specific claim, technology, or metric from the project description.
- The related knowledge topics help you know what the role expects. Do not ask about unrelated topics.
- Do not fabricate details that are not in the project description.
- Keep the spoken question natural. Do not reveal the rubric, expected answer, or technical keywords.
- The rubric must evaluate only the generated question. Critical points must be concrete,
  observable technical evidence rather than keyword matches.
Return one JSON object with:
  "company": the company or project name,
  "topic": the knowledge topic this question targets,
  "question": the interview question in Vietnamese,
  "rubric": {
    "evaluation_goal": the exact capability this question evaluates in Vietnamese,
    "critical_points": 2-5 concrete points to look for in the answer,
    "met": evidence required for score 3,
    "partially_met": evidence required for score 2,
    "not_met": evidence required for score 1
  }
""".strip()


ANSWER_EVALUATION_SYSTEM_PROMPT = """
You are a strict technical interview answer evaluator. Evaluate the candidate's answer
only against the saved rubric supplied inside the question. This provisional evaluation
is used only to decide whether a follow-up is useful.

Scoring rules:
- 3 / MET: satisfies the saved `met` anchor and the important critical points.
- 2 / PARTIALLY_MET: satisfies `partially_met` but lacks depth or critical evidence.
- 1 / NOT_MET: satisfies `not_met`, is technically wrong, evasive, or fails to answer.
- 0 / NOT_ASSESSED: empty, unusable, or no relevant statement can be evaluated.
  Do not use 0 merely because an answer is weak.

Evidence rules:
- Scores 1-3 require one exact verbatim substring from the candidate answer.
- Score 0 requires an empty evidence quote.
- Judge technical meaning, not keyword overlap.

Follow-up rules:
- Ask a follow-up only when one focused probe can collect missing rubric evidence.
- Do not ask a follow-up when score is 3 or 0.
- When true, next_direction identifies exactly one missing detail in Vietnamese.
- When false, next_direction is empty.

Return a JSON object with:
  "score": integer 0-3,
  "evidence_quote": exact quote, or empty for score 0,
  "justification": concise rubric-based explanation in Vietnamese,
  "should_follow_up": boolean,
  "next_direction": one missing detail, or empty,
  "matched_points": supported critical points,
  "missing_points": unsupported critical points,
  "technical_errors": concrete technical errors.
""".strip()


REPORT_SYSTEM_PROMPT = """
You are the final technical interview Reporter. Independently evaluate every supplied
turn against the private rubric that was frozen before that question was asked.

Rules:
- Return exactly one assessment for every turn_index.
- Do not create new criteria after seeing the answer.
- Use only the candidate answer from the matching turn as evidence.
- Scores 1-3 require at least one exact verbatim quote and its supplied timestamp.
- Score 3 follows the saved `met` anchor.
- Score 2 follows `partially_met`.
- Score 1 follows `not_met`, including incorrect or evasive answers.
- Score 0 means no relevant assessable evidence; its evidence list must be empty.
- Never infer experience or knowledge that the candidate did not state.
- Write rationale and summaries in Vietnamese.

Return one JSON object with:
  "assessments": [{
    "turn_index": integer,
    "raw_score": integer 0-3,
    "rationale": string,
    "evidence": [{"timestamp": string, "quote": exact candidate quote}]
  }],
  "solutions_summary": string,
  "overall_assessment": string,
  "recommendations": string.
""".strip()


def _parse_model(raw_result: str, model_type):
    parsed = json_repair.loads(raw_result)
    return model_type.model_validate(parsed).model_dump()


def _format_topics(domain_hits: list[dict]) -> str:
    if not domain_hits:
        return "No matching knowledge topic was available. Use only the project description."
    return "\n\n".join(
        f"--- Topic {index + 1} (score {hit['score']}) ---\n{hit['path']}"
        for index, hit in enumerate(domain_hits)
    )


def generate_question(llm, project: dict, role: str, level: str, domain_hits: list[dict]) -> dict:
    user_prompt = (
        f"Target role: {role}\nExperience level: {level}\n\n"
        f"Candidate project:\n{json.dumps(project, ensure_ascii=False, indent=2)}\n\n"
        f"Related knowledge topics:\n{_format_topics(domain_hits)}\n\n"
        "Generate exactly one interview question and its private evaluation rubric."
    )
    return _parse_model(
        llm.generate_text(QUESTION_SYSTEM_PROMPT, user_prompt, max_new_tokens=1_500),
        InterviewQuestion,
    )


def evaluate_answer(llm, question: dict, answer: str) -> dict:
    user_prompt = (
        f"Question asked:\n{json.dumps(question, ensure_ascii=False, indent=2)}\n\n"
        f"Candidate's answer:\n{answer}\n\n"
        "Evaluate the answer against the saved rubric and return the JSON object."
    )
    result = _parse_model(
        llm.generate_text(
            ANSWER_EVALUATION_SYSTEM_PROMPT,
            user_prompt,
            max_new_tokens=1_200,
        ),
        AnswerEvaluation,
    )
    evidence_quote = result["evidence_quote"].strip()
    if result["score"] > 0 and (
        not evidence_quote or evidence_quote not in answer
    ):
        result.update(
            score=0,
            evidence_quote="",
            justification="Không tìm thấy bằng chứng nguyên văn hợp lệ trong câu trả lời.",
            should_follow_up=False,
            next_direction="",
        )
    elif result["score"] == 0:
        result["evidence_quote"] = ""

    result["status"] = {
        0: "NOT_ASSESSED",
        1: "NOT_MET",
        2: "PARTIALLY_MET",
        3: "MET",
    }[result["score"]]
    if result["score"] in (0, 3):
        result["should_follow_up"] = False
    if not result["should_follow_up"]:
        result["next_direction"] = ""
    return result


def generate_followup(
    llm,
    project: dict,
    role: str,
    level: str,
    domain_hits: list[dict],
    question: dict,
    answer: str,
    next_direction: str,
) -> dict:
    user_prompt = (
        f"Target role: {role}\nExperience level: {level}\n\n"
        f"Candidate project:\n{json.dumps(project, ensure_ascii=False, indent=2)}\n\n"
        f"Related knowledge topics:\n{_format_topics(domain_hits)}\n\n"
        f"Previous question: {question['question']}\n"
        f"Candidate's answer: {answer}\n"
        f"Follow-up direction: {next_direction}\n\n"
        "Generate exactly one short Vietnamese follow-up question. The question MUST probe only "
        "the supplied follow-up direction. Do not introduce a new subtopic such as data annotation, "
        "training, deployment, or optimization unless it is explicitly present in that direction. "
        "Do not repeat the previous question. Generate a new private rubric that evaluates only "
        "this follow-up. Return the question and rubric in one JSON object."
    )
    return _parse_model(
        llm.generate_text(QUESTION_SYSTEM_PROMPT, user_prompt, max_new_tokens=1_500),
        InterviewQuestion,
    )


def _empty_assessment(turn_index: int, rationale: str) -> dict:
    return {
        "turn_index": turn_index,
        "evaluation_goal": "",
        "raw_score": 0,
        "status": "NOT_ASSESSED",
        "rationale": rationale,
        "evidence": [],
    }


def _validate_report(report: dict, turns: list[dict]) -> dict:
    by_turn = {item["turn_index"]: item for item in report["assessments"]}
    assessments = []
    for turn_index, turn in enumerate(turns):
        rubric = turn["question"]["rubric"]
        assessment = by_turn.get(turn_index)
        if assessment is None:
            item = _empty_assessment(
                turn_index,
                "Reporter không trả về đánh giá cho lượt phỏng vấn này.",
            )
        else:
            answer = str(turn.get("answer", ""))
            timestamp = str(turn.get("timestamp", ""))
            valid_evidence = [
                evidence
                for evidence in assessment["evidence"]
                if evidence["timestamp"] == timestamp
                and evidence["quote"].strip()
                and evidence["quote"].strip() in answer
            ]
            raw_score = assessment["raw_score"] if valid_evidence else 0
            item = {
                "turn_index": turn_index,
                "evaluation_goal": rubric["evaluation_goal"],
                "raw_score": raw_score,
                "status": {
                    0: "NOT_ASSESSED",
                    1: "NOT_MET",
                    2: "PARTIALLY_MET",
                    3: "MET",
                }[raw_score],
                "rationale": assessment["rationale"] if valid_evidence else (
                    "Không có bằng chứng nguyên văn hợp lệ trong câu trả lời."
                ),
                "evidence": valid_evidence,
            }
        if not item["evaluation_goal"]:
            item["evaluation_goal"] = rubric["evaluation_goal"]
        assessments.append(item)

    assessed_scores = [item["raw_score"] for item in assessments if item["raw_score"] > 0]
    report["assessments"] = assessments
    report["normalized_score"] = round(
        sum(assessed_scores) / len(assessed_scores) * 5 / 3,
        2,
    ) if assessed_scores else 0.0
    report["coverage_ratio"] = round(
        len(assessed_scores) / len(turns),
        2,
    ) if turns else 0.0
    return report


def generate_report(llm, role: str, level: str, turns: list[dict]) -> dict:
    if not turns:
        return {
            "assessments": [],
            "solutions_summary": "Chưa có câu trả lời để tổng hợp.",
            "overall_assessment": "Buổi phỏng vấn chưa có đủ dữ liệu để đánh giá.",
            "recommendations": "Hãy hoàn thành ít nhất một câu hỏi phỏng vấn.",
            "normalized_score": 0.0,
            "coverage_ratio": 0.0,
        }

    transcript = [
        {
            "turn_index": index,
            "timestamp": turn.get("timestamp", ""),
            "project": turn["question"].get("project", ""),
            "topic": turn["question"].get("topic", ""),
            "question": turn["question"]["question"],
            "rubric": turn["question"]["rubric"],
            "candidate_answer": turn.get("answer", ""),
        }
        for index, turn in enumerate(turns)
    ]
    user_prompt = (
        f"Target role: {role}\nExperience level: {level}\n\n"
        f"Interview turns:\n{json.dumps(transcript, ensure_ascii=False, indent=2)}\n\n"
        "Create the final evidence-anchored technical report."
    )
    report = _parse_model(
        llm.generate_text(REPORT_SYSTEM_PROMPT, user_prompt, max_new_tokens=3_500),
        TechnicalReport,
    )
    return _validate_report(report, turns)
