#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import asyncio
from datetime import datetime, timedelta
from telethon import events, types
from telethon.errors import FloodWaitError as FloodWait
import config
from config import adminlist, chatstats, clean, userstats
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_particular_top,
    get_served_chats,
    get_served_users,
    get_user_top,
    is_cleanmode_on,
    set_queries,
    update_particular_top,
    update_user_top,
)
from YukkiMusic.utils.formatters import alpha_to_int

BROADCAST_COMMAND = get_command("BROADCAST_COMMAND")
AUTO_DELETE = config.CLEANMODE_DELETE_MINS
AUTO_SLEEP = 5
IS_BROADCASTING = False
cleanmode_group = 15


@app.on(events.Raw())
async def clean_mode(event):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return
    if not isinstance(event, types.UpdateReadChannelOutbox):
        return

    chat_id = int(f"-100{event.channel_id}")
    message_id = event.max_id

    if not await is_cleanmode_on(chat_id):
        return

    if chat_id not in clean:
        clean[chat_id] = []

    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=AUTO_DELETE),
    }
    clean[chat_id].append(put)
    await set_queries(1)


@app.on_message(
    command=BROADCAST_COMMAND,
    from_user=config.OWNER_ID,
)
async def broadcast_message(event):
    global IS_BROADCASTING
    query = None

    if event.is_reply:
        x = await event.get_reply_message()
        y = event.chat_id
    else:
        if len(event.message.message.split()) < 2:
            return await event.reply("Provide a message or reply to a message.")
        query = event.message.message.split(None, 1)[1]

        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await event.reply("Provide a message or reply to a message.")

    IS_BROADCASTING = True

    if "-nobot" not in event.message.message:
        sent, pin = 0, 0
        chats = [int(chat["chat_id"]) for chat in await get_served_chats()]

        for chat_id in chats:
            if chat_id == config.LOG_GROUP_ID:
                continue
            try:
                m = (
                    await app.forward_messages(chat_id, y, x.id)
                    if event.is_reply
                    else await app.send_message(chat_id, query)
                )
                if "-pin" in event.message.message:
                    await app.pin_message(chat_id, m.id, notify=False)
                    pin += 1
                elif "-pinloud" in event.message.message:
                    await app.pin_message(chat_id, m.id, notify=True)
                    pin += 1
                sent += 1
            except FloodWait as e:
                await asyncio.sleep(e.seconds)
            except Exception:
                continue
        await event.reply(
            f"Broadcast complete.\nSent to {sent} chats.\nPinned in {pin} chats."
        )

    if "-user" in event.message.message:
        susr, pin = 0, 0
        users = [int(user["user_id"]) for user in await get_served_users()]

        for user_id in users:
            try:
                m = (
                    await app.forward_messages(user_id, y, x.id)
                    if event.is_reply
                    else await app.send_message(user_id, query)
                )
                if "-pin" in event.message.message:
                    await m.pin(notify=False)
                    pin += 1
                elif "-pinloud" in event.message.message:
                    await m.pin(notify=True)
                    pin += 1
                susr += 1
            except FloodWait as e:
                await asyncio.sleep(e.seconds)
            except Exception:
                continue
        await event.reply(
            f"Broadcast to users complete.\nSent to {susr} users.\nPinned in {pin} users."
        )

    if "-assistant" in event.message.message:
        assistants = await app.get_me()
        for assistant in assistants:
            client = await get_client(assistant)
            sent = 0
            contacts = [user.id for user in await client.get_contacts()]
            async for dialog in client.iter_dialogs():
                if dialog.id in contacts or dialog.id == config.LOG_GROUP_ID:
                    continue
                try:
                    (
                        await client.forward_messages(dialog.id, y, x.id)
                        if event.is_reply
                        else await client.send_message(dialog.id, query)
                    )
                    sent += 1
                except FloodWait as e:
                    await asyncio.sleep(e.seconds)
                except Exception:
                    continue
            await event.reply(
                f"Broadcast by assistant {assistant} complete.\nSent to {sent} chats."
            )

    IS_BROADCASTING = False


async def auto_clean():
    while True:
        await asyncio.sleep(AUTO_SLEEP)
        try:
            for chat_id in chatstats:
                for dic in chatstats[chat_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    chatstats[chat_id].pop(0)
                    spot = await get_particular_top(chat_id, vidid)
                    next_spot = (spot["spot"] + 1) if spot else 1
                    new_spot = {"spot": next_spot, "title": title}
                    await update_particular_top(chat_id, vidid, new_spot)

            for user_id in userstats:
                for dic in userstats[user_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    userstats[user_id].pop(0)
                    spot = await get_user_top(user_id, vidid)
                    next_spot = (spot["spot"] + 1) if spot else 1
                    new_spot = {"spot": next_spot, "title": title}
                    await update_user_top(user_id, vidid, new_spot)

            for chat_id in clean:
                if chat_id == config.LOG_GROUP_ID:
                    continue
                for x in clean[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.seconds)
                        except:
                            continue

            for chat_id in await get_active_chats():
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    admins = await app.get_participants(
                        chat_id, filter=types.ChannelParticipantsAdmins
                    )
                    adminlist[chat_id].extend(
                        user.id
                        for user in admins
                        if user.admin_rights and user.admin_rights.manage_call
                    )
                    authusers = await get_authuser_names(chat_id)
                    adminlist[chat_id].extend(
                        await alpha_to_int(user) for user in authusers
                    )
        except:
            continue


asyncio.create_task(auto_clean())
