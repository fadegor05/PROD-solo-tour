from . import travel, start, notes


def get_dialogs():
    return [
        *travel.menu_dialogs(),
        *start.menu_dialogs(),
        *notes.menu_dialogs(),
    ]