#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from pytgcalls.exceptions import NoActiveGroupCall

import config
from strings import get_command
from YukkiMusic import app
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.decorators.play import PlayWrapper
from YukkiMusic.utils.logger import play_logs
from YukkiMusic.utils.stream.stream import stream

# Command
STREAM_COMMAND = get_command("STREAM_COMMAND")


@app.on_message(
    command=STREAM_COMMAND,
    is_group=True,
    from_user=config.BANNED_USERS,
    is_restricted=True,
)
@PlayWrapper
async def stream_command(
    event,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):

    if url:
        mystic = await event.reply(
            _["play_2"].format(channel) if channel else _["play_1"]
        )
        try:
            await Yukki.stream_call(url)
        except NoActiveGroupCall:
            await mystic.edit(
                "There's an issue with the bot. Please report it to my owner and ask them to check the logger group."
            )
            text = "Please turn on voice chat. The bot is unable to stream URLs."
            await app.send_message(config.LOG_GROUP_ID, text)
            return
        except Exception as e:
            return await mystic.edit(_["general_3"].format(type(e).__name__))

        await mystic.edit(_["str_2"])
        try:
            await stream(
                _,
                mystic,
                event.sender_id,
                url,
                chat_id,
                event.sender.first_name,
                event.chat_id,
                video=True,
                streamtype="index",
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = (
                str(e) if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
            )
            return await mystic.edit(err)
        return await play_logs(event, streamtype="M3u8 or Index Link")
    else:
        await event.reply(_["str_1"])
