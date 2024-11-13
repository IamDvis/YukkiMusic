#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import asyncio

from telethon import events
from telethon.errors import FloodWaitError

from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils import get_readable_time
from YukkiMusic.utils.database import (
    add_banned_user,
    get_banned_count,
    get_banned_users,
    get_served_chats,
    is_banned_user,
    remove_banned_user,
)
from YukkiMusic.utils.decorators.language import language

# Commands
GBAN_COMMAND = get_command("GBAN_COMMAND")
UNGBAN_COMMAND = get_command("UNGBAN_COMMAND")
GBANNED_COMMAND = get_command("GBANNED_COMMAND")


@app.on_message(command=GBAN_COMMAND, from_user=SUDOERS)
@language
async def gbanuser(event, _):
    if not event.is_reply and len(event.message.text.split()) != 2:
        await event.reply(_["general_1"])
        return
    if event.is_reply:
        user_id = (await event.get_reply_message()).sender_id
    else:
        user_id = (await app.get_entity(event.message.text.split()[1])).id
    mention = f"[User](tg://user?id={user_id})"

    if user_id == event.sender_id:
        await event.reply(_["gban_1"])
        return
    elif user_id == app.me.id:
        await event.reply(_["gban_2"])
        return
    elif user_id in SUDOERS:
        await event.reply(_["gban_3"])
        return

    if await is_banned_user(user_id):
        await event.reply(_["gban_4"].format(mention))
        return

    if user_id not in BANNED_USERS:
        BANNED_USERS.add(user_id)

    served_chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    time_expected = get_readable_time(len(served_chats))
    mystic = await event.reply(_["gban_5"].format(mention, time_expected))
    number_of_chats = 0

    for chat_id in served_chats:
        try:
            await app.edit_permissions(chat_id, user_id, ban=True)
            number_of_chats += 1
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception:
            pass

    await add_banned_user(user_id)
    await event.reply(_["gban_6"].format(mention, number_of_chats))
    await mystic.delete()


@app.on_message(command=UNGBAN_COMMAND, from_user=SUDOERS)
@language
async def ungbanuser(event, _):
    if not event.is_reply and len(event.message.text.split()) != 2:
        await event.reply(_["general_1"])
        return
    if event.is_reply:
        user_id = (await event.get_reply_message()).sender_id
    else:
        user_id = (await app.get_entity(event.message.text.split()[1])).id
    mention = f"[User](tg://user?id={user_id})"

    if not await is_banned_user(user_id):
        await event.reply(_["gban_7"].format(mention))
        return

    if user_id in BANNED_USERS:
        BANNED_USERS.remove(user_id)

    served_chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    time_expected = get_readable_time(len(served_chats))
    mystic = await event.reply(_["gban_8"].format(mention, time_expected))
    number_of_chats = 0

    for chat_id in served_chats:
        try:
            await app.edit_permissions(chat_id, user_id, ban=False)
            number_of_chats += 1
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception:
            pass

    await remove_banned_user(user_id)
    await event.reply(_["gban_9"].format(mention, number_of_chats))
    await mystic.delete()


@app.on_message(command=GBANNED_COMMAND, from_user=SUDOERS)
@language
async def gbanned_list(event, _):
    counts = await get_banned_count()
    if counts == 0:
        await event.reply(_["gban_10"])
        return

    mystic = await event.reply(_["gban_11"])
    msg = "Gbanned Users:\n\n"
    count = 0

    for user_id in await get_banned_users():
        count += 1
        try:
            user = await app.get_entity(user_id)
            name = user.first_name if not user.username else f"@{user.username}"
            msg += f"{count}➤ {name}\n"
        except Exception:
            msg += f"{count}➤ [Unfetched User]{user_id}\n"
            continue

    if count == 0:
        await mystic.edit(_["gban_10"])
    else:
        await mystic.edit(msg)
