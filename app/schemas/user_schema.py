from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, Annotated

PasswordStr = Annotated[str, Field(min_length=8)]
RoleStr = Annotated[str, Field(min_length=5)]
FullNameStr = Annotated[str, Field(min_length=2, max_length=100)]
PhoneStr = Annotated[str, Field(min_length=7, max_length=15)]
GymNameStr = Annotated[str, Field(min_length=2, max_length=100)]
GymCodeStr = Annotated[str, Field(min_length=1, max_length=50)]
GenderStr = Annotated[Optional[str], Field(max_length=10)]
FitnessGoalStr = Annotated[Optional[str], Field(max_length=255)]
SpecializationStr = Annotated[Optional[str], Field(max_length=100)]

class LoginSchema(BaseModel):
    email: EmailStr
    password: PasswordStr
    role: RoleStr

class TraineeRegisterSchema(BaseModel):
    full_name: FullNameStr
    email: EmailStr
    password: PasswordStr
    confirm_password: PasswordStr
    phone: PhoneStr
    gym_name: GymNameStr
    gym_code: GymCodeStr
    age: int = Field(gt=0)
    gender: GenderStr = None
    fitness_goal: FitnessGoalStr = None

    @model_validator(mode="before")
    def passwords_match(cls, values):
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords do not match")
        return values

class TrainerRegisterSchema(BaseModel):
    full_name: FullNameStr
    email: EmailStr
    password: PasswordStr
    confirm_password: PasswordStr
    phone: PhoneStr
    gym_name: GymNameStr
    gym_code: GymCodeStr
    years_of_experience: int = Field(ge=0)
    specialization: SpecializationStr = None

    @model_validator(mode="before")
    def passwords_match(cls, values):
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords do not match")
        return values

class AdminRegisterSchema(BaseModel):
    full_name: FullNameStr
    email: EmailStr
    password: PasswordStr
    confirm_password: PasswordStr

    @model_validator(mode="before")
    def passwords_match(cls, values):
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords do not match")
        return values
