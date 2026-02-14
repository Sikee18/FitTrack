from sqlalchemy.orm import Session
from app.models.progress import Progress
from app.schemas.progress_schema import ProgressCreate
from datetime import date

class ProgressRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_progress(self, user_id: int, progress: ProgressCreate):
        db_progress = Progress(
            user_id=user_id,
            date=progress.date,
            food_points=progress.food_points,
            workout_points=progress.workout_points,
            hydration_points=progress.hydration_points,
            sleep_points=progress.sleep_points,
        )
        self.db.add(db_progress)
        self.db.commit()
        self.db.refresh(db_progress)
        return db_progress

    def get_progress_by_date(self, user_id: int, date_obj: date):
        return self.db.query(Progress).filter(Progress.user_id == user_id, Progress.date == date_obj).first()

    def get_all_progress(self, user_id: int):
        return self.db.query(Progress).filter(Progress.user_id == user_id).all()
