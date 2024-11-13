#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.

import sys
from loguru import logger
from config import LOG_FILE_NAME

logger.add(
    LOG_FILE_NAME,
    rotation="5 MB",
    retention=10,
    level="INFO",
    format="{time:DD-MMM-YY HH:mm:ss} - {level} - {name} - {message}",
)
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:DD-MMM-YY HH:mm:ss} - {level} - {name} - {message}",
)

logger.disable("pyrogram")
logger.disable("telethon")
logger.disable("pytgcalls")
logger.disable("pymongo")
logger.disable("httpx")

ntgcalls_logger = logger.bind(name="ntgcalls")
ntgcalls_logger.level("CRITICAL")

def LOGGER(name: str):
    return logger.bind(name=name)