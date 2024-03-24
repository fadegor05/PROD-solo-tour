from aiogram_dialog import DialogManager

from app.crud.member import get_member_by_id
from app.crud.travel import get_travel_by_id
from app.database import async_session


async def get_members(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        travel_id = int(dialog_manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)

        return {
            'members': travel.members
        }


async def get_member(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        member_id = int(dialog_manager.dialog_data.get('member_id'))
        member = await get_member_by_id(session, member_id)
        user = member.user

        return {
            'name': user.name,
            'age': user.age,
            'bio': user.bio,
            'is_owner': member.is_owner,
            'is_owner_icon': '⚖️ Организатор' if member.is_owner else '🌐 Участник'
        }
