import requests
from bs4 import BeautifulSoup as bs

cookies = {
    'PHPSESSID': 'cetu6njlc18bgfkiajf48a8830',
    'user_info': '2.60.19.1.-..-.',
    'refer': 'https%3A%2F%2Fwww.google.com%2F',
    'promonew': '1677947740',
    '_ym_uid': '1677947742323794919',
    '_ga': 'GA1.2.348118986.1677947742',
    '_gid': 'GA1.2.777115869.1678107155',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ym_d': '1678107224',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded;',
    # 'Cookie': 'PHPSESSID=cetu6njlc18bgfkiajf48a8830; user_info=2.60.19.1.-..-.; refer=https%3A%2F%2Fwww.google.com%2F; promonew=1677947740; _ym_uid=1677947742323794919; _ga=GA1.2.348118986.1677947742; _gid=GA1.2.777115869.1678107155; _ym_isad=2; _ym_visorc=w; _ym_d=1678107224',
    'Origin': 'https://csserv.ru',
    'Referer': 'https://csserv.ru/90.189.165.248_27035',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'server_address': '90.189.165.248_27035',
}

response = requests.post('http://curl', cookies=cookies, headers=headers, data=data)
r = requests.post('https://csserv.ru/includes/server/info/index.php', cookies=cookies, headers=headers, data=data)
soup = bs(r.text, "html.parser")
names = soup.find_all('td', class_='text_white_')
players = list()
bots_count = 0
for name in names:
    if 'left' in str(name):
            # and '[BOTik]' not in name.text:
        players.append(name.text)
    if '[BOTik]' in name.text:
        bots_count += 1
print(', '.join(players), len(players), bots_count)

