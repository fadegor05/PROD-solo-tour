from aiogram_dialog import Dialog

from app.dialogs.travel import windows


def menu_dialogs():
    return [
        Dialog(
            windows.travels_window(),
        )
    ]