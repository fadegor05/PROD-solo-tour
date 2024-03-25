from typing import List
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.user import User


async def get_user_by_uuid(session: AsyncSession, uuid: str) -> User | None:
    stmt = select(User).where(User.uuid == uuid)
    user = await session.scalar(stmt)
    return user


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    stmt = select(User).where(User.id == id)
    user = await session.scalar(stmt)
    return user


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    user = await session.scalar(stmt)
    return user


async def create_user(session: AsyncSession, telegram_id: int, name: str) -> User:
    user = User(telegram_id=telegram_id, name=name, uuid=str(uuid4()))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_detailed_by_telegram_id(session: AsyncSession, telegram_id: int, age: int, city: str,
                                              country: str, bio: str, lon: float, lat: float) -> User:
    user = await get_user_by_telegram_id(session, telegram_id)
    user.age = age
    user.city = city
    user.country = country
    user.bio = bio
    user.lon = lon
    user.lat = lat
    await session.commit()
    return user


async def get_user_with_similar_age(session: AsyncSession, user: User) -> List[User]:
    stmt = select(User).where(and_(User.age >= user.age - 5, User.age <= user.age + 5, User.id != user.id))
    result = await session.scalars(stmt)
    users = result.all()
    return users