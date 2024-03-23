import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_locations(on_click):
    return ScrollingGroup(
        Select(
            Format('{item.city}'),
            id='s_scroll_notes',
            item_id_getter=operator.attrgetter('id'),
            items='locations',
            on_click=on_click
        ),
        id='notes_id',
        width=1, height=5
    )