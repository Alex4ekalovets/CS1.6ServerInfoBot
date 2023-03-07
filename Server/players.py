"""Модуль парсинга данных по серверу CS1.6 с сайта.

Functions:
    server_info_request: Запросить данные по серверу
    player_on_server: Вернуть информацию по игрокам на сервере
"""
import datetime

import requests
from bs4 import BeautifulSoup as bs
from typing import Dict

from utils.logging import logger


class ServerStatus:
        players = set()
        last_update_time = datetime.datetime.min
        chats_id_auto_update = set()


def server_info_request(
        server: str = 'https://csserv.ru/',
        server_ip: str = '90.189.165.248_27035') -> requests.models.Response:

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
    logger.success("Направлен запрос серверу")
    return response


def player_on_server(bot_preffix: str = '[BOTik]') -> Dict:
    r = server_info_request()
    soup = bs(r.text, "html.parser")
    names = soup.find_all('td', class_='text_white_')
    players = {
        'names': set(),
        'players_count': 0,
        'bots_count': 0,
    }
    for name in names:
        if 'left' in str(name) and bot_preffix not in name.text:
            players['names'].add(name.text)
        if bot_preffix in name.text:
            players['bots_count'] += 1
        players['players_count'] = len(players['names'])
    return players


if __name__ == '__main__':
    print(player_on_server())
