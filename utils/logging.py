"""Модуль настройки loguru."""

import json
import sys
from typing import Any, Dict

from loguru import logger


def serialize(record: Dict) -> str:
    """Сериализация сообщения loguru.

    :param record: Сообщение loguru
    :return: Сериализованное сообщение
    """
    subset = {
        "timestamp": record["time"].timestamp(),
        "message": record["message"],
        "level": record["level"].name,
    }
    return json.dumps(subset)


def patching(record: Any) -> None:
    """Изменение вывода сообщений loguru."""
    record["extra"]["serialized"] = serialize(record)


logger.remove(0)
logger = logger.patch(patching)
logger.add("logs/logs_{time}.json", format="{extra[serialized]}", rotation="1 month")
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>",
)
