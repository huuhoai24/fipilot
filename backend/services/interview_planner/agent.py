from infrastructure.llm.base import BaseLLMService
from shared.schemas.candidate import CandidateProfile
from shared.schemas.interview import InterviewConfig, InterviewPlan


class InterviewPlannerAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def generate_plan(self, profile: CandidateProfile, config: InterviewConfig) -> InterviewPlan:
        system_prompt = """
You are an expert Technical Interview Planner.
Based on the candidate's profile and the interview configuration, generate a structured interview plan.
The plan should be divided into logical rounds, progressing from general experience to deep technical dives.
Only target skills that the candidate claims to have in their profile.
Use the candidate's specific project details and work experience to craft contextual, relevant rounds.
"""

        # Build rich skill evidence summary
        evidence_lines = []
        for se in profile.skill_evidence[:15]:
            evidence_str = "; ".join(se.evidence) if isinstance(se.evidence, list) else str(se.evidence)
            evidence_lines.append(f"  - {se.skill}: {evidence_str}")
        evidence_block = "\n".join(evidence_lines) if evidence_lines else "  (none)"

        # Build experience summary
        exp_lines = []
        for exp in profile.experiences:
            techs = ", ".join(exp.technologies) if exp.technologies else "N/A"
            exp_lines.append(f"  - {exp.title} at {exp.company} ({exp.start_date} ~ {exp.end_date}): {exp.description} [Tech: {techs}]")
        exp_block = "\n".join(exp_lines) if exp_lines else "  (none)"

        # Build project summary
        proj_lines = []
        for proj in profile.projects:
            techs = ", ".join(proj.technologies) if proj.technologies else "N/A"
            proj_lines.append(f"  - {proj.name} ({proj.role}): {proj.description} [Tech: {techs}]")
        proj_block = "\n".join(proj_lines) if proj_lines else "  (none)"

        user_prompt = f"""
Interview Config:
  Role: {config.role}
  Level: {config.level}
  Duration: {config.duration_minutes} minutes

Candidate Profile:
  Name: {profile.name}
  Recent Role: {profile.recent_role}
  Experience: {profile.years_experience} years
  Skills: {', '.join(profile.skills)}

Skill Evidence:
{evidence_block}

Work Experience:
{exp_block}

Projects:
{proj_block}
"""

        plan = await self.llm_service.generate_json(
            prompt=user_prompt,
            output_schema=InterviewPlan,
            system_instruction=system_prompt,
            temperature=0.7,
        )

        return plan
