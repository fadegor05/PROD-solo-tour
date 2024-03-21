from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from app.dialogs.start import states, selected


def start_age_window():
    return Window(
        Const('Введите свой возраст'),
        TextInput(
            id='enter_age',
            on_success=selected.on_entered_age
        ),
        state=states.StartMenu.age
    )


def start_bio_window():
    return Window(
        Const('Напишите немного о себе'),
        TextInput(
            id='enter_bio',
            on_success=selected.on_entered_bio
        ),
        state=states.StartMenu.bio
    )


def start_city_window():
    return Window(
        Const('Напишите свой город'),
        TextInput(
            id='enter_city',
            on_success=selected.on_entered_city
        ),
        state=states.StartMenu.city
    )
