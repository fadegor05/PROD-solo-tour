from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Select

from app.crud.invitation import create_invitation, is_user_invited_to_travel
from app.crud.member import get_member_by_id, delete_member
from app.crud.travel import is_user_travel_owner_by_user, get_travel_by_id, is_user_travel_member
from app.crud.user import get_user_by_telegram_id, get_user_by_uuid
from app.database import async_session
from app.dialogs.member.states import InviteMember, MemberMenu, KickMember
from app.misc.constants import SwitchToWindow


async def on_chosen_member(c: CallbackQuery, widget: Select, manager: DialogManager, member_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(member_id=member_id)
    await manager.switch_to(MemberMenu.select_action)


async def on_member_kick(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(KickMember.kick_member, {'member_id': manager.dialog_data.get('member_id'),
                                                 'travel_id': manager.start_data.get('travel_id')})


async def on_member_kick_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    async with async_session() as session:
        travel_id = int(manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)
        user_id = manager.middleware_data.get('event_chat').id
        user = await get_user_by_telegram_id(session, user_id)
        is_owner = await is_user_travel_owner_by_user(session, travel, user)
        if not is_owner:
            await c.answer('У вас недостаточно прав')
            await manager.done()
            return
        member_id = int(manager.start_data.get('member_id'))
        member = await get_member_by_id(session, member_id)
        name = member.user.name
        if member.is_owner:
            await c.answer(f'Пользователь {name} является организатором ❌')
            await manager.done()
            return
        await delete_member(session, member)
        await c.answer(f'Пользователь {name} был успешно исключен ✅')
    await manager.done(
        {
            'switch_to_window': SwitchToWindow.SelectMember
        }
    )


async def on_invite_member(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(InviteMember.code, data={'travel_id': manager.start_data.get('travel_id')})


async def on_entered_code(m: Message, widget: TextInput, manager: DialogManager, code, **kwargs):
    async with async_session() as session:
        travel_id = int(manager.start_data.get('travel_id'))
        travel = await get_travel_by_id(session, travel_id)
        user = await get_user_by_uuid(session, code)
        if not user or await is_user_travel_member(session, travel, user) or await is_user_invited_to_travel(session, travel, user):
            await m.reply('Попробуйте еще раз ⚠️')
            return
        await create_invitation(session, travel, user)
        await m.answer(f'Пользователю {user.name} было успешно отправлено приглашение в путешествие {travel.name}')
        await manager.done()
