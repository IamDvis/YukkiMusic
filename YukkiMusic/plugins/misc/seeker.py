#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import time
import asyncio

from pyrogram.types import InlineKeyboardMarkup

from strings import get_string
from YukkiMusic import app
from YukkiMusic.misc import db
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import get_active_chats, get_lang, is_music_playing, get_assistant, set_loop
from YukkiMusic.utils.formatters import seconds_to_min
from YukkiMusic.utils.inline import stream_markup_timer, telegram_markup_timer
from config import MUTE_WARNING_TIME

from ..admins.callback import wrong


checker = {}
mute_warnings = {}

if MUTE_WARNING_TIME < 60:
    t = f"{MUTE_WARNING_TIME} seconds"
else:
    t = time.strftime("%M:%S minutes", time.gmtime(MUTE_WARNING_TIME))

async def timer():
    while not await asyncio.sleep(1):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            if not await is_music_playing(chat_id):
                continue
            playing = db.get(chat_id)
            if not playing:
                continue
            file_path = playing[0]["file"]
            if "index_" in file_path or "live_" in file_path:
                continue
            duration = int(playing[0]["seconds"])
            if duration == 0:
                continue
            db[chat_id][0]["played"] += 1


asyncio.create_task(timer())


async def process_mute_warnings():
    while True:
        await asyncio.sleep(2)
        for chat_id, details in list(mute_warnings.items()):
            if time.time() - details["timestamp"] >= MUTE_WARNING_TIME:
                _ = details["_"]
                try:
                    await app.delete_messages(chat_id, details["msg_id"])
                except:
                    pass
                try:
                    userbot = await get_assistant(chat_id)
                    members = []
                    async for member in userbot.get_call_members(chat_id):
                        if member is None:
                            continue
                        members.append(member)

                    m = next((m for m in members if m.chat.id == userbot.id), None)
                    is_muted = bool(m.is_muted and not m.can_self_unmute) if m else True

                    if is_muted:
                        await Yukki.stop_stream(chat_id)
                        await set_loop(chat_id, 0)
                        await app.send_message(chat_id, _["admin_35"].format(t))

                    mute_warnings.pop(chat_id, None)
                except:
                    mute_warnings.pop(chat_id, None)

async def markup_timer():
    while not await asyncio.sleep(2):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            if chat_id in mute_warnings:
                continue

            try:
                if not await is_music_playing(chat_id):
                    continue
                playing = db.get(chat_id)
                if not playing:
                    continue
                duration_seconds = int(playing[0]["seconds"])
                if duration_seconds == 0:
                    continue
                try:
                    mystic = playing[0]["mystic"]
                    markup = playing[0]["markup"]
                except:
                    continue
                try:
                    check = wrong[chat_id][mystic.message_id]
                    if check is False:
                        continue
                except:
                    pass
                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except:
                    _ = get_string("en")

                try:
                    userbot = await get_assistant(chat_id)
                    members = []
                    async for member in userbot.get_call_members(chat_id):
                        if member is None:
                            continue
                        members.append(member)

                    if not members:
                        await Yukki.stop_stream(chat_id)
                        await set_loop(chat_id, 0)
                        continue

                    m = next((m for m in members if m.chat.id == userbot.id), None)
                    is_muted = bool(m.is_muted and not m.can_self_unmute) if m else True

                    if is_muted:
                        ab = await app.send_message(chat_id, _["admin_36"].format(t))
                        mute_warnings[chat_id] = {"timestamp": time.time(), "_": _, "msg_id": ab.id}

                except:
                    continue

                try:
                    buttons = (
                        stream_markup_timer(
                            _,
                            playing[0]["vidid"],
                            chat_id,
                            seconds_to_min(playing[0]["played"]),
                            playing[0]["dur"],
                        )
                        if markup == "stream"
                        else telegram_markup_timer(
                            _,
                            chat_id,
                            seconds_to_min(playing[0]["played"]),
                            playing[0]["dur"],
                        )
                    )
                    await mystic.edit_reply_markup(
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except:
                    continue

            except:
                continue

asyncio.create_task(markup_timer())
asyncio.create_task(process_mute_warnings())
