from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from app.database import async_session
from app.dialogs.travel.states import TravelMenu
from app.dialogs.start.states import StartMenu
from app.handlers.router import router
from app.crud.user import get_user_by_telegram_id, create_user


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    async with async_session() as session:
        user = await get_user_by_telegram_id(session, message.from_user.id)
        if not user:
            await create_user(session, message.from_user.id, message.from_user.first_name)
            await dialog_manager.start(StartMenu.age, mode=StartMode.RESET_STACK)
            return
        await dialog_manager.start(TravelMenu.select_travel, mode=StartMode.RESET_STACK)
