from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Travel, Member, User


async def create_member(session: AsyncSession, travel: Travel, user: User, is_owner: bool = False) -> Member:
    member = Member(user=user, travel=travel, is_owner=is_owner)
    session.add(member)
    await session.commit()
    await session.refresh(member)
    return member


async def delete_member(session: AsyncSession, member: Member) -> None:
    await session.delete(member)
    await session.commit()


async def get_member_by_id(session: AsyncSession, id: int) -> Member | None:
    stmt = Select(Member).where(Member.id == id)
    member = await session.scalar(stmt)
    return member


async def delete_members_by_travel(session: AsyncSession, travel: Travel) -> None:
    for member in travel.members:
        await session.delete(member)
    await session.commit()
