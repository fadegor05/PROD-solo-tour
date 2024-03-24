from aiogram.fsm.state import StatesGroup, State


class MemberMenu(StatesGroup):
    select_member = State()
    select_action = State()


class InviteMember(StatesGroup):
    code = State()


class KickMember(StatesGroup):
    kick_member = State()