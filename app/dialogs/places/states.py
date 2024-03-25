from aiogram.fsm.state import State, StatesGroup


class PlaceMenu(StatesGroup):
    select_category = State()
    select_place = State()
    view_place = State()