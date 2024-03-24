from aiogram_dialog import Dialog

from app.dialogs.member import windows


def menu_dialogs():
    return [
        Dialog(
            windows.members_window(),
            windows.member_info_window(),
            on_process_result=windows.on_process_result,
        ),
        Dialog(
            windows.member_invite_window()
        )
    ]