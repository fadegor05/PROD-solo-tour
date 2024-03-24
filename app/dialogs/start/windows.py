from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from app.dialogs.start import states, selected


def start_window():
    return Window(
        Const('Добро Пожаловать в Travel Agent 😎\n\nЗдесь вы можете начать свое комфортное путешествиe в пару кликов и без каких-либо проблем 💼\n\nВыберите тот пункт меню, который хотите'),
        Button(Const('✈️ Мои путешествия'), 'start_travels', selected.on_start_travels),
        Button(Const('✉️ Приглашения'), 'start_invitations', selected.on_start_invitations),
        state=states.StartMenu.select_menu,
    )

def start_age_window():
    return Window(
        Const('Введите свой возраст 🧔‍♂️'),
        TextInput(
            id='start_enter_age',
            on_success=selected.on_entered_age
        ),
        state=states.CreateUser.age
    )


def start_bio_window():
    return Window(
        Const('Напишите немного о себе 😎'),
        TextInput(
            id='start_enter_bio',
            on_success=selected.on_entered_bio
        ),
        state=states.CreateUser.bio
    )


def start_city_window():
    return Window(
        Const('Напишите свой город 🏠'),
        TextInput(
            id='start_enter_city',
            on_success=selected.on_entered_city
        ),
        state=states.CreateUser.city
    )
