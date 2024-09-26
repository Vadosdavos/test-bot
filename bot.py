import asyncio
import logging
from aiogram import Bot, Dispatcher
from utils.config_reader import config
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.chat_action import ChatActionMiddleware

from handlers import books, group_answers, meme, start
from utils.memes import get_memes

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(
            token=config.bot_token.get_secret_value(), 
            default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ))
    dp = Dispatcher()
    dp.message.middleware(ChatActionMiddleware())
    dp.include_routers(start.router, meme.router, books.router)
    # dp.include_routers(start.router, meme.router, group_answers.router, books.router)

    memes = await get_memes()
    memes_ids = {}

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, memes=memes, memes_ids=memes_ids)

if __name__ == "__main__":
    asyncio.run(main())