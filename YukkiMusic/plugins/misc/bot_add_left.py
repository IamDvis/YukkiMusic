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
from config import LOG, LOG_GROUP_ID
from YukkiMusic import app
from YukkiMusic.utils.database import delete_served_chat, get_assistant, is_on_off


@app.on(events.ChatAction)
async def on_bot_added_or_kicked(event):
    try:
        if not await is_on_off(LOG):
            return

        chat = await event.get_chat()
        userbot = await get_assistant(chat.id)

        if event.user_added or event.user_joined:
            for member in event.users:
                if member.id == app.id:
                    count = await app.get_participants_count(chat.id)
                    username = chat.username if chat.username else "Private Chat"
                    added_by = await app.get_entity(event.added_by) if event.added_by else None
                    added_by_mention = (
                        await app.create_mention(added_by) if added_by else "Unknown"
                    )

                    msg = (
                        f"**Music bot added in new Group #New_Group**\n\n"
                        f"**Chat Name:** {chat.title}\n"
                        f"**Chat Id:** {chat.id}\n"
                        f"**Chat Username:** @{username}\n"
                        f"**Chat Member Count:** {count}\n"
                        f"**Added By:** {added_by_mention}"
                    )
                    await app.send_message(
                        LOG_GROUP_ID,
                        message=msg,
                        buttons=[
                            [
                                Button.url(
                                    text=f"Added by: {added_by.first_name}" if added_by else "Unknown",
                                    url=f"tg://user?id={added_by.id}" if added_by else "tg://user?id=0",
                                )
                            ]
                        ],
                    )
                    if chat.username:
                        await userbot.join_chat(chat.username)

        elif event.user_kicked or event.user_left:
            if event.user_id == app.id:
                removed_by = await app.get_entity(event.action_message.from_id) if event.action_message else None
                remove_by_mention = (
                    await app.create_mention(removed_by) if removed_by else "Unknown User"
                )

                title = chat.title
                username = f"@{chat.username}" if chat.username else "Private Chat"
                chat_id = chat.id
                left = (
                    f"Bot was Removed in {title} #Left_group\n"
                    f"**Chat Name**: {title}\n"
                    f"**Chat Id**: {chat_id}\n"
                    f"**Chat Username**: {username}\n"
                    f"**Removed By**: {remove_by_mention}"
                )

                await app.send_message(
                    LOG_GROUP_ID,
                    message=left,
                    buttons=[
                        [
                            Button.url(
                                text=f"Removed By: {removed_by.first_name}" if removed_by else "Unknown User",
                                url=f"tg://user?id={removed_by.id}" if removed_by else "tg://user?id=0",
                            )
                        ]
                    ],
                )
                await delete_served_chat(chat_id)
                await userbot.leave_chat(chat_id)
    except Exception:
        pass