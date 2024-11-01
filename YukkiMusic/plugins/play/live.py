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
from YukkiMusic import YouTube, app
from YukkiMusic.utils.channelplay import get_channeplayCB
from YukkiMusic.utils.decorators.language import languageCB
from YukkiMusic.utils.stream.stream import stream


@app.on(
    events.CallbackQuery(
        pattern=r"^LiveStream\s(\S+)\|(\d+)\|(\w+)\|(\w+)\|(\w+)",
        func=lambda e: e.sender_id not in BANNED_USERS,
    )
)
@languageCB
async def play_live_stream(event, _):
    callback_data = event.pattern_match.groups()
    vidid, user_id, mode, cplay, fplay = callback_data

    if event.sender_id != int(user_id):
        try:
            return await event.answer(_["playcb_1"], alert=True)
        except:
            return

    try:
        chat_id, channel = await get_channeplayCB(_, cplay, event)
    except:
        return

    video = mode == "v"
    user_name = event.sender.first_name
    await event.message.delete()

    try:
        await event.answer()
    except:
        pass

    mystic = await event.message.reply(
        _["play_2"].format(channel) if channel else _["play_1"]
    )

    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit(_["play_3"])

    ffplay = fplay == "f"
    if not details["duration_min"]:
        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                event.chat_id,
                video,
                streamtype="live",
                forceplay=ffplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = (
                str(e) if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
            )
            return await mystic.edit(err)
    else:
        return await mystic.edit(
            _["play_4"]
        )  # Assuming _["play_4"] is the text for "Not a live stream"

    await mystic.delete()
