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
from telethon import events, Button
from telethon.errors import FloodWaitError

import config
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import db
from YukkiMusic.utils import Yukkibin, get_channeplayCB, seconds_to_min
from YukkiMusic.utils.database import get_cmode, is_active_chat, is_music_playing
from YukkiMusic.utils.decorators.language import language, languageCB
from YukkiMusic.utils.inline.queue import queue_back_markup, queue_markup

### Commands
QUEUE_COMMAND = get_command("QUEUE_COMMAND")

basic = {}

def get_image(videoid):
    try:
        url = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
        return url
    except Exception:
        return config.YOUTUBE_IMG_URL

def get_duration(playing):
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return "Unknown"
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return "Unknown"
    else:
        return "Inline"

@app.on(events.NewMessage(pattern=f"^{QUEUE_COMMAND}"))
@language
async def ping_com(event, _):
    if event.sender_id in BANNED_USERS:
        return
    message = event.message
    is_cplay = message.text.startswith("c")
    
    chat_id = await get_cmode(event.chat_id) if is_cplay else event.chat_id
    if chat_id is None:
        await message.reply(_["setting_12"])
        return

    if not await is_active_chat(chat_id):
        await message.reply(_["general_6"])
        return

    got = db.get(chat_id)
    if not got:
        await message.reply(_["queue_2"])
        return

    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    type = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    
    if "live_" in file:
        IMAGE = get_image(videoid)
    elif "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        IMAGE = config.TELEGRAM_AUDIO_URL if type == "Audio" else config.TELEGRAM_VIDEO_URL

    send = (
        "**⌛️ Duration:** Unknown duration limit\n\n" + _["queue_4"]
        if DUR == "Unknown"
        else "\n" + _["queue_4"]
    )

    cap = f"""**{app.mention} Player**

🎥**{_["playing"]}:** {title}

🔗**{_["stream_type"]}:** {type}
🙍‍♂️**{_["played_by"]}:** {user}
{send}"""

    upl = (
        queue_markup(_, DUR, "c" if is_cplay else "g", videoid)
        if DUR == "Unknown"
        else queue_markup(
            _,
            DUR,
            "c" if is_cplay else "g",
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )

    basic[videoid] = True
    mystic = await message.reply(file=IMAGE, message=cap, buttons=upl)
    
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid] and await is_music_playing(chat_id):
                        try:
                            buttons = queue_markup(
                                _,
                                DUR,
                                "c" if is_cplay else "g",
                                videoid,
                                seconds_to_min(db[chat_id][0]["played"]),
                                db[chat_id][0]["dur"],
                            )
                            await mystic.edit(buttons=buttons)
                        except FloodWaitError as e:
                            await asyncio.sleep(e.seconds)
                    else:
                        break
                else:
                    break
        except:
            return


@app.on(events.CallbackQuery(pattern="GetTimer"))
async def quite_timer(event):
    try:
        await event.answer()
    except:
        pass


@app.on(events.CallbackQuery(pattern="GetQueued"))
@languageCB
async def queued_tracks(event, _):
    if event.sender_id in BANNED_USERS:
        return
    await event.answer()
    
    data = event.data.decode().split("|")
    what, videoid = data[0], data[1]
    chat_id, channel = await get_channeplayCB(_, what, event)
    
    if not await is_active_chat(chat_id):
        await event.answer(_["general_6"], alert=True)
        return

    got = db.get(chat_id)
    if not got or len(got) == 1:
        await event.answer(_["queue_5"], alert=True)
        return

    basic[videoid] = False
    msg = "Queue:\n"
    for i, item in enumerate(got, 1):
        msg += f"{i}. {item['title']} - {item['dur']} by {item['by']}\n"

    link = await Yukkibin(msg)
    await event.edit("Queue:\n" + link, buttons=queue_back_markup(_, what))

@app.on(events.CallbackQuery(pattern="queue_back_timer"))
@languageCB
async def queue_back(event, _):
    if event.sender_id in BANNED_USERS:
        return
    await event.answer(_["set_cb_8"], alert=True)

    callback_data = event.data.decode().split("|")
    cplay = callback_data[0]
    
    chat_id, channel = await get_channeplayCB(_, cplay, event)
    if not await is_active_chat(chat_id):
        await event.answer(_["general_6"], alert=True)
        return

    got = db.get(chat_id)
    if not got:
        await event.answer(_["queue_2"], alert=True)
        return

    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    type = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    
    if "live_" in file:
        IMAGE = get_image(videoid)
    elif "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        IMAGE = config.TELEGRAM_AUDIO_URL if type == "Audio" else config.TELEGRAM_VIDEO_URL

    send = (
        "**⌛️ Duration:** Unknown duration limit\n\n" + _["queue_4"]
        if DUR == "Unknown"
        else "\n" + _["queue_4"]
    )

    cap = f"""**{app.mention} Player**

🎥**{_["playing"]}:** {title}

🔗**{_["stream_type"]}:** {type}
🙍‍♂️**{_["played_by"]}:** {user}
{send}"""

    upl = (
        queue_markup(_, DUR, cplay, videoid)
        if DUR == "Unknown"
        else queue_markup(
            _,
            DUR,
            cplay,
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )

    basic[videoid] = True
    mystic = await event.edit(file=med, message=cap, buttons=upl)
    
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid] and await is_music_playing(chat_id):
                        try:
                            buttons = queue_markup(
                                _,
                                DUR,
                                cplay,
                                videoid,
                                seconds_to_min(db[chat_id][0]["played"]),
                                db[chat_id][0]["dur"],
                            )
                            await mystic.edit(buttons=buttons)
                        except FloodWaitError as e:
                            await asyncio.sleep(e.seconds)
                    else:
                        break
                else:
                    break
        except:
            return