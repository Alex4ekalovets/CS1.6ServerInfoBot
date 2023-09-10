"""Модуль парсинга данных по серверу CS1.6 с сайта.

Functions:
    server_info_request: Запросить данные по серверу
    player_on_server: Вернуть информацию по игрокам на сервере
    is_changing_map: Логирование смены карты
"""

from typing import Tuple

import requests
from bs4 import BeautifulSoup as bs

from config_data.config import BOTS_NICKNAMES, SERVER_IP
from utils.logging import logger
from loader import current_state as cs


def server_info_request(
    server: str = "https://csserv.ru/", server_ip: str = SERVER_IP
) -> requests.models.Response:
    """Запрос информации о сервере."""

    headers = {
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded;",
        "Origin": server,
        "Referer": f"{server}{server_ip}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    data = {
        "server_address": server_ip,
    }
    response = requests.post(
        f"{server}includes/server/info/index.php", headers=headers, data=data
    )
    if response.status_code == 200:
        if not cs.parse_started:
            logger.success("Выполняется парсинг")
            cs.parse_started = True
    else:
        logger.warning(f"Status code: {response.status_code}")
        cs.parse_started = False
    return response


def player_on_server() -> Tuple:
    """Получение списка и количества игроков на сервере."""
    r = server_info_request()
    soup = bs(r.text, "html.parser")
    players_info = soup.find_all("td", class_="text_white_")
    players_names = set()
    bots_count = 0
    is_changing_map(soup=soup)
    for player_info in players_info:
        is_player = all(
            [bot_nickname not in player_info.text for bot_nickname in BOTS_NICKNAMES]
        )
        is_bot = any([bot_nickname in player_info.text for bot_nickname in BOTS_NICKNAMES])
        if "left" in str(player_info) and is_player:
            players_names.add(player_info.text)
        if is_bot:
            bots_count += 1
    return players_names, len(players_names), bots_count


def is_changing_map(soup: bs) -> None:
    """Логирование смены карты на сервере."""
    current_map = soup.find_all("img")[1]["title"]
    if current_map != cs.current_map:
        logger.info(f"Changed map form {cs.current_map} to {current_map}")
        cs.current_map = current_map
