from . import travel, start


def get_dialogs():
    return [
        *travel.menu_dialogs(),
        *start.menu_dialogs()
    ]