import os
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.handlers import start, new, on_message


bot = Bot(os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

dp.register_message_handler(start, commands=['start'])
dp.register_message_handler(new, commands=['new'])
dp.register_message_handler(on_message, content_types=['text'])


if __name__ == '__main__':
    asyncio.run(dp.start_polling())
