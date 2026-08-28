import asyncio
import uuid
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import Request
from fipilot.database import database_session
from fipilot.models import InterviewSession
from sqlalchemy import select
from core.dependencies import CurrentUser
from gateway.api.interview import generate_interview_report
from shared.schemas.interview import InterviewReportRequest
from infrastructure.llm.azure_openai import AzureOpenAIService
from services.interview_evaluation.report_agent import ReportGeneratorAgent

async def main():
    with database_session() as db:
        session = db.scalars(select(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(1)).first()
        client_id = str(session.client_id)
        session_id = session.id
        
    req = InterviewReportRequest(session_id=session_id)
    cu = CurrentUser(uid=client_id)
    llm = AzureOpenAIService()
    agent = ReportGeneratorAgent(llm)
    
    try:
        res = await generate_interview_report(req, cu, agent)
        print("Success:", res)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(main())
