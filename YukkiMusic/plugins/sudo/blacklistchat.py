#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from telethon import events
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app, SUDOERS
from YukkiMusic.utils.database import blacklist_chat, blacklisted_chats, whitelist_chat
from YukkiMusic.utils.decorators.language import language

# Commands
BLACKLISTCHAT_COMMAND = get_command("BLACKLISTCHAT_COMMAND")
WHITELISTCHAT_COMMAND = get_command("WHITELISTCHAT_COMMAND")
BLACKLISTEDCHAT_COMMAND = get_command("BLACKLISTEDCHAT_COMMAND")


@app.on_message(command=BLACKLISTCHAT_COMMAND, from_user=SUDOERS)
@language
async def blacklist_chat_func(event, _):
    args = event.message.text.split()
    if len(args) != 2:
        return await event.reply(_["black_1"])

    chat_id = int(args[1])
    if chat_id in await blacklisted_chats():
        return await event.reply(_["black_2"])

    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await event.reply(_["black_3"])
    else:
        await event.reply("Something went wrong.")

    try:
        await app.leave_chat(chat_id)
    except:
        pass


@app.on_message(command=WHITELISTCHAT_COMMAND, from_user=SUDOERS)
@language
async def whitelist_chat_func(event, _):
    args = event.message.text.split()
    if len(args) != 2:
        return await event.reply(_["black_4"])

    chat_id = int(args[1])
    if chat_id not in await blacklisted_chats():
        return await event.reply(_["black_5"])

    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        await event.reply(_["black_6"])
    else:
        await event.reply("Something went wrong.")


@app.on_message(
    command=BLACKLISTEDCHAT_COMMAND, from_user=BANNED_USERS, is_restricted=True
)
@language
async def all_chats(event, _):
    text = _["black_7"]
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            chat = await app.get_entity(chat_id)
            title = chat.title if chat.title else "Private"
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"

    if j == 0:
        await event.reply(_["black_8"])
    else:
        await event.reply(text)
