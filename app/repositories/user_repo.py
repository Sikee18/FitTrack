from sqlalchemy.orm import Session
from app.models.user import User, TraineeDetails, TrainerDetails, AdminDetails
from app.core.security import hash_password

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict, role: str):
    # Extract password and hash it for User table
    password_hash = hash_password(user_data.pop("password"))
    
    # Extract fields for User table
    email = user_data.pop("email")
    
    # Create User object
    user = User(email=email, password_hash=password_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Filter user_data for fields belonging to detail tables
    if role == "trainee":
        allowed_fields = {"full_name", "phone", "gym_name", "gym_code", "age", "gender", "fitness_goal"}
        details_data = {k: v for k, v in user_data.items() if k in allowed_fields}
        trainee = TraineeDetails(user_id=user.id, **details_data)
        db.add(trainee)
    elif role == "trainer":
        allowed_fields = {"full_name", "phone", "gym_name", "gym_code", "years_of_experience", "specialization"}
        details_data = {k: v for k, v in user_data.items() if k in allowed_fields}
        trainer = TrainerDetails(user_id=user.id, **details_data)
        db.add(trainer)
    elif role == "admin":
        allowed_fields = {"full_name"}
        details_data = {k: v for k, v in user_data.items() if k in allowed_fields}
        admin = AdminDetails(user_id=user.id, **details_data)
        db.add(admin)

    db.commit()
    return user
