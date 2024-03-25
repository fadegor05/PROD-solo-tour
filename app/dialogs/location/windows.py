from typing import Dict

from aiogram_dialog import Window, Data, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Button, Next
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.location import keyboards, selected, states, getters
from app.misc.constants import SwitchToWindow


def locations_window():
    return Window(
        DynamicMedia('image'),
        Const('Выберите локацию, которую хотите 🌎'),
        keyboards.paginated_locations(selected.on_chosen_location),
        Button(Const('📍 Добавить локацию'), 'create_location', selected.on_create_location),
        Cancel(Const('⬅️ Назад')),
        state=states.LocationMenu.select_location,
        getter=getters.get_locations,
    )


def location_info_window():
    return Window(
        Format('Локация {city}, {country} 📍\n\n{weather_dates_type}\n{weather}\n🌡 {temperature} °C\n\nВремя пребывания ⏳\n{arrive_at} - {departure_at}'),
        Button(Const('🏛️ Активности и места'), 'view_places', selected.on_view_places),
        Button(Const('🗑️ Удалить локацию'), 'delete_location', selected.on_delete_location),
        Back(Const('⬅️ Назад')),
        state=states.LocationMenu.select_action,
        getter=getters.get_location,
    )


def location_delete_confirm():
    return Window(
        Const('Вы действительно хотите удалить локацию? 🗑️'),
        Button(Const('✅ Да'), 'delete_location_confirm', selected.on_delete_location_confirm),
        Cancel(Const('⬅️ Назад')),
        state=states.DeleteLocation.delete_location
    )


def location_city_window():
    return Window(
        Const('Введите название города 🗺️'),
        TextInput(
            id='location_enter_city',
            on_success=selected.on_entered_city
        ),
        state=states.CreateLocation.city
    )


def location_confirm_city_window():
    return Window(
        Format('{city}, {country} - Верно? 🌎'),
        Next(Const('✅ Да')),
        Back(Const('❌ Нет')),
        getter=getters.get_city_confirm,
        state=states.CreateLocation.confirm_city
    )


def location_arrive_at_window():
    return Window(
        Const('Введите дату прибытия (в формате 10/03/2024) 📅'),
        TextInput(
            id='location_enter_arrive_at',
            on_success=selected.on_entered_arrive_at
        ),
        state=states.CreateLocation.arrive_at
    )


def location_departure_at_window():
    return Window(
        Const('Введите дату отправления (в формате 10/03/2024) 📅'),
        TextInput(
            id='location_enter_arrive_at',
            on_success=selected.on_entered_departure_at
        ),
        state=states.CreateLocation.departure_at
    )


async def on_process_result(data: Data, result: Dict, manager: DialogManager):
    if result:
        switch_to_window = result.get('switch_to_window')
        if switch_to_window == SwitchToWindow.SelectLocation:
            await manager.switch_to(states.LocationMenu.select_location)