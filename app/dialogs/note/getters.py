from aiogram_dialog import DialogManager

from app.crud.travel import get_travel_by_id
from app.crud.user import get_user_by_telegram_id
from app.database import async_session
from app.crud.note import get_accessible_notes_by_user_and_travel, get_note_by_id


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


async def get_note(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        note_id = int(dialog_manager.dialog_data.get('note_id'))
        note = await get_note_by_id(session, note_id)

        return {
            'note_name': note.name,
            'note_text': note.text,
            'is_public': note.is_public,
            'is_public_icon': '🌐 Публичная' if note.is_public else '🔒 Личная',
            'user': note.user.name
        }