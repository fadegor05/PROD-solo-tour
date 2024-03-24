from aiogram_dialog import Dialog

from app.dialogs.note import windows


def menu_dialogs():
    return [
        Dialog(
            windows.notes_window(),
            windows.note_info_window(),
            on_process_result=windows.on_process_result,
        ),
        Dialog(
            windows.note_name_window(),
            windows.note_is_public_window(),
            windows.note_text_window(),
        ),
        Dialog(
            windows.note_delete_confirm(),
        ),
    ]