from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from app.crud.invitation import get_invitation_by_id, delete_invitation
from app.crud.member import create_member
from app.database import async_session
from app.dialogs.invitation.states import InvitationMenu
from app.misc.constants import SwitchToWindow


async def on_chosen_invitation(c: CallbackQuery, widget: Select, manager: DialogManager, invitation_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(invitation_id=invitation_id)
    await manager.switch_to(InvitationMenu.select_action)


async def on_invitation_agree(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    async with async_session() as session:
        invitation_id = int(manager.dialog_data.get('invitation_id'))
        invitation = await get_invitation_by_id(session, invitation_id)
        name = invitation.travel.name
        await create_member(session, invitation.travel, invitation.user)
        await delete_invitation(session, invitation)
        await c.answer(f'Приглашение {name} было успешно принято ✅')
    await manager.done(
        {
            'switch_to_window': SwitchToWindow.SelectInvitation
        }
    )


async def on_invitation_reject(c: CallbackQuery, widget: Button, manager: DialogManager, **kwargs):
    async with async_session() as session:
        invitation_id = int(manager.dialog_data.get('invitation_id'))
        invitation = await get_invitation_by_id(session, invitation_id)
        name = invitation.travel.name
        await delete_invitation(session, invitation)
        await c.answer(f'Приглашение {name} было успешно отклонено ✅')
    await manager.done(
        {
            'switch_to_window': SwitchToWindow.SelectInvitation
        }
    )