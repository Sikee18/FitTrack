from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from realtime import List
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.exercise import ExerciseSession, RepRecord
from app.schemas.exercise_schema import ExerciseSessionCreate, ExerciseSessionEnd, RepRecordSchema, ExerciseSessionSummary
from app.models.user import User
from app.core.dependencies import get_current_user  # Your JWT user dependency

router = APIRouter(prefix="/exercise/session", tags=["Exercise Sessions"])

@router.post("/start")
def start_session(payload: ExerciseSessionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session = ExerciseSession(
        user_id=user.id,
        exercise_name=payload.exercise_name
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id, "start_time": session.start_time}

@router.post("/{session_id}/data")
def add_rep_data(session_id: int, rep_record: RepRecordSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(ExerciseSession).filter_by(id=session_id, user_id=user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    rep = RepRecord(session_id=session_id, **rep_record.dict())
    db.add(rep)
    db.commit()
    return {"message": "Recorded successfully"}

@router.post("/{session_id}/end")
def end_session(session_id: int, end_payload: ExerciseSessionEnd, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(ExerciseSession).filter_by(id=session_id, user_id=user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.end_time = datetime.now(datetime.timezone.utc)
    session.total_reps = end_payload.total_reps
    session.avg_score = end_payload.avg_score
    db.commit()
    return {
        "message": "Session ended",
        "session_summary": ExerciseSessionSummary.from_orm(session)
    }

@router.get("/history", response_model=List[ExerciseSessionSummary])
def get_history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    sessions = db.query(ExerciseSession).filter_by(user_id=user.id).all()
    return sessions
