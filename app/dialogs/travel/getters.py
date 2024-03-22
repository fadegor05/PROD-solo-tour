from aiogram_dialog import DialogManager
from app.database import async_session
from app.crud.user import get_user_by_telegram_id
from app.crud.travel import get_travel_by_id, get_travel_owner_by_travel


async def get_travels(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        user_id = dialog_manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        travels = []
        for member in user.travels:
            travel = member.travel
            travels.append(travel)

        return {
            'travels': travels
        }


async def get_travel(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        user_id = dialog_manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        travel = await get_travel_by_id(session, int(dialog_manager.dialog_data.get('travel_id')))
        owner = await get_travel_owner_by_travel(session, travel)

        return {
            'travel_id': travel.id,
            'travel_name': travel.name,
            'travel_description': travel.description,
            'members_amount': len(travel.members),
            'owner_name': owner.name
        }
