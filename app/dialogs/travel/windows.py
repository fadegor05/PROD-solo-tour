from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Button, Back
from aiogram_dialog.widgets.text import Const, Format

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


def travel_info_window():
    return Window(
        Format(
            'Путешествие {travel_name}\n{travel_description}\n\nКоличество участников: {members_amount}\nОрганизатор: {owner_name}'),
        Button(Const('Заметки'), 'travel_notes_button', selected.on_travel_notes),
        Button(Const('Локации'), 'travel_locations_button'),
        Button(Const('Участники'), 'travel_members_button'),
        Back(Const('Назад')),
        state=states.TravelMenu.select_action,
        getter=getters.get_travel
    )


def travel_name_window():
    return Window(
        Const('Напишите имя путешествия'),
        TextInput(
            id='travel_enter_name',
            on_success=selected.on_entered_name
        ),
        state=states.CreateTravel.name
    )


def travel_description_window():
    return Window(
        Const('Напишите описание путешествия'),
        TextInput(
            id='travel_enter_description',
            on_success=selected.on_entered_description
        ),
        state=states.CreateTravel.description
    )
