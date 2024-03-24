from aiogram_dialog import DialogManager

from app.crud.location import get_location_by_id
from app.crud.travel import get_travel_by_id
from app.database import async_session
from app.misc.exists import is_location_exists


async def get_locations(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        travel_id = int(dialog_manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)

        return {
            'locations': travel.locations
        }


async def get_location(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        location_id = int(dialog_manager.dialog_data.get('location_id'))
        location = await get_location_by_id(session, location_id)
        if not await is_location_exists(location_id):
            await dialog_manager.done()
            return

        return {
            'city': location.city,
            'country': location.country,
            'arrive_at': location.arrive_at.strftime('%d/%m/%Y'),
            'departure_at': location.departure_at.strftime('%d/%m/%Y')
        }


async def get_city_confirm(dialog_manager: DialogManager, **kwargs):
    return {
        'city': dialog_manager.current_context().dialog_data.get('city'),
        'country': dialog_manager.current_context().dialog_data.get('country')
    }
