import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_invitations(on_click):
    return ScrollingGroup(
        Select(
            Format('✉️ {item.travel.name}'),
            id='s_scroll_invitations',
            item_id_getter=operator.attrgetter('id'),
            items='invitations',
            on_click=on_click
        ),
        id='invitations_id',
        width=1, height=5
    )