from aiogram_dialog import DialogManager

from app.crud.user import get_user_by_telegram_id, get_user_with_similar_age, get_user_by_id
from app.database import async_session


async def get_people(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        user_id = dialog_manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        users = await get_user_with_similar_age(session, user)
        return {
            'people': users
        }


async def get_person(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        user_id = int(dialog_manager.dialog_data.get('user_id'))
        user = await get_user_by_id(session, user_id)
        return {
            'name': user.name,
            'age': user.age,
            'city': user.city,
            'country': user.country,
            'bio': user.bio,
            'uuid': user.uuid
        }