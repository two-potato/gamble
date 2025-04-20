import os
import logging
from aiogram import Bot, Dispatcher
from gb_handlers import (
    start_handler,
    gamble_handler,
    on_chat_member_update,
)
from aiogram.filters import Command

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log"),
    ],
)
logger = logging.getLogger(__name__)


def load_env_vars():
    required_vars = {
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "API_LINK": os.getenv("API_LINK"),
        "CHANNEL_ID": os.getenv("CHANNEL_ID"),
    }
    for var_name, var_value in required_vars.items():
        if not var_value:
            logger.critical(f"Missing environment variable: {var_name}")
            raise ValueError(f"Environment variable {var_name} is not set")
    return required_vars


async def main():
    try:
        env_vars = load_env_vars()
        TOKEN = env_vars["TELEGRAM_BOT_TOKEN"]
        API_LINK = env_vars["API_LINK"]
        CHANNEL_ID = env_vars["CHANNEL_ID"]

        bot = Bot(token=TOKEN)
        dp = Dispatcher()

        dp.message.register(
            start_handler,
            Command(commands=["start"]),
            API_LINK=API_LINK,
            CHANNEL_ID=CHANNEL_ID,
        )

        dp.message.register(
            gamble_handler, Command(commands=["gamble"]), API_LINK=API_LINK
        )

        dp.chat_member.register(on_chat_member_update, CHANNEL_ID=CHANNEL_ID)

        logger.info("Starting bot polling")
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"Polling failed: {e}")
        await bot.session.close()
        exit(1)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
