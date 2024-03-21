from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.travel import Travel
from app.models.user import User
from app.models.member import Member


async def create_travel(session: AsyncSession, name: str, description: str, owner: User) -> Travel:
    member = Member(user=owner, is_owner=True)
    travel = Travel(name=name, description=description, members=[member])
    session.add(travel)
    await session.commit()
    await session.refresh(travel)
    return travel


async def get_travel_by_name(session: AsyncSession, name: str) -> Travel | None:
    stmt = select(Travel).where(Travel.name == name)
    travel = await session.scalar(stmt)
    return travel


async def get_travel_by_id(session: AsyncSession, id: int) -> Travel | None:
    stmt = select(Travel).where(Travel.id == id)
    travel = await session.scalar(stmt)
    return travel
