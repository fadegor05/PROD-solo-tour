from aiogram.fsm.state import State, StatesGroup


class LocationMenu(StatesGroup):
    select_location = State()
    select_action = State()


class CreateLocation(StatesGroup):
    city = State()
    confirm_city = State()
    arrive_at = State()
    departure_at = State()
