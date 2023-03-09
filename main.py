"""Модуль запуска телеграмм бота."""
import threading

import schedule as schedule
from telebot import custom_filters, types

from TelegramBot import handlers
from TelegramBot.handlers.custom_handlers.players import auto_update
from config_data.config import DELAY
from loader import bot
from utils.set_bot_commands import set_default_commands


def starter():
    """Запускает функцию auto_update каждые DELAY секунд"""
    schedule.every(DELAY).seconds.do(auto_update)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    set_default_commands(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    t2 = threading.Thread(target=starter)
    t2.start()
    bot.infinity_polling()



