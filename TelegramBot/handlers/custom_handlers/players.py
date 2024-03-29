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
from loader import bot
from loader import current_state as cs
from Server.players import player_on_server
from utils.logging import logger


@bot.message_handler(commands=["players"])
def show_players_on_server(message: Message) -> None:
    """Показывает количество игроков на сервере."""
    try:
        names, players_count, bots_count = player_on_server()
    except Exception as ex:
        logger.error(f"{ex}")
    else:
        players_names = "\n".join(names)
        bot.send_message(
            message.chat.id,
            f"На сервере: 👨‍🦳:{players_count} 🤖:{bots_count}\n"
            f"{players_names}",
        )


@bot.message_handler(commands=["auto_update_on"])
def auto_update_on(message: Message) -> None:
    """Запускает автообновление количества игроков на сервере."""
    cs.add_autoupdate_chat(message.chat.id)
    logger.info(
        f"Chats with autoupdate: {len(cs.chats_id_with_auto_update)}"
    )


def auto_update() -> None:
    if len(cs.chats_id_with_auto_update) != 0:
        show_players_if_changed()


@bot.message_handler(commands=["auto_update_off"])
def auto_update_off(message: Message) -> None:
    """Отключает автообновление количества игроков на сервере."""
    cs.remove_autoupdate_chat(message.chat.id)
    logger.info(
        f"Chats with autoupdate: {len(cs.chats_id_with_auto_update)}"
    )
    if len(cs.chats_id_with_auto_update) == 0:
        logger.info("Autoupdate off")


def show_players_if_changed() -> None:
    """Показывает количество игроков, если оно изменилось."""
    try:
        names, players_count, bots_count = player_on_server()
    except Exception as ex:
        cs.site_request_attempts += 1
        logger.error(f"Tries: {cs.site_request_attempts}: {ex}")
        if cs.site_request_attempts == 10:
            for chat_id in cs.chats_id_with_auto_update:
                message = bot.send_message(
                    chat_id,
                    f"Сайт csserv.ru не отвечает. Информация об игроках временно недоступна",
                )
                cs.next_delete_message[chat_id] = message.id
    else:
        cs.site_request_attempts = 0
        if cs.players != names:
            logger.info(f"Изменение количества игроков с {len(cs.players)} на {len(names)}")
            logger.info(f"Игроки на сервере {cs.players}")
            for chat_id in cs.chats_id_with_auto_update:
                icon = (
                    "📈" if len(cs.players) < players_count else "📉"
                )
                cs.players = names
                players_names = "\n".join(names)
                if chat_id in cs.next_delete_message and DELETE_PREVIOUS_MESSAGE:
                    try:
                        bot.delete_message(
                            chat_id, cs.next_delete_message[chat_id]
                        )
                    except Exception as ex:
                        logger.exception(f"При попытке удаления сообщения вызвано исключение: {ex}")
                message = bot.send_message(
                    chat_id,
                    f"{icon}На сервере: {players_count}\n"
                    f"{players_names}",
                )
                cs.next_delete_message[chat_id] = message.id
                logger.success(f"Reply sent to chat with id: {chat_id}")
