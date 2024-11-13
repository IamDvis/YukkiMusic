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
from YukkiMusic.utils.database import add_gban_user, remove_gban_user
from YukkiMusic.utils.decorators.language import language

# Commands
BLOCK_COMMAND = get_command("BLOCK_COMMAND")
UNBLOCK_COMMAND = get_command("UNBLOCK_COMMAND")
BLOCKED_COMMAND = get_command("BLOCKED_COMMAND")


@app.on_message(command=BLOCK_COMMAND, from_user=SUDOERS)
@language
async def useradd(event, _):
    if not event.is_reply:
        args = event.message.text.split()
        if len(args) != 2:
            return await event.reply(_["general_1"])

        user = args[1].replace("@", "")
        user_obj = await app.get_entity(user)

        mention = f"[{user_obj.first_name}](tg://user?id={user_obj.id})"

        if user_obj.id in BANNED_USERS:
            return await event.reply(_["block_1"].format(mention))

        await add_gban_user(user_obj.id)
        BANNED_USERS.add(user_obj.id)
        await event.reply(_["block_2"].format(mention))
        return

    replied_user = await event.get_reply_message()
    replied_user_id = replied_user.sender_id
    mention = f"[{replied_user.sender.first_name}](tg://user?id={replied_user_id})"

    if replied_user_id in BANNED_USERS:
        return await event.reply(_["block_1"].format(mention))

    await add_gban_user(replied_user_id)
    BANNED_USERS.add(replied_user_id)
    await event.reply(_["block_2"].format(mention))


@app.on_message(command=UNBLOCK_COMMAND, from_user=SUDOERS)
@language
async def userdel(event, _):
    if not event.is_reply:
        args = event.message.text.split()
        if len(args) != 2:
            return await event.reply(_["general_1"])

        user = args[1].replace("@", "")
        user_obj = await app.get_entity(user)

        mention = f"[{user_obj.first_name}](tg://user?id={user_obj.id})"

        if user_obj.id not in BANNED_USERS:
            return await event.reply(_["block_3"])

        await remove_gban_user(user_obj.id)
        BANNED_USERS.remove(user_obj.id)
        await event.reply(_["block_4"])
        return

    replied_user = await event.get_reply_message()
    replied_user_id = replied_user.sender_id
    mention = f"[{replied_user.sender.first_name}](tg://user?id={replied_user_id})"

    if replied_user_id not in BANNED_USERS:
        return await event.reply(_["block_3"])

    await remove_gban_user(replied_user_id)
    BANNED_USERS.remove(replied_user_id)
    await event.reply(_["block_4"])


@app.on_message(command=BLOCKED_COMMAND, from_user=SUDOERS)
@language
async def sudoers_list(event, _):
    if not BANNED_USERS:
        return await event.reply(_["block_5"])

    mystic = await event.reply(_["block_6"])
    msg = _["block_7"]
    count = 0
    for user_id in BANNED_USERS:
        try:
            user = await app.get_entity(user_id)
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            count += 1
        except Exception:
            continue
        msg += f"{count} ➤ {mention}\n"

    if count == 0:
        return await mystic.edit(_["block_5"])
    else:
        await mystic.edit(msg)
