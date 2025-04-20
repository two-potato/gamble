import random
from aiogram import types
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from aiogram.exceptions import TelegramUnauthorizedError
import aiohttp
import logging
from gb_keyboards import create_webapp_keyboard

logger = logging.getLogger(__name__)


async def check_subscription(bot, CHANNEL_ID, user_id: int) -> bool:
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


async def on_chat_member_update(event: ChatMemberUpdated, bot, CHANNEL_ID):
    if event.chat.id == CHANNEL_ID:
        if (
            event.new_chat_member.status == "member"
            and event.old_chat_member.status in ["left", "kicked"]
        ):
            user_id = event.from_user.id
            username = (
                event.from_user.username or event.from_user.first_name or "пользователь"
            )
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=f"Привет, {username}! Спасибо за подписку на наш канал! 🎉\n"
                    f"Теперь ты будешь получать эксклюзивные обновления прямо сюда!",
                )
                logger.info(f"Сообщение отправлено пользователю {user_id}")
            except Exception as e:
                logger.error(
                    f"Ошибка при отправке сообщения пользователю {user_id}: {e}"
                )


async def gamble_handler(message: types.Message, API_LINK):
    logger.info(f"Received /gamble from {message.from_user.id}")
    winner = await get_random_user(API_LINK)
    if winner:
        logger.info(f"Announcing winner: {winner}")
        await message.answer(f"🎉 Победитель: {winner}")
    else:
        logger.info("No users registered yet")
        await message.answer("Пока нет зарегистрированных пользователей.")


async def start_handler(message: types.Message, bot, API_LINK, CHANNEL_ID):
    user = message.from_user
    logger.info(f"Received /start from {user.id} ({user.username})")
    is_subscribed = await check_subscription(bot, CHANNEL_ID, user.id)

    keyboard = create_webapp_keyboard(user, API_LINK, is_subscribed)

    try:
        await message.answer(
            "Нажми на кнопку и участвуй в розыгрыше!", reply_markup=keyboard
        )
        logger.info("Sent WebApp button to user")
    except Exception as e:
        logger.error(f"Failed to send message to user {user.id}: {e}")
        return

    async with aiohttp.ClientSession() as session:
        try:
            post_url = f"{API_LINK}/gamble/register/"
            params = {
                "telegram_id": user.id,
                "telegram_username": user.username or "",
                "is_subscribed": int(is_subscribed),
            }
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


async def get_random_user(API_LINK):
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
