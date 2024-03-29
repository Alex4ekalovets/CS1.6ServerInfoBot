from telebot.types import CallbackQuery

from Server.cmd import server_cmd
from loader import bot


@bot.callback_query_handler(func=lambda call: True)
def send_select_cmd(call: CallbackQuery) -> None:
    """Отправляет выбранную команду на сервер"""
    server_cmd(call.data)
