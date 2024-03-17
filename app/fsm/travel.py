from aiogram.fsm.state import StatesGroup, State

class CreateTravel(StatesGroup):
    name = State()
    description = State()

class GetTravel(StatesGroup):
    name = State()