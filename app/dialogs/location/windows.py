from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Cancel, Button
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.location import keyboards, selected, states, getters


def locations_window():
    return Window(
        Const('Выберите локацию, которую хотите'),
        keyboards.paginated_locations(selected.on_chosen_location),
        Button(Const('Добавить локацию'), 'create_location', selected.on_create_location),
        Cancel(Const('Назад')),
        state=states.LocationMenu.select_location,
        getter=getters.get_locations,
    )


def location_info_window():
    return Window(
        Format('Локация {city}, {country}\n\nПрибытие: {arrive_at}\nОтправление: {departure_at}'),
        Back(Const('Назад')),
        state=states.LocationMenu.select_action,
        getter=getters.get_location,
    )

"""
def location_city_window():
    return Window(
        Const('Введите название заметки'),
        TextInput(
            id='note_enter_name',
            on_success=selected.on_entered_name
        ),
        state=states.CreateNote.name
    )


def note_is_public_window():
    return Window(
        Const('Будет ли эта заметка публичной?'),
        Button(Const('Да'), 'note_public_true', selected.on_is_public_true),
        Button(Const('Нет'), 'note_public_false', selected.on_is_public_false),
        state=states.CreateNote.is_public
    )


def note_text_window():
    return Window(
        Const('Введите текст заметки'),
        TextInput(
            id='note_enter_text',
            on_success=selected.on_entered_text
        ),
        state=states.CreateNote.text
    )
"""