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
import platform
from sys import version as pyver

import psutil

from telethon import events
from telethon.errors import MessageIdInvalidError

from pyrogram import __version__ as pyrover
from telethon import __version__ as telever
from pytgcalls.__version__ import __version__ as pytgver

import config
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import YouTube, app
from YukkiMusic.core.userbot import assistants
from YukkiMusic.misc import SUDOERS, pymongodb
from YukkiMusic.plugins import ALL_MODULES
from YukkiMusic.utils.database import (
    get_global_tops,
    get_particulars,
    get_queries,
    get_served_chats,
    get_served_users,
    get_sudoers,
    get_top_chats,
    get_topp_users,
)
from YukkiMusic.utils.decorators.language import language, languageCB
from YukkiMusic.utils.inline.stats import (
    back_stats_buttons,
    back_stats_markup,
    get_stats_markup,
    overallback_stats_markup,
    stats_buttons,
    top_ten_stats_markup,
)

loop = asyncio.get_running_loop()

# Commands
GSTATS_COMMAND = get_command("GSTATS_COMMAND")
STATS_COMMAND = get_command("STATS_COMMAND")


@app.on_message(
    command=STATS_COMMAND,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@language
async def stats_global(event, _):
    upl = stats_buttons(_, True if event.sender_id in SUDOERS else False)
    await event.reply(
        file=config.STATS_IMG_URL,
        message=_["gstats_11"].format(app.mention),
        buttons=upl,
    )


@app.on_message(
    command=GSTATS_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@language
async def gstats_global(event, _):
    mystic = await event.reply(_["gstats_1"])
    stats = await get_global_tops()
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit(_["gstats_2"])

    def get_stats():
        results = {}
        for i in stats:
            top_list = stats[i]["spot"]
            results[str(i)] = top_list
            list_arranged = dict(
                sorted(
                    results.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not results:
            return mystic.edit(_["gstats_2"])
        videoid = None
        co = None
        for vidid, count in list_arranged.items():
            if vidid == "telegram":
                continue
            else:
                videoid = vidid
                co = count
            break
        return videoid, co

    try:
        videoid, co = await loop.run_in_executor(None, get_stats)
    except Exception:
        return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = title.title()
    final = f"Top played Tracks on  {app.mention}\n\n**Title:** {title}\n\nPlayed** {co} **times"
    upl = get_stats_markup(_, True if event.sender_id in SUDOERS else False)
    await app.send_file(
        event.chat_id,
        file=thumbnail,
        caption=final,
        buttons=upl,
    )
    await mystic.delete()


@app.on(events.CallbackQuery(pattern=r"GetStatsNow", func=lambda e: e.sender_id not in BANNED_USERS))
@languageCB
async def top_users_ten(event, _):
    chat_id = event.chat_id
    callback_data = event.data.decode('utf-8').strip()
    what = callback_data.split(None, 1)[1]
    upl = back_stats_markup(_)
    try:
        await event.answer()
    except:
        pass
    chat = await event.get_chat()
    mystic = await event.edit(
        _["gstats_3"].format(
            f"of {chat.title}" if what == "Here" else what
        )
    )
    if what == "Tracks":
        stats = await get_global_tops()
    elif what == "Chats":
        stats = await get_top_chats()
    elif what == "Users":
        stats = await get_topp_users()
    elif what == "Here":
        stats = await get_particulars(chat_id)
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit(_["gstats_2"], buttons=upl)
    queries = await get_queries()

    def get_stats():
        results = {}
        for i in stats:
            top_list = stats[i] if what in ["Chats", "Users"] else stats[i]["spot"]
            results[str(i)] = top_list
            list_arranged = dict(
                sorted(
                    results.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not results:
            return mystic.edit(_["gstats_2"], buttons=upl)
        msg = ""
        limit = 0
        total_count = 0
        if what in ["Tracks", "Here"]:
            for items, count in list_arranged.items():
                total_count += count
                if limit == 10:
                    continue
                limit += 1
                details = stats.get(items)
                title = (details["title"][:35]).title()
                if items == "telegram":
                    msg += f"🔗[TelegramVideos and media's](https://t.me/telegram) ** Played {count} Times**\n\n"
                else:
                    msg += f"🔗 [{title}](https://www.youtube.com/watch?v={items}) ** Played {count} Times**\n\n"

            temp = (
                _["gstats_4"].format(
                    queries,
                    app.mention,
                    len(stats),
                    total_count,
                    limit,
                )
                if what == "Tracks"
                else _["gstats_7"].format(len(stats), total_count, limit)
            )
            msg = temp + msg
        return msg, list_arranged

    try:
        msg, list_arranged = await loop.run_in_executor(None, get_stats)
    except Exception:
        return
    limit = 0
    if what in ["Users", "Chats"]:
        for items, count in list_arranged.items():
            if limit == 10:
                break
            try:
                extract = (
                    (await app.get_entity(items)).first_name
                    if what == "Users"
                    else (await app.get_entity(items)).title
                )
                if extract is None:
                    continue
                await asyncio.sleep(0.5)
            except:
                continue
            limit += 1
            msg += f"🔗`{extract}` Played {count} Times on bot.\n\n"
        temp = (
            _["gstats_5"].format(limit, app.mention)
            if what == "Chats"
            else _["gstats_6"].format(limit, app.mention)
        )
        msg = temp + msg
    try:
        await event.edit(file=config.GLOBAL_IMG_URL, message=msg, buttons=upl)
    except MessageIdInvalidError:
        await event.reply(
            file=config.GLOBAL_IMG_URL, message=msg, buttons=upl
        )


@app.on(events.CallbackQuery(pattern=r"TopOverall", func=lambda e: e.sender_id not in BANNED_USERS))
@languageCB
async def overall_stats(event, _):
    callback_data = event.data.decode('utf-8').strip()
    what = callback_data.split(None, 1)[1]
    if what != "s":
        upl = overallback_stats_markup(_)
    else:
        upl = back_stats_buttons(_)
    try:
        await event.answer()
    except:
        pass
    await event.edit(_["gstats_8"])
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(SUDOERS)
    mod = len(ALL_MODULES)
    assistant = len(assistants)
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    song = config.SONG_DOWNLOAD_DURATION
    play_duration = config.DURATION_LIMIT_MIN
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        ass = "Yes"
    else:
        ass = "No"
    text = f"""**Bot's Stats and information:**

**Imported Modules:** {mod}
**Served chats:** {served_chats} 
**Served Users:** {served_users} 
**Blocked Users:** {blocked} 
**Sudo Users:** {sudoers} 
    
**Total Queries:** {total_queries} 
**Total Assistant:** {assistant}
**Auto Leaving Assistsant:** {ass}

**Play Duration Limit:** {play_duration} ᴍɪɴs
**Song Download Limit:** {song} ᴍɪɴs
**Bot's Server Playlist Limit:** {playlist_limit}
**Playlist Play Limit:** {fetch_playlist}"""
    try:
        await event.edit(file=config.STATS_IMG_URL, message=text, buttons=upl)
    except MessageIdInvalidError:
        await event.reply(
            file=config.STATS_IMG_URL, message=text, buttons=upl
        )


@app.on(events.CallbackQuery(pattern=r"bot_stats_sudo"))
@languageCB
async def overall_stats(event, _):
    if event.sender_id not in SUDOERS:
        return await event.answer("Only for sudoer's", alert=True)
    callback_data = event.data.decode('utf-8').strip()
    what = callback_data.split(None, 1)[1]
    if what != "s":
        upl = overallback_stats_markup(_)
    else:
        upl = back_stats_buttons(_)
    try:
        await answer.answer()
    except:
        pass
    await event.edit(_["gstats_8"])
    sc = platform.system()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}MHz"
    except:
        cpu_freq = "Unable to Fetch"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    total = str(total)
    used = hdd.used / (1024.0**3)
    used = str(used)
    free = hdd.free / (1024.0**3)
    free = str(free)
    mod = len(ALL_MODULES)
    db = pymongodb
    call = db.command("dbstats")
    datasize = call["dataSize"] / 1024
    datasize = str(datasize)
    storage = call["storageSize"] / 1024
    objects = call["objects"]
    collections = call["collections"]

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(await get_sudoers())
    text = f""" **Bot Stats and information:**

**Imported modules:** {mod}
**Platform:** {sc}
**Ram:** {ram}
**Physical Cores:** {p_core}
**Total Cores:** {t_core}
**Cpu frequency:** {cpu_freq}

**Python Version:** {pyver.split()[0]}
**Telethon Version:** {telever}
**Pyrogram Version:** {pyrover}
**Py-tgcalls Version:** {pytgver}
**Total Storage:** {total[:4]} ɢiʙ
**Storage Used:** {used[:4]} ɢiʙ
**Storage Left:** {free[:4]} ɢiʙ

**Served chats:** {served_chats} 
**Served users:** {served_users} 
**Blocked users:** {blocked} 
**Sudo users:** {sudoers} 

**Total DB Storage:** {storage} ᴍʙ
**Total DB Collection:** {collections}
**Total DB Keys:** {objects}
**Total Bot Queries:** `{total_queries} `
    """
    try:
        await event.edit(file=config.STATS_IMG_URL, message=text, buttons=upl)
    except MessageIdInvalidError:
        await event.reply(
            file=config.STATS_IMG_URL, message=text, buttons=upl
        )
@app.on(events.CallbackQuery(pattern=r"^(TOPMARKUPGET|GETSTATS|GlobalStats)$", func=lambda e: e.sender_id not in BANNED_USERS))
@languageCB
async def back_buttons(event, _):
    try:
        await event.answer()
    except:
        pass
    command = event.pattern_match.group(1)
    if command == "TOPMARKUPGET":
        upl = top_ten_stats_markup(_)
        try:
            await event.edit(
                file=config.GLOBAL_IMG_URL,
                message=_["gstats_9"],
                buttons=upl
            )
        except MessageIdInvalidError:
            await event.respond(
                file=config.GLOBAL_IMG_URL,
                message=_["gstats_9"],
                buttons=upl
            )
    elif command == "GlobalStats":
        upl = get_stats_markup(
            _,
            True if event.sender_id in SUDOERS else False,
        )
        try:
            await event.edit(
                file=config.GLOBAL_IMG_URL,
                message=_["gstats_10"].format(app.mention),
                buttons=upl
            )
        except MessageIdInvalidError:
            await event.respond(
                file=config.GLOBAL_IMG_URL,
                message=_["gstats_10"].format(app.mention),
                buttons=upl
            )
    elif command == "GETSTATS":
        upl = stats_buttons(
            _,
            True if event.sender_id in SUDOERS else False,
        )
        try:
            await event.edit(
                file=config.STATS_IMG_URL,
                message=_["gstats_11"].format(app.mention),
                buttons=upl
            )
        except MessageIdInvalidError:
            await event.respond(
                file=config.STATS_IMG_URL,
                message=_["gstats_11"].format(app.mention),
                buttons=upl
            )