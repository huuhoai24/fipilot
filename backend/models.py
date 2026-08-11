from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)
    name = Column(String, index=True, nullable=True)
    profile_json = Column(Text, nullable=True)
    profile_version = Column(Integer, nullable=False, default=1)
    raw_resume_text = Column(Text, nullable=True)
    
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"))
    user_id = Column(String, index=True, nullable=True)
    status = Column(String, default="created")
    role = Column(String, nullable=True) # e.g. AI, DE, DA
    level = Column(String, nullable=True) # e.g. Fresher, Junior, Senior
    language = Column(String, default="vi") # en, vi
    candidate_name = Column(String, nullable=True)
    question_count = Column(Integer, default=0)
    template_id = Column(String, nullable=True)
    current_question_id = Column(Integer, default=0)
    follow_up_count = Column(Integer, default=0)
    completed_question_ids = Column(Text, default="[]")
    state = Column(String, default="GREETING")
    question_plan_json = Column(Text, nullable=True)
    proctoring_events_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)
    report_id = Column(String, nullable=True)
    report_data = Column(Text, nullable=True)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")
    evaluations = relationship("Evaluation", back_populates="session")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    role = Column(String) # user or ai
    content = Column(Text)
    created_at = Column(DateTime, default=utc_now)

    session = relationship("Session", back_populates="messages")

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    question_id = Column(Integer, ForeignKey("messages.id"))
    answer_id = Column(Integer, ForeignKey("messages.id"))
    correctness = Column(String) # Correct, Partial, Wrong
    score = Column(Integer)
    explanation = Column(Text)
    rubric_json = Column(Text, nullable=True)
    
    session = relationship("Session", back_populates="evaluations")


class InterviewBlueprintArtifact(Base):
    __tablename__ = "interview_blueprint_artifacts"

    artifact_key = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    candidate_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    plan_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)


class ResumeExtractionArtifact(Base):
    __tablename__ = "resume_extraction_artifacts"

    artifact_key = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    profile_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
