from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from ..models.user import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: UserRole


class UserCreate(UserBase):
    password: str
    lab_id: Optional[int] = None
    hospital_id: Optional[int] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    user_id: int
    lab_id: Optional[int] = None
    hospital_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
