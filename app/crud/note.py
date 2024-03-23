from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, and_, or_

from app.models.note import Note
from app.models.travel import Travel
from app.models.user import User


async def delete_notes_by_travel(session: AsyncSession, travel: Travel) -> None:
    for note in travel.notes:
        await session.delete(note)
    await session.commit()


async def get_accessible_notes_by_user_and_travel(session: AsyncSession, user: User, travel: Travel) -> List[Note]:
    stmt = Select(Note).where(and_(Note.travel_id == travel.id, or_(Note.user_id == user.id, Note.is_public)))
    result = await session.scalars(stmt)
    notes = result.all()
    return notes


async def get_note_by_id(session: AsyncSession, id: int) -> Note | None:
    stmt = Select(Note).where(Note.id == id)
    note = await session.scalar(stmt)
    return note


async def create_note(session: AsyncSession, name: str, text: str, is_public: bool, user: User, travel: Travel) -> Note:
    note = Note(name=name, text=text, is_public=is_public, travel=travel, user=user)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note
