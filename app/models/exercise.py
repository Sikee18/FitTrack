from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class ExerciseSession(Base):
    __tablename__ = "exercise_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_name = Column(String(50))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    total_reps = Column(Integer, default=0)
    avg_score = Column(Float, default=0.0)

    reps = relationship("RepRecord", back_populates="session")

class RepRecord(Base):
    __tablename__ = "rep_records"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("exercise_sessions.id"))
    rep_number = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    correctness = Column(Float)
    feedback = Column(String(255))
    landmarks = Column(JSON)

    session = relationship("ExerciseSession", back_populates="reps")
