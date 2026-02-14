from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    trainee = relationship("TraineeDetails", uselist=False, back_populates="user")
    trainer = relationship("TrainerDetails", uselist=False, back_populates="user")
    admin = relationship("AdminDetails", uselist=False, back_populates="user")

class TraineeDetails(Base):
    __tablename__ = "trainee_details"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    gym_name = Column(String(100), nullable=False)
    gym_code = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10))
    fitness_goal = Column(String(255))

    user = relationship("User", back_populates="trainee")

class TrainerDetails(Base):
    __tablename__ = "trainer_details"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    gym_name = Column(String(100), nullable=False)
    gym_code = Column(String(50), nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    specialization = Column(String(100))

    user = relationship("User", back_populates="trainer")

class AdminDetails(Base):
    __tablename__ = "admin_details"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(100), nullable=False)

    user = relationship("User", back_populates="admin")
