from aiogram.fsm.state import StatesGroup, State


class TravelMenu(StatesGroup):
    select_travel = State()
    select_action = State()
