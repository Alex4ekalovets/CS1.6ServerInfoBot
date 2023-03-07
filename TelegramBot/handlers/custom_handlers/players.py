"""Модуль для обработки команд боту.

Functions:
    show_servers_players:
        Показывает количество игроков на сервере.
    auto_update_on:
        Запускает автообновление количества игроков на сервере
    auto_update_off:
        Отключает автообновление количества игроков на сервере
    show_players_after_changes:
        Показывает количество игроков, если оно изменилось
"""
import time

from telebot.types import Message

from loader import bot

from Server.players import player_on_server, ServerStatus

from utils.logging import logger


@bot.message_handler(commands=["players"])
def show_servers_players(message: Message) -> None:
    """Показывает количество игроков на сервере."""
    try:
        players = player_on_server()
    except Exception as ex:
        logger.error(f'Ошибка при обращении к серверу {ex}')
    else:
        players_names = '\n'.join(players['names'])
        bot.send_message(
            message.chat.id,
            f"Человек на сервере: {players['players_count']}:\n"
            f"{players_names}\nБотов: {players['bots_count']}"
        )


@bot.message_handler(commands=["auto_update_on"])
def auto_update_on(message: Message) -> None:
    """
    Запускает автообновление количества игроков на сервере.

    Запускается по таймеру одного чата, но выводит информацию во всех чатах, где включено автообновление
    """
    ServerStatus.chats_id_auto_update.add(message.chat.id)
    if len(ServerStatus.chats_id_auto_update) == 1:
        while True:
            show_players_after_changes()
            logger.info(f"Чатов с автообновлением: {len(ServerStatus.chats_id_auto_update)}")
            if len(ServerStatus.chats_id_auto_update) == 0:
                logger.info("Автообновление отключено")
                break
            time.sleep(10)


@bot.message_handler(commands=["auto_update_off"])
def auto_update_off(message: Message) -> None:
    """Отключает автообновление количества игроков на сервере."""
    if message.chat.id in ServerStatus.chats_id_auto_update:
        ServerStatus.chats_id_auto_update.remove(message.chat.id)


def show_players_after_changes():
    """Показывает количество игроков, если оно изменилось."""
    try:
        players = player_on_server()
    except Exception as ex:
        logger.error(f'Ошибка при обращении к серверу {ex}')
    else:
        if ServerStatus.players != players['names']:
            for chat_id in ServerStatus.chats_id_auto_update:
                ServerStatus.players = players['names']
                players_names = '\n'.join(players['names'])
                bot.send_message(
                    chat_id,
                    f"Человек на сервере: {players['players_count']}:\n"
                    f"{players_names}"
                )
                logger.success(f"Направлен ответ в чат с id: {chat_id}")
