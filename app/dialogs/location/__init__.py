from aiogram_dialog import Dialog

from app.dialogs.location import windows


def menu_dialogs():
    return [
        Dialog(
            windows.locations_window(),
            windows.location_info_window(),
        ),
    ]