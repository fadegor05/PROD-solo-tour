from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Cancel
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.places import states, selected, keyboards, getters


def categories_window():
    return Window(
        Const('Выберите категорию места, которую вы хотите'),
        keyboards.paginated_categories(selected.on_chosen_category),
        Cancel(Const('Назад')),
        state=states.PlaceMenu.select_category,
        getter=getters.get_categories
    )


def places_window():
    return Window(
        Const('Выберите место, которое вам интересно'),
        keyboards.paginated_places(selected.on_chosen_place),
        Back(Const('Назад')),
        state=states.PlaceMenu.select_place,
        getter=getters.get_places
    )


def place_info_window():
    return Window(
        Format('Место {description}'),
        Back(Const('Назад')),
        state=states.PlaceMenu.view_place,
        getter=getters.get_place
    )