import json
from difflib import SequenceMatcher
import re
import unicodedata

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
    score: int = Field(ge=0, le=10)
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
    raw_score: int = Field(ge=0, le=10)
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
- The retrieved knowledge is reference guidance, not a candidate claim.
- Use retrieved knowledge to choose technical depth and evaluation criteria, but never attribute it to the candidate.
- Do not ask about a retrieved topic unless it connects directly to the supplied project evidence and selected round.
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
- 10: complete and technically correct.
- 8-9: strong evidence with at most minor quality or depth limitations.
- 6-7: acceptable evidence that meets the core requirements.
- 4-5: partially correct evidence with important omissions.
- 2-3: very weak evidence.
- 0-1: incorrect or no meaningful answer. An empty/unusable answer is NOT_ASSESSED.

Mandatory semantic comparison procedure:
1. Before scoring, silently normalize the rubric and answer into language-neutral technical claims.
2. Interpret Vietnamese, English, mixed-language, missing-diacritic, and paraphrased claims equally.
3. Map each numbered canonical criterion to concrete answer evidence by technical meaning.
4. Treat the score anchors as coverage descriptions of the canonical criteria. They must not
   create hidden vocabulary requirements or new criteria.
5. Assign a lower score only when a required technical concept is absent, contradicted, or wrong
   after semantic normalization. Absence of an exact rubric word is never proof of absence.
6. Verify that matched_points and missing_points are a disjoint partition of the canonical
   critical points and contain their exact canonical text. Never invent a missing point.

Evidence rules:
- Every assessable score from 0-10 requires one exact verbatim substring from the answer.
- An empty/unusable answer uses score 0 with an empty evidence quote and is NOT_ASSESSED.
- Judge technical meaning, not keyword overlap.
- Accept semantically equivalent evidence even when Vietnamese, English, or mixed-language
  wording differs from the rubric. Do not require the candidate to repeat a rubric label.
- A concrete risk together with its mitigation can demonstrate the corresponding trade-off.
- Do not count the same concept as both matched and missing under different wording.
- Keywords without a coherent correct explanation are not evidence. Ignore unrelated terminology,
  regardless of answer length, and keep technically wrong answers in the low score band.

Follow-up rules:
- Ask a follow-up only when one focused probe can collect missing rubric evidence.
- Do not ask a follow-up when score is 10 or the answer is NOT_ASSESSED.
- When true, next_direction identifies exactly one missing detail in Vietnamese.
- When false, next_direction is empty.

Return a JSON object with:
  "score": integer 0-10,
  "evidence_quote": exact quote, or empty only when NOT_ASSESSED,
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
- Candidate facts must remain within the supplied authoritative candidate-evidence scope.
- Question wording is never candidate evidence and must not be restated as candidate history.
- Preserve project versus employment, prototype versus production, familiarity versus
  implementation, contribution versus ownership, team membership versus leadership,
  unknown duration, historical role, and proficiency scope.
- A validated NOT_ASSESSED interaction provides no strength, weakness, skill-gap, or score evidence.
- Prefer the supplied validated evaluation and final score over a new interpretation.
- Use the canonical 0-10 scale from the evaluator.
- Scores 0-10 are valid when supported by an exact verbatim quote and timestamp.
- 8-10 is strong-to-complete evidence, 6-7 meets core requirements, 4-5 is partial,
  and 0-3 is weak, incorrect, or not meaningful.
- A missing/unassessable turn is represented by omitting its assessment; do not use score 0
  as a substitute for missing data.
- Never infer experience or knowledge that the candidate did not state.
- Write rationale and summaries in Vietnamese.

Return one JSON object with:
  "assessments": [{
    "turn_index": integer,
    "raw_score": integer 0-10,
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
        (
            f"--- Retrieved knowledge {index + 1} (score {hit.get('score', 0)}) ---\n"
            f"Source: {hit.get('source') or hit.get('path') or 'unknown'}\n"
            f"Content:\n{str(hit.get('content', ''))[:1800]}"
        )
        for index, hit in enumerate(domain_hits)
    )


def _normalized_question_text(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", text))


def _semantic_text(value) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).casefold()
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = text.replace("đ", "d")
    return " ".join(re.findall(r"\w+", text))


def _contains_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    return any(re.search(rf"\b{re.escape(phrase)}\b", text) for phrase in phrases)


_QUESTION_STOP_TERMS = {
    "a", "about", "and", "approach", "ban", "bang", "cach", "candidate", "cho",
    "co", "cua", "did", "do", "evidence", "explain", "for", "from", "how", "in",
    "is", "it", "la", "lam", "mot", "nay", "of", "on", "project", "role", "scope",
    "system", "technology", "the", "this", "to", "trong", "use", "used", "using",
    "va", "ve", "what", "with", "would", "you", "your",
}


def _significant_terms(value) -> set[str]:
    return {
        term for term in _semantic_text(value).split()
        if len(term) >= 3 and term not in _QUESTION_STOP_TERMS
    }


def _comparable_terms(value) -> set[str]:
    terms = _significant_terms(value)
    return terms | {
        term[:-1]
        for term in terms
        if len(term) > 4 and term.endswith("s") and not term.endswith("ss")
    }


def _is_hypothetical_or_knowledge_question(question_text: str) -> bool:
    hypothetical = (
        "how would you", "what would you", "how might you", "suppose", "imagine",
        "ban se", "neu ban", "gia su", "theo ban", "hay de xuat",
    )
    knowledge = (
        "what do you know", "what is", "what are", "explain the concept",
        "ban biet gi", "khai niem la gi",
    )
    return _contains_phrase(question_text, hypothetical + knowledge)


def _has_experiential_premise(question_text: str) -> bool:
    return _contains_phrase(
        question_text,
        (
            "how did you", "tell me about your experience", "in your previous",
            "during your", "your experience", "you deployed", "you implemented",
            "you operated", "your role", "your system", "ban da", "ban tung",
            "kinh nghiem cua ban", "trong vai tro", "cua ban", "chung minh",
        ),
    )


def _topic_is_candidate_supported(
    result: dict,
    project: dict,
    domain_hits: list[dict],
    *,
    comparable_terms: bool = False,
) -> bool:
    term_extractor = _comparable_terms if comparable_terms else _significant_terms
    evidence_terms = term_extractor(project)
    topic_terms = term_extractor(result.get("topic"))
    question_terms = term_extractor(result.get("question"))
    if topic_terms & evidence_terms:
        return True
    for hit in domain_hits:
        knowledge_terms = term_extractor(
            f"{hit.get('source', '')} {hit.get('path', '')} {hit.get('content', '')}"
        )
        if topic_terms & knowledge_terms and evidence_terms & knowledge_terms:
            return True
    return bool(question_terms & evidence_terms) if not topic_terms else False


def _question_semantic_violations(
    result: dict,
    *,
    project: dict,
    role: str,
    domain_hits: list[dict],
    interview_round: dict | None,
    claim_mode: bool = False,
) -> list[str]:
    question_text = _semantic_text(result.get("question"))
    evidence_text = _semantic_text(json.dumps(project, ensure_ascii=False, sort_keys=True))
    hypothetical = _is_hypothetical_or_knowledge_question(question_text)
    experiential = _has_experiential_premise(question_text)
    violations: list[str] = []

    production_terms = (
        "production", "live traffic", "production incident", "enterprise usage",
        "real customers", "served customers", "moi truong production", "khach hang thuc te",
    )
    if (
        not hypothetical
        and _contains_phrase(question_text, production_terms)
        and not _contains_phrase(evidence_text, production_terms)
    ):
        violations.append("production scope is not supported by candidate evidence")

    deployment_terms = ("deploy", "deployed", "deployment", "trien khai")
    if (
        not hypothetical
        and (experiential or claim_mode)
        and _contains_phrase(question_text, deployment_terms)
        and not _contains_phrase(evidence_text, deployment_terms)
    ):
        violations.append("deployment experience is not supported by candidate evidence")

    weak_strength_terms = (
        "familiar with", "basic knowledge", "learned", "interested in", "studied",
        "learning", "read about", "lam quen", "kien thuc co ban", "hoc", "quan tam",
    )
    implementation_terms = (
        "implement", "implemented", "deploy", "deployed", "optimize", "optimized",
        "operate", "operated", "architect", "architected", "design", "designed",
        "build", "built", "manage", "managed", "use", "used",
        "trien khai", "toi uu", "van hanh",
        "kien truc", "thiet ke", "xay dung", "quan ly",
    )
    if (
        not hypothetical
        and _contains_phrase(evidence_text, weak_strength_terms)
        and _contains_phrase(question_text, implementation_terms)
    ):
        violations.append("knowledge or familiarity is promoted to implementation experience")

    limited_contribution_terms = (
        "assisted", "contributed", "supported", "participated", "helped",
        "ho tro", "tham gia", "dong gop",
    )
    ownership_terms = (
        "owned", "architected", "led", "managed", "responsible for the entire",
        "architect the entire", "solely", "entire system", "lead the team",
        "manage engineers", "tu thiet ke", "kien truc toan bo", "mot minh",
        "toan bo", "lanh dao", "quan ly ky su", "ca nhan thuc hien",
    )
    if (
        not hypothetical
        and _contains_phrase(evidence_text, limited_contribution_terms)
        and _contains_phrase(question_text, ownership_terms)
    ):
        violations.append("limited contribution is promoted to ownership")

    team_terms = ("team project", "worked with a team", "team member", "du an nhom", "lam viec nhom")
    if claim_mode:
        team_terms += ("member of", "project team", "thanh vien nhom")
    leadership_evidence_terms = (
        "team lead", "led the team", "managed engineers", "engineering manager",
        "lanh dao nhom", "truong nhom", "quan ly ky su",
    )
    if (
        not hypothetical
        and _contains_phrase(evidence_text, team_terms)
        and not _contains_phrase(evidence_text, leadership_evidence_terms)
        and _contains_phrase(question_text, ownership_terms)
    ):
        violations.append("team participation is promoted to leadership")

    duration_value = (
        r"(?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten)"
        if claim_mode
        else r"\d{1,2}"
    )
    question_years = re.findall(rf"\b({duration_value})\s*(?:years?|nam)\b", question_text)
    evidence_years = set(re.findall(rf"\b({duration_value})\s*(?:years?|nam)\b", evidence_text))
    if any(year not in evidence_years for year in question_years):
        violations.append("experience duration is not supported by candidate evidence")
    if (
        _contains_phrase(question_text, ("several years", "many years", "nhieu nam"))
        and not evidence_years
    ):
        violations.append("experience duration is unknown")

    question_metrics = re.findall(r"\b\d+(?:[.,]\d+)?\s*%", str(result.get("question", "")))
    evidence_raw = str(project)
    if any(metric.replace(" ", "") not in evidence_raw.replace(" ", "") for metric in question_metrics):
        violations.append("question metric is not supported by candidate evidence")

    reasoning = _semantic_text((interview_round or {}).get("reasoning"))
    role_terms = _significant_terms(role)
    if (
        "role mismatch" in reasoning
        and not hypothetical
        and experiential
        and role_terms
        and role_terms <= _significant_terms(result.get("question"))
    ):
        violations.append("target role is promoted to a historical candidate role")

    if claim_mode:
        professional_claim_terms = (
            "professional experience", "industry experience", "professional work",
            "industry work", "professional employment", "employed as", "worked professionally",
            "kinh nghiem chuyen nghiep", "kinh nghiem nganh", "kinh nghiem doanh nghiep",
        )
        professional_evidence_terms = (
            "type work", "professional experience", "professional work",
            "employment", "employer", "industry experience", "company role",
            "kinh nghiem chuyen nghiep", "kinh nghiem doanh nghiep",
        )
        if (
            _contains_phrase(question_text, professional_claim_terms)
            and not _contains_phrase(evidence_text, professional_evidence_terms)
        ):
            violations.append("project evidence is promoted to professional employment")

        historical_role_terms = (
            "employment", "employed", "professional role", "previous role", "worked as",
            "industry role", "vai tro truoc day", "lam viec nhu",
        )
        if (
            role_terms
            and role_terms <= _significant_terms(result.get("question"))
            and not role_terms <= _significant_terms(project)
            and _contains_phrase(question_text, historical_role_terms)
        ):
            violations.append("target role is promoted to a historical candidate role")

    if (
        not hypothetical
        and (experiential or claim_mode)
        and not _topic_is_candidate_supported(
            result,
            project,
            domain_hits,
            comparable_terms=claim_mode,
        )
    ):
        violations.append("experiential topic is not grounded in candidate evidence")
    return list(dict.fromkeys(violations))


def _report_claim_violations(
    claim: str,
    *,
    topic: str,
    candidate_evidence,
    role: str,
) -> list[str]:
    return _question_semantic_violations(
        {"question": claim, "topic": topic},
        project=candidate_evidence,
        role=role,
        domain_hits=[],
        interview_round=None,
        claim_mode=True,
    )


def _is_duplicate_question(question: str, previous_questions: list[str]) -> bool:
    normalized = _normalized_question_text(question)
    if not normalized:
        return True
    question_terms = set(normalized.split())
    for previous in previous_questions:
        previous_normalized = _normalized_question_text(previous)
        if not previous_normalized:
            continue
        previous_terms = set(previous_normalized.split())
        overlap = len(question_terms & previous_terms) / max(
            1,
            len(question_terms | previous_terms),
        )
        if (
            normalized == previous_normalized
            or SequenceMatcher(None, normalized, previous_normalized).ratio() >= 0.9
            or overlap >= 0.8
        ):
            return True
    return False


def _generate_unique_question(
    llm,
    user_prompt: str,
    previous_questions: list[str],
    semantic_validator=None,
) -> dict:
    history = json.dumps(previous_questions, ensure_ascii=False, indent=2)
    rejection_reason = ""
    for attempt in range(2):
        retry_instruction = f"\nThe previous output was rejected: {rejection_reason}. Generate a materially different, evidence-grounded question." if attempt else ""
        result = _parse_model(
            llm.generate_text(
                QUESTION_SYSTEM_PROMPT,
                f"{user_prompt}\n\nQuestions already asked:\n{history}{retry_instruction}",
                max_new_tokens=1_500,
            ),
            InterviewQuestion,
        )
        if _is_duplicate_question(result["question"], previous_questions):
            rejection_reason = "it duplicated the interview history"
            continue
        semantic_violations = semantic_validator(result) if semantic_validator else []
        if semantic_violations:
            rejection_reason = "; ".join(semantic_violations)
            continue
        if not semantic_violations:
            return result
    if rejection_reason == "it duplicated the interview history":
        raise ValueError("Question generation returned a duplicate interview question")
    raise ValueError(f"Question generation returned no acceptable interview question: {rejection_reason}")


def generate_question(
    llm,
    project: dict,
    role: str,
    level: str,
    domain_hits: list[dict],
    *,
    interview_round: dict | None = None,
    previous_questions: list[str] | None = None,
) -> dict:
    user_prompt = (
        f"Target role: {role}\nExperience level: {level}\n\n"
        f"Selected interview round:\n{json.dumps(interview_round or {}, ensure_ascii=False, indent=2)}\n\n"
        f"Candidate project:\n{json.dumps(project, ensure_ascii=False, indent=2)}\n\n"
        "The following retrieved knowledge is reference guidance, not a candidate claim.\n"
        f"Retrieved role knowledge:\n{_format_topics(domain_hits)}\n\n"
        "Generate exactly one interview question and its private evaluation rubric."
    )
    return _generate_unique_question(
        llm,
        user_prompt,
        previous_questions or [],
        semantic_validator=lambda result: _question_semantic_violations(
            result,
            project=project,
            role=role,
            domain_hits=domain_hits,
            interview_round=interview_round,
        ),
    )


def _normalized_grounding_text(value) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return re.sub(r"[^\w]+", " ", text).strip()


def _denies_assumed_experience(answer: str) -> bool:
    normalized = _semantic_text(answer)
    return _contains_phrase(
        normalized,
        (
            "i did not", "i do not have", "never used",
            "no experience", "not in production", "only used", "only studied",
            "only learned", "only contributed", "not the lead", "older version",
            "haven t used", "haven t implemented", "haven t deployed", "haven t operated",
            "have not used", "have not implemented", "have not deployed", "have not operated",
            "no longer", "was only", "it was only", "chua tung", "khong co kinh nghiem",
            "khong trien khai", "khong van hanh", "chi dung", "chi hoc", "chi tham gia",
            "khong phai truong nhom", "cv cu", "khong con", "chi la",
        ),
    )


def _validate_evaluation_score(result: dict, rubric: dict) -> str:
    canonical_points = {
        _normalized_grounding_text(point)
        for point in rubric.get("critical_points") or []
        if _normalized_grounding_text(point)
    }
    if not canonical_points:
        return ""

    matched_points = {
        _normalized_grounding_text(point)
        for point in result.get("matched_points") or []
    } & canonical_points
    missing_points = {
        _normalized_grounding_text(point)
        for point in result.get("missing_points") or []
    } & canonical_points
    technical_errors = [
        error for error in result.get("technical_errors") or [] if str(error).strip()
    ]
    raw_score = result["score"]
    full_coverage = (
        matched_points == canonical_points
        and not missing_points
    )

    if full_coverage and not technical_errors and raw_score < 8:
        result["score"] = 8
        return (
            "Raised score into the strong range because structured evidence shows full "
            "canonical coverage with no missing criteria or technical errors."
        )
    if full_coverage and technical_errors and raw_score > 7:
        result["score"] = 7
        return (
            "Clamped score below the strong range because structured evidence contains "
            "technical errors."
        )
    coverage_ratio = len(matched_points) / len(canonical_points)
    if coverage_ratio == 0:
        maximum_consistent_score = 3
    elif coverage_ratio <= 1 / 3:
        maximum_consistent_score = 5
    elif coverage_ratio < 1:
        maximum_consistent_score = 7
    else:
        maximum_consistent_score = 10
    if raw_score > maximum_consistent_score:
        result["score"] = maximum_consistent_score
        return (
            "Clamped score to the highest band supported by canonical criterion coverage."
        )
    return ""


def _evaluation_status(score: int, *, assessed: bool) -> str:
    if not assessed:
        return "NOT_ASSESSED"
    if score <= 3:
        return "NOT_MET"
    if score <= 5:
        return "PARTIALLY_MET"
    return "MET"


def evaluate_answer(
    llm,
    question: dict,
    answer: str,
    *,
    candidate_context: dict | None = None,
) -> dict:
    candidate_context = candidate_context or question.get("project_context")
    rubric = question.get("rubric") or {}
    unsupported_claims = _question_semantic_violations(
        question,
        project=candidate_context or {},
        role=str(question.get("interview_role") or ""),
        domain_hits=[],
        interview_round={"reasoning": question.get("reasoning", "")},
    ) if candidate_context else []
    candidate_correction = bool(unsupported_claims) and _denies_assumed_experience(answer)
    evaluation_contract = {
        "evaluation_goal": rubric.get("evaluation_goal", ""),
        "canonical_criteria": [
            {"criterion_id": f"CP-{index}", "canonical_text": point}
            for index, point in enumerate(rubric.get("critical_points") or [], start=1)
        ],
        "score_anchors": {
            "met": rubric.get("met", ""),
            "partially_met": rubric.get("partially_met", ""),
            "not_met": rubric.get("not_met", ""),
        },
        "semantic_evidence_policy": {
            "compare": "technical meaning across languages and paraphrases",
            "verbatim_rubric_vocabulary_required": False,
            "keyword_presence_alone_is_evidence": False,
            "anchors_may_add_hidden_criteria": False,
        },
        "premise_validation": {
            "authoritative_source": "candidate evidence from the current interview session",
            "unsupported_claims": unsupported_claims,
            "candidate_correction": candidate_correction,
            "question_text_is_candidate_evidence": False,
        },
    }
    question_context = {
        key: value for key, value in question.items() if key != "rubric"
    }
    user_prompt = (
        f"Question context:\n{json.dumps(question_context, ensure_ascii=False, indent=2)}\n\n"
        f"Saved evaluation contract:\n{json.dumps(evaluation_contract, ensure_ascii=False, indent=2)}\n\n"
        f"Candidate evidence:\n{json.dumps(candidate_context or {}, ensure_ascii=False, indent=2)}\n\n"
        f"Candidate's answer:\n{answer}\n\n"
        "First verify that the question's assumed experience is supported by the candidate evidence. "
        "If it is unsupported and the candidate denies that experience, do not treat the denial as a technical failure. "
        "Otherwise evaluate the answer against the saved rubric and return the JSON object."
    )
    result = _parse_model(
        llm.generate_text(
            ANSWER_EVALUATION_SYSTEM_PROMPT,
            user_prompt,
            max_new_tokens=1_200,
        ),
        AnswerEvaluation,
    )
    raw_llm_score = result["score"]
    correction_reason = ""
    unsupported_denial = candidate_correction
    evidence_quote = result["evidence_quote"].strip()
    if unsupported_denial:
        result.update(
            score=0,
            evidence_quote="",
            justification=(
                "The question premise is not supported by the supplied candidate evidence; "
                "the candidate's denial is not a technical failure."
            ),
            should_follow_up=False,
            next_direction="",
            matched_points=[],
            missing_points=[],
            technical_errors=[],
        )
        if raw_llm_score != 0:
            correction_reason = (
                "Corrected score because the unsupported question premise was denied; "
                "the denial is not a technical failure."
            )
    elif not evidence_quote or evidence_quote not in answer:
        result.update(
            score=0,
            evidence_quote="",
            justification="Không tìm thấy bằng chứng nguyên văn hợp lệ trong câu trả lời.",
            should_follow_up=False,
            next_direction="",
        )
        correction_reason = (
            "Corrected score because the model did not return valid verbatim answer evidence."
        )
    if not correction_reason:
        correction_reason = _validate_evaluation_score(result, rubric)
    result["raw_llm_score"] = raw_llm_score
    result["validated_score"] = result["score"]
    result["final_score"] = result["score"]
    result["score_scale"] = 10
    result["score_correction_reason"] = correction_reason
    result["status"] = _evaluation_status(
        result["score"],
        assessed=not unsupported_denial and bool(result["evidence_quote"]),
    )
    if result["score"] == 10 or result["status"] == "NOT_ASSESSED":
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
    *,
    previous_questions: list[str] | None = None,
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
    return _generate_unique_question(llm, user_prompt, previous_questions or [])


def _empty_assessment(turn_index: int, rationale: str) -> dict:
    return {
        "turn_index": turn_index,
        "evaluation_goal": "",
        "raw_score": None,
        "status": "NOT_ASSESSED",
        "rationale": rationale,
        "evidence": [],
    }


def _consistent_report_narrative(assessments: list[dict]) -> dict[str, str]:
    counts = {
        status: sum(item["status"] == status for item in assessments)
        for status in ("MET", "PARTIALLY_MET", "NOT_MET", "NOT_ASSESSED")
    }
    assessed_count = len(assessments) - counts["NOT_ASSESSED"]
    solutions_summary = (
        f"Validated {len(assessments)} rubric goals: {counts['MET']} met, "
        f"{counts['PARTIALLY_MET']} partially met, {counts['NOT_MET']} not met, "
        f"and {counts['NOT_ASSESSED']} not assessed."
    )

    if assessed_count == 0:
        overall_assessment = "There is insufficient assessable evidence for an overall conclusion."
    elif counts["MET"] == assessed_count:
        overall_assessment = "The candidate evidence met all assessed rubric goals."
    elif counts["NOT_MET"] == assessed_count:
        overall_assessment = "The candidate evidence did not meet the assessed rubric goals."
    else:
        overall_assessment = (
            "The candidate evidence shows mixed results across the assessed rubric goals."
        )
    if counts["NOT_ASSESSED"]:
        overall_assessment += (
            f" {counts['NOT_ASSESSED']} rubric goal(s) remained not assessed."
        )

    development_goals = list(dict.fromkeys(
        item["evaluation_goal"]
        for item in assessments
        if item["status"] in {"PARTIALLY_MET", "NOT_MET"}
    ))
    unassessed_goals = list(dict.fromkeys(
        item["evaluation_goal"]
        for item in assessments
        if item["status"] == "NOT_ASSESSED"
    ))
    if development_goals:
        recommendations = (
            "Review the rubric goals that were not fully met: "
            + "; ".join(development_goals[:3])
            + "."
        )
    elif unassessed_goals:
        recommendations = "No competency recommendation is made from not-assessed interactions."
    else:
        recommendations = "Maintain the demonstrated evidence across future interview rounds."
    return {
        "solutions_summary": solutions_summary,
        "overall_assessment": overall_assessment,
        "recommendations": recommendations,
    }


def _report_candidate_evidence(turn: dict, candidate_context):
    if candidate_context is not None:
        return candidate_context
    return turn.get("question", {}).get("project_context") or {}


def _validated_evaluation_assessment(
    turn_index: int,
    turn: dict,
    *,
    candidate_context,
    role: str,
) -> dict | None:
    evaluation = turn.get("evaluation")
    if not isinstance(evaluation, dict):
        return None
    if evaluation.get("status") == "NOT_ASSESSED":
        return _empty_assessment(
            turn_index,
            "This interaction was not assessed and provides no candidate competency conclusion.",
        )
    final_score = evaluation.get(
        "final_score",
        evaluation.get("validated_score", evaluation.get("score")),
    )
    if (
        isinstance(final_score, bool)
        or not isinstance(final_score, (int, float))
        or not 0 <= final_score <= 10
    ):
        return _empty_assessment(
            turn_index,
            "The saved evaluation did not contain a valid final score.",
        )
    answer = str(turn.get("answer", ""))
    evidence_quote = str(evaluation.get("evidence_quote", "")).strip()
    if not evidence_quote or evidence_quote not in answer:
        return _empty_assessment(
            turn_index,
            "The saved evaluation did not contain valid verbatim answer evidence.",
        )
    rationale = str(evaluation.get("justification", "")).strip()
    evidence_scope = {
        "session_snapshot": _report_candidate_evidence(turn, candidate_context),
        "validated_answer_evidence": evidence_quote,
    }
    if _report_claim_violations(
        rationale,
        topic=str(turn.get("question", {}).get("topic", "")),
        candidate_evidence=evidence_scope,
        role=role,
    ):
        rationale = (
            "The validated answer evidence supports the recorded rubric score without "
            "additional candidate-experience claims."
        )
    return {
        "turn_index": turn_index,
        "evaluation_goal": "",
        "raw_score": final_score,
        "status": _evaluation_status(final_score, assessed=True),
        "rationale": rationale,
        "evidence": [{"timestamp": str(turn.get("timestamp", "")), "quote": evidence_quote}],
    }


def _validate_report(
    report: dict,
    turns: list[dict],
    *,
    candidate_context=None,
    role: str = "",
) -> dict:
    by_turn = {item["turn_index"]: item for item in report["assessments"]}
    assessments = []
    for turn_index, turn in enumerate(turns):
        rubric = turn["question"]["rubric"]
        item = _validated_evaluation_assessment(
            turn_index,
            turn,
            candidate_context=candidate_context,
            role=role,
        )
        assessment = by_turn.get(turn_index)
        if item is not None:
            pass
        elif assessment is None:
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
            raw_score = assessment["raw_score"] if valid_evidence else None
            snapshot = _report_candidate_evidence(turn, candidate_context)
            unsupported_question = _question_semantic_violations(
                turn["question"],
                project=snapshot,
                role=role,
                domain_hits=[],
                interview_round={"reasoning": turn["question"].get("reasoning", "")},
            ) if snapshot else []
            unsupported_denial = bool(unsupported_question) and _denies_assumed_experience(answer)
            rationale = assessment["rationale"]
            if valid_evidence and not unsupported_denial:
                evidence_scope = {
                    "session_snapshot": snapshot,
                    "validated_answer_evidence": [evidence["quote"] for evidence in valid_evidence],
                }
                if _report_claim_violations(
                    rationale,
                    topic=str(turn["question"].get("topic", "")),
                    candidate_evidence=evidence_scope,
                    role=role,
                ):
                    rationale = (
                        "The validated answer evidence supports the recorded rubric score without "
                        "additional candidate-experience claims."
                    )
            item = {
                "turn_index": turn_index,
                "evaluation_goal": rubric["evaluation_goal"],
                "raw_score": None if unsupported_denial else raw_score,
                "status": _evaluation_status(
                    raw_score if raw_score is not None else 0,
                    assessed=raw_score is not None and not unsupported_denial,
                ),
                "rationale": (
                    "This interaction was not assessed and provides no candidate competency conclusion."
                    if unsupported_denial
                    else rationale
                ) if valid_evidence else (
                    "Không có bằng chứng nguyên văn hợp lệ trong câu trả lời."
                ),
                "evidence": [] if unsupported_denial else valid_evidence,
            }
        if not item["evaluation_goal"]:
            item["evaluation_goal"] = rubric["evaluation_goal"]
        assessments.append(item)

    component_scores = [item["raw_score"] for item in assessments]
    assessed_scores = [score for score in component_scores if score is not None]
    report["assessments"] = assessments
    report["normalized_score"] = round(
        sum(assessed_scores) / len(assessed_scores),
        2,
    ) if assessed_scores else 0.0
    report["coverage_ratio"] = round(
        len(assessed_scores) / len(turns),
        2,
    ) if turns else 0.0
    report["score_scale"] = 10
    report.update(_consistent_report_narrative(assessments))
    return report


def generate_report(
    llm,
    role: str,
    level: str,
    turns: list[dict],
    *,
    candidate_context=None,
) -> dict:
    if not turns:
        return {
            "assessments": [],
            "solutions_summary": "Chưa có câu trả lời để tổng hợp.",
            "overall_assessment": "Buổi phỏng vấn chưa có đủ dữ liệu để đánh giá.",
            "recommendations": "Hãy hoàn thành ít nhất một câu hỏi phỏng vấn.",
            "normalized_score": 0.0,
            "coverage_ratio": 0.0,
            "score_scale": 10,
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
            "authoritative_candidate_evidence": _report_candidate_evidence(
                turn,
                candidate_context,
            ),
            "validated_evaluation": turn.get("evaluation"),
            "question_wording_is_candidate_evidence": False,
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
    return _validate_report(
        report,
        turns,
        candidate_context=candidate_context,
        role=role,
    )
