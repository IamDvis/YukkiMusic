#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from strings import get_command, get_string
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)

# Commands
MAINTENANCE_COMMAND = get_command("MAINTENANCE_COMMAND")


@app.on_message(command=MAINTENANCE_COMMAND, from_user=SUDOERS)
async def maintenance(event):
    try:
        language = await get_lang(event.chat_id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    usage = _["maint_1"]
    if len(event.text.split()) != 2:
        return await event.reply(usage)
    state = event.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        if await is_maintenance() is False:
            await event.reply(_["maint_6"])
        else:
            await maintenance_on()
            await event.reply(_["maint_2"])
    elif state == "disable":
        if await is_maintenance() is False:
            await maintenance_off()
            await event.reply(_["maint_3"])
        else:
            await event.reply(_["maint_5"])
    else:
        await event.reply(usage)
