from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from urllib.parse import urlencode


def create_webapp_keyboard(user, API_LINK, is_subscribed):
    params = {
        "telegram_id": user.id,
        "telegram_username": user.username or "",
        "is_subscribed": int(is_subscribed),
    }
    qs = urlencode(params)
    web_app_url = f"{API_LINK}/gamble/register/?{qs}"

    web_app_button = InlineKeyboardButton(
        text="Участвовать в розыгрыше",
        web_app=WebAppInfo(url=web_app_url),
    )
    return InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])
