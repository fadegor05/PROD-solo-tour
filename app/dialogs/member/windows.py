from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.member import keyboards, selected, states, getters


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
        Button(Const('❌ Исключить'), 'kick_member'),
        Back(Const('⬅️ Назад')),
        state=states.MemberMenu.select_action,
        getter=getters.get_member,
    )
