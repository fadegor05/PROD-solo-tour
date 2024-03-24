from aiogram_dialog import Dialog

from app.dialogs.member import windows


def menu_dialogs():
    return [
        Dialog(
            windows.members_window(),
            windows.member_info_window(),
        ),
    ]