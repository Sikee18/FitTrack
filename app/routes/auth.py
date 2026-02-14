from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user_schema import (LoginSchema, TraineeRegisterSchema,
                                     TrainerRegisterSchema, AdminRegisterSchema)
from app.repositories import user_repo
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/register")
def register(payload: TraineeRegisterSchema | TrainerRegisterSchema | AdminRegisterSchema, db: Session = Depends(get_db)):
    role = ""
    if isinstance(payload, TraineeRegisterSchema):
        role = "trainee"
    elif isinstance(payload, TrainerRegisterSchema):
        role = "trainer"
    elif isinstance(payload, AdminRegisterSchema):
        role = "admin"
    else:
        raise HTTPException(status_code=400, detail="Invalid role or payload")

    existing_user = user_repo.get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = payload.model_dump()
    user_data.pop("confirm_password", None)
    user_repo.create_user(db, user_data, role)

    return {"message": f"{role.capitalize()} registered successfully."}

@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = user_repo.get_user_by_email(db, payload.email)
    if not user or user.role != payload.role:
        raise HTTPException(status_code=400, detail="Incorrect email or role")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
