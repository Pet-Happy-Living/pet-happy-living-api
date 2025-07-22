# api/v1/endpoints/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.users import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # 이미 존재하는 사용자 확인
    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user