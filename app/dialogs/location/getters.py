from aiogram_dialog import DialogManager

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

        return {
            'city': '123',
            'country': '321',
        }