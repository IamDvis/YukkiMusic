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
from YukkiMusic import app
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import is_muted, mute_off, mute_on
from YukkiMusic.utils.decorators import AdminRightsCheck


@app.on_message(
    command="vcmute",
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminRightsCheck
async def mute_admin(event, _, chat_id):
    if len(event.message.text.split()) != 1 or event.reply_to:
        await event.reply(_["general_2"])
        return
    if await is_muted(chat_id):
        await event.reply(_["admin_5"], link_preview=False)
        return
    await mute_on(chat_id)
    await Yukki.mute_stream(chat_id)

    sender = await event.get_sender()
    mention = f"[{sender.first_name}](tg://user?id={sender.id})"
    await event.reply(_["admin_6"].format(mention), link_preview=False)


@app.on_message(
    command="vcunmute",
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminRightsCheck
async def unmute_admin(event, _, chat_id):
    if len(event.message.text.split()) != 1 or event.reply_to:
        await event.reply(_["general_2"])
        return
    if not await is_muted(chat_id):
        await event.reply(_["admin_7"], link_preview=False)
        return
    await mute_off(chat_id)
    await Yukki.unmute_stream(chat_id)

    sender = await event.get_sender()
    mention = f"[{sender.first_name}](tg://user?id={sender.id})"
    await event.reply(_["admin_8"].format(mention), link_preview=False)
