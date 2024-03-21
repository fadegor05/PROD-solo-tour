import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_travels(on_click):
    return ScrollingGroup(
        Select(
            Format('{item.name}'),
            id='s_scroll_travels',
            item_id_getter=operator.attrgetter('id'),
            items='travels',
            on_click=on_click
        ),
        id='travels_id',
        width=1, height=5
    )
