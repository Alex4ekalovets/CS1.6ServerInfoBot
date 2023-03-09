"""Модуль для обработки команд боту.

Functions:
    show_players_on_server:
        Показывает количество игроков на сервере.
    auto_update_on:
        Запускает автообновление количества игроков на сервере
    auto_update_off:
        Отключает автообновление количества игроков на сервере
    auto_update:
        Автообновление
    show_players_if_changed:
        Показывает количество игроков, если оно изменилось
"""

from telebot.types import Message

from config_data.config import DELETE_PREVIOUS_MESSAGE
from loader import bot, server_status
from Server.players import player_on_server
from utils.logging import logger


@bot.message_handler(commands=["players"])
def show_players_on_server(message: Message) -> None:
    """Показывает количество игроков на сервере."""
    try:
        players = player_on_server()
    except Exception as ex:
        logger.error(f"{ex}")
    else:
        players_names = "\n".join(players["names"])
        bot.send_message(
            message.chat.id,
            f"На сервере: 👨‍🦳:{players['players_count']} 🤖:{players['bots_count']} \n"
            f"{players_names}",
        )


@bot.message_handler(commands=["auto_update_on"])
def auto_update_on(message: Message) -> None:
    """Запускает автообновление количества игроков на сервере."""
    server_status.add_autoupdate_chat(message.chat.id)
    logger.info(
        f"Chats with autoupdate: {len(server_status.chats_id_with_auto_update)}"
    )


def auto_update() -> None:
    if len(server_status.chats_id_with_auto_update) != 0:
        show_players_if_changed()


@bot.message_handler(commands=["auto_update_off"])
def auto_update_off(message: Message) -> None:
    """Отключает автообновление количества игроков на сервере."""
    server_status.remove_autoupdate_chat(message.chat.id)
    logger.info(
        f"Chats with autoupdate: {len(server_status.chats_id_with_auto_update)}"
    )
    if len(server_status.chats_id_with_auto_update) == 0:
        logger.info("Autoupdate off")


def show_players_if_changed() -> None:
    """Показывает количество игроков, если оно изменилось."""
    try:
        players = player_on_server()
    except Exception as ex:
        logger.error(f"{ex}")
    else:
        if server_status.players != players["names"]:
            for chat_id in server_status.chats_id_with_auto_update:
                icon = (
                    "📈" if len(server_status.players) < len(players["names"]) else "📉"
                )
                server_status.players = players["names"]
                players_names = "\n".join(players["names"])
                if chat_id in server_status.next_delete_message and DELETE_PREVIOUS_MESSAGE:
                    bot.delete_message(
                        chat_id, server_status.next_delete_message[chat_id]
                    )
                message = bot.send_message(
                    chat_id,
                    f"{icon}На сервере: {players['players_count']}\n"
                    f"{players_names}",
                )
                server_status.next_delete_message[chat_id] = message.id
                logger.success(f"Reply sent to chat with id: {chat_id}")
