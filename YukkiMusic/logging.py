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

logger.add(
    LOG_FILE_NAME,
    rotation="5 MB",
    retention=10,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name} - {message}",
    serialize=False,
)

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name} - {message}",
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

def LOGGER(name: str):
    return logger.bind(name=name)