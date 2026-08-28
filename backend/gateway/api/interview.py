import uuid

from fastapi import APIRouter, Depends, HTTPException

from core.dependencies import (
    CurrentUser,
    get_current_user,
    get_interview_planner_agent,
    get_question_generator_agent,
    get_rag_retriever,
    get_resume_repository,
)
from fipilot.database import database_session
from fipilot.models import InterviewSession
from infrastructure.interview_knowledge.rag_mock import RagRetrieverMock
from infrastructure.repositories.postgres_repository import PostgresResumeRepository
from services.interview_planner.agent import InterviewPlannerAgent
from services.interview_planner.question_agent import QuestionGeneratorAgent
from shared.schemas.interview import (
    InterviewPlan,
    InterviewPrepareRequest,
    InterviewPrepareResponse,
    InterviewStartRequest,
    InterviewStartResponse,
    SessionState,
)
from sqlalchemy import select

router = APIRouter()


@router.post("/api/v2/interview/prepare", response_model=InterviewPrepareResponse)
async def prepare_interview(
    request: InterviewPrepareRequest,
    current_user: CurrentUser = Depends(get_current_user),
    repository: PostgresResumeRepository = Depends(get_resume_repository),
    planner_agent: InterviewPlannerAgent = Depends(get_interview_planner_agent),
):
    # 1. Fetch Candidate Profile from DB or Create Mock
    from shared.schemas.candidate import CandidateProfile
    
    profile = None
    if request.candidate_id:
        profile = repository.find_by_candidate_id(current_user.uid, request.candidate_id)
        
    if profile:
        # Validate: profile must be interview-ready
        has_evidence = (len(profile.skill_evidence) > 0 or len(profile.experiences) > 0 or len(profile.projects) > 0)
        if not profile.name or not profile.skills or not has_evidence:
            raise HTTPException(status_code=422, detail="Profile is incomplete and not ready for interview.")
    else:
        # Create a mock profile from custom_description for Custom Role interviews
        mock_skills = [s.strip() for s in (request.custom_description or "General Software Engineering").split(",")]
        profile = CandidateProfile(
            name="Anonymous Candidate",
            skills=mock_skills,
            recent_role=request.config.role,
            years_experience=0,
            specialization=request.config.role,
            projects=[],
            experiences=[],
            education="",
            skill_evidence=[]
        )

    # 3. Generate Interview Plan (Blueprint) via LLM
    try:
        plan = await planner_agent.generate_plan(profile, request.config)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate interview plan: {e}",
        )

    # 4. Persist InterviewSession to PostgreSQL
    session_id = str(uuid.uuid4())
    try:
        # Build work_experience JSONB from profile experiences
        work_exp_jsonb = [
            {
                "company": exp.company,
                "title": exp.title,
                "start_date": exp.start_date,
                "end_date": exp.end_date,
                "description": exp.description,
                "technologies": exp.technologies,
            }
            for exp in profile.experiences
        ]
        
        valid_resume_id = uuid.UUID(request.candidate_id) if request.candidate_id and repository.find_by_candidate_id(current_user.uid, request.candidate_id) else None

        with database_session() as db:
            interview_session = InterviewSession(
                id=session_id,
                client_id=uuid.UUID(current_user.uid),
                resume_id=valid_resume_id,
                role=request.config.role,
                level=request.config.level,
                custom_description=plan.model_dump_json(),  # store full blueprint
                work_experience=work_exp_jsonb,
                status="prepared",
            )
            db.add(interview_session)
            # commit happens automatically via context manager
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save interview session: {e}",
        )

    return InterviewPrepareResponse(session_id=session_id, plan=plan)

@router.post("/api/v2/interview/start", response_model=InterviewStartResponse)
async def start_interview(
    request: InterviewStartRequest,
    current_user: CurrentUser = Depends(get_current_user),
    repository: PostgresResumeRepository = Depends(get_resume_repository),
    question_agent: QuestionGeneratorAgent = Depends(get_question_generator_agent),
    rag_retriever: RagRetrieverMock = Depends(get_rag_retriever),
):
    # 1. Fetch the InterviewSession
    with database_session() as db:
        stmt = select(InterviewSession).where(
            InterviewSession.id == request.session_id,
            InterviewSession.client_id == uuid.UUID(current_user.uid)
        )
        session_row = db.scalars(stmt).first()
        
        if not session_row:
            raise HTTPException(status_code=404, detail="Interview session not found.")
            
        # 2. Parse the blueprint and candidate profile
        try:
            plan = InterviewPlan.model_validate_json(session_row.custom_description)
        except Exception:
            raise HTTPException(status_code=500, detail="Corrupted interview plan in database.")
            
        from shared.schemas.candidate import CandidateProfile
        
        if session_row.resume_id:
            profile = repository.find_by_candidate_id(current_user.uid, str(session_row.resume_id))
            if not profile:
                raise HTTPException(status_code=404, detail="Associated candidate profile not found.")
        else:
            # Reconstruct mock profile
            profile = CandidateProfile(
                name="Anonymous Candidate",
                skills=plan.focus_areas,
                recent_role=session_row.role,
                years_experience=0,
                specialization=session_row.role,
                projects=[],
                experiences=[],
                education="",
                skill_evidence=[]
            )

        # 3. Get the first round
        if not plan.rounds:
            raise HTTPException(status_code=500, detail="Interview plan has no rounds.")
        first_round = plan.rounds[0]

        # 4. RAG Retrieval for background context
        rag_context = ""
        if plan.focus_areas:
            try:
                rag_context = await rag_retriever.retrieve_for_focus_areas(plan.focus_areas, top_k=3)
            except Exception:
                pass # Fallback if RAG fails

        # 5. Generate the first question
        try:
            question_result = await question_agent.generate_question(
                profile=profile,
                round_info=first_round,
                rag_context=rag_context
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate question: {e}")

        # 6. Update session status
        session_row.status = "in_progress"
        db.add(session_row)
        # db commit is automatic on exit

    # 7. Return the result
    session_state = SessionState(
        session_id=request.session_id,
        status="in_progress",
        current_round_id=first_round.round_id,
        turn_count=1
    )

    return InterviewStartResponse(
        session_id=request.session_id,
        session_state=session_state,
        question=question_result,
        round_info=first_round
    )

from pydantic import BaseModel
from typing import List

class RagDebugRequest(BaseModel):
    focus_areas: List[str]

class RagDebugResponse(BaseModel):
    context: str

@router.post("/api/v2/debug/rag-search", response_model=RagDebugResponse)
async def debug_rag_search(
    request: RagDebugRequest,
    rag_retriever: RagRetrieverMock = Depends(get_rag_retriever),
):
    try:
        # Giới hạn top_k=3 để dễ đọc
        context = await rag_retriever.retrieve_for_focus_areas(request.focus_areas, top_k=3)
        return RagDebugResponse(context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Error: {e}")

from shared.schemas.interview import (
    InterviewTurnRequest,
    InterviewTurnResponse,
    ExpectationStatus
)
from services.interview_evaluation.evaluator_agent import EvaluatorAgent
from core.dependencies import get_evaluator_agent
from fipilot.models import InterviewTurn

@router.post("/api/v2/interview/next", response_model=InterviewTurnResponse)
async def next_interview_turn(
    request: InterviewTurnRequest,
    current_user: CurrentUser = Depends(get_current_user),
    repository: PostgresResumeRepository = Depends(get_resume_repository),
    question_agent: QuestionGeneratorAgent = Depends(get_question_generator_agent),
    evaluator_agent: EvaluatorAgent = Depends(get_evaluator_agent),
    rag_retriever: RagRetrieverMock = Depends(get_rag_retriever),
):
    with database_session() as db:
        # 1. Fetch Session
        stmt = select(InterviewSession).where(
            InterviewSession.id == request.session_id,
            InterviewSession.client_id == uuid.UUID(current_user.uid)
        )
        session_row = db.scalars(stmt).first()
        if not session_row:
            raise HTTPException(status_code=404, detail="Interview session not found.")
            
        plan = InterviewPlan.model_validate_json(session_row.custom_description)
        
        # 2. Evaluate Answer
        try:
            evaluation = await evaluator_agent.evaluate_answer(
                question_text=request.current_question.question_text,
                expected_points=request.current_question.expected_key_points,
                candidate_answer=request.answer
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Evaluation failed: {e}")
            
        # Save this turn to database (even if the next question generation fails later, but we prefer a single transaction ideally. Here we just rely on SQLAlchemy session commit at the end).
        turn = InterviewTurn(
            session_id=request.session_id,
            sequence=request.session_state.turn_count,
            question=request.current_question.model_dump(),
            answer=request.answer,
            evaluation=evaluation.model_dump()
        )
        db.add(turn)
        
        # 3. Decision Controller
        missing_gaps = [
            ev.key_point for ev in evaluation.evaluations 
            if ev.status in (ExpectationStatus.MISSING, ExpectationStatus.PARTIAL)
        ]
        
        next_decision = "NEXT_ROUND"
        target_gap = None
        
        if missing_gaps and request.follow_up_count < 2:
            next_decision = "FOLLOW_UP"
            target_gap = missing_gaps[0]
            
        # Advance State
        next_state = request.session_state.model_copy()
        next_state.turn_count += 1
        
        next_question_result = None
        next_round_info = None
        
        # 4. Generate next question
        if next_decision == "FOLLOW_UP":
            next_state.follow_up_count = request.follow_up_count + 1
            next_question_result = await question_agent.generate_followup_question(
                original_question=request.current_question.question_text,
                candidate_answer=request.answer,
                missing_point=target_gap,
                level=session_row.level
            )
            # Find the current round info to send back
            next_round_info = next((r for r in plan.rounds if r.round_id == request.session_state.current_round_id), None)
            
        else: # NEXT_ROUND
            next_state.follow_up_count = 0
            
            # Find next round
            current_idx = next((i for i, r in enumerate(plan.rounds) if r.round_id == request.session_state.current_round_id), -1)
            
            if current_idx >= 0 and current_idx + 1 < len(plan.rounds):
                next_round = plan.rounds[current_idx + 1]
                next_state.current_round_id = next_round.round_id
                next_round_info = next_round
                
                # Setup context for next round
                rag_context = ""
                if plan.focus_areas:
                    try:
                        rag_context = await rag_retriever.retrieve_for_focus_areas(plan.focus_areas, top_k=3)
                    except Exception:
                        pass
                
                # Fetch profile for the QuestionGeneratorAgent
                from shared.schemas.candidate import CandidateProfile
                if session_row.resume_id:
                    profile = repository.find_by_candidate_id(current_user.uid, str(session_row.resume_id))
                else:
                    profile = CandidateProfile(
                        name="Anonymous Candidate",
                        skills=plan.focus_areas,
                        recent_role=session_row.role,
                        years_experience=0,
                        specialization=session_row.role,
                        projects=[],
                        experiences=[],
                        education="",
                        skill_evidence=[]
                    )
                    
                next_question_result = await question_agent.generate_question(
                    profile=profile,
                    round_info=next_round,
                    rag_context=rag_context
                )
            else:
                next_decision = "END_INTERVIEW"
                session_row.status = "completed"
                next_state.status = "completed"
                db.add(session_row)

    return InterviewTurnResponse(
        session_state=next_state,
        evaluation=evaluation,
        decision=next_decision,
        question=next_question_result,
        round_info=next_round_info
    )

from shared.schemas.interview import (
    InterviewReportRequest,
    InterviewReportResponse,
    ReportAssessment,
)
from services.interview_evaluation.report_agent import ReportGeneratorAgent
from core.dependencies import get_report_agent

@router.post("/api/v2/interview/report", response_model=InterviewReportResponse)
async def generate_interview_report(
    request: InterviewReportRequest,
    current_user: CurrentUser = Depends(get_current_user),
    report_agent: ReportGeneratorAgent = Depends(get_report_agent),
):
    with database_session() as db:
        # Verify Session ownership
        stmt = select(InterviewSession).where(
            InterviewSession.id == request.session_id,
            InterviewSession.client_id == uuid.UUID(current_user.uid)
        )
        session_row = db.scalars(stmt).first()
        if not session_row:
            raise HTTPException(status_code=404, detail="Interview session not found.")
            
        # Get all turns
        turns_stmt = select(InterviewTurn).where(InterviewTurn.session_id == request.session_id).order_by(InterviewTurn.sequence.asc())
        turns = db.scalars(turns_stmt).all()
        
        if not turns:
            raise HTTPException(status_code=400, detail="No interview turns found to generate a report.")
            
        assessments = []
        all_gaps = []
        total_earned = 0
        total_possible = 0
        
        score_map = {"MET": 3, "PARTIAL": 1, "MISSING": 0}
        
        for turn in turns:
            if not turn.evaluation:
                continue
                
            eval_data = turn.evaluation.get("evaluations", [])
            for ev in eval_data:
                status = ev.get("status", "NOT_ASSESSED")
                # Calculate Math
                if status in score_map:
                    total_earned += score_map[status]
                    total_possible += 3
                    
                # Collect gaps
                if status in ["MISSING", "PARTIAL"]:
                    all_gaps.append(ev)
                    
            # Create ReportAssessment for Frontend
            # Here we map one Turn to one ReportAssessment to match V1 UI, 
            # where the 'rationale' is the overall assessment of the turn
            overall = turn.evaluation.get("overall_assessment", "")
            
            # Identify missing vs met
            turn_score = 0
            if len(eval_data) > 0:
                turn_earned = sum(score_map.get(e.get("status", "NOT_ASSESSED"), 0) for e in eval_data)
                turn_possible = len(eval_data) * 3
                turn_score = int(round((turn_earned / turn_possible) * 3))
            
            # Collect evidences
            evidence_list = []
            for e in eval_data:
                if e.get("evidence"):
                    evidence_list.append({
                        "timestamp": "N/A",  # Mock timestamp since we don't store it granularly
                        "quote": e.get("evidence")
                    })
                    
            # Determine overall turn status
            turn_status = "NOT_ASSESSED"
            if len(eval_data) > 0:
                if all(e.get("status") == "MET" for e in eval_data):
                    turn_status = "MET"
                elif any(e.get("status") == "MISSING" for e in eval_data):
                    turn_status = "NOT_MET"
                else:
                    turn_status = "PARTIALLY_MET"

            topic = turn.question.get("topic") or "Technical Evaluation" if turn.question else "Technical Evaluation"
                    
            assessments.append(ReportAssessment(
                turn_index=turn.sequence,
                evaluation_goal=topic,
                raw_score=turn_score,
                status=turn_status,
                rationale=overall,
                evidence=evidence_list
            ))
            
        # Normalize score to 5.0
        normalized_score = (total_earned / total_possible) * 5.0 if total_possible > 0 else 0.0
        
        # Generate Coaching Feedback via AI
        feedback = await report_agent.generate_coaching_feedback(all_gaps)
        
        # Mark session as completed
        session_row.status = "completed"
        db.add(session_row)
        
        response_model = InterviewReportResponse(
            assessments=assessments,
            solutions_summary=feedback.solutions_summary,
            overall_assessment=feedback.overall_assessment,
            recommendations=feedback.recommendations,
            normalized_score=round(normalized_score, 1)
        )
        
        # Save to InterviewReport table
        from fipilot.models import InterviewReport
        report_row = InterviewReport(
            session_id=request.session_id,
            content=response_model.model_dump()
        )
        db.add(report_row)
        
    return response_model
