from aiogram.types import Message
from aiogram.filters import Command

from app.handlers.router import router
from app.messages import messages
from app.handlers.keyboards import HOME_KEYBOARD


@router.message(Command('home'))
async def home_handler(message: Message):
    await message.answer(messages['home'], parse_mode='Markdown', reply_markup=HOME_KEYBOARD)