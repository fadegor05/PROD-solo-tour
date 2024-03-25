from aiogram.fsm.state import State, StatesGroup


class PlaceMenu(StatesGroup):
    select_place = State()
    view_place = State()