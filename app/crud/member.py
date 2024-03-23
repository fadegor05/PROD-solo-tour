from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Travel


async def delete_members_by_travel(session: AsyncSession, travel: Travel) -> None:
    for member in travel.members:
        await session.delete(member)
    await session.commit()