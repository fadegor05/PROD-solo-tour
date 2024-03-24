from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Invitation


async def get_invitation_by_id(session: AsyncSession, id: int) -> Invitation | None:
    stmt = Select(Invitation).where(Invitation.id == id)
    invitation = await session.scalar(stmt)
    return invitation
