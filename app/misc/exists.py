from app.crud.note import get_note_by_id
from app.database import async_session


async def is_note_exists(note_id: int | str) -> bool:
    async with async_session() as session:
        note = await get_note_by_id(session, int(note_id))
        return True if note else False
