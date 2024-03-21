from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_inline_keyboard(data: dict):
    keyboard = InlineKeyboardBuilder()

    for text in data:
        keyboard.add(InlineKeyboardButton(text=data[text], callback_data=text))
    
    return keyboard.as_markup()