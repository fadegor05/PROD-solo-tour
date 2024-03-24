from typing import Dict

from aiogram_dialog import Data, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Back
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.invitation import states, keyboards, selected, getters
from app.misc.constants import SwitchToWindow


def invitations_window():
    return Window(
        Format('Выберите приглашение, которое хотите 📨\n\n🔑 Ваш код для приглашения другими:\n{code}'),
        keyboards.paginated_invitations(selected.on_chosen_invitation),
        Cancel(Const('⬅️ Назад')),
        state=states.InvitationMenu.select_invitation,
        getter=getters.get_invitations
    )


def invitation_info_window():
    return Window(
        Format('Приглашение {name} ✉️\n{description}\n\n👥 Участники: {members} ({members_amount})\n🏷️ {owner_name}'),
        Button(Const('✅ Принять'), 'invitation_agree', selected.on_invitation_agree),
        Button(Const('❌ Отклонить'), 'invitation_reject', selected.on_invitation_reject),
        Back(Const('⬅️ Назад')),
        state=states.InvitationMenu.select_action,
        getter=getters.get_invitation
    )


async def on_process_result(data: Data, result: Dict, manager: DialogManager):
    if result:
        switch_to_window = result.get('switch_to_window')
        if switch_to_window == SwitchToWindow.SelectInvitation:
            await manager.switch_to(states.InvitationMenu.select_invitation)
