"""Модуль для обработки команд боту.

Functions:
    start_hotels_search:
        Показывает количество игроков на сервере.
"""
import time

from telebot.types import Message

from loader import bot

from Server.players import player_on_server, ServerStatus

from utils.logging import logger


@bot.message_handler(commands=["players"])
def show_servers_players(message: Message) -> None:
    """Показывает количество игроков на сервере."""
    players = player_on_server()
    players_names = '\n'.join(players['names'])
    bot.send_message(
        message.chat.id,
        f"Человек сервере сейчас: {players['players_count']}:\n{players_names}\nБотов: {players['bots_count']}"
    )


@bot.message_handler(commands=["auto_update_on"])
def send_players_info(message: Message) -> None:
    """Показывает количество игроков на сервере."""
    ServerStatus.auto_update = True
    while ServerStatus.auto_update:
        players = player_on_server()
        if ServerStatus.players != players['names']:
            logger.info("Количество игроков изменилось")
            ServerStatus.players = players['names']
            players_names = '\n'.join(players['names'])
            bot.send_message(
                message.chat.id,
                f"Человек сервере сейчас: {players['players_count']}:\n{players_names}\nБотов: {players['bots_count']}"
            )
        time.sleep(10)
        logger.info("Направлен ответ пользователю")


@bot.message_handler(commands=["auto_update_off"])
def auto_update_off(message: Message) -> None:
    ServerStatus.auto_update = False
