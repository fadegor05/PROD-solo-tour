from aiogram.types import Message
from aiogram.filters import CommandStart

from app.messages import messages
from app.database import async_session
from app.crud.user import create_user, get_user_by_telegram_id
from app.handlers.router import router

@router.message(CommandStart())
async def start_handler(message: Message):
    async with async_session() as session:
        user = await get_user_by_telegram_id(session, message.from_user.id)
        if not user:
            user = await create_user(session, message.from_user.id)
        await message.answer(messages['start'], parse_mode="Markdown")