import geocoder
from OSMPythonTools.nominatim import Nominatim
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from app.crud.user import update_user_detailed_by_telegram_id
from app.database import async_session
from app.dialogs.invitation.states import InvitationMenu
from app.dialogs.people.states import PersonMenu
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
    try:
        nominatim = Nominatim()
        geo = nominatim.query(city).toJSON()[0]
        country = geo['display_name'].split(' ')[-1]
        city = geo['name']
        lon = float(geo['lon'])
        lat = float(geo['lat'])
    except:
        await m.answer('Попробуйте еще раз ⚠️')
        return
    ctx = manager.current_context()
    ctx.dialog_data.update(city=city, country=country, lon=lon, lat=lat)
    await manager.switch_to(CreateUser.confirm_city)


async def on_city_confirm(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    ctx = manager.current_context()
    user_id = manager.middleware_data.get('event_chat').id
    async with async_session() as session:
        await update_user_detailed_by_telegram_id(session, user_id, ctx.dialog_data.get('age'),
                                                  ctx.dialog_data.get('city'), ctx.dialog_data.get('country'),
                                                  ctx.dialog_data.get('bio'), ctx.dialog_data.get('lon'),
                                                  ctx.dialog_data.get('lat'))
    await manager.done()
    await manager.start(StartMenu.select_menu)


async def on_start_travels(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    await manager.start(TravelMenu.select_travel)


async def on_start_invitations(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    await manager.start(InvitationMenu.select_invitation)


async def on_start_people(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    await manager.start(PersonMenu.select_person)
