from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext

from app.handlers.travel.views import travel_out
from app.messages import messages
from app.handlers.router import router
from app.crud.user import get_user_by_telegram_id
from app.crud.travel import get_travel_by_name, create_travel
from app.database import async_session
from app.handlers.keyboards import get_reply_keyboard
from app.fsm.travel import GetTravel, CreateTravel

from app.handlers.keyboards import TRAVEL_KEYBOARD

@router.message(StateFilter(None), F.text == messages['travel_button'])
async def home_travel_handler(message: Message, state: FSMContext):
    async with async_session() as session:
        user = await get_user_by_telegram_id(session, message.from_user.id)
        buttons = []
        for member in user.travels:
            buttons.append(member.travel.name)
        buttons.append(messages['create_travel_button'])
        keyboard = get_reply_keyboard(*buttons)
        await message.answer(messages['choose_travel'], parse_mode='Markdown', reply_markup=keyboard)
        await state.set_state(GetTravel.name)

@router.message(GetTravel.name, F.text)
async def get_travel_handler(message: Message, state: FSMContext):
    if message.text == messages['create_travel_button']:
        await message.answer(messages['travel_name_input'], parse_mode='Markdown')
        await state.set_state(CreateTravel.name)
        return
    async with async_session() as session:
        travel = await get_travel_by_name(session, message.text)
        if not travel:
            await message.answer(messages['incorrect_input'], parse_mode='Markdown')
            return
        string = await travel_out(travel)
        await message.answer(string, parse_mode='Markdown', reply_markup=TRAVEL_KEYBOARD)
        await state.clear()

@router.message(CreateTravel.name, F.text)
async def get_travel_name_handler(message: Message, state: FSMContext):
    async with async_session() as session:
        travel = await get_travel_by_name(session, message.text)
        if travel:
            await message.answer(messages['incorrect_input'], parse_mode='Markdown')
            return
        await state.update_data(name=message.text)
        await message.answer(messages['travel_description_input'], parse_mode='Markdown')
        await state.set_state(CreateTravel.description)

@router.message(CreateTravel.description, F.text)
async def get_travel_description_handler(message: Message, state: FSMContext):
    async with async_session() as session:
        await state.update_data(description=message.text)
        data = await state.get_data()
        user = await get_user_by_telegram_id(session, message.from_user.id)
        travel = await create_travel(session, data['name'], data['description'], user)
        string = await travel_out(travel)
        await message.answer(string, parse_mode='Markdown', reply_markup=TRAVEL_KEYBOARD)
        await state.clear()