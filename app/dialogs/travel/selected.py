from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.travel import create_travel, get_travel_by_name
from app.database import async_session
from app.dialogs.travel.states import TravelMenu, CreateTravel
from app.dialogs.note.states import NoteMenu
from app.dialogs.location.states import LocationMenu
from app.crud.user import get_user_by_telegram_id


async def on_chosen_travel(c: CallbackQuery, widget: Select, manager: DialogManager, travel_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(travel_id=travel_id)
    await manager.switch_to(TravelMenu.select_action)


async def on_create_travel(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    await manager.start(CreateTravel.name)


async def on_entered_name(m: Message, widget: TextInput, manager: DialogManager, name, **kwargs):
    ctx = manager.current_context()
    async with async_session() as session:
        travel = await get_travel_by_name(session, name)
        if travel:
            await m.reply('Данное имя путешествия занято')
            return
    ctx.dialog_data.update(name=name)
    await manager.switch_to(CreateTravel.description)


async def on_entered_description(m: Message, widget: TextInput, manager: DialogManager, description, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(description=description)
    user_id = manager.middleware_data.get('event_chat').id
    async with async_session() as session:
        user = await get_user_by_telegram_id(session, user_id)
        travel = await create_travel(session, ctx.dialog_data.get('name'), ctx.dialog_data.get('description'), user)
        await m.answer(f'Путешествие {travel.name} было успешно создано')
    await manager.done()


async def on_travel_notes(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    await manager.start(NoteMenu.select_note, {'travel_id': manager.dialog_data.get('travel_id')})


async def on_travel_locations(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    await manager.start(LocationMenu.select_location, {'travel_id': manager.dialog_data.get('travel_id')})