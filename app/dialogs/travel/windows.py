from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from app.dialogs.travel import states, selected, keyboards, getters


def travels_window():
    return Window(
        Const('Выберите путешествие, которые вы хотите'),
        keyboards.paginated_travels(selected.on_chosen_travel),
        Cancel(Const('Выход')),
        state=states.TravelMenu.select_travel,
        getter=getters.get_travels,
    )