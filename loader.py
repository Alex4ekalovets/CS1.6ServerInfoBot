"""Данный модуль создает экземпляр Телеграм бота"""

from telebot import TeleBot

from config_data import config
from states.bot_state import CurrentState

bot = TeleBot(token=config.BOT_TOKEN)
current_state = CurrentState()
