import re

file_path = "gateway/api/interview.py"

with open(file_path, "r") as f:
    content = f.read()

# Make sure we import InterviewReport
if "InterviewReport" not in content:
    content = content.replace("from fipilot.models import InterviewSession, InterviewTurn", "from fipilot.models import InterviewSession, InterviewTurn, InterviewReport")
    if "from fipilot.models import InterviewSession" in content and "InterviewTurn" not in content:
        content = content.replace("from fipilot.models import InterviewSession", "from fipilot.models import InterviewSession, InterviewTurn, InterviewReport")

old_return = """        # Mark session as completed
        session_row.status = "completed"
        db.add(session_row)
        
    return InterviewReportResponse("""

new_return = """        # Mark session as completed
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
        
    return response_model"""

content = content.replace(old_return, new_return)

# Wait, there's another replace needed to remove the direct return instantiation.
old_return_full = """    return InterviewReportResponse(
        assessments=assessments,
        solutions_summary=feedback.solutions_summary,
        overall_assessment=feedback.overall_assessment,
        recommendations=feedback.recommendations,
        normalized_score=round(normalized_score, 1)
    )"""
content = content.replace(old_return_full, "")

with open(file_path, "w") as f:
    f.write(content)
