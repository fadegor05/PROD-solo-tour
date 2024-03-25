from aiogram.fsm.state import StatesGroup, State


class StartMenu(StatesGroup):
    select_menu = State()


class CreateUser(StatesGroup):
    age = State()
    bio = State()
    city = State()
    confirm_city = State()