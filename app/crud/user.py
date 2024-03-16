from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import async_session
from app.models.user import User

async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    stmt = select(User).where(User.id == id)
    user = await session.scalar(stmt)
    return user

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    user = await session.scalar(stmt)
    return user

async def create_user(session: AsyncSession, telegram_id: int) -> User:
    user = User(telegram_id=telegram_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
    
