"""Данный модуль создает экземпляр Телеграм бота"""

from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config_data import config
from Server.players import ServerStatus

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
server_status = ServerStatus()
