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
from config import BANNED_USERS, MONGO_DB_URI, OWNER_ID
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import add_sudo, remove_sudo
from YukkiMusic.utils.decorators.language import language

# Command
ADDSUDO_COMMAND = get_command("ADDSUDO_COMMAND")
DELSUDO_COMMAND = get_command("DELSUDO_COMMAND")
SUDOUSERS_COMMAND = get_command("SUDOUSERS_COMMAND")

@app.on_message(
    command=ADDSUDO_COMMAND,
    from_user=SUDOERS,
)
@language
async def useradd(event, _):
    if event.sender_id not in OWNER_ID:
        return
    if MONGO_DB_URI is None:
        return await event.reply(
            "**Due to privacy issues, You can't manage sudoers when you are on Yukki Database.\n\n Please fill Your MONGO_DB_URI in your vars to use this features**"
        )
    if not event.is_reply:
        if len(event.message.text.split()) != 2:
            return await event.reply(_["general_1"])
        user = event.message.text.split()[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_entity(user)
        if user.id in SUDOERS:
            return await event.reply(_["sudo_1"].format(user.username))
        added = await add_sudo(user.id)
        if added:
            SUDOERS.add(user.id)
            await event.reply(_["sudo_2"].format(user.username))
        else:
            await event.reply("Something wrong happened")
        return
    reply_user = await event.message.get_reply_message()
    if reply_user.sender_id in SUDOERS:
        return await event.reply(
            _["sudo_1"].format(reply_user.sender.username)
        )
    added = await add_sudo(reply_user.sender_id)
    if added:
        SUDOERS.add(reply_user.sender_id)
        await event.reply(
            _["sudo_2"].format(reply_user.sender.username)
        )
    else:
        await event.reply("Something wrong happened")
    return

@app.on_message(
    command=DELSUDO_COMMAND,
    from_user=SUDOERS,
)
@language
async def userdel(event, _):
    if event.sender_id not in OWNER_ID:
        return
    if MONGO_DB_URI is None:
        return await event.reply(
            "**Due to privacy issues, You can't manage sudoers when you are on Yukki Database.\n\n Please fill Your MONGO_DB_URI in your vars to use this features**"
        )
    if not event.is_reply:
        if len(event.text.split()) != 2:
            return await event.reply(_["general_1"])
        user = event.text.split()[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_entity(user)
        if user.id not in SUDOERS:
            return await event.reply(_["sudo_3"])
        removed = await remove_sudo(user.id)
        if removed:
            SUDOERS.remove(user.id)
            await event.reply(_["sudo_4"])
            return
        await event.reply(f"Something wrong happened")
        return
    reply_user = await event.message.get_reply_message()
    user_id = reply_user.sender_id
    if user_id not in SUDOERS:
        return await event.reply(_["sudo_3"])
    removed = await remove_sudo(user_id)
    if removed:
        SUDOERS.remove(user_id)
        await event.reply(_["sudo_4"])
        return
    await event.reply(f"Something wrong happened")

@app.on_message(
    command=SUDOUSERS_COMMAND,
    from_user=SUDOERS,
)
@language
async def sudoers_list(event, _):
    if event.sender_id in BANNED_USERS:
        return
    text = _["sudo_5"]
    count = 0
    for x in OWNER_ID:
        try:
            user = await app.get_entity(x)
            user_name = user.first_name if not user.username else user.username
            count += 1
            text += f"{count}➤ {user_name}\n"
        except Exception:
            continue
    smex = 0
    for user_id in SUDOERS:
        if user_id not in OWNER_ID:
            try:
                user = await app.get_entity(user_id)
                user_name = user.first_name if not user.username else user.username
                if smex == 0:
                    smex += 1
                    text += _["sudo_6"]
                count += 1
                text += f"{count}➤ {user_name} ({user_id})\n"
            except Exception:
                continue
    if not text:
        await event.reply(_["sudo_7"])
    else:
        await event.reply(text)