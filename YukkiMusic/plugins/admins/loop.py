#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.database.memorydatabase import get_loop, set_loop
from YukkiMusic.utils.decorators import AdminRightsCheck

# Commands
LOOP_COMMAND = get_command("LOOP_COMMAND")


@app.on_message(
    command=LOOP_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminRightsCheck
async def admins(event, _, chat_id):
    usage = _["admin_24"]
    if len(event.text.split()) != 2:
        return await event.reply(usage)
    state = event.text.split(None, 1)[1].strip()
    if state.isnumeric():
        state = int(state)
        if 1 <= state <= 10:
            got = await get_loop(chat_id)
            if got != 0:
                state = got + state
            if int(state) > 10:
                state = 10
            await set_loop(chat_id, state)
            return await event.reply(
                _["admin_25"].format((await event.get_sender()).first_name, state)
            )
        else:
            return await event.reply(_["admin_26"])
    elif state.lower() == "enable":
        await set_loop(chat_id, 10)
        return await event.reply(
            _["admin_25"].format((await event.get_sender()).first_name, 10)
        )
    elif state.lower() == "disable":
        await set_loop(chat_id, 0)
        return await event.reply(_["admin_27"])
    else:
        return await event.reply(usage)
