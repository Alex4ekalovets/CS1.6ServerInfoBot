from telebot.types import Message

from TelegramBot.keyboards.inline import bots
from loader import bot


@bot.message_handler(commands=["bots_control"])
def change_bots(message: Message) -> None:
    """Предлагает выбрать команду управления ботами"""
    bot.send_message(
        message.chat.id, "Управление ботами", reply_markup=bots()
    )
