from app.crud.location import get_location_by_id
from app.crud.note import get_note_by_id
from app.crud.travel import get_travel_by_id
from app.database import async_session


async def is_note_exists(note_id: int | str) -> bool:
    async with async_session() as session:
        note = await get_note_by_id(session, int(note_id))
        return True if note else False


async def is_location_exists(location_id: int | str) -> bool:
    async with async_session() as session:
        location = await get_location_by_id(session, int(location_id))
        return True if location else False


async def is_travel_exists(travel_id: int | str) -> bool:
    async with async_session() as session:
        travel = await get_travel_by_id(session, int(travel_id))
        return True if travel else False
