#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from config import BANNED_USERS, START_IMG_URL
from strings import get_command, get_string
from YukkiMusic import app
from YukkiMusic.utils.database import get_lang, is_commanddelete_on
from YukkiMusic.utils.decorators.language import LanguageStart
from YukkiMusic.utils.inline.help import private_help_panel, help_markup

### Command
HELP_COMMAND = get_command("HELP_COMMAND")


@app.on_message(
    command=HELP_COMMAND,
    is_private=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@app.on(events.CallbackQuery(pattern=r"settings_back_helper"))
async def helper_private(event):
    chat_id = event.chat_id
    language = await get_lang(chat_id)
    _ = get_string(language)
    is_callback = hasattr(event, "data")
    if is_callback:
        try:
            await event.answer()
        except:
            pass
        await event.edit(_["help_1"], buttons=help_markup)
    else:
        if await is_commanddelete_on(event.chat_id):
            try:
                await update.delete()
            except:
                pass
        if START_IMG_URL:
            await app.send_file(
                event.chat_id,
                file=START_IMG_URL,
                caption=_["help_1"],
                buttons=help_markup,
            )

        else:
            await event.respond(
                text=_["help_1"],
                buttons=help_markup,
            )


@app.on_message(
    command=HELP_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@LanguageStart
async def help_com_group(event, _):
    keyboard = private_help_panel(_)
    await event.reply(_["help_2"], buttons=keyboard)


@app.on(events.CallbackQuery(pattern=r"help_callback (.*)"))
@LanguageCB
async def helper_cb(event, _):
    cba = event.data.decode("utf-8").split(" ", 1)[-1]
    keyboard = help_back_markup(_)
    if cb == "hb1":
        await event.edit(helpers.HELP_1, buttons=keyboard)
    elif cb == "hb2":
        await event.edit(helpers.HELP_2, buttons=keyboard)
    elif cb == "hb3":
        await event.edit(helpers.HELP_3, buttons=keyboard)
    elif cb == "hb4":
        await event.edit(helpers.HELP_4, buttons=keyboard)
    elif cb == "hb5":
        await event.edit(helpers.HELP_5, buttons=keyboard)
    elif cb == "hb6":
        await event.edit(helpers.HELP_6, buttons=keyboard)
    elif cb == "hb7":
        await event.edit(helpers.HELP_7, buttons=keyboard)
    elif cb == "hb8":
        await event.edit(helpers.HELP_8, buttons=keyboard)
    elif cb == "hb9":
        await event.edit(helpers.HELP_9, buttons=keyboard)
