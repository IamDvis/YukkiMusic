from telethon import Button
import config
from strings import get_command
from YukkiMusic import app

PRIVACY_COMMAND = get_command("PRIVACY_COMMAND")

TEXT = f"""
🔒 **Privacy Policy for {app.name} !**

Your privacy is important to us. To learn more about how we collect, use, and protect your data, please review our Privacy Policy here: [Privacy Policy]({config.PRIVACY_LINK}).

If you have any questions or concerns, feel free to reach out to our [Support Team]({config.SUPPORT_GROUP}).
"""


@app.on_message(PRIVACY_COMMAND)
async def privacy(event):
    keyboard = [[Button.url("View Privacy Policy", url=config.PRIVACY_LINK)]]
    await event.reply(
        TEXT,
        buttons=keyboard,
        link_preview=False,
    )
