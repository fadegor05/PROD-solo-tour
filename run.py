import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from config import TOKEN
from app.database import db_init
from app.handlers.router import router

async def main() -> None:
    await db_init()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stopped')
