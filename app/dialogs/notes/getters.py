from aiogram_dialog import DialogManager

from app.crud.travel import get_travel_by_id
from app.crud.user import get_user_by_telegram_id
from app.database import async_session
from app.crud.note import get_accessible_notes_by_user_and_travel


async def get_notes(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        user_id = dialog_manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        travel_id = int(dialog_manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)
        notes = await get_accessible_notes_by_user_and_travel(session, user, travel)
        return {
            'notes': notes
        }