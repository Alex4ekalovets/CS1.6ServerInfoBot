"""Модуль создания клавиатуры выбора карты."""
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from config_data.config import MAPS


def maps() -> InlineKeyboardMarkup:
    """Создание клавиатуры с перечнем карт."""
    buttons = [
        [InlineKeyboardButton(new_map, callback_data=f"changelevel {new_map}")] for new_map in MAPS
    ]
    return InlineKeyboardMarkup(buttons)
