from aiogram.fsm.state import StatesGroup, State


class PersonMenu(StatesGroup):
    select_person = State()
    view_person = State()