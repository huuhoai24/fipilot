import re

def fix_args(file_path, old_call, new_call):
    with open(file_path, "r") as f:
        content = f.read()
    content = content.replace(old_call, new_call)
    with open(file_path, "w") as f:
        f.write(content)

# EvaluatorAgent
old_eval = """        result = await self.llm_service.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=AnswerEvaluationResult
        )"""
new_eval = """        result = await self.llm_service.generate_json(
            prompt=user_prompt,
            output_schema=AnswerEvaluationResult,
            system_instruction=system_prompt
        )"""
fix_args("services/interview_evaluation/evaluator_agent.py", old_eval, new_eval)

# QuestionGeneratorAgent
old_qg = """        result = await self.llm_service.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=QuestionGenerationResult
        )"""
new_qg = """        result = await self.llm_service.generate_json(
            prompt=user_prompt,
            output_schema=QuestionGenerationResult,
            system_instruction=system_prompt
        )"""
fix_args("services/interview_planner/question_agent.py", old_qg, new_qg)

