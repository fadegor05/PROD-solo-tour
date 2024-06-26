import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_notes(on_click):
    return ScrollingGroup(
        Select(
            Format('📖 {item.name} - {item.user.name}'),
            id='s_scroll_notes',
            item_id_getter=operator.attrgetter('id'),
            items='notes',
            on_click=on_click
        ),
        id='notes_id',
        width=1, height=5
    )