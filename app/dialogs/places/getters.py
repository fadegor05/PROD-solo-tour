from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from app.crud.location import get_location_by_id
from app.database import async_session
from app.services.kudago.service import get_categories_kudago, get_places_kudago, get_place_kudago


async def get_categories(dialog_manager: DialogManager, **kwargs):
    categories = await get_categories_kudago()
    return {
        'categories': categories
    }


async def get_places(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        location_id = int(dialog_manager.start_data.get('location_id'))
        location = await get_location_by_id(session, location_id)
        category = dialog_manager.dialog_data.get('category_slug')
        places = await get_places_kudago((location.lon, location.lat), category)
        return {
            'places': places
        }


async def get_place(dialog_manager: DialogManager, **kwargs):
    place_id = int(dialog_manager.dialog_data.get('place_id'))
    place = await get_place_kudago(place_id)
    data = place.model_dump(exclude_none=True)
    if len(place.images) >= 1:
        data['image'] = MediaAttachment(ContentType.PHOTO, url=place.images[0]['image'])
    return data
