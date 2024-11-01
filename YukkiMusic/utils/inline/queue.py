#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
from typing import Union
from telethon import Button


def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    not_dur = [
        [
            Button.inline(
                text=_["QU_B_1"],
                data=f"GetQueued {CPLAY}|{videoid}",
            ),
            Button.inline(
                text=_["CLOSEMENU_BUTTON"],
                data="close",
            ),
        ]
    ]
    dur_buttons = [
        [
            Button.inline(
                text=_["QU_B_2"].format(played, dur),
                data="GetTimer",
            )
        ],
        [
            Button.inline(
                text=_["QU_B_1"],
                data=f"GetQueued {CPLAY}|{videoid}",
            ),
            Button.inline(
                text=_["CLOSEMENU_BUTTON"],
                data="close",
            ),
        ],
    ]
    buttons = not_dur if DURATION == "Unknown" else dur_buttons
    return buttons


def queue_back_markup(_, CPLAY):
    buttons = [
        [
            Button.inline(
                text=_["BACK_BUTTON"],
                data=f"queue_back_timer {CPLAY}",
            ),
            Button.inline(
                text=_["CLOSE_BUTTON"],
                data="close",
            ),
        ]
    ]
    return buttons
