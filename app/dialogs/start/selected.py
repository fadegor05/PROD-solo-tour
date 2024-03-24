import geocoder
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from app.crud.user import update_user_detailed_by_telegram_id
from app.database import async_session
from app.dialogs.invitation.states import InvitationMenu
from app.dialogs.start.states import StartMenu, CreateUser
from app.dialogs.travel.states import TravelMenu


async def on_entered_age(m: Message, widget: TextInput, manager: DialogManager, age, **kwargs):
    if not age.isdigit():
        await m.answer('Пожайлуста, введите число ⚠️')
        return
    age = int(age)
    ctx = manager.current_context()
    ctx.dialog_data.update(age=age)
    await manager.switch_to(CreateUser.bio)


async def on_entered_bio(m: Message, widget: TextInput, manager: DialogManager, bio, **kwargs):
    bio = str(bio)
    ctx = manager.current_context()
    ctx.dialog_data.update(bio=bio)
    await manager.switch_to(CreateUser.city)


async def on_entered_city(m: Message, widget: TextInput, manager: DialogManager, city, **kwargs):
    city = str(city)
    geo = geocoder.osm(city)
    if not geo.country or not geo.city:
        await m.answer('Попробуйте еще раз ⚠️')
        return
    ctx = manager.current_context()
    user_id = manager.middleware_data.get('event_chat').id
    async with async_session() as session:
        await update_user_detailed_by_telegram_id(session, user_id, ctx.dialog_data.get('age'), geo.city, geo.country,
                                                  ctx.dialog_data.get('bio'), geo.json['lng'], geo.json['lat'])
    await manager.done()
    await manager.start(StartMenu.select_menu)


async def on_start_travels(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    await manager.start(TravelMenu.select_travel)


async def on_start_invitations(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    await manager.start(InvitationMenu.select_invitation)
