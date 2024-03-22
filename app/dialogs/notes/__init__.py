from aiogram_dialog import Dialog

from app.dialogs.notes import windows


def menu_dialogs():
    return [
        Dialog(
            windows.notes_window(),
            windows.note_info_window(),
        )
    ]