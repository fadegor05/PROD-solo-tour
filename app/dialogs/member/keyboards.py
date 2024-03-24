import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_members(on_click):
    return ScrollingGroup(
        Select(
            Format('👤 {item.user.name}'),
            id='s_scroll_members',
            item_id_getter=operator.attrgetter('id'),
            items='members',
            on_click=on_click
        ),
        id='members_id',
        width=1, height=5
    )