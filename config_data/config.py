"""Модуль загружает токен телеграм бота, список команд бота."""

import os

from dotenv import find_dotenv, load_dotenv

if find_dotenv():
    load_dotenv()
else:
    exit("Переменные окружения не загружены т.к отсутствует файл .env")


BOT_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_COMMANDS = (
    ("players", "🔫Игроки на сервере"),
    ("auto_update_on", "🔄Включить автообновление"),
    ("auto_update_off", "🚫Выключить автообновление"),

)
COMMAND_MESSAGES = ["/" + DEFAULT_COMMANDS[command][0] for command in range(0, len(DEFAULT_COMMANDS))]
COMMAND_MESSAGES.extend(["/start", ])
# укажите текст, который может содержаться в никнеймах ботов для исключения
BOTS_NICKNAMES = ['[BOTik]', 'addons/amxmods']
