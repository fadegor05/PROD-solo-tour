from aiogram_dialog import Dialog

from app.dialogs.location import windows


def menu_dialogs():
    return [
        Dialog(
            windows.locations_window(),
            windows.location_info_window(),
            on_process_result=windows.on_process_result,
        ),
        Dialog(
            windows.location_city_window(),
            windows.location_confirm_city_window(),
            windows.location_arrive_at_window(),
            windows.location_departure_at_window(),
        ),
        Dialog(
            windows.location_delete_confirm(),
        ),
    ]