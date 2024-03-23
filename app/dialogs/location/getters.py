from aiogram_dialog import DialogManager

from app.crud.location import get_location_by_id
from app.crud.travel import get_travel_by_id
from app.database import async_session


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

        return {
            'city': location.city,
            'country': location.country,
            'arrive_at': location.arrive_at.strftime('%d/%m/%Y %H:%M:%S'),
            'departure_at': location.departure_at.strftime('%d/%m/%Y %H:%M:%S')
        }