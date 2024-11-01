#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import config
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import YouTube, app
from YukkiMusic.core.call import Yukki
from YukkiMusic.misc import db
from YukkiMusic.utils.database import get_loop
from YukkiMusic.utils.decorators import AdminRightsCheck
from YukkiMusic.utils.inline.play import stream_markup, telegram_markup
from YukkiMusic.utils.stream.autoclean import auto_clean
from YukkiMusic.utils.thumbnails import gen_thumb

# Commands
SKIP_COMMAND = get_command("SKIP_COMMAND")


@app.on_message(
    command=SKIP_COMMAND,
    is_group=True,
    from_user=BANNED_USERS,
    is_restricted=True,
)
@AdminRightsCheck
async def skip(event, _, chat_id):
    if len(event.message.text.split()) >= 2:
        loop = await get_loop(chat_id)
        if loop != 0:
            await event.reply(_["admin_12"])
            return
        state = event.message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            check = db.get(chat_id)
            if check:
                count = len(check)
                if count > 2:
                    count -= 1
                    if 1 <= state <= count:
                        for _ in range(state):
                            try:
                                popped = check.pop(0)
                                if popped and popped.get("mystic"):
                                    await popped.get("mystic").delete()
                                await auto_clean(popped)
                            except:
                                await event.reply(_["admin_16"])
                                return
                            if not check:
                                await event.reply(
                                    _["admin_10"].format(
                                        (await event.get_sender()).first_name
                                    )
                                )
                                await Yukki.stop_stream(chat_id)
                                return
                    else:
                        await event.reply(_["admin_15"].format(count))
                        return
                else:
                    await event.reply(_["admin_14"])
                    return
            else:
                await event.reply(_["queue_2"])
                return
        else:
            await event.reply(_["admin_13"])
            return
    else:
        check = db.get(chat_id)
        try:
            popped = check.pop(0)
            await auto_clean(popped)
            if popped and popped.get("mystic"):
                await popped.get("mystic").delete()
            if not check:
                await event.reply(
                    _["admin_10"].format((await event.get_sender()).first_name)
                )
                await Yukki.stop_stream(chat_id)
                return
        except:
            await event.reply(
                _["admin_10"].format((await event.get_sender()).first_name)
            )
            await Yukki.stop_stream(chat_id)
            return

    queued = check[0]["file"]
    title = check[0]["title"].title()
    user = check[0]["by"]
    streamtype = check[0]["streamtype"]
    videoid = check[0]["vidid"]
    duration_min = check[0]["dur"]
    status = True if str(streamtype) == "video" else None

    if "live_" in queued:
        n, link = await YouTube.video(videoid, True)
        if n == 0:
            await event.reply(_["admin_11"].format(title))
            return
        try:
            await Yukki.skip_stream(chat_id, link, video=status)
        except:
            await event.reply(_["call_7"])
            return
        button = telegram_markup(_, chat_id)
        img = await gen_thumb(videoid)
        run = await app.send_file(
            event.chat_id,
            file=img,
            caption=_["stream_1"].format(
                user, f"https://t.me/{app.username}?start=info_{videoid}"
            ),
            buttons=button,
            reply_to=event.message.id,
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
    elif "vid_" in queued:
        mystic = await event.reply(_["call_8"])
        try:
            file_path, _ = await YouTube.download(
                videoid, mystic, videoid=True, video=status
            )
        except:
            await mystic.edit(_["call_7"])
            return
        try:
            await Yukki.skip_stream(chat_id, file_path, video=status)
        except:
            await mystic.edit(_["call_7"])
            return
        button = stream_markup(_, videoid, chat_id)
        img = await gen_thumb(videoid)
        run = await app.send_file(
            event.chat_id,
            file=img,
            caption=_["stream_1"].format(
                title[:27],
                f"https://t.me/{app.username}?start=info_{videoid}",
                duration_min,
                user,
            ),
            buttons=button,
            reply_to=event.message.id,
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "stream"
        await mystic.delete()
    elif "index_" in queued:
        try:
            await Yukki.skip_stream(chat_id, videoid, video=status)
        except:
            await event.reply(_["call_7"])
            return
        button = telegram_markup(_, chat_id)
        run = await app.send_file(
            event.chat_id,
            file=config.STREAM_IMG_URL,
            caption=_["stream_2"].format(user),
            buttons=button,
            reply_to=event.message.id,
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
    else:
        try:
            await Yukki.skip_stream(chat_id, queued, video=status)
        except:
            await event.reply(_["call_7"])
            return
        if videoid == "telegram":
            button = telegram_markup(_, chat_id)
            run = await app.send_file(
                event.chat_id,
                file=(
                    config.TELEGRAM_AUDIO_URL
                    if str(streamtype) == "audio"
                    else config.TELEGRAM_VIDEO_URL
                ),
                caption=_["stream_1"].format(
                    title, config.SUPPORT_GROUP, check[0]["dur"], user
                ),
                buttons=button,
                reply_to=event.message.id,
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif videoid == "soundcloud":
            button = telegram_markup(_, chat_id)
            run = await app.send_file(
                event.chat_id,
                file=(
                    config.SOUNCLOUD_IMG_URL
                    if str(streamtype) == "audio"
                    else config.TELEGRAM_VIDEO_URL
                ),
                caption=_["stream_1"].format(
                    title, config.SUPPORT_GROUP, check[0]["dur"], user
                ),
                buttons=button,
                reply_to=event.message.id,
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif "saavn" in videoid:
            button = telegram_markup(_, chat_id)
            run = await app.send_file(
                event.chat_id,
                file=check[0]["thumb"],
                caption=_["stream_1"].format(
                    title, config.SUPPORT_GROUP, check[0]["dur"], user
                ),
                buttons=button,
                reply_to=event.message.id,
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            button = stream_markup(_, videoid, chat_id)
            img = await gen_thumb(videoid)
            run = await app.send_file(
                event.chat_id,
                file=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    duration_min,
                    user,
                ),
                buttons=button,
                reply_to=event.message.id,
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
