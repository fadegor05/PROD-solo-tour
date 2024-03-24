from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Travel, Member


async def get_member_by_id(session: AsyncSession, id: int) -> Member | None:
    stmt = Select(Member).where(Member.id == id)
    member = await session.scalar(stmt)
    return member


async def delete_members_by_travel(session: AsyncSession, travel: Travel) -> None:
    for member in travel.members:
        await session.delete(member)
    await session.commit()
