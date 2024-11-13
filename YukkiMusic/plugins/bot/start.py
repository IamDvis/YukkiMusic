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
import time

from telethon import events
from telethon.tl.types import Channel
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS, START_IMG_URL
from config.config import OWNER_ID
from strings import get_command, get_string
from YukkiMusic import Telegram, YouTube, app
from YukkiMusic.misc import SUDOERS, _boot_
from YukkiMusic.plugins.play.playlist import del_plist_msg
from YukkiMusic.plugins.sudo.sudoers import sudoers_list
from YukkiMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from YukkiMusic.utils.decorators.language import LanguageStart
from YukkiMusic.utils.formatters import get_readable_time
from YukkiMusic.utils.inline import private_panel, start_pannel, help_markup

loop = asyncio.get_running_loop()

START_COMMAND = get_command("START_COMMAND")

@app.on_message(
    command=START_COMMAND,
    is_private=True,
    is_group=False,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@LanguageStart
async def start_comm(event, _):
    chat_id = event.chat_id
    sender = await event.get_sender()
    mention = f"[{sender.first_name}](tg://user?id={sender.id})"

    await add_served_user(event.sender_id)
    if len(event.message.text.split()) > 1:
        name = event.message.text.split(None, 1)[1]
        if name[0:4] == "help":
            if config.START_IMG_URL:
                return await app.send_file(
                    event.chat_id,
                    photo=START_IMG_URL,
                    caption=_["help_1"],
                    buttons=help_markup,
                )
            else:
                return await event.respond(
                    message=_["help_1"],
                    buttons=help_markup,
                )
        if name[0:4] == "song":
            await event.respond(_["song_2"])
            return
        if name[0:3] == "sta":
            m = await event.respond("Fetching your personal stats.")
            stats = await get_userss(event.sender_id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
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
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"[Telegram files and audios]({config.SUPPORT_GROUP}) played {count} times\n\n"
                    else:
                        msg += f"[{title}](https://www.youtube.com/watch?v={vidid}) played {count} times\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            videoid, msg = await loop.run_in_executor(None, get_stats)
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await app.send_file(event.chat_id, photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(event=event, _=_)
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                sender_id = event.sender_id
                sender_mention = message.from_user.mention
                sender_name = sender.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} has just started the bot to check `sudolist`\n\n**User ID:** {sender_id}\n**Username:** {sender_name}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                await Telegram.send_split_text(event, lyrics)
                return
            else:
                await event.respond("Failed to get lyrics.")
                return
        if name[0:3] == "del":
            await del_plist_msg(event=event, _=_)
            await asyncio.sleep(1)
        if name[0:3] == "inf":
            m = await event.respond("Fetching info!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍 **Video Track Information**

❇️ **Title:** {title}

⏳ **Duration:** {duration} mins  
👀 **Views:** `{views}`  
⏰ **Published Time:** {published}  
🎥 **Channel Name:** {channel}  
📎 **Channel Link:** [Visit Here]({channellink})  
🔗 **Video Link:** [Link]({link})
"""
            key = [
                [
                    Button.url(text="Watch", url=f"{link}"),
                    Button.inline(text="Close", callback_data="close"),
                ],
            ]
            await m.delete()
            await app.send_file(
                event.chat_id,
                file=thumbnail,
                caption=searched_text,
                buttons=key,
            )
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{mention} has just started the bot to check video information. \n\n**User ID:** {event.sender_id}\n**User Name:** {sender.first_name}",
                )
    else:
        try:
            await app.get_entity(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        if config.START_IMG_URL:
            try:
                await app.send_file(
                    event.chat_id,
                    file=config.START_IMG_URL,
                    caption=_["start_1"].format(app.mention),
                    buttons=out,
                    reply_to=event.message_id,
                )
            except:
                await event.respond(
                    message=_["start_1"].format(app.mention),
                    buttons=out,
                )
        else:
            await event.respond(
                message=_["start_1"].format(app.mention),
                buttons=out,
            )
        if await is_on_off(config.LOG):
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"{mention} has started the bot. \n\n**User ID:** {sender.id}\n**User Name:** {sender.first_name}",
            )


@app.on_message(
    command=START_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@LanguageStart
async def testbot(event, _):
    uptime = int(time.time() - _boot_)
    chat_id = event.chat_id
    await event.reply(_["start_7"].format(get_readable_time(uptime)))

    return await add_served_chat(event.chat_id)


@app.on(events.ChatAction)
async def welcome(event):
    if event.user_joined or event.user_added:
        chat_id = event.chat_id
        if config.PRIVATE_BOT_MODE == str(True):
            if not await is_served_private_chat(chat_id):
                await event.reply(
                    "This bot's private mode has been enabled. Only my owner can use this. If you want to use this in your chat, please ask my owner to authorize your chat."
                )
                return await app.leave_chat(chat_id)
        else:
            await add_served_chat(chat_id)

        for member in event.users:
            language = await get_lang(chat_id)
            _ = get_string(language)

            if member.id == app.id:
                chat = await event.get_chat()
                if not isinstance(chat, Channel) or (
                    isinstance(chat, Channel) and not chat.megagroup
                ):
                    await event.reply(_["start_5"])
                    return await app.leave_chat(chat_id)
                if chat_id in await blacklisted_chats():
                    await event.reply(
                        _["start_6"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)

                userbot = await get_assistant(chat_id)
                out = start_pannel(_)
                await event.reply(
                    _["start_2"].format(
                        app.mention,
                        userbot.username,
                        userbot.id,
                    ),
                    buttons=out,
                )
            if member.id in config.OWNER_ID:
                return await event.reply(
                    _["start_3"].format(app.mention, member.mention)
                )
            if member.id in SUDOERS:
                return await event.reply(
                    _["start_4"].format(app.mention, member.mention)
                )