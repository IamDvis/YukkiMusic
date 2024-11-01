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
from YukkiMusic import app
from YukkiMusic.utils.database import get_playmode, get_playtype, is_nonadmin_chat
from YukkiMusic.utils.decorators import language
from YukkiMusic.utils.inline.settings import playmode_users_markup

# Commands
PLAYMODE_COMMAND = get_command("PLAYMODE_COMMAND")


@app.on_message(
    command=PLAYMODE_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@language
async def playmode_(event, _):
    if event.is_group and event.sender_id not in BANNED_USERS:
        playmode = await get_playmode(event.chat_id)
        Direct = playmode == "Direct"

        is_non_admin = await is_nonadmin_chat(event.chat_id)
        Group = not is_non_admin

        playty = await get_playtype(event.chat_id)
        Playtype = playty != "Everyone"

        buttons = playmode_users_markup(_, Direct, Group, Playtype)

        response = await event.reply(
            _["playmode_1"].format(event.chat.title), buttons=buttons
        )
