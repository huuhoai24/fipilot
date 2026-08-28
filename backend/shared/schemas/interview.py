from pydantic import BaseModel, Field
from typing import List

class InterviewConfig(BaseModel):
    role: str = Field(..., description="Role to interview for")
    level: str = Field(..., description="Seniority level (e.g., Junior, Mid, Senior)")
    duration_minutes: int = Field(30, description="Expected interview duration in minutes")

class InterviewRound(BaseModel):
    round_id: int = Field(..., description="Order of the round")
    topic: str = Field(..., description="Main topic of this round")
    target_skills: List[str] = Field(..., description="Skills to evaluate from the candidate profile")
    difficulty: str = Field(..., description="Difficulty level (e.g., Easy, Medium, Hard)")
    weight_percentage: int = Field(..., description="Importance weight out of 100%")

class InterviewPlan(BaseModel):
    rounds: List[InterviewRound] = Field(..., description="List of interview rounds")
    focus_areas: List[str] = Field(..., description="Key areas the interviewer should focus on")

class InterviewPrepareRequest(BaseModel):
    candidate_id: str | None = Field(None, description="ID of the candidate resume")
    config: InterviewConfig = Field(..., description="Configuration for the interview")
    custom_description: str | None = Field(None, description="Custom job description or focus areas")

class InterviewPrepareResponse(BaseModel):
    session_id: str
    plan: InterviewPlan


# --- Interview Start schemas ---

class QuestionGenerationResult(BaseModel):
    question_text: str = Field(..., description="The technical question to ask the candidate")
    expected_key_points: List[str] = Field(..., description="Key points expected in a good answer (hidden from candidate)")


class SessionState(BaseModel):
    session_id: str
    status: str
    current_round_id: int
    turn_count: int
    follow_up_count: int = 0


class InterviewStartRequest(BaseModel):
    session_id: str = Field(..., description="Session ID returned from /interview/prepare")


class InterviewStartResponse(BaseModel):
    session_id: str
    session_state: SessionState
    question: QuestionGenerationResult
    round_info: InterviewRound

from enum import Enum
from typing import Optional

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

class InterviewTurnRequest(BaseModel):
    session_id: str
    session_state: SessionState
    current_question: QuestionGenerationResult
    answer: str
    follow_up_count: int = 0

class InterviewTurnResponse(BaseModel):
    session_state: SessionState
    evaluation: AnswerEvaluationResult
    decision: str = Field(..., description="FOLLOW_UP, NEXT_ROUND, or END_INTERVIEW")
    question: Optional[QuestionGenerationResult] = None
    round_info: Optional[InterviewRound] = None

class ReportAssessment(BaseModel):
    turn_index: int
    evaluation_goal: str
    raw_score: int
    status: str
    rationale: str
    evidence: List[dict] = Field(default_factory=list)

class ReportFeedback(BaseModel):
    overall_assessment: str
    recommendations: str
    solutions_summary: str = ""

class InterviewReportResponse(BaseModel):
    assessments: List[ReportAssessment]
    solutions_summary: str
    overall_assessment: str
    recommendations: str
    normalized_score: float
    coverage_ratio: float = 1.0

class InterviewReportRequest(BaseModel):
    session_id: str
