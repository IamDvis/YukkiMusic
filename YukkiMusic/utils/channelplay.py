#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#


from YukkiMusic import app
from YukkiMusic.utils.database import get_cmode


async def get_channeplayCB(_, command, event):
    if command == "c":
        chat_id = await get_cmode(event.chat_id)
        if chat_id is None:
            try:
                return await event.answer(_["setting_12"], show_alert=True)
            except:
                return
        try:
            chat = await app.get_entity(chat_id)
            channel = chat.title
        except:
            try:
                return await event.answer(_["cplay_4"], alert=True)
            except:
                return
    else:
        chat_id = event.chat_id
        channel = None
    return chat_id, channel
