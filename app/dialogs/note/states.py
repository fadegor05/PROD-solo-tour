from aiogram.fsm.state import State, StatesGroup


class NoteMenu(StatesGroup):
    select_note = State()
    select_action = State()


class CreateNote(StatesGroup):
    name = State()
    is_public = State()
    text = State()
