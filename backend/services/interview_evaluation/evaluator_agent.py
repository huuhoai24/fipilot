from typing import List
from infrastructure.llm.base import BaseLLMService
from shared.schemas.interview import AnswerEvaluationResult

class EvaluatorAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def evaluate_answer(
        self,
        question_text: str,
        expected_points: List[str],
        candidate_answer: str,
    ) -> AnswerEvaluationResult:
        system_prompt = """
        You are a strict, evidence-based technical interviewer.
        Evaluate the candidate's answer against the Expected Key Points.
        For EACH key point, you must assign a status:
        - MET: The candidate clearly and accurately addressed this with specificity.
        - PARTIAL: The candidate touched on this, but lacked depth, specificity, or examples.
        - MISSING: The candidate completely failed to address this or was incorrect.
        
        You MUST extract a direct quote (`evidence`) from the candidate's answer if the status is MET or PARTIAL.
        Do NOT guess or assume. If it's not explicitly in the answer, it's MISSING.
        """
        
        expected_str = "\n".join([f"- {p}" for p in expected_points])
        user_prompt = f"""
        Question: {question_text}
        
        Expected Key Points:
        {expected_str}
        
        Candidate's Answer:
        {candidate_answer}
        """

        result = await self.llm_service.generate_json(
            prompt=user_prompt,
            output_schema=AnswerEvaluationResult,
            system_instruction=system_prompt
        )
        return result
