#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from config import BANNED_USERS, adminlist
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.database import (
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
)
from YukkiMusic.utils.decorators import AdminActual, language
from YukkiMusic.utils.formatters import int_to_alpha

# Command
AUTH_COMMAND = get_command("AUTH_COMMAND")
UNAUTH_COMMAND = get_command("UNAUTH_COMMAND")
AUTHUSERS_COMMAND = get_command("AUTHUSERS_COMMAND")


@app.on_message(
    command=AUTH_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminActual
async def auth(event, _):
    if not event.is_reply:
        if len(event.text.split()) != 2:
            return await event.reply(_["general_1"])
        user = event.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_entity(user)
        user_id = event.sender_id
        token = await int_to_alpha(user.id)
        msg_user = await event.get_sender()
        from_user_name = msg_user.first_name
        from_user_id = event.sender_id
        _check = await get_authuser_names(event.chat_id)
        count = len(_check)
        if int(count) == 20:
            return await event.reply(_["auth_1"])
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            get = adminlist.get(event.chat_id)
            if get:
                if user.id not in get:
                    get.append(user.id)
            await save_authuser(event.chat_id, token, assis)
            return await event.reply(_["auth_2"])
        else:
            await event.reply(_["auth_3"])
        return
    from_user_id = event.sender_id
    replied = await event.get_reply_message()
    replied_msg_user = await replied.get_sender()
    user_id = replied_msg_user.id
    user_name = replied_msg_user.first_name
    token = await int_to_alpha(user_id)
    _check = await get_authuser_names(event.chat_id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 20:
        return await event.reply(_["auth_1"])
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        get = adminlist.get(event.chat_id)
        if get:
            if user_id not in get:
                get.append(user_id)
        await save_authuser(event.chat_id, token, assis)
        return await event.reply(_["auth_2"])
    else:
        await event.reply(_["auth_3"])


@app.on_message(
    command=UNAUTH_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminActual
async def unauthusers(event, _):
    if not event.is_reply:
        if len(event.text.split()) != 2:
            return await event.reply(_["general_1"])
        user = event.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_entity(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(event.chat_id, token)
        get = adminlist.get(event.chat_id)
        if get:
            if user.id in get:
                get.remove(user.id)
        if deleted:
            return await event.reply(_["auth_4"])
        else:
            return await event.reply(_["auth_5"])
    reply_message = await event.get_reply_message()
    sender = await reply_message.get_sender()
    user_id = sender.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(event.chat_id, token)
    get = adminlist.get(event.chat_id)
    if get:
        if user_id in get:
            get.remove(user_id)
    if deleted:
        return await event.reply(_["auth_4"])
    else:
        return await event.reply(_["auth_5"])


@app.on_message(
    command=AUTHUSERS_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@language
async def authusers(event, _):
    _playlist = await get_authuser_names(event.chat_id)
    if not _playlist:
        return await event.reply(_["setting_5"])
    else:
        j = 0
        mystic = await event.reply(_["auth_6"])
        text = _["auth_7"]
        for note in _playlist:
            _note = await get_authuser(event.chat_id, note)
            user_id = _note["auth_user_id"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_entity(user_id)
                user = user.first_name
                j += 1
            except Exception:
                continue
            text += f"{j}➤ {user}[`{user_id}`]\n"
            text += f"   {_['auth_8']} {admin_name}[`{admin_id}`]\n\n"
        await mystic.delete()
        await event.reply(text)
