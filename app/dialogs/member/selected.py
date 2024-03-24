from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from app.dialogs.member.states import InviteMember, MemberMenu


async def on_chosen_member(c: CallbackQuery, widget: Select, manager: DialogManager, member_id: str, **kwargs):
    ctx = manager.current_context()
    ctx.dialog_data.update(member_id=member_id)
    await manager.switch_to(MemberMenu.select_action)


#TODO
async def on_invite_member(c: CallbackQuery, widget: Button, manager: DialogManager):
    pass
    #await manager.start(InviteMember.code, data={'travel_id': manager.start_data.get('travel_id')})