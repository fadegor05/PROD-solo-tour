from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from app.crud.location import get_location_by_id
from app.crud.travel import get_travel_by_id
from app.crud.user import get_user_by_telegram_id
from app.database import async_session
from app.misc.exists import is_location_exists
from app.services.om.schemas import Weather
from app.services.om.service import get_location_weather
from app.services.ors.service import get_rendered_map
import json


async def get_locations(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        user_id = dialog_manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        travel_id = int(dialog_manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)
        locations = travel.locations
        points = [(user.lon, user.lat)]
        for location in locations:
            points.append((location.lon, location.lat))
        if len(points) == 1: points.append((user.lon, user.lat))
        url = json.dumps({"points": points}).replace(' ', '')
        image = MediaAttachment(ContentType.PHOTO, url=f'memory://{url}')
        return {
            'locations': locations,
            'image': image
        }


async def get_location(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        location_id = int(dialog_manager.dialog_data.get('location_id'))
        location = await get_location_by_id(session, location_id)
        if not await is_location_exists(location_id):
            await dialog_manager.done()
            return
        weather: Weather = await get_location_weather((location.lon, location.lat), location.arrive_at,
                                             location.departure_at)
        return {
            'city': location.city,
            'country': location.country,
            'arrive_at': location.arrive_at.strftime('%d/%m/%Y'),
            'departure_at': location.departure_at.strftime('%d/%m/%Y'),
            'weather_dates_type': 'Погода в поездке 💼' if weather.is_dates else 'Погода сейчас 📆',
            'temperature': weather.temperature,
            'weather': weather.weather
        }


async def get_city_confirm(dialog_manager: DialogManager, **kwargs):
    return {
        'city': dialog_manager.current_context().dialog_data.get('city'),
        'country': dialog_manager.current_context().dialog_data.get('country')
    }
