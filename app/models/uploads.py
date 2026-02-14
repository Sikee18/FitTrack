from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base
from datetime import timezone


class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    image_path = Column(String, nullable=False)
    upload_type = Column(String(50))  # food, workout, progress_photo
    upload_metadata = Column(JSONB)  # renamed from metadata to upload_metadata
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="uploads")
