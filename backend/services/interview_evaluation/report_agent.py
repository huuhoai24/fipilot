from typing import List, Dict, Any
from infrastructure.llm.base import BaseLLMService
from shared.schemas.interview import ReportFeedback

class ReportGeneratorAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def generate_coaching_feedback(self, gaps: List[Dict[str, Any]]) -> ReportFeedback:
        if not gaps:
            return ReportFeedback(
                overall_assessment="Tuyệt vời! Bạn đã trả lời xuất sắc tất cả các tiêu chí.",
                recommendations="Hãy tiếp tục duy trì phong độ này trong các buổi phỏng vấn thực tế.",
                solutions_summary="Không có lỗi nào cần khắc phục."
            )
            
        gap_descriptions = "\n".join([
            f"- Kiến thức thiếu hụt: {gap['key_point']} (Lý do: {gap['reasoning']})"
            for gap in gaps
        ])
        
        system_prompt = """
        You are an expert AI Interview Coach.
        Based on the candidate's missing or partial gaps during the interview, write a constructive, and highly actionable coaching feedback in VIETNAMESE.
        Tell the candidate exactly what they missed and how they can improve their answers in actual job interviews.
        Maintain a professional, encouraging, and direct tone.
        """
        
        user_prompt = f"Candidate Gaps:\n{gap_descriptions}"
        
        result = await self.llm_service.generate_json(
            prompt=user_prompt,
            output_schema=ReportFeedback,
            system_instruction=system_prompt
        )
        return result
