from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.uploads_schema import UploadCreate, UploadResponse
from app.repositories.upload_repo import UploadRepository
from app.database.database import get_db


router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/", response_model=UploadResponse)
def create_upload(upload: UploadCreate, db: Session = Depends(get_db), user_id: int = 1):
    repo = UploadRepository(db)
    return repo.create_upload(user_id, upload)


@router.get("/", response_model=List[UploadResponse])
def get_uploads(db: Session = Depends(get_db), user_id: int = 1):
    repo = UploadRepository(db)
    return repo.get_uploads_by_user(user_id)
