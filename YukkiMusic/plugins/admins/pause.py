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
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import is_music_playing, music_off
from YukkiMusic.utils.decorators import AdminRightsCheck

# Commands
PAUSE_COMMAND = get_command("PAUSE_COMMAND")


@app.on_message(
    command=PAUSE_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminRightsCheck
async def pause_admin(event, _, chat_id):
    if not len(event.text.split()) == 1:
        return await event.reply(_["general_2"])
    if not await is_music_playing(chat_id):
        return await event.reply(_["admin_1"])
    await music_off(chat_id)
    await Yukki.pause_stream(chat_id)
    sender = await event.get_sender()
    mention = f"[{sender.first_name}](tg://user?id={sender.id})"
    await event.reply(_["admin_2"].format(mention))
