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
from strings import get_command
from YukkiMusic import YouTube, app
from YukkiMusic.core.call import Yukki
from YukkiMusic.misc import db
from YukkiMusic.utils import AdminRightsCheck, seconds_to_min

SEEK_COMMAND = get_command("SEEK_COMMAND")


@app.on_message(
    command=SEEK_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminRightsCheck
async def seek_comm(event, _, chat_id):
    if len(event.message.text.split()) == 1:
        await event.reply(_["admin_28"])
        return
    query = event.message.text.split(None, 1)[1].strip()
    if not query.isnumeric():
        await event.reply(_["admin_29"])
        return
    playing = db.get(chat_id)
    if not playing:
        await event.reply(_["queue_2"])
        return
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        await event.reply(_["admin_30"])
        return
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        await event.reply(_["admin_30"])
        return
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]

    if event.message.text.split()[0][-2] == "c":
        if (duration_played - duration_to_skip) <= 10:
            await event.reply(
                _["admin_31"].format(seconds_to_min(duration_played), duration)
            )
            return
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            await event.reply(
                _["admin_31"].format(seconds_to_min(duration_played), duration)
            )
            return
        to_seek = duration_played + duration_to_skip + 1

    mystic = await event.reply(_["admin_32"])
    if "vid_" in file_path:
        n, file_path = await YouTube.video(playing[0]["vidid"], True)
        if n == 0:
            await event.reply(_["admin_30"])
            return
    try:
        await Yukki.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except:
        await mystic.edit(_["admin_34"])
        return

    if event.message.text.split()[0][-2] == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip

    await mystic.edit(_["admin_33"].format(seconds_to_min(to_seek)))
