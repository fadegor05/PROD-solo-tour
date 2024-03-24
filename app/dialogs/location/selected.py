import re, datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button
import geocoder

from app.crud.location import create_location
from app.crud.travel import get_travel_by_id
from app.database import async_session
from app.dialogs.location.states import LocationMenu, CreateLocation


async def on_chosen_location(c: CallbackQuery, widget: Select, manager: DialogManager, location_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(location_id=location_id)
    await manager.switch_to(LocationMenu.select_action)


async def on_create_location(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(CreateLocation.city, data={'travel_id': manager.start_data.get('travel_id')})


async def on_entered_city(m: Message, widget: TextInput, manager: DialogManager, city, **kwargs):
    ctx = manager.current_context()
    geo = geocoder.osm(city)
    if not geo.country or not geo.city:
        await m.reply('Попробуйте еще раз ⚠️')
        return
    ctx.dialog_data.update(city=geo.city, country=geo.country)
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
                                         arrive_at_datetime, departure_at_datetime)
        await m.answer(f'Локация {location.city}, {location.country} была успешно добавлена ✅')
    await manager.done()
