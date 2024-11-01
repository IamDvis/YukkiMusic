#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import random
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import db
from YukkiMusic.utils.decorators import AdminRightsCheck

SHUFFLE_COMMAND = get_command("SHUFFLE_COMMAND")


@app.on_message(
    command=SHUFFLE_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminRightsCheck
async def admins(event, _, chat_id):
    if len(event.message.text.split()) != 1:
        await event.reply(_["general_2"])
        return

    check = db.get(chat_id)
    if not check:
        await event.reply(_["admin_21"])
        return

    try:
        popped = check.pop(0)
    except:
        await event.reply(_["admin_22"])
        return

    check = db.get(chat_id)
    if not check:
        check.insert(0, popped)
        await event.reply(_["admin_22"])
        return

    random.shuffle(check)
    check.insert(0, popped)

    sender = await event.get_sender()
    mention = f"[{sender.first_name}](tg://user?id={sender.id})"
    await event.reply(_["admin_23"].format(mention))
