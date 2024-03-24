from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.note import create_note, get_note_by_id, delete_note
from app.crud.travel import get_travel_by_id
from app.crud.user import get_user_by_telegram_id
from app.database import async_session
from app.dialogs.note.states import NoteMenu, CreateNote, DeleteNote
from app.misc.constants import SwitchToWindow
from app.misc.exists import is_note_exists


async def on_chosen_note(c: CallbackQuery, widget: Select, manager: DialogManager, note_id: str, **kwargs):
    if not await is_note_exists(note_id):
        await c.answer('Такой заметки не существует ⚠️')
        return
    ctx = manager.current_context()
    ctx.dialog_data.update(note_id=note_id)
    await manager.switch_to(NoteMenu.select_action)


async def on_create_note(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(CreateNote.name, data={'travel_id': manager.start_data.get('travel_id')})


async def on_delete_note(c: CallbackQuery, widget: Button, manager: DialogManager):
    note_id = manager.dialog_data.get('note_id')
    if not await is_note_exists(note_id):
        await c.answer('Такой заметки не существует ⚠️')
        await manager.back()
        return
    await manager.start(DeleteNote.delete_note, data={'note_id': note_id})


async def on_delete_note_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    note_id = int(manager.start_data.get('note_id'))
    if not await is_note_exists(note_id):
        await c.answer('Такой заметки не существует ⚠️')
        await manager.done(
            {
                'switch_to_window': SwitchToWindow.SelectNote
            }
        )
        return
    async with async_session() as session:
        user_id = manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        note = await get_note_by_id(session, note_id)
        if user.id != note.user.id:
            await c.answer('У вас недостаточно прав ❌')
            await manager.done()
            return
        name = note.name
        await delete_note(session, note)
        await c.answer(f'Заметка {name} была успешно удалена ✅')
    await manager.done(
        {
            'switch_to_window': SwitchToWindow.SelectNote
        }
    )

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
        await m.answer(f'Заметка {note.name} была создана ✅')
    await manager.done()

