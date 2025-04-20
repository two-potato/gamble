import os
import random
import aiohttp
import asyncio
from urllib.parse import urlencode
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.filters import IS_NOT_MEMBER, MEMBER
from aiogram.types import ChatMemberUpdated
import logging

# Настройка логирования в самом начале
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler("bot.log"),  # Сохранение в файл
    ],
)
logger = logging.getLogger(__name__)


# Загрузка настроек из окружения с проверкой
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


try:
    env_vars = load_env_vars()
    TOKEN = env_vars["TELEGRAM_BOT_TOKEN"]
    API_LINK = env_vars["API_LINK"]
    CHANNEL_ID = env_vars["CHANNEL_ID"]
except ValueError as e:
    logger.critical(f"Failed to load environment variables: {e}")
    exit(1)

# Инициализация бота и диспетчера
try:
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    logger.info("Bot initialized successfully")
except Exception as e:
    logger.critical(f"Failed to initialize bot: {e}")
    exit(1)


async def get_random_user():
    """
    Получает случайного зарегистрированного пользователя из внешнего API.
    """
    url = f"{API_LINK}/gamble/api/users/"
    logger.info(f"Fetching users from API: {url}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    users = await resp.json()
                    logger.info(f"Retrieved {len(users)} users")
                    if users:
                        winner = random.choice(users).get("lucky_username")
                        logger.info(f"Selected random user: {winner}")
                        return winner
                    else:
                        logger.info("No users found in API response")
                        return None
                else:
                    logger.warning(
                        f"Unexpected status {resp.status} when fetching users"
                    )
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"Network error in get_random_user: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error in get_random_user: {e}")
            return None


async def check_subscription(user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на канал.
    """
    logger.info(f"Checking subscription status for user_id={user_id}")
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        subscribed = member.status not in ("left", "kicked")
        logger.info(f"Subscription status for {user_id}: {subscribed}")
        return subscribed
    except TelegramUnauthorizedError:
        logger.error("Bot unauthorized to check subscription or channel missing")
        return False
    except Exception as e:
        logger.exception(f"Error checking subscription for {user_id}: {e}")
        return False


# Хэндлер для обработки подписки на канал
# Хэндлер для обработки события изменения статуса участника
@dp.chat_member()
async def on_chat_member_update(event: ChatMemberUpdated):
    # Проверяем, что событие произошло в нужном канале
    if event.chat.id == CHANNEL_ID:
        # Проверяем, что пользователь перешел в статус "member" (подписался)
        if (
            event.new_chat_member.status == "member"
            and event.old_chat_member.status in ["left", "kicked"]
        ):
            user_id = event.from_user.id
            username = (
                event.from_user.username or event.from_user.first_name or "пользователь"
            )
            try:
                # Отправляем сообщение в личный чат пользователю
                await bot.send_message(
                    chat_id=user_id,
                    text=f"Привет, {username}! Спасибо за подписку на наш канал! 🎉\n"
                    f"Теперь ты будешь получать эксклюзивные обновления прямо сюда!",
                )
                logging.info(f"Сообщение отправлено пользователю {user_id}")
            except Exception as e:
                # Логируем ошибку, если не удалось отправить сообщение
                logging.error(
                    f"Ошибка при отправке сообщения пользователю {user_id}: {e}"
                )


@dp.message(Command("gamble"))
async def gamble_handler(message: types.Message):
    """
    Обработчик команды /gamble: выбирает случайного победителя.
    """
    logger.info(f"Received /gamble from {message.from_user.id}")
    winner = await get_random_user()
    if winner:
        logger.info(f"Announcing winner: {winner}")
        await message.answer(f"🎉 Победитель: {winner}")
    else:
        logger.info("No users registered yet")
        await message.answer("Пока нет зарегистрированных пользователей.")


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    """
    Обработчик команды /start: отправляет кнопку WebApp и сразу POST-ит данные пользователя.
    """
    user = message.from_user
    logger.info(f"Received /start from {user.id} ({user.username})")
    is_subscribed = await check_subscription(user.id)
    logger.info(f"-------->{is_subscribed}")

    # Формируем query-параметры для WebApp
    params = {
        "telegram_id": user.id,
        "telegram_username": user.username or "",
        "is_subscribed": int(is_subscribed),
    }
    qs = urlencode(params)
    web_app_url = f"{API_LINK}/gamble/register/?{qs}"
    logger.info(f"WebApp URL: {web_app_url}")

    # Кнопка WebApp
    web_app_button = InlineKeyboardButton(
        text="Участвовать в розыгрыше",
        web_app=WebAppInfo(url=web_app_url),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

    # Отправляем сообщение с кнопкой
    try:
        await message.answer(
            "Нажми на кнопку и участвуй в розыгрыше!", reply_markup=keyboard
        )
        logger.info("Sent WebApp button to user")
    except Exception as e:
        logger.error(f"Failed to send message to user {user.id}: {e}")
        return

    # Асинхронно сохраняем данные пользователя на вашем API
    async with aiohttp.ClientSession() as session:
        try:
            post_url = f"{API_LINK}/gamble/register/"
            logger.info(f"Posting user data to {post_url}: {params}")
            async with session.post(post_url, json=params, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"User data saved successfully: {data}")
                else:
                    logger.error(f"Failed to save user data, status {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Network error posting user data: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error posting user data: {e}")


async def main():
    """
    Основная функция для запуска бота.
    """
    logger.info("Starting bot polling")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Polling failed: {e}")
        await bot.session.close()
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
