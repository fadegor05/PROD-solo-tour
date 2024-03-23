from aiogram_dialog import Dialog

from app.dialogs.travel import windows


def menu_dialogs():
    return [
        Dialog(
            windows.travels_window(),
            windows.travel_info_window(),
            on_process_result=windows.on_process_result,
        ),
        Dialog(
            windows.travel_name_window(),
            windows.travel_description_window(),
        ),
        Dialog(
            windows.travel_delete_confirm_window(),
        ),
    ]