#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from telethon import events, Button
from telethon.tl.types import InputBotInlineResultPhoto, InputWebDocument, DocumentAttributeImageSize

from youtubesearchpython.__future__ import VideosSearch
from config import BANNED_USERS
from YukkiMusic import app

answer = [
    lambda event: event.builder.article(
        title="Pause Stream",
        description="Pause the currently playing song on voice chat.",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/c0a1c789def7b93f13745.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/pause",
    ),
    lambda event: event.builder.article(
        title="Resume Stream",
        description="Resume the paused song on voice chat.",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/02d1b7f967ca11404455a.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/resume",
    ),
    lambda event: event.builder.article(
        title="Mute Stream",
        description="Mute the ongoing song on voice chat.",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/66516f2976cb6d87e20f9.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/vcmute",
    ),
    lambda event: event.builder.article(
        title="Unmute Stream",
        description="Unmute the ongoing song on voice chat.",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/3078794f9341ffd582e18.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/vcunmute",
    ),
    lambda event: event.builder.article(
        title="Skip Stream",
        description="Skip to the next track, or specify a track number with /skip [number].",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/98b88e52bc625903c7a2f.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/skip",
    ),
    lambda event: event.builder.article(
        title="End Stream",
        description="Stop the currently playing song on group voice chat.",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/d2eb03211baaba8838cc4.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/stop",
    ),
    lambda event: event.builder.article(
        title="Shuffle Stream",
        description="Shuffle the queued tracks list.",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/7f6aac5c6e27d41a4a269.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/shuffle",
    ),
    lambda event: event.builder.article(
        title="Seek Stream",
        description="Seek the ongoing stream to a specific duration.",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/cd25ec6f046aa8003cfee.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/seek 10",
    ),
    lambda event: event.builder.article(
        title="Loop Stream",
        description="Loop the currently playing music. Usage: /loop [enable|disable].",
        thumb=InputWebDocument(
            url="https://telegra.ph/file/081c20ce2074ea3e9b952.png",
            mime_type="image/png",
            size=0,
            attributes=[DocumentAttributeImageSize(320, 180)],
        ),
        text="/loop 3",
    ),
]

@app.on(events.InlineQuery)
async def inline_query_handler(event):
    if event.sender_id in BANNED_USERS:
        return

    text = event.text.strip().lower()
    answers = []

    if text.strip() == "":
        try:
            await event.answer([a(event) for a in answer], cache_time=10)
        except:
            return
    else:
        a = VideosSearch(text, limit=20)
        result = (await a.next()).get("result")
        for x in range(15):
            title = (result[x]["title"]).title()
            duration = result[x]["duration"]
            views = result[x]["viewCount"]["short"]
            thumbnail = result[x]["thumbnails"][0]["url"].split("?")[0]
            channellink = result[x]["channel"]["link"]
            channel = result[x]["channel"]["name"]
            link = result[x]["link"]
            published = result[x]["publishedTime"]
            description = f"{views} | {duration} Mins | {channel}  | {published}"
            buttons = [[Button.url("🎥 Watch on YouTube", url=link)]]
            searched_text = f"""
❇️**Title:** [{title}]({link})

⏳**Duration:** {duration} Mins
👀**Views:** `{views}`
⏰**Published Time:** {published}
🎥**Channel Name:** {channel}
📎**Channel Link:** [Visit from here]({channellink})

__Reply with /play on this searched message to stream it on voice chat.__

⚡️ ** Inline search by {app.name} **"""

            answers.append(
                InputBotInlineResultPhoto(
                    id=str(x),
                    type="photo",
                    photo=InputWebDocument(
                        url=thumbnail,
                        mime_type="image/jpeg",
                        size=0,
                        attributes=[DocumentAttributeImageSize(320, 180)]
                    ),
                    title=title,
                    description=description,
                    caption=searched_text,
                    reply_markup=buttons,
                )
            )

        await event.answer(answers)