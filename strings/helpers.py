HELP_1 = """
**Auth Users can use Admin commands without admin rights in your chat.**

**✧ /auth** [Username] - Add a user to AUTH LIST of the Group.

**✧ /unauth** [Username] - Remove a user from AUTH LIST of the group.

**✧ /authusers** - Check AUTH LIST of the Group."""

HELP_2 = """
**c** stands for channel play

**/pause** / **/cpause** - Pause the playing music.  
**/resume** / **/cresume** - Resume the paused music.  
**/cmute** / **/mute** - Mute the playing music.  
**/unmute** / **/cunmute** - Unmute the muted music.  
**/skip** / **/cskip** - Skip the current playing music.  
**/stop** / **/end** / **/cstop** / **/cend** - Stop the playing music.  
**/shuffle** / **/cshuffle** - Randomly shuffle the queued playlist/songs.  
**/seek** / **/cseek** - Forward seek the music.  
**/seekback** / **/cseekback** - Backward seek the music to your duration.  
**/reboot** - Reboot bot for your chat.

**/skip** / **/cskip** [Number (Example: 3)] - Skip music to a specific number. Example: **/skip 3** will skip to the third queued music and will ignore 1 and 2 in the queue.

**/loop** / **/cloop** [Enable/Disable] or [Number between 1-10] - When activated, the bot will loop the current music 1-10 times in voice chat. Default loop value is 10 times."""

HELP_3 = """
**/activevoice** / **/activevc** - Check active voice chats on the bot.  
**/activevideo** / **/activevd** - Check active voice and video calls on the bot.  
**/ac** - Check active video calls on the bot.  
**/stats** - Check bot stats."""

HELP_4 = """
**/play** / **/vplay** / **/cplay** / **/cvplay** / **/playforce** / **/vplayforce** / **/cplayforce** / **/cvplayforce** - Bot will start playing your given query on voice chat or stream live links on voice chats.

**/playmode** - Force Play stops the current playing track on voice chat and starts playing the searched track instantly without disturbing/clearing the queue.

**/channelplay** - Connect channel to a group and stream music on the channel's voice chat from your group.

**/stream** / **/cstream** / **/streamforce** / **/cstreamforce** - Stream a URL that you believe is direct or m3u8 that can't be played by **/play**."""

HELP_5 = """
**/gstats** - Get Top 10 Tracks Global Stats, Top 10 Users of Bot, Top 10 Chats on Bot, Top 10 Played in a chat, etc.

**/sudolist** - Check Sudo users of the bot.

**/lyrics** [Music Name] - Search lyrics for the particular music on the web.

**/song** / **/video** [Track Name] or [YT Link] - Download any track from YouTube in MP3 or MP4 formats.

**/queue** / **/cqueue** / **/cplayer** / **/playing** / **/cplaying** / **/player** - Check the queue list of music.

⚡️**Private Bot**:

**/authorize** [CHAT_ID] - Allow a chat to use your bot.

**/unauthorize** [CHAT_ID] - Disallow a chat from using your bot.

**/authorized** - Check all allowed chats of your bot."""

HELP_6 = """
**/broadcast /gcast [Message or Reply to any message]** » Broadcast a message to served chats of bot
Broadcasting Modes:

`-pin` » Pins your broadcasted message in served chats

`-pinloud` » Pins your broadcasted message in served chats and sends notification to the members

`-user` » Broadcast the message to users who have started your bot [You can also pin the message by adding -pin or -pinloud]

`-assistant` » Broadcast your message through all assistants of the bot

`-nobot` » Ensures that the bot doesn't broadcast the message [Useful when you don't want to broadcast the message to groups]

> Example: /broadcast /gcast -user -assistant -pin Testing broadcast"""

HELP_7 = """
**/playlist** - Check your whole playlist on the bot server.

**/deleteplaylist** / **/delplaylist** - Delete any song from your saved playlist.

**/playplaylist** / **/vplayplaylist** - Start playing your saved playlist in audio.

**/playplaylist** / **/vplayplaylist** - Start playing your playlist in video."""

HELP_8 = """
**Add and remove sudoers:**

**/addsudo** [Username or reply to a user] - Add sudo in your bot.  
**/delsudo** [Username or userid or reply to a user] - Remove from bot sudoers.  
**/sudolist** - Get a list of all sudoers.

**Heroku:**

**/usage** - Dyno usage.  
**/get_var** / **/getvar** [Var Name] - Get a config var from vars.  
**/del_var** / **/delvar** [Var Name] - Delete a var from vars.  
**/set_var** / **/setvar** [Var Name] [Value] - Add or update a var. Separate var and its value with a space.

**Bot command:**

**/restart** - Restart the bot.  
**/update** / **/gitpull** / **/up** - Update the bot.  
**/speedtest** - Check server speeds.  
**/maintenance** [enable / disable] - Toggle bot maintenance mode.  
**/logger** [enable / disable] - Toggle bot logging of searched queries to log group.  
**/log** / **/logs** / **/get_log** / **/getlog** / **/get_logs** / **/getlogs** [Number of lines] - Get logs from server.  
**/autoend** [enable / disable] - Automatically end the stream after 30s if no one is listening to songs."""

HELP_9 = """
**/blacklistchat** [chat ID] - Blacklist any chat from using the Music Bot.  
**/whitelistchat** [chat ID] - Whitelist any blacklisted chat from using the Music Bot.  
**/blacklistedchat** - Check all blocked chats.

**/block** [Username or reply to a user] - Prevents a user from using bot commands.  
**/unblock** [Username or reply to a user] - Remove a user from the bot's blocked list.  
**/blockedusers** - Check the list of blocked users.

**/gban** [Username or reply to a user] - Gban a user from all served chats and stop them from using your bot.  
**/ungban** [Username or reply to a user] - Remove a user from the bot's gban list and allow them to use your bot.  
**/gbannedusers** - Check the list of gban users."""
