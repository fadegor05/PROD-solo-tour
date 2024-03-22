from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.note import create_note
from app.crud.travel import get_travel_by_id
from app.crud.user import get_user_by_telegram_id
from app.database import async_session
from app.dialogs.notes.states import NoteMenu, CreateNote


async def on_chosen_note(c: CallbackQuery, widget: Select, manager: DialogManager, note_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(note_id=note_id)
    await manager.switch_to(NoteMenu.select_action)


async def on_create_note(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(CreateNote.name, data={'travel_id': manager.start_data.get('travel_id')})


async def on_entered_name(m: Message, widget: TextInput, manager: DialogManager, name, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(name=name)
    await manager.switch_to(CreateNote.is_public)


async def on_is_public_true(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(is_public=True)
    await manager.switch_to(CreateNote.text)


async def on_is_public_false(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(is_public=False)
    await manager.switch_to(CreateNote.text)


async def on_entered_text(m: Message, widget: TextInput, manager: DialogManager, text, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(text=text)
    async with async_session() as session:
        travel_id = int(manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)
        user_id = manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        note = await create_note(session, ctx.dialog_data.get('name'), ctx.dialog_data.get('text'),
                                 ctx.dialog_data.get('is_public'), user, travel)
        await m.answer(f'Заметка {note.name} была создана')
    await manager.done()

