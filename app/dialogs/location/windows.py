from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Button, Next
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


def location_city_window():
    return Window(
        Const('Введите название города'),
        TextInput(
            id='location_enter_city',
            on_success=selected.on_entered_city
        ),
        state=states.CreateLocation.city
    )


def location_confirm_city_window():
    return Window(
        Format('{city}, {country} - Верно?'),
        Next(Const('Да')),
        Back(Const('Нет')),
        getter=getters.get_city_confirm,
        state=states.CreateLocation.confirm_city
    )


def location_arrive_at_window():
    return Window(
        Const('Введите дату прибытия (например, 23/03/2024)'),
        TextInput(
            id='location_enter_arrive_at',
            on_success=selected.on_entered_arrive_at
        ),
        state=states.CreateLocation.arrive_at
    )


def location_departure_at_window():
    return Window(
        Const('Введите дату отправления (например, 23/03/2024)'),
        TextInput(
            id='location_enter_arrive_at',
            on_success=selected.on_entered_departure_at
        ),
        state=states.CreateLocation.departure_at
    )
