from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.location import delete_locations_by_travel
from app.crud.member import delete_members_by_travel
from app.crud.note import delete_notes_by_travel
from app.crud.travel import create_travel, get_travel_by_name, get_travel_by_id, delete_travel, \
    is_user_travel_owner_by_user
from app.database import async_session
from app.dialogs.member.states import MemberMenu
from app.dialogs.travel.states import TravelMenu, CreateTravel, DeleteTravel
from app.dialogs.note.states import NoteMenu
from app.dialogs.location.states import LocationMenu
from app.crud.user import get_user_by_telegram_id
from app.misc.constants import SwitchToWindow
from app.misc.exists import is_travel_exists


async def on_chosen_travel(c: CallbackQuery, widget: Select, manager: DialogManager, travel_id: str, **kwargs):
    if not await is_travel_exists(travel_id):
        await c.answer('Такого путешествия не существует ⚠️')
        return
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
            await m.reply('Данное имя путешествия занято ⚠️')
            return
    ctx.dialog_data.update(name=name)
    await manager.switch_to(CreateTravel.description)


async def on_entered_description(m: Message, widget: TextInput, manager: DialogManager, description, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(description=description)
    async with async_session() as session:
        user_id = manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        travel = await create_travel(session, ctx.dialog_data.get('name'), ctx.dialog_data.get('description'), user)
        await m.answer(f'Путешествие {travel.name} было успешно создано ✅')
    await manager.done()


async def on_travel_notes(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    travel_id = manager.dialog_data.get('travel_id')
    if not await is_travel_exists(travel_id):
        await c.answer('Такого путешествия не существует ⚠️')
        await manager.done()
        return
    await manager.start(NoteMenu.select_note, {'travel_id': travel_id})


async def on_travel_locations(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    travel_id = manager.dialog_data.get('travel_id')
    if not await is_travel_exists(travel_id):
        await c.answer('Такого путешествия не существует ⚠️')
        await manager.done()
        return
    await manager.start(LocationMenu.select_location, {'travel_id': travel_id})


async def on_travel_members(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    travel_id = manager.dialog_data.get('travel_id')
    if not await is_travel_exists(travel_id):
        await c.answer('Такого путешествия не существует ⚠️')
        await manager.done()
        return
    await manager.start(MemberMenu.select_member, {'travel_id': travel_id})


async def on_travel_delete(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    travel_id = manager.dialog_data.get('travel_id')
    if not await is_travel_exists(travel_id):
        await c.answer('Такого путешествия не существует ⚠️')
        await manager.done()
        return
    await manager.start(DeleteTravel.delete_travel, {'travel_id': travel_id})


async def on_travel_delete_confirm(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    async with async_session() as session:
        travel_id = int(manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)
        if not await is_travel_exists(travel_id):
            await c.answer('Такого путешествия не существует ⚠️')
            await manager.done(
                {
                    'switch_to_window': SwitchToWindow.SelectTravel
                }
            )
            return
        user_id = manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        is_owner = await is_user_travel_owner_by_user(session, travel, user)
        if not is_owner:
            await c.answer('У вас недостаточно прав')
            await manager.done()
            return
        name = travel.name
        await delete_locations_by_travel(session, travel)
        await session.refresh(travel)
        await delete_notes_by_travel(session, travel)
        await session.refresh(travel)
        await delete_members_by_travel(session, travel)
        await session.refresh(travel)
        await delete_travel(session, travel)
    await c.answer(f'Путешествие {name} было успешно удалено ✅')
    await manager.done(
        {
            'switch_to_window': SwitchToWindow.SelectTravel
        }
    )
