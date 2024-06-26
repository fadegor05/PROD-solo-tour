from aiogram.fsm.state import StatesGroup, State


class TravelMenu(StatesGroup):
    select_travel = State()
    select_action = State()


class CreateTravel(StatesGroup):
    name = State()
    description = State()


class DeleteTravel(StatesGroup):
    delete_travel = State()
