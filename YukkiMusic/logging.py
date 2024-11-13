#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.

import sys
import logging
from loguru import logger
from config import LOG_FILE_NAME
from datetime import timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))

logger.add(
    LOG_FILE_NAME,
    rotation="5 MB",
    retention=10,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name} - {message}",
    serialize=False,
    tz=IST
)
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name} - {message}",
    tz=IST
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

ntgcalls_logger = logger.bind(name="ntgcalls")
ntgcalls_logger.level("CRITICAL")

def LOGGER(name: str):
    return logger.bind(name=name)