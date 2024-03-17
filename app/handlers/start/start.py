from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
import geocoder

from app.handlers.keyboards import HOME_KEYBOARD
from app.fsm.user import CreateUser
from app.messages import messages
from app.database import async_session
from app.crud.user import create_user, get_user_by_telegram_id, update_user_detailed_by_telegram_id
from app.handlers.router import router

@router.message(StateFilter(None), CommandStart())
async def start_handler(message: Message, state: FSMContext):
    async with async_session() as session:
        user = await get_user_by_telegram_id(session, message.from_user.id)
        if not user:
            user = await create_user(session, message.from_user.id, message.from_user.first_name)
        await message.answer(f'{messages['start']}\n\n{messages['age_input']}', parse_mode='Markdown')
        await state.set_state(CreateUser.age)


@router.message(CreateUser.age, F.text)
async def add_age_user_start_handler(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
    except:
        await message.answer(messages['incorrect_input'], parse_mode='Markdown')
        return
    await message.answer(messages['city_input'] , parse_mode='Markdown')
    await state.set_state(CreateUser.city)
    

@router.message(CreateUser.city, F.text)
async def add_city_user_start_handler(message: Message, state: FSMContext):
    try:
        city = str(message.text)
        geo = geocoder.osm(city)
        if not geo.country or not geo.city:
            await message.answer(messages['incorrect_input'], parse_mode='Markdown')
            return
        await state.update_data(city=geo.city, country=geo.country)
        await message.answer(f'*Ваше местоположение: {geo.country}, {geo.city}* 📍', parse_mode='Markdown')
    except:
        await message.answer(messages['incorrect_input'], parse_mode='Markdown')
        return
    await message.answer(messages['bio_input'], parse_mode='Markdown')
    await state.set_state(CreateUser.bio)

@router.message(CreateUser.bio, F.text)
async def add_city_user_start_handler(message: Message, state: FSMContext):
    try:
        bio = str(message.text)
        await state.update_data(bio=bio)
    except:
        await message.answer(messages['incorrect_input'], parse_mode='Markdown')
        return
    data = await state.get_data()
    async with async_session() as session:
        await update_user_detailed_by_telegram_id(session, message.from_user.id, data['age'], data['city'], data['country'], data['bio'])
    await message.answer(messages['home'], parse_mode='Markdown', reply_markup=HOME_KEYBOARD)
    await state.clear()