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
from telethon.errors import MessageNotModified
from telethon.tl.types import Chat
from config import BANNED_USERS, CLEANMODE_DELETE_MINS, OWNER_ID
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.database import (
    add_nonadmin_chat,
    cleanmode_off,
    cleanmode_on,
    commanddelete_off,
    commanddelete_on,
    get_aud_bit_name,
    get_authuser,
    get_authuser_names,
    get_playmode,
    get_playtype,
    get_vid_bit_name,
    is_cleanmode_on,
    is_commanddelete_on,
    is_nonadmin_chat,
    remove_nonadmin_chat,
    save_audio_bitrate,
    save_video_bitrate,
    set_playmode,
    set_playtype,
)
from YukkiMusic.utils.decorators.admins import ActualAdminCB
from YukkiMusic.utils.decorators.language import language, languageCB
from YukkiMusic.utils.inline.settings import (
    audio_quality_markup,
    auth_users_markup,
    cleanmode_settings_markup,
    playmode_users_markup,
    setting_markup,
    video_quality_markup,
)
from YukkiMusic.utils.inline.start import private_panel

### Command
SETTINGS_COMMAND = get_command("SETTINGS_COMMAND")


# Settings command handler
@app.on_message(
    command=SETTINGS_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@language
async def settings_mar(event, _):
    buttons = setting_markup(_)
    await event.reply(
        _["setting_1"].format(event.chat.title, event.chat.id),
        buttons=buttons,
    )


@app.on(
    events.CallbackQuery(
        pattern=r"settings_helper", func=lambda e: e.sender_id not in BANNED_USERS
    )
)
@languageCB
async def settings_cb(event, _):
    await event.answer(_["set_cb_8"], alert=True)
    buttons = setting_markup(_)
    await event.edit(
        _["setting_1"].format(event.chat.title, event.chat.id),
        buttons=buttons,
    )


@app.on(
    events.CallbackQuery(
        pattern=r"settingsback_helper", func=lambda e: e.sender_id not in BANNED_USERS
    )
)
@languageCB
async def settings_back_markup(event, _):
    await event.answer()
    if isinstance(event.chat, Chat):
        try:
            await app.get_entity(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        buttons = private_panel(_, app.username, OWNER)
        try:
            await event.edit(
                _["start_1"].format(app.mention),
                buttons=buttons,
            )
        except MessageNotModified:
            pass
    else:
        buttons = setting_markup(_)
        try:
            await event.edit(buttons=buttons)
        except MessageNotModified:
            pass


# Generate buttons for audio quality
async def gen_buttons_aud(_, aud):
    if aud == "STUDIO":
        buttons = audio_quality_markup(_, STUDIO=True)
    elif aud == "HIGH":
        buttons = audio_quality_markup(_, HIGH=True)
    elif aud == "MEDIUM":
        buttons = audio_quality_markup(_, MEDIUM=True)
    elif aud == "LOW":
        buttons = audio_quality_markup(_, LOW=True)
    return buttons


# Generate buttons for video quality
async def gen_buttons_vid(_, aud):
    if aud == "UHD_4K":
        buttons = video_quality_markup(_, UHD_4K=True)
    elif aud == "QHD_2K":
        buttons = video_quality_markup(_, QHD_2K=True)
    elif aud == "FHD_1080p":
        buttons = video_quality_markup(_, FHD_1080p=True)
    elif aud == "HD_720p":
        buttons = video_quality_markup(_, HD_720p=True)
    elif aud == "SD_480p":
        buttons = video_quality_markup(_, SD_480p=True)
    elif aud == "SD_360p":
        buttons = video_quality_markup(_, SD_360p=True)
    return buttons


@app.on(
    events.CallbackQuery(
        pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|CMANSWER|COMMANDANSWER|CM|AQ|VQ|PM|AU)$",
        func=lambda e: e.sender_id not in BANNED_USERS,
    )
)
@languageCB
async def without_Admin_rights(event, _):
    command = event.pattern_match.group(1)
    if command == "SEARCHANSWER":
        await event.answer(_["setting_3"], alert=True)
    elif command == "PLAYMODEANSWER":
        await event.answer(_["setting_10"], alert=True)
    elif command == "PLAYTYPEANSWER":
        await event.answer(_["setting_11"], alert=True)
    elif command == "AUTHANSWER":
        await event.answer(_["setting_4"], alert=True)
    elif command == "CMANSWER":
        await event.answer(_["setting_9"].format(CLEANMODE_DELETE_MINS), alert=True)
    elif command == "COMMANDANSWER":
        await event.answer(_["setting_14"], alert=True)
    elif command == "CM":
        await event.answer(_["set_cb_5"], alert=True)
        sta = await is_commanddelete_on(event.chat_id)
        cle = await is_cleanmode_on(event.chat_id)
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
    elif command == "AQ":
        await event.answer(_["set_cb_1"], alert=True)
        aud = await get_aud_bit_name(event.chat_id)
        buttons = await gen_buttons_aud(_, aud)
    elif command == "VQ":
        await event.answer(_["set_cb_2"], alert=True)
        aud = await get_vid_bit_name(event.chat_id)
        buttons = await gen_buttons_vid(_, aud)
    elif command == "PM":
        await event.answer(_["set_cb_4"], alert=True)
        playmode = await get_playmode(event.chat_id)
        is_non_admin = await is_nonadmin_chat(event.chat_id)
        playty = await get_playtype(event.chat_id)
        buttons = playmode_users_markup(
            _, playmode == "Direct", not is_non_admin, playty != "Everyone"
        )
    elif command == "AU":
        await event.answer(_["set_cb_3"], alert=True)
        is_non_admin = await is_nonadmin_chat(event.chat_id)
        buttons = auth_users_markup(_, not is_non_admin)
    await event.edit(buttons=buttons)


@app.on(
    events.CallbackQuery(
        pattern=r"^(LOW|MEDIUM|HIGH|STUDIO|SD_360p|SD_480p|HD_720p|FHD_1080p|QHD_2K|UHD_4K)$",
        func=lambda e: e.sender_id not in BANNED_USERS,
    )
)
@ActualAdminCB
async def aud_vid_cb(event, _):
    command = event.pattern_match.group(1)
    await event.answer(_["set_cb_6"], alert=True)
    if command in ["LOW", "MEDIUM", "HIGH", "STUDIO"]:
        await save_audio_bitrate(event.chat_id, command)
        buttons = audio_quality_markup(_, **{command: True})
    else:
        await save_video_bitrate(event.chat_id, command)
        buttons = video_quality_markup(_, **{command: True})
    await event.edit(buttons=buttons)


@app.on(
    events.CallbackQuery(
        pattern=r"^(CLEANMODE|COMMANDELMODE)$",
        func=lambda e: e.sender_id not in BANNED_USERS,
    )
)
@ActualAdminCB
async def cleanmode_mark(event, _):
    command = event.pattern_match.group(1)
    await event.answer(_["set_cb_6"], alert=True)
    if command == "CLEANMODE":
        cle = not await is_cleanmode_on(event.chat_id)
        sta = await is_commanddelete_on(event.chat_id)
        await (cleanmode_on if cle else cleanmode_off)(event.chat_id)
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
    elif command == "COMMANDELMODE":
        sta = not await is_commanddelete_on(event.chat_id)
        cle = await is_cleanmode_on(event.chat_id)
        await (commanddelete_on if sta else commanddelete_off)(event.chat_id)
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
    await event.edit(buttons=buttons)


# Play Mode Settings
@app.on(
    events.CallbackQuery(
        pattern=r"^(MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$",
        func=lambda e: e.sender_id not in BANNED_USERS,
    )
)
@ActualAdminCB
async def playmode_ans(event, _):
    command = event.pattern_match.group(1)
    await event.answer(_["set_cb_6"], alert=True)
    if command == "CHANNELMODECHANGE":
        is_non_admin = not await is_nonadmin_chat(event.chat_id)
        await (remove_nonadmin_chat if is_non_admin else add_nonadmin_chat)(
            event.chat_id
        )
        buttons = playmode_users_markup(
            _,
            await get_playmode(event.chat_id) == "Direct",
            is_non_admin,
            await get_playtype(event.chat_id) != "Everyone",
        )
    elif command == "MODECHANGE":
        playmode = await get_playmode(event.chat_id)
        await set_playmode(
            event.chat_id, "Direct" if playmode == "Inline" else "Inline"
        )
        buttons = playmode_users_markup(
            _,
            playmode == "Direct",
            not await is_nonadmin_chat(event.chat_id),
            await get_playtype(event.chat_id) != "Everyone",
        )
    elif command == "PLAYTYPECHANGE":
        playtype = await get_playtype(event.chat_id)
        await set_playtype(
            event.chat_id, "Admin" if playtype == "Everyone" else "Everyone"
        )
        buttons = playmode_users_markup(
            _,
            await get_playmode(event.chat_id) == "Direct",
            not await is_nonadmin_chat(event.chat_id),
            playtype != "Everyone",
        )
    await event.edit(buttons=buttons)


# Auth Users Settings
@app.on(
    events.CallbackQuery(
        pattern=r"^(AUTH|AUTHLIST)$", func=lambda e: e.sender_id not in BANNED_USERS
    )
)
@ActualAdminCB
async def authusers_mar(event, _):
    command = event.pattern_match.group(1)
    if command == "AUTHLIST":
        _authusers = await get_authuser_names(event.chat_id)
        if not _authusers:
            await event.answer(_["setting_5"], alert=True)
        else:
            await event.answer(_["set_cb_7"], alert=True)
            j = 0
            msg = _["auth_7"]
            for note in _authusers:
                _note = await get_authuser(event.chat_id, note)
                user_id = _note["auth_user_id"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_entity(user_id)
                    user_name = user.first_name
                    j += 1
                    msg += f"{j} ➤ {user_name} [`{user_id}`]\n"
                    msg += f"   {_['auth_8']} {admin_name} [`{admin_id}`]\n\n"
                except:
                    continue

            upl = [
                [
                    Button.inline(text=_["BACK_BUTTON"], data="AU"),
                    Button.inline(text=_["CLOSE_BUTTON"], data="close"),
                ]
            ]
            await event.edit(msg, buttons=upl)
    else:  # command == "AUTH"
        await event.answer(_["set_cb_6"], alert=True)
        is_non_admin = await is_nonadmin_chat(event.chat_id)
        buttons = auth_users_markup(_, not is_non_admin)
        await event.edit(buttons=buttons)
