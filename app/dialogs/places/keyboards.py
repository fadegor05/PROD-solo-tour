import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_places(on_click):
    return ScrollingGroup(
        Select(
            Format('{item.description}'),
            id='s_scroll_places',
            item_id_getter=operator.attrgetter('id'),
            items='places',
            on_click=on_click
        ),
        id='places_id',
        width=1, height=5
    )