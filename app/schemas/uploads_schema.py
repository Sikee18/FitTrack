from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class UploadBase(BaseModel):
    image_path: str
    upload_type: Optional[str]
    metadata: Optional[Dict] = None
    verified: Optional[bool] = False


class UploadCreate(UploadBase):
    pass


class UploadResponse(UploadBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
