from aiogram.fsm.state import State, StatesGroup


class LocationMenu(StatesGroup):
    select_location = State()
    select_action = State()
