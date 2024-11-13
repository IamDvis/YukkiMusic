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
from telethon.errors import FloodWaitError as FloodWait
from pykeyboard import InlineKeyboard

from strings import get_command, get_string, languages_present
from YukkiMusic import app
from config import BANNED_USERS
from YukkiMusic.utils.database import get_lang, set_lang
from YukkiMusic.utils.decorators import ActualAdminCB, language, languageCB


def languages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            (
                Button.inline(
                    text=languages_present[i],
                    data=f"languages:{i}",
                )
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        Button.inline(
            text=_["BACK_BUTTON"],
            data="settingsback_helper",
        ),
        Button.inline(text=_["CLOSE_BUTTON"], data="close"),
    )
    return keyboard


@app.on_message(
    command=get_command("LANGUAGE_COMMAND"),
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@language
async def langs_command(event, _):
    keyboard = languages_keyboard(_)
    await event.reply(
        _["setting_1"].format(event.chat.title, event.chat_id),
        buttons=keyboard,
    )


@app.on(events.CallbackQuery(data="LG"))
@languageCB
async def language_cb(event, _):
    try:
        await event.answer()
    except FloodWait as e:
        await asyncio.sleep(e.seconds)
    keyboard = languages_keyboard(_)
    await event.edit(buttons=keyboard)


@app.on(events.CallbackQuery(data=r"languages:(.*?)"))
@ActualAdminCB
async def language_markup(event, _):
    language_code = event.data.decode("utf-8").split(":")[1]
    old_lang = await get_lang(event.chat_id)

    if str(old_lang) == str(language_code):
        return await event.answer(
            "You are already using the selected language.", alert=True
        )

    try:
        _ = get_string(language_code)
        await event.answer("Language changed successfully.", alert=True)
    except:
        return await event.answer(
            "Failed to change language or language is under update.", alert=True
        )

    await set_lang(event.chat_id, language_code)
    keyboard = languages_keyboard(_)
    await event.edit(buttons=keyboard)
