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
def auto_update_on(message: Message) -> None:
    """Показывает количество игроков на сервере."""
    ServerStatus.chats_id_auto_update.add(message.chat.id)
    while True:
        show_players_after_changes()
        time.sleep(10)


@bot.message_handler(commands=["auto_update_off"])
def auto_update_off(message: Message) -> None:
    ServerStatus.chats_id_auto_update.remove(message.chat.id)


def show_players_after_changes():
    for chat_id in ServerStatus.chats_id_auto_update:
        try:
            players = player_on_server()
        except Exception as ex:
            logger.error(f'Ошибка при обращении к серверу {ex}')
        else:
            if ServerStatus.players != players['names']:
                logger.info("Количество игроков изменилось")
                ServerStatus.players = players['names']
                players_names = '\n'.join(players['names'])
                bot.send_message(
                    chat_id,
                    f"Человек сервере сейчас: {players['players_count']}:\n{players_names}\nБотов: {players['bots_count']}"
                )
            logger.success(f"Направлен ответ пользователю{chat_id}")



