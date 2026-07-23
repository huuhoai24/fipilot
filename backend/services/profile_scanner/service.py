from __future__ import annotations

from services.profile_scanner.agent import ResumeAgent
from shared.schemas import CandidateProfile


class ProfileScannerService:
    def __init__(self, agent: ResumeAgent):
        self.agent = agent

    async def scan_resume(self, resume_text: str) -> CandidateProfile:
        return await self.agent.extract_profile(resume_text)

