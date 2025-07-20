from app.models.users import User
from sqlalchemy.future import select

async def get_pet_by_id(db, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
