from aiogram.fsm.state import StatesGroup, State


class StartMenu(StatesGroup):
    age = State()
    bio = State()
    city = State()