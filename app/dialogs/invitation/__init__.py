from aiogram_dialog import Dialog

from app.dialogs.invitation import windows


def menu_dialogs():
    return [
        Dialog(
            windows.invitations_window(),
            windows.invitation_info_window(),
            on_process_result=windows.on_process_result,
        ),
    ]