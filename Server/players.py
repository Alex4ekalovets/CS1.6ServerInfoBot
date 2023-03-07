"""Модуль парсинга данных по серверу CS1.6 с сайта.

Functions:
    server_info_request: Запросить данные по серверу
    player_on_server: Вернуть информацию по игрокам на сервере
    is_changing_map: Логирование смены карты
"""
import datetime

import requests
from bs4 import BeautifulSoup as bs
from typing import Dict

from utils.logging import logger

from config_data.config import BOTS_NICKNAMES


class ServerStatus:
        players = set()
        last_update_time = datetime.datetime.min
        chats_id_auto_update = set()
        current_map = ''
        next_delete_message = {}


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
        logger.success("Получен ответ от сервера")
    else:
        logger.warning(f"Статус-код запроса: {response.status_code}")
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
        'is_changing_map': is_changing_map(soup)
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


def is_changing_map(soup: bs) -> bool:
    """Логирование смены карты на сервере."""
    current_map = soup.find_all('img')[1]['title']
    if current_map != ServerStatus.current_map:
        logger.info(f"Смена карты с {ServerStatus.current_map} на {current_map}")
        ServerStatus.current_map = current_map
        return True
    return False
