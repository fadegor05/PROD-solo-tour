import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_categories(on_click):
    return ScrollingGroup(
        Select(
            Format('📢 {item.name}'),
            id='s_scroll_categories',
            item_id_getter=operator.attrgetter('slug'),
            items='categories',
            on_click=on_click
        ),
        id='categories_id',
        width=1, height=5
    )


def paginated_places(on_click):
    return ScrollingGroup(
        Select(
            Format('🧭 {item.title}'),
            id='s_scroll_places',
            item_id_getter=operator.attrgetter('id'),
            items='places',
            on_click=on_click
        ),
        id='places_id',
        width=1, height=5
    )