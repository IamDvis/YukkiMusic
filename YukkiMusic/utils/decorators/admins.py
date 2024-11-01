#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from telethon import Button
from telethon.tl.types import (
    User,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
)

from config import adminlist
from strings import get_string
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_nonadmin_chat,
)

from ..formatters import int_to_alpha


def AdminRightsCheck(mystic):
    async def wrapper(event):
        if not await is_maintenance():
            if event.sender_id not in SUDOERS:
                return
        if await is_commanddelete_on(event.chat_id):
            try:
                await event.delete()
            except:
                pass
        try:
            language = await get_lang(event.chat_id)
            _ = get_string(language)
        except:
            _ = get_string("en")
        sender = await event.get_sender()
        if not isinstance(sender, User):
            upl = [
                [
                    Button.inline(
                        text="How to Fix this? ",
                        data="AnonymousAdmin",
                    ),
                ]
            ]
            return await event.reply(_["general_4"], reply_markup=upl)
        if event.raw_text.split()[0][0] == "c":
            chat_id = await get_cmode(event.chat_id)
            if chat_id is None:
                return await event.reply(_["setting_12"])
            try:
                await app.get_entity(chat_id)
            except:
                return await event.reply(_["cplay_4"])
        else:
            chat_id = event.chat_id
        if not await is_active_chat(chat_id):
            return await event.reply(_["general_6"])
        is_non_admin = await is_nonadmin_chat(event.chat_id)
        if not is_non_admin:
            if event.sender_id not in SUDOERS:
                admins = adminlist.get(event.chat_id)
                if not admins:
                    return await event.reply(_["admin_18"])
                else:
                    if event.sender_id not in admins:
                        return await event.reply(_["admin_19"])
        return await mystic(event, _, chat_id)

    return wrapper


def AdminActual(mystic):
    async def wrapper(event):
        if not await is_maintenance():
            if event.sender_id not in SUDOERS:
                return

        if await is_commanddelete_on(event.chat_id):
            try:
                await event.delete()
            except:
                pass

        try:
            language = await get_lang(event.chat_id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        sender = await event.get_sender()
        if not isinstance(sender, User):
            upl = [
                [
                    Button.inline(
                        text="How to Fix this?",
                        data="AnonymousAdmin",
                    ),
                ]
            ]

            return await event.reply(_["general_4"], reply_markup=upl)

        if event.sender_id not in SUDOERS:
            try:
                member = await app.get_participant(event.chat_id, event.sender_id)
                if (
                    not isinstance(
                        member, (ChannelParticipantAdmin, ChannelParticipantCreator)
                    )
                    or not member.admin_rights
                    or not member.admin_rights.manage_call
                ):

                    return await event.reply(_["general_5"])

            except Exception as e:
                return await event.reply(f"Error: {str(e)}")

        return await mystic(event, _)

    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(event):
        try:
            language = await get_lang(event.chat_id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        if not await is_maintenance():
            if event.sender_id not in SUDOERS:
                return await event.answer(
                    _["maint_4"],
                    alert=True,
                )

        if event.is_private:
            return await mystic(event, _)

        is_non_admin = await is_nonadmin_chat(event.chat_id)
        if not is_non_admin:
            try:
                member = await app.get_participant(event.chat_id, event.sender_id)
                if (
                    not isinstance(
                        member, (ChannelParticipantAdmin, ChannelParticipantCreator)
                    )
                    or not member.admin_rights
                    or not member.admin_rights.manage_call
                ):
                    if event.sender_id not in SUDOERS:
                        token = await int_to_alpha(event.sender_id)
                        _check = await get_authuser_names(event.sender_id)
                        if token not in _check:
                            return await event.answer(
                                _["general_5"],
                                alert=True,
                            )

            except Exception as e:
                return await event.answer(f"Error: {str(e)}")

        return await mystic(event, _)

    return wrapper
