from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.progress_schema import ProgressCreate, ProgressResponse
from app.repositories.progress_repo import ProgressRepository
from app.database.database import get_db
from typing import List
from datetime import date

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/", response_model=ProgressResponse)
def create_progress(progress: ProgressCreate, db: Session = Depends(get_db), user_id: int = 1):
    # user_id would come from auth session/token
    repo = ProgressRepository(db)
    existing = repo.get_progress_by_date(user_id, progress.date)
    if existing:
        raise HTTPException(400, "Progress on this date already exists.")
    return repo.create_progress(user_id, progress)

@router.get("/", response_model=List[ProgressResponse])
def get_all_progress(db: Session = Depends(get_db), user_id: int = 1):
    repo = ProgressRepository(db)
    return repo.get_all_progress(user_id)
