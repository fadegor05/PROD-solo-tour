from aiogram_dialog import Dialog

from app.dialogs.places import windows


def menu_dialogs():
    return [
        Dialog(
            windows.categories_window(),
            windows.places_window(),
            windows.place_info_window(),
        ),
    ]

