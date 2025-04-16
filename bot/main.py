import aiohttp
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Замените на ваш токен
TOKEN = "7374201034:AAHZ48nTvc1n4I02veri2ry-mkuFcnd2FFM"
bot = Bot(token=TOKEN)
dp = Dispatcher()
API_LINK = "https://ee7e-62-60-152-151.ngrok-free.app"


async def get_random_user():
    """
    Получает случайного пользователя из API.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_LINK}/gamble/api/users/") as response:
                if response.status == 200:
                    users = await response.json()
                    print(users)
                    if users:
                        return random.choice(users)["lucky_username"]
        except Exception as e:
            print(f"Ошибка при запросе пользователей: {e}")
    return None


@dp.message(Command("gamble"))
async def gamble_handler(message: types.Message):
    """
    Обработчик команды /gamble.
    Отправляет случайного пользователя.
    """
    username = await get_random_user()
    if username:
        await message.answer(f"Случайный пользователь: {username}")
    else:
        await message.answer("Пока нет зарегистрированных пользователей.")


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    """
    Обработчик команды /start.
    Отправляет сообщение с кнопкой для участия в розыгрыше.
    """
    web_app_button = InlineKeyboardButton(
        text="Участвовать в розыгрыше",
        web_app=WebAppInfo(url=f"{API_LINK}/gamble/register/"),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])
    await message.answer(
        "Нажми на кнопку и участвуй в розыгрыше!", reply_markup=keyboard
    )
    user_data = {
        "telegram_id": message.from_user.id,
        "telegram_username": message.from_user.username,
        # Можно добавить дополнительные поля, например:
        # "first_name": message.from_user.first_name,
        # "last_name": message.from_user.last_name,
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_LINK}/register/", json=user_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print("Данные пользователя успешно отправлены на API:", result)
                else:
                    print(
                        "Ошибка при отправке данных пользователя. Код:", response.status
                    )
        except Exception as e:
            print("Ошибка при POST запросе данных пользователя:", e)


async def main():
    """
    Основная функция запуска бота.
    """
    try:
        # Убедитесь, что вы заменили @YourChannelName на реальный ID канала или чата
        await bot.send_message(
            chat_id="@YourChannelName",
            text="Нажми на кнопку и участвуй в розыгрыше!",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Участвовать в розыгрыше",
                            web_app=WebAppInfo(url=f"{API_LINK}/gamble/register/"),
                        )
                    ]
                ]
            ),
        )
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
