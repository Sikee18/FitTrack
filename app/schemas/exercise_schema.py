from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RepRecordSchema(BaseModel):
    rep_number: int
    timestamp: datetime
    correctness: float
    feedback: str
    landmarks: list

class ExerciseSessionCreate(BaseModel):
    exercise_name: str

class ExerciseSessionEnd(BaseModel):
    total_reps: int
    avg_score: float

class ExerciseSessionSummary(BaseModel):
    id: int
    exercise_name: str
    start_time: datetime
    end_time: Optional[datetime]
    total_reps: int
    avg_score: float

    class Config:
        orm_mode = True
