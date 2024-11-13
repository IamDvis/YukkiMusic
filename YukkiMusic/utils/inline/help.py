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
from config import SUPPORT_GROUP
from YukkiMusic import app


def support_group_markup(_):
    upl = [
        [
            Button.url(
                text=_["S_B_3"],
                url=SUPPORT_GROUP,
            ),
        ]
    ]
    return upl


def help_back_markup(_):
    upl = [
        [
            Button.inline(text=_["BACK_BUTTON"], data="settings_back_helper"),
            Button.inline(text=_["CLOSE_BUTTON"], data="close"),
        ]
    ]
    return upl


def private_help_panel(_):
    buttons = [
        [Button.url(text=_["S_B_1"], url=f"https://t.me/{app.username}?start=help")],
    ]
    return buttons


help_markup = [
    [
        Button.inline("Auth", data="help_callback hb1"),
        Button.inline("Admin", data="help_callback hb2"),
        Button.inline("Active", data="help_callback hb3"),
    ],
    [
        Button.inline("Play", data="help_callback hb4"),
        Button.inline("Bot", data="help_callback hb5"),
        Button.inline("Gcast", data="help_callback hb6"),
    ],
    [
        Button.inline("Plist", data="help_callback hb7"),
        Button.inline("Dev", data="help_callback hb8"),
        Button.inline("B-list", data="help_callback hb9"),
    ],
   [
            Button.inline(text="Back", data="settingsback_helper"),
    ],
]
