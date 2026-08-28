from infrastructure.llm.base import BaseLLMService
from shared.schemas.candidate import CandidateProfile
from shared.schemas.interview import InterviewRound, QuestionGenerationResult


class QuestionGeneratorAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def generate_question(
        self,
        profile: CandidateProfile,
        round_info: InterviewRound,
        rag_context: str = "",
    ) -> QuestionGenerationResult:
        system_prompt = """
You are a technical interviewer for an AI Engineering role.
Your task is to generate the VERY FIRST technical question for the candidate based on their profile and the current interview round.

IMPORTANT RULES:
1. DO NOT include any greetings, pleasantries, or opening messages (e.g., no "Hello", no "Welcome").
2. Get straight to the technical question.
3. Ask exactly ONE clear, concise question related to the Target Skills.
4. Base the context of the question on the candidate's actual experience if possible.
5. If background knowledge context is provided, use it to ensure the question is technically accurate and the expected key points are grounded in real knowledge.
6. The question_text and expected_key_points MUST be written in VIETNAMESE.
"""

        # Build skill evidence summary
        evidence_lines = []
        for se in profile.skill_evidence[:10]:
            evidence_str = "; ".join(se.evidence) if isinstance(se.evidence, list) else str(se.evidence)
            evidence_lines.append(f"  - {se.skill}: {evidence_str}")
        evidence_block = "\n".join(evidence_lines) if evidence_lines else "  (none)"

        # Build project summary
        proj_lines = []
        for proj in profile.projects:
            techs = ", ".join(proj.technologies) if proj.technologies else "N/A"
            proj_lines.append(f"  - {proj.name} ({proj.role}): {proj.description} [Tech: {techs}]")
        proj_block = "\n".join(proj_lines) if proj_lines else "  (none)"

        rag_section = ""
        if rag_context and rag_context != "No background knowledge available (npz files not loaded).":
            rag_section = f"""
Background Knowledge Context (use this to ensure technical accuracy):
{rag_context}
"""

        user_prompt = f"""
Candidate Name: {profile.name}
Candidate Skills: {', '.join(profile.skills)}
Recent Role: {profile.recent_role}

Skill Evidence:
{evidence_block}

Projects:
{proj_block}

Current Round Topic: {round_info.topic}
Target Skills for this Round: {', '.join(round_info.target_skills)}
Difficulty: {round_info.difficulty}
{rag_section}
"""

        result = await self.llm_service.generate_json(
            prompt=user_prompt,
            output_schema=QuestionGenerationResult,
            system_instruction=system_prompt,
            temperature=0.7,
        )

        return result

    async def generate_followup_question(
        self,
        original_question: str,
        candidate_answer: str,
        missing_point: str,
        level: str,
    ) -> QuestionGenerationResult:
        system_prompt = f"""
        You are an adaptive AI interviewer for a {level}-level AI Engineer.
        The candidate missed or was superficial about a specific expectation in their previous answer.
        Generate a SINGLE, sharp follow-up question to probe the candidate specifically on this missing expectation.
        DO NOT repeat the original question. Just ask the follow-up directly.
        The question MUST be written in VIETNAMESE.
        """

        user_prompt = f"""
        Original Question: {original_question}
        
        Candidate Answer: {candidate_answer}
        
        Missing/Partial Expectation to Probe: {missing_point}
        """

        result = await self.llm_service.generate_json(
            prompt=user_prompt,
            output_schema=QuestionGenerationResult,
            system_instruction=system_prompt
        )
        return result
