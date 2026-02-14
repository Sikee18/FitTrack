from sqlalchemy.orm import Session
from app.models.uploads import Upload
from app.schemas.uploads_schema import UploadCreate


class UploadRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_upload(self, user_id: int, upload: UploadCreate):
        db_upload = Upload(
            user_id=user_id,
            image_path=upload.image_path,
            upload_type=upload.upload_type,
            metadata=upload.metadata,
            verified=upload.verified,
        )
        self.db.add(db_upload)
        self.db.commit()
        self.db.refresh(db_upload)
        return db_upload

    def get_uploads_by_user(self, user_id: int):
        return self.db.query(Upload).filter(Upload.user_id == user_id).all()
