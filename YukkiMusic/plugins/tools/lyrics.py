#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import random
import re
import string
import lyricsgenius as lg
from telethon import Button
from config import BANNED_USERS, lyrical
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.decorators.language import language

LYRICS_COMMAND = get_command("LYRICS_COMMAND")

api_key = "Vd9FvPMOKWfsKJNG9RbZnItaTNIRFzVyyXFdrGHONVsGqHcHBoj3AI3sIlNuqzuf0ZNG8uLcF9wAd5DXBBnUzA"
y = lg.Genius(
    api_key,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True,
)
y.verbose = False


@app.on_message(
    command=LYRICS_COMMAND,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@language
async def lrsearch(event, _):
    sender_id = event.sender_id
    if sender_id in BANNED_USERS:
        return

    if len(event.text.split()) < 2:
        await event.reply(_["lyrics_1"])
        return

    title = event.text.split(None, 1)[1]
    m = await event.reply(_["lyrics_2"])

    S = y.search_song(title, get_full_info=False)
    if S is None:
        await m.edit(_["lyrics_3"].format(title))
        return

    ran_hash = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    lyric = S.lyrics
    if "Embed" in lyric:
        lyric = re.sub(r"\d*Embed", "", lyric)
    lyrical[ran_hash] = lyric

    buttons = [
        [
            Button.url(
                _["L_B_1"], url=f"https://t.me/{app.username}?start=lyrics_{ran_hash}"
            )
        ]
    ]

    await m.edit(_["lyrics_4"], buttons=buttons)
