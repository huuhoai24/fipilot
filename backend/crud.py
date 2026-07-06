from sqlalchemy.orm import Session
import models

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def create_user(db: Session, name: str):
    db_user = models.User(name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_session(db: Session, user_id: int):
    db_session = models.Session(user_id=user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def update_session_info(db: Session, session_id: int, role: str, level: str):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if db_session:
        db_session.role = role
        db_session.level = level
        db_session.status = "INTERVIEWING"
        db.commit()
        db.refresh(db_session)
    return db_session

def increment_question_count(db: Session, session_id: int):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if db_session:
        db_session.question_count += 1
        db.commit()
        db.refresh(db_session)
    return db_session

def update_session_status(db: Session, session_id: int, status: str):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if db_session:
        db_session.status = status
        db.commit()
        db.refresh(db_session)
    return db_session

def create_message(db: Session, session_id: int, role: str, content: str):
    db_message = models.Message(session_id=session_id, role=role, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_session_messages(db: Session, session_id: int, limit: int = 100):
    return db.query(models.Message).filter(models.Message.session_id == session_id).order_by(models.Message.created_at).limit(limit).all()

def create_evaluation(db: Session, session_id: int, question_id: int, answer_id: int, correctness: str, score: int, explanation: str):
    db_evaluation = models.Evaluation(
        session_id=session_id,
        question_id=question_id,
        answer_id=answer_id,
        correctness=correctness,
        score=score,
        explanation=explanation
    )
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation
