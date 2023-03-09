"""Модуль парсинга данных по серверу CS1.6 с сайта.

Functions:
    server_info_request: Запросить данные по серверу
    player_on_server: Вернуть информацию по игрокам на сервере
    is_changing_map: Логирование смены карты
"""
import json
import os

import requests
from bs4 import BeautifulSoup as bs
from typing import Dict

from utils.logging import logger

from config_data.config import BOTS_NICKNAMES


class ServerStatus:
    def __init__(self):
        self.players = set()
        self.current_map = ''
        self.next_delete_message = {}
        if os.path.isfile('chats_with_autoupdate.json'):
            with open('chats_with_autoupdate.json', 'r') as file:
                self.chats_id_with_auto_update = json.load(file)
                print(self.chats_id_with_auto_update)
        else:
            self.chats_id_with_auto_update = dict()

    def add_autoupdate_chat(self, chat_id):
        chat_id = str(chat_id)
        if chat_id not in self.chats_id_with_auto_update:
            self.chats_id_with_auto_update[chat_id] = None
            self.save_chats_to_json()

    def remove_autoupdate_chat(self, chat_id):
        chat_id = str(chat_id)
        if chat_id in self.chats_id_with_auto_update:
            self.chats_id_with_auto_update.pop(chat_id)
            self.save_chats_to_json()

    def save_chats_to_json(self):
        with open('chats_with_autoupdate.json', 'w') as file:
            json.dump(self.chats_id_with_auto_update, file)


def server_info_request(
        server: str = 'https://csserv.ru/',
        server_ip: str = '90.189.165.248_27035') -> requests.models.Response:
    """Запрос информации о сервере."""

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;',
        'Origin': server,
        'Referer': f'{server}{server_ip}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    data = {
        'server_address': server_ip,
    }
    response = requests.post(
        f'{server}includes/server/info/index.php',
        headers=headers,
        data=data
    )
    if response.status_code == 200:
        logger.success("Received a response from the server")
    else:
        logger.warning(f"Status code: {response.status_code}")
    return response


def player_on_server() -> Dict:
    """Получение списка и количества игроков на сервере."""
    r = server_info_request()
    soup = bs(r.text, "html.parser")
    names = soup.find_all('td', class_='text_white_')
    players = {
        'names': set(),
        'players_count': 0,
        'bots_count': 0,
    }
    for name in names:
        is_player = all([bot_nickname not in name.text for bot_nickname in BOTS_NICKNAMES])
        is_bot = any([bot_nickname in name.text for bot_nickname in BOTS_NICKNAMES])
        if 'left' in str(name) and is_player:
            players['names'].add(name.text)
        if is_bot:
            players['bots_count'] += 1
        players['players_count'] = len(players['names'])
    return players


def is_changing_map(soup: bs) -> None:
    """Логирование смены карты на сервере."""
    current_map = soup.find_all('img')[1]['title']
    if current_map != ServerStatus.current_map:
        logger.info(f"Changed map form {ServerStatus.current_map} to {current_map}")
        ServerStatus.current_map = current_map
