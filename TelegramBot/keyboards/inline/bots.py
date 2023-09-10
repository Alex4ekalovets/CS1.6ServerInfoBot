"""Модуль создания клавиатуры выбора карты."""
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from config_data.config import MAPS


def bots() -> InlineKeyboardMarkup:
    """Создание клавиатуры с перечнем карт."""
    buttons = [
        [InlineKeyboardButton("Убрать ботов", callback_data="bot_kick")],
        [InlineKeyboardButton("+ бот за контров", callback_data="bot_add_ct")],
        [InlineKeyboardButton("+ бот за терров", callback_data="bot_add_t")],
    ]
    return InlineKeyboardMarkup(buttons)
