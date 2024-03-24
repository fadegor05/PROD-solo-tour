from aiogram.fsm.state import State, StatesGroup


class InvitationMenu(StatesGroup):
    select_invitation = State()
    select_action = State()