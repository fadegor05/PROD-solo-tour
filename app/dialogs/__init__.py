from . import travel, start, note, location, member, invitation


def get_dialogs():
    return [
        *travel.menu_dialogs(),
        *start.menu_dialogs(),
        *note.menu_dialogs(),
        *location.menu_dialogs(),
        *member.menu_dialogs(),
        *invitation.menu_dialogs(),
    ]