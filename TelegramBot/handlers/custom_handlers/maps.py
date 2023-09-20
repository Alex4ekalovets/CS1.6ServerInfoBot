from telebot.types import Message

from TelegramBot.keyboards.inline import maps
from loader import bot


@bot.message_handler(commands=["change_map"])
def select_map(message: Message) -> None:
    """Предлагает выбрать карту из списка"""
    bot.send_message(
        message.chat.id, "Выберите карту", reply_markup=maps()
    )
