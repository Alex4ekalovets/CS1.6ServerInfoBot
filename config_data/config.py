"""Модуль загружает токен телеграм бота, список команд бота."""

import os

from dotenv import find_dotenv, load_dotenv

if find_dotenv():
    load_dotenv()
else:
    exit("Переменные окружения не загружены т.к отсутствует файл .env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
TG_ID_FOR_LOGS = os.getenv("TG_ID_FOR_LOGS")
DEFAULT_COMMANDS = (
    ("players", "🔫Игроки на сервере"),
    ("auto_update_on", "🔄Включить автообновление"),
    ("auto_update_off", "🚫Выключить автообновление"),
    ("change_map", "Сменить карту"),
    ("bots_control", "Управление ботами"),
)
COMMAND_MESSAGES = [
    "/" + DEFAULT_COMMANDS[command][0] for command in range(0, len(DEFAULT_COMMANDS))
]
COMMAND_MESSAGES.extend(
    [
        "/start",
    ]
)
# укажите текст, который может содержаться в никнеймах ботов для исключения
BOTS_NICKNAMES = ["[BOTik]", "addons/", "B_"]
# задержка при обращении к сайту для запроса количества игроков
DELAY = 10
#  укажите True, если необходимо удалять предыдущее сообщение бота при включенном автоматическом обновлении
DELETE_PREVIOUS_MESSAGE = True
# введите ip сервера по примеру ниже для хостинга серверов https://csserv.ru/
SERVER_IP = '90.189.165.248_27035'
MAPS = (
    "aim_headshot",
    "aim_map",
    "aim_map2",
    "cs_assault",
    "cs_deathmatch",
    "cs_italy",
    "cs_mansion",
    "cs_mansion_snow",
    "de_aztec",
    "de_aztec2x2",
    "de_clan1_mill_2x2",
    "de_dust",
    "de_dust2",
    "de_dust2_2x2",
    "de_dust2_2x2_winter",
    "de_dust2_2x2_xmas",
    "de_dust2_3x3",
    "de_inferno",
    "de_inferno_2x2",
    "de_mirage",
    "de_mirage_2x2",
    "de_tuscan",
    "de_tuscan_2x2",
    "fy_pool_day",
    "fy_pool_night",
)