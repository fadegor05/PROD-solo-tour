from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Const

from app.dialogs.travel import states, selected, keyboards, getters


def travels_window():
    return Window(
        Const('Выберите путешествие, которые вы хотите'),
        keyboards.paginated_travels(selected.on_chosen_travel),
        Button(Const('Создать путешествие'), 'create_travel', selected.on_create_travel),
        Cancel(Const('Выход')),
        state=states.TravelMenu.select_travel,
        getter=getters.get_travels,
    )


def travel_name_window():
    return Window(
        Const('Напишите имя путешествия'),
        TextInput(
            id='travel_enter_name',
            on_success=selected.on_entered_name
        ),
        state=states.TravelMenu.travel_name
    )


def travel_description_window():
    return Window(
        Const('Напишите описание путешествия'),
        TextInput(
            id='travel_enter_description',
            on_success=selected.on_entered_description
        ),
        state=states.TravelMenu.travel_description
    )
