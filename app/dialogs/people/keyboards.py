import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_people(on_click):
    return ScrollingGroup(
        Select(
            Format('👤 {item.name} ({item.age})'),
            id='s_scroll_people',
            item_id_getter=operator.attrgetter('id'),
            items='people',
            on_click=on_click
        ),
        id='people_id',
        width=1, height=5
    )
