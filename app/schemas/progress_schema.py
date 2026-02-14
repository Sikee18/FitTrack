from pydantic import BaseModel
from datetime import date, datetime

class ProgressBase(BaseModel):
    date: date
    food_points: int
    workout_points: int
    hydration_points: int
    sleep_points: int

class ProgressCreate(ProgressBase):
    pass

class ProgressResponse(ProgressBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
