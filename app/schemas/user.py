# schemas/user.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemy 모델 → Pydantic 모델 자동 변환 가능
