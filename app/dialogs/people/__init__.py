from aiogram_dialog import Dialog

from app.dialogs.people import windows


def menu_dialogs():
    return [
        Dialog(
            windows.people_window(),
            windows.person_info_window()
        ),
    ]