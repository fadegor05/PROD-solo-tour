from aiogram.fsm.state import State, StatesGroup


class NoteMenu(StatesGroup):
    select_note = State()
    select_action = State()