from aiogram.fsm.state import StatesGroup, State

class CreateUser(StatesGroup):
    age = State()
    city = State()
    country = State()
    bio = State()