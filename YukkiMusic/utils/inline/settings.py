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


def setting_markup(_):
    buttons = [
        [
            Button.inline(text=_["ST_B_1"], data="AQ"),
            Button.inline(text=_["ST_B_2"], data="VQ"),
        ],
        [
            Button.inline(text=_["ST_B_3"], data="AU"),
            Button.inline(text=_["ST_B_6"], data="LG"),
        ],
        [
            Button.inline(text=_["ST_B_5"], data="PM"),
            Button.inline(text=_["ST_B_7"], data="CM"),
        ],
        [
            Button.inline(text=_["CLOSE_BUTTON"], data="close"),
        ],
    ]
    return buttons


def audio_quality_markup(
    _,
    LOW: Union[bool, str] = None,
    MEDIUM: Union[bool, str] = None,
    HIGH: Union[bool, str] = None,
    STUDIO: Union[bool, str] = None,
):
    buttons = [
        [
            Button.inline(
                text=_["ST_B_8"].format("✅") if LOW else _["ST_B_8"].format(""),
                data="LOW",
            ),
            Button.inline(
                text=_["ST_B_9"].format("✅") if MEDIUM else _["ST_B_9"].format(""),
                data="MEDIUM",
            ),
        ],
        [
            Button.inline(
                text=_["ST_B_10"].format("✅") if HIGH else _["ST_B_10"].format(""),
                data="HIGH",
            ),
            Button.inline(
                text=_["ST_B_11"].format("✅") if STUDIO else _["ST_B_11"].format(""),
                data="STUDIO",
            ),
        ],
        [
            Button.inline(
                text=_["BACK_BUTTON"],
                data="settingsback_helper",
            ),
            Button.inline(text=_["CLOSE_BUTTON"], data="close"),
        ],
    ]
    return buttons


def video_quality_markup(
    _,
    SD_360p: Union[bool, str] = None,
    SD_480p: Union[bool, str] = None,
    HD_720p: Union[bool, str] = None,
    FHD_1080p: Union[bool, str] = None,
    QHD_2K: Union[bool, str] = None,
    UHD_4K: Union[bool, str] = None,
):
    buttons = [
        [
            Button.inline(
                text=_["ST_B_12"].format("✅") if SD_360p else _["ST_B_12"].format(""),
                data="SD_360p",
            ),
            Button.inline(
                text=_["ST_B_13"].format("✅") if SD_480p else _["ST_B_13"].format(""),
                data="SD_480p",
            ),
        ],
        [
            Button.inline(
                text=_["ST_B_14"].format("✅") if HD_720p else _["ST_B_14"].format(""),
                data="HD_720p",
            ),
            Button.inline(
                text=(
                    _["ST_B_15"].format("✅") if FHD_1080p else _["ST_B_15"].format("")
                ),
                data="FHD_1080p",
            ),
        ],
        [
            Button.inline(
                text=_["ST_B_16"].format("✅") if QHD_2K else _["ST_B_16"].format(""),
                data="QHD_2K",
            ),
            Button.inline(
                text=_["ST_B_17"].format("✅") if UHD_4K else _["ST_B_17"].format(""),
                data="UHD_4K",
            ),
        ],
        [
            Button.inline(
                text=_["BACK_BUTTON"],
                data="settingsback_helper",
            ),
            Button.inline(text=_["CLOSE_BUTTON"], data="close"),
        ],
    ]
    return buttons


def cleanmode_settings_markup(
    _,
    status: Union[bool, str] = None,
    dels: Union[bool, str] = None,
):
    buttons = [
        [
            Button.inline(text=_["ST_B_7"], data="CMANSWER"),
            Button.inline(
                text=_["ST_B_18"] if status else _["ST_B_19"],
                data="CLEANMODE",
            ),
        ],
        [
            Button.inline(text=_["ST_B_30"], data="COMMANDANSWER"),
            Button.inline(
                text=_["ST_B_18"] if dels else _["ST_B_19"],
                data="COMMANDELMODE",
            ),
        ],
        [
            Button.inline(
                text=_["BACK_BUTTON"],
                data="settingsback_helper",
            ),
            Button.inline(text=_["CLOSE_BUTTON"], data="close"),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    buttons = [
        [
            Button.inline(text=_["ST_B_3"], data="AUTHANSWER"),
            Button.inline(
                text=_["ST_B_20"] if status else _["ST_B_21"],
                data="AUTH",
            ),
        ],
        [
            Button.inline(text=_["ST_B_22"], data="AUTHLIST"),
        ],
        [
            Button.inline(
                text=_["BACK_BUTTON"],
                data="settingsback_helper",
            ),
            Button.inline(text=_["CLOSE_BUTTON"], data="close"),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    buttons = [
        [
            Button.inline(text=_["ST_B_23"], data="SEARCHANSWER"),
            Button.inline(
                text=_["ST_B_24"] if Direct else _["ST_B_25"],
                data="MODECHANGE",
            ),
        ],
        [
            Button.inline(text=_["ST_B_26"], data="AUTHANSWER"),
            Button.inline(
                text=_["ST_B_20"] if Group else _["ST_B_21"],
                data="CHANNELMODECHANGE",
            ),
        ],
        [
            Button.inline(text=_["ST_B_29"], data="PLAYTYPEANSWER"),
            Button.inline(
                text=_["ST_B_20"] if Playtype else _["ST_B_21"],
                data="PLAYTYPECHANGE",
            ),
        ],
        [
            Button.inline(
                text=_["BACK_BUTTON"],
                data="settingsback_helper",
            ),
            Button.inline(text=_["CLOSE_BUTTON"], data="close"),
        ],
    ]
    return buttons
