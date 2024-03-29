![](images/logo.jpg)
## Телеграм бот для вывода количества игроков на сервере CS 1.6
## Содержание
<!-- TOC -->
  * [Основные функции](#основные-функции)
  * [Установка и настройка](#установка-и-настройка)
  * [Используемые технологии](#используемые-технологии)
  * [Работа телеграм-бота](#работа-телеграм-бота)
    * [Начало работы](#начало-работы)
    * [Вывод количества игроков](#вывод-количества-игроков)
    * [Пример работы телеграм-бота](#пример-работы-телеграм-бота)
  * [#TODO](#todo)
<!-- TOC -->


## Основные функции

* Отображение количества игроков на сервере CS 1.6 https://csserv.ru/ по команде пользователя 
* Включение/выключение автообновления количества игроков на сервере и отображения измененного количества
* Удаление предыдущего сообщения бота при автообновлении количества игроков (выключается)
* Логирование изменения количества чатов с автообновлением, запросов к серверу, ответов пользователю и смены карты на сервере
* Сохранение списка чатов с автообновлением и восстановление при перезапуске бота без необходимости повторного ввода команды

## Установка и настройка

1. Скопируйте файлы проекта
```commandline
git clone git@github.com:Alex4ekalovets/CS1.6ServerInfoBot.git
```
Эта команда создаст папку `СS1.6ServerInfoBot`  и сохранит в ней все требуемые файлы.

2. Настройте виртуальное окружение (инструкция для MacOS)

* Перейти в папку с телеграм-ботом
```commandline
cd /path/to/S1.6ServerInfoBot
```
* Создать виртуальное окружение
```commandline
python3 -m venv env
```
* Активировать виртуальное окружение
```commandline
source env/bin/activate
```
3. Установите зависимости в виртуальное окружение:
```commandline
pip install -r requirements.txt
```
4. Переименуйте файл `env.template` в `.env`

5. Зарегистрируйте вашего телеграм-бота
* Для регистрации нового бота запустите в Telegram бота [BotFather](https://t.me/botfather) и отправьте команду:
```commandline
/newbot
```
* Введите название бота, которое будет отображаться у пользователя
* Введите имя бота, оканчивающееся на "bot".
Если имя уже занято, Вам будет предложено ввести новое
* Из сообщения об успешном создании бота скопируйте токен в файл `.env`. В результате должна получиться строка вида:
```dotenv
BOT_TOKEN='1234567890:GHND5d897ndsHDE89nasds644sasd8sah7as3'
```
* Дополнительно можно настроить бота, с помощью команды в чате с ботом [BotFather](https://t.me/botfather)
```commandline
/mybots
```
Подробную информацию о настройках и возможностях телеграм-ботов можно получить [здесь](https://core.telegram.org/bots#6-botfather)

6. Запустите бота командой
```commandline
python main.py
```

7. Настройте основные параметры бота в `/config_data/config.py`
```python
# укажите текст, который может содержаться в никнеймах ботов для исключения
BOTS_NICKNAMES = ["[BOTik]", "addons/"]
# задержка при обращении к сайту для запроса количества игроков
DELAY = 10
# укажите True, если необходимо удалять предыдущее сообщение бота 
# при включенном автоматическом обновлении
DELETE_PREVIOUS_MESSAGE = True
# введите ip сервера по примеру ниже для хостинга серверов https://csserv.ru/
SERVER_IP = '90.189.165.248_27035'
```

## Используемые технологии
* Python 3.11
* beautifulsoup4 4.11.2
* certifi 2022.12.7
* charset-normalizer 3.1.0
* idna 3.4
* loguru 0.6.0
* pyTelegramBotAPI 4.10.0
* python-dotenv 1.0.0
* requests 2.28.2
* soupsieve 2.4
* urllib3 1.26.14

## Работа телеграм-бота
### Начало работы
Для начала работы отправьте боту команду `/start`

### Вывод количества игроков
Выберите одну из предложенных команд бота:
* `/players` - Игроки на сервере
* `/auto_update_on` - Включить автообновление
* `/auto_update_off` - Выключить автообновление


### Пример работы телеграм-бота  
[![Watch the video](https://img.youtube.com/vi/JCR1ZzCttuA/maxresdefault.jpg)](https://youtube.com/shorts/JCR1ZzCttuA?feature=share)

## #TODO
- [ ] Добавить поддержку нескольких серверов ботом. IP сервера должно 
быть запрошено при запуске бота. Предусмотреть возможность изменения адреса
- [ ] Организовать хранение ID чата бота, статус автообновления, id последнего сообщения бота и ip сервера в SQLite
- [ ] Все настройки бота для каждого чата должны выполняться из самого чата кроме задержки. 
- [x] Добавить сообщение об отсутствии ответа от сайта в чат.
- [x] Добавить управление сменой карты и количества ботов через чат-бота.
