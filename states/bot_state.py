"""Модуль состояний телеграм бота"""

import json
import os
from typing import Set, Dict


class CurrentState:
    """Класс, описывающей текущее состояние телеграм-бота."""
    def __init__(self) -> None:
        self.players: Set = set()
        self.current_map: str = ""
        self.next_delete_message: Dict = dict()
        if os.path.isfile("chats_with_autoupdate.json"):
            with open("chats_with_autoupdate.json", "r") as file:
                self.chats_id_with_auto_update = json.load(file)
                print(self.chats_id_with_auto_update)
        else:
            self.chats_id_with_auto_update: Dict = dict()

    def add_autoupdate_chat(self, chat_id: int) -> None:
        """Добавляет чат в список автообновления."""
        if str(chat_id) not in self.chats_id_with_auto_update:
            self.chats_id_with_auto_update[str(chat_id)] = None
            self.save_chats_to_json()

    def remove_autoupdate_chat(self, chat_id: int) -> None:
        """Удаляет чат из списока автообновления."""
        if str(chat_id) in self.chats_id_with_auto_update:
            self.chats_id_with_auto_update.pop(str(chat_id))
            self.save_chats_to_json()

    def save_chats_to_json(self) -> None:
        """Сохраняет список автообновления в файл json."""
        with open("chats_with_autoupdate.json", "w") as file:
            json.dump(self.chats_id_with_auto_update, file)
