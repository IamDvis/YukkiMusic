#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from strings import get_command
from YukkiMusic import app, SUDOERS
from YukkiMusic.utils.database import autoend_off, autoend_on

# Commands
AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")

@app.on_message(command=AUTOEND_COMMAND, from_user=SUDOERS)
async def auto_end_stream(event):
    usage = "**Usage:**\n\n/autoend [enable|disable]"
    args = event.message.text.split(maxsplit=1)
    
    if len(args) != 2:
        return await event.reply(usage)

    state = args[1].strip().lower()
    if state == "enable":
        await autoend_on()
        await event.reply(
            "Auto End enabled.\n\nBot will leave voice chat automatically after 30 seconds if no one is listening, with a warning message."
        )
    elif state == "disable":
        await autoend_off()
        await event.reply("Auto End disabled.")
    else:
        await event.reply(usage)