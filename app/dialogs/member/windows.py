from typing import Dict

from aiogram_dialog import Window, DialogManager, Data
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.member import keyboards, selected, states, getters
from app.misc.constants import SwitchToWindow


def members_window():
    return Window(
        Const('Выберите участника, который вам интересен 👥'),
        keyboards.paginated_members(selected.on_chosen_member),
        Button(Const('✉️ Пригласить пользователя'), 'invite_member', selected.on_invite_member),
        Cancel(Const('⬅️ Назад')),
        state=states.MemberMenu.select_member,
        getter=getters.get_members,
    )


def member_info_window():
    return Window(
        Format('Участник {name} ({age}) 👤\n\n{bio}\n\n{is_owner_icon}'),
        Button(Const('❌ Исключить'), 'kick_member', selected.on_member_kick),
        Back(Const('⬅️ Назад')),
        state=states.MemberMenu.select_action,
        getter=getters.get_member,
    )


def member_kick_confirm_window():
    return Window(
        Format('Вы действительно хотите исключить участника? ❌'),
        Button(Const('✅ Да'), 'member_kick_confirm_button', selected.on_member_kick_confirm),
        Cancel(Const('⬅️ Назад')),
        state=states.KickMember.kick_member
    )


def member_invite_window():
    return Window(
        Const('Введите код пользователя, которого вы хотите пригласить 🔑'),
        TextInput(
            id='member_enter_code',
            on_success=selected.on_entered_code
        ),
        state=states.InviteMember.code
    )


async def on_process_result(data: Data, result: Dict, manager: DialogManager):
    if result:
        switch_to_window = result.get('switch_to_window')
        if switch_to_window == SwitchToWindow.SelectMember:
            await manager.switch_to(states.MemberMenu.select_member)