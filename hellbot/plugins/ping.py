import asyncio
import datetime

from . import *

@bot.on(Speedo_cmd(pattern="ping$"))
@bot.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def pong(speedo):
    if speedo.fwd_from:
        return
    start = datetime.datetime.now()
    event = await eor(speedo, "`·.·★ ℘ıŋɠ ★·.·´")
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(
        f"╰•★★  ℘ơŋɠ ★★•╯\n\n    ⚘  `{ms}`\n    ⚘  __**Oɯɳҽɾ**__ **:**  {speedo_mention}"
    )


CmdHelp("ping").add_command(
  "ping", None, "Checks the ping speed of your SPEEDOBOT"
).add_warning(
  "✅ Harmless Module"
).add()

# Speedo
