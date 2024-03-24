from aiogram_dialog import DialogManager

from app.crud.invitation import get_invitation_by_id
from app.crud.travel import get_travel_owner_by_travel
from app.crud.user import get_user_by_telegram_id
from app.database import async_session


async def get_invitations(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        user_id = dialog_manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)

        return {
            'invitations': user.invitations,
            'code': user.uuid
        }


async def get_invitation(dialog_manager: DialogManager, **kwargs):
    async with async_session() as session:
        invitation_id = int(dialog_manager.dialog_data.get('invitation_id'))
        invitation = await get_invitation_by_id(session, invitation_id)

        travel = invitation.travel
        owner = await get_travel_owner_by_travel(session, travel)
        members_list = []
        for member in travel.members:
            members_list.append(member.user.name)

        return {
            'name': travel.name,
            'description': travel.description,
            'owner_name': owner.name,
            'members': ', '.join(members_list),
            'members_amount': len(members_list)
        }
