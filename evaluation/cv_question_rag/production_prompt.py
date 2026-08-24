from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


def production_base_prompt(repo_root: Path, scenario: Any) -> tuple[str, str]:
    backend = repo_root / "backend"
    if str(backend) not in sys.path:
        sys.path.insert(0, str(backend))
    from services.question_generator.prompts import (
        QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
        build_question_generator_prompt,
    )
    from shared.schemas import CandidateProfile, InterviewConfig, InterviewRound

    difficulty = {
        "Intern": "easy",
        "Junior": "medium",
        "Middle": "medium",
        "Senior": "hard",
    }[scenario.level]
    profile = CandidateProfile.model_validate(scenario.candidate_profile)
    interview_round = InterviewRound(
        round_id=f"{scenario.scenario_id}-round",
        topic=scenario.target_topic,
        objective=scenario.interview_objective,
        difficulty=difficulty,
        reasoning=(
            f"Controlled M6 {scenario.question_type} at position "
            f"{scenario.question_position}"
        ),
        recommended_question_areas=[
            scenario.question_type,
            scenario.target_topic,
            *scenario.previous_questions,
        ],
        weight=1.0,
        target_skills=profile.skills[:3],
        question_budget=1,
    )
    config = InterviewConfig(
        mode="text",
        language=scenario.language,
        experience_level=scenario.level.lower(),
        duration_minutes=30,
        interview_style="technical",
        question_count=6,
        objective=scenario.interview_objective,
        interviewer_personality="professional",
    )
    return (
        build_question_generator_prompt(profile, interview_round, config),
        QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
    )

