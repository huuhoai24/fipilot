from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="CHITCHAT") # CHITCHAT, INTERVIEWING, ENDED
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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

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
