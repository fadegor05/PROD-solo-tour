import re, datetime

from OSMPythonTools.nominatim import Nominatim
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button
import geocoder

from app.crud.location import create_location, get_location_by_id, delete_location
from app.crud.travel import get_travel_by_id, is_user_travel_owner_by_user
from app.crud.user import get_user_by_telegram_id
from app.database import async_session
from app.dialogs.location.states import LocationMenu, CreateLocation, DeleteLocation
from app.dialogs.places.states import PlaceMenu
from app.misc.constants import SwitchToWindow
from app.misc.exists import is_location_exists


async def on_chosen_location(c: CallbackQuery, widget: Select, manager: DialogManager, location_id: str, **kwargs):
    if not await is_location_exists(location_id):
        await c.answer('Такой локации не существует ⚠️')
        return
    ctx = manager.current_context()
    ctx.dialog_data.update(location_id=location_id)
    await manager.switch_to(LocationMenu.select_action)


async def on_create_location(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(CreateLocation.city, data={'travel_id': manager.start_data.get('travel_id')})


async def on_delete_location(c: CallbackQuery, widget: Button, manager: DialogManager):
    location_id = manager.dialog_data.get('location_id')
    travel_id = manager.start_data.get('travel_id')
    if not await is_location_exists(location_id):
        await c.answer('Такой локации не существует ⚠️')
        await manager.done()
        return
    await manager.start(DeleteLocation.delete_location, data={'location_id': location_id, 'travel_id': travel_id})


async def on_view_places(c: CallbackQuery, widget: Button, manager: DialogManager):
    location_id = manager.dialog_data.get('location_id')
    travel_id = manager.start_data.get('travel_id')
    if not await is_location_exists(location_id):
        await c.answer('Такой локации не существует ⚠️')
        await manager.done()
        return
    await manager.start(PlaceMenu.select_category, data={'location_id': location_id, 'travel_id': travel_id})


async def on_delete_location_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    async with async_session() as session:
        travel_id = int(manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)
        user_id = manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        is_owner = await is_user_travel_owner_by_user(session, travel, user)
        if not is_owner:
            await c.answer('У вас недостаточно прав ❌')
            await manager.done()
            return
        location_id = int(manager.start_data.get('location_id'))
        if not await is_location_exists(location_id):
            await c.answer('Такой локации не существует ⚠️')
            await manager.done(
                {
                    'switch_to_window': SwitchToWindow.SelectLocation
                }
            )
            return
        location = await get_location_by_id(session, location_id)
        name = f'{location.city}, {location.country}'
        await delete_location(session, location)
        await c.answer(f'Локация {name} была успешно удалена ✅')
    await manager.done(
        {
            'switch_to_window': SwitchToWindow.SelectLocation
        }
    )


async def on_entered_city(m: Message, widget: TextInput, manager: DialogManager, city, **kwargs):
    ctx = manager.current_context()
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
    ctx.dialog_data.update(city=city, country=country, lon=lon, lat=lat)
    await manager.switch_to(CreateLocation.confirm_city)


async def on_entered_arrive_at(m: Message, widget: TextInput, manager: DialogManager, arrive_at, **kwargs):
    ctx = manager.current_context()
    match = re.match(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\d{4}$', arrive_at)
    if not match:
        await m.reply('Попробуйте еще раз ⚠️')
        return
    try:
        date = datetime.datetime.strptime(match.group(), '%d/%m/%Y')
    except:
        await m.reply('Попробуйте еще раз ⚠️')
        return
    ctx.dialog_data.update(arrive_at=match.group())
    await manager.switch_to(CreateLocation.departure_at)


async def on_entered_departure_at(m: Message, widget: TextInput, manager: DialogManager, departure_at, **kwargs):
    ctx = manager.current_context()
    match = re.match(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\d{4}$', departure_at)
    if not match:
        await m.reply('Попробуйте еще раз ⚠️')
        return
    try:
        date = datetime.datetime.strptime(match.group(), '%d/%m/%Y')
    except:
        await m.reply('Попробуйте еще раз ⚠️')
        return
    ctx.dialog_data.update(departure_at=match.group())

    arrive_at_datetime = datetime.datetime.strptime(ctx.dialog_data.get('arrive_at'), '%d/%m/%Y')
    departure_at_datetime = datetime.datetime.strptime(ctx.dialog_data.get('departure_at'), '%d/%m/%Y')
    async with async_session() as session:
        travel_id = int(manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)
        location = await create_location(session, travel, ctx.dialog_data.get('city'), ctx.dialog_data.get('country'),
                                         float(ctx.dialog_data.get('lon')), float(ctx.dialog_data.get('lat')),
                                         arrive_at_datetime, departure_at_datetime)
        await m.answer(f'Локация {location.city}, {location.country} была успешно добавлена ✅')
    await manager.done()
