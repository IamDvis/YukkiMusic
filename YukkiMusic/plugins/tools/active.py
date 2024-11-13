#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from telethon.errors import ChannelInvalidError
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS, db
from YukkiMusic.utils.database.memorydatabase import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from strings import get_command

# Commands
ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")
AC_COMMAND = get_command("AC_COMMAND")


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


@app.on_message(
    command=ACTIVEVC_COMMAND,
    from_user=SUDOERS,
)
async def activevc(event):
    mystic = await event.reply("Getting Active Voice Chats...\nPlease hold on")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            chat = await app.get_entity(x)
            title = chat.title
            username = chat.username
            if username:
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{username})[`{x}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
            j += 1
        except ChannelInvalidError:
            await _clear_(x)
            continue
    if not text:
        await mystic.edit("No active chats found.")
    else:
        await mystic.edit(f"**Active Voice Chats:**\n\n{text}", link_preview=False)


@app.on_message(
    command=ACTIVEVIDEO_COMMAND,
    from_user=SUDOERS,
)
async def activevi(event):
    mystic = await event.reply("Getting Active Video Chats...\nPlease hold on")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            chat = await app.get_entity(x)
            title = chat.title
            username = chat.username
            if username:
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{username})[`{x}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
            j += 1
        except ChannelInvalidError:
            await _clear_(x)
            continue
    if not text:
        await mystic.edit("No active chats found.")
    else:
        await mystic.edit(f"**Active Video Chats:**\n\n{text}", link_preview=False)


@app.on_message(
    command=AC_COMMAND,
    from_user=SUDOERS,
)
async def vc(event):
    ac_audio = str(len(await get_active_chats()))
    await event.reply(f"Active Chats info: {ac_audio}")
