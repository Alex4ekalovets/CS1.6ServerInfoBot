import requests

from utils.logging import logger


def server_cmd(cmd):
    cookies = {
        '_ym_uid': '1694360537832957569',
        '_ym_isad': '2',
        'PHPSESSID': 'fd84ahicuui1eobm5afv61vq82',
        'user_info': '2.60.4.23.-..-.',
        'refer': 'https%3A%2F%2Fmonitoring.csserv.ru%2F',
        'promonew': '1694360539',
        '_gid': 'GA1.2.1457110739.1694360541',
        'userid': '257810',
        'auth': '%7B%22userid%22%3A%22257810%22%2C%22pass%22%3A%220b31aa45f9386cf8ab5c9d5df2fd7b00%22%7D',
        'redirect4': '1694360547',
        '_ym_visorc': 'w',
        'redirect3': '1694369178',
        'user_login': '%2541%256c%2565%2578%2534%2565%256b%2561%256c%256f%2576%2565%2574%2573.-.0b31aa45f9386cf8ab5c9d5df2fd7b00',
        'order_login_friend': '430104',
        '_ym_d': '1694369860',
        '_ga_RE2DH2K0P5': 'GS1.1.1694365331.3.1.1694369882.0.0.0',
        '_ga': 'GA1.1.1971002549.1694360541',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_ym_uid=1694360537832957569; _ym_isad=2; PHPSESSID=fd84ahicuui1eobm5afv61vq82; user_info=2.60.4.23.-..-.; refer=https%3A%2F%2Fmonitoring.csserv.ru%2F; promonew=1694360539; _gid=GA1.2.1457110739.1694360541; userid=257810; auth=%7B%22userid%22%3A%22257810%22%2C%22pass%22%3A%220b31aa45f9386cf8ab5c9d5df2fd7b00%22%7D; redirect4=1694360547; _ym_visorc=w; redirect3=1694369178; user_login=%2541%256c%2565%2578%2534%2565%256b%2561%256c%256f%2576%2565%2574%2573.-.0b31aa45f9386cf8ab5c9d5df2fd7b00; order_login_friend=430104; _ym_d=1694369860; _ga_RE2DH2K0P5=GS1.1.1694365331.3.1.1694369882.0.0.0; _ga=GA1.1.1971002549.1694360541',
        'Origin': 'https://csserv.ru',
        'Referer': 'https://csserv.ru/panel2/control',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    data = {
        'el': '',
        'action': 'server_cmd',
        'btn': '',
        'btn_html': 'Сменить',
        'cmd': cmd,
        'script': 'server_cmd',
        'section': 'srvcontrol',
        'menulink': 'control',
    }

    response = requests.post('https://csserv.ru/includes/panel2/index.php', cookies=cookies, headers=headers, data=data)

    logger.info(
        f"Серверу направлена команда: {cmd}, status: {response.status_code}"
    )
