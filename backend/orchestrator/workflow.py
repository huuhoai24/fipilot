"""Workflow boundary for the modular monolith.

This project intentionally does not use LangGraph in this refactor. The
workflow is coordinated in-process by InterviewOrchestrator.
"""

from orchestrator.interview_orchestrator import InterviewOrchestrator

__all__ = ["InterviewOrchestrator"]

