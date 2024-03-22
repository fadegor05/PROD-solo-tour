from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from app.models.note import Note
from app.models.travel import Travel
from app.models.user import User


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
