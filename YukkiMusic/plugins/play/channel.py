#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from telethon.tl.types import ChannelParticipantsAdmins, Channel
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.database import set_cmode
from YukkiMusic.utils.decorators.admins import AdminActual

CHANNELPLAY_COMMAND = get_command("CHANNELPLAY_COMMAND")


@app.on_message(
    command=CHANNELPLAY_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminActual
async def playmode_(event, _):
    message = event.message
    if event.is_group:
        if len(message.message.split()) < 2:
            return await message.reply(
                _["cplay_1"].format(event.chat.title, CHANNELPLAY_COMMAND[0])
            )

        query = message.message.split(None, 2)[1].lower().strip()

        if query == "disable":
            await set_cmode(event.chat_id, None)
            return await message.reply("Channel Play Disabled")

        elif query == "linked":
            chat = await app.get_entity(event.chat_id)
            if chat.linked_chat_id:
                linked_chat = await app.get_entity(chat.linked_chat_id)
                await set_cmode(event.chat_id, linked_chat.id)
                return await message.reply(
                    _["cplay_3"].format(linked_chat.title, linked_chat.id)
                )
            else:
                return await message.reply(_["cplay_2"])

        else:
            try:
                target_chat = await app.get_entity(query)
            except:
                return await message.reply(_["cplay_4"])

            if not isinstance(target_chat, Channel):
                return await message.reply(_["cplay_5"])

            try:
                creator_id = None
                creator_username = None
                async for user in app.iter_participants(
                    target_chat.id, filter=ChannelParticipantsAdmins
                ):
                    if (
                        user.participant.admin_rights
                        and user.participant.admin_rights.is_creator
                    ):
                        creator_id = user.id
                        creator_username = user.username
                        break
            except:
                return await message.reply(_["cplay_4"])

            if creator_id != event.sender_id:
                return await message.reply(
                    _["cplay_6"].format(target_chat.title, creator_username)
                )

            await set_cmode(event.chat_id, target_chat.id)
            return await message.reply(
                _["cplay_3"].format(target_chat.title, target_chat.id)
            )
