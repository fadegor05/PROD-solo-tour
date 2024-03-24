from sqlalchemy import Select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Invitation, Travel, User


async def create_invitation(session: AsyncSession, travel: Travel, user: User) -> Invitation:
    invitation = Invitation(travel=travel, user=user)
    session.add(invitation)
    await session.commit()
    await session.refresh(invitation)
    return invitation


async def delete_invitation(session: AsyncSession, invitation: Invitation) -> None:
    await session.delete(invitation)
    await session.commit()


async def get_invitation_by_id(session: AsyncSession, id: int) -> Invitation | None:
    stmt = Select(Invitation).where(Invitation.id == id)
    invitation = await session.scalar(stmt)
    return invitation


async def is_user_invited_to_travel(session: AsyncSession, travel: Travel, user: User) -> bool:
    stmt = Select(Invitation).where(and_(Invitation.user_id == user.id, Invitation.travel_id == travel.id))
    invitation = await session.scalar(stmt)
    return True if invitation else False
