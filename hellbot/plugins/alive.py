from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

#-------------------------------------------------------------------------------

speedo_pic = Config.ALIVE_PIC or "https://telegra.ph/file/ea9e11f7c9db21c1b8d5e.mp4"
alive_c = f"__**π₯π₯Speedo Ι¨s ΦΥΌΚΙ¨ΥΌΙπ₯π₯**__\n\n"
alive_c += f"__βΌ ΓwΓ±Γͺr β__ : γ {speedo_mention} γ\n\n"
alive_c += f"β’β¦β’ Telethon     :  `{tel_ver}` \n"
alive_c += f"β’β¦β’ SPEEDOBOT       :  __**{speedo_ver}**__\n"
alive_c += f"β’β¦β’ Sudo            :  `{is_sudo}`\n"
alive_c += f"β’β¦β’ Channel      :  {speedo_channel}\n"

#-------------------------------------------------------------------------------

@bot.on(Speedo_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def up(speedo):
    if speedo.fwd_from:
        return
    await speedo.get_chat()
    await speedo.delete()
    await bot.send_file(speedo.chat_id, speedo_pic, caption=alive_c)
    await speedo.delete()

msg = f"""
**β‘ Π½ΡββΠ²ΟΡ ΞΉΡ ΟΠΈβΞΉΠΈΡ β‘**
{Config.ALIVE_MSG}
**π π±ππ ππππππ π**
**Telethon :**  `{tel_ver}`
**SPEEDOBOT  :**  **{speedo_ver}**
**Abuse    :**  **{abuse_m}**
**Sudo      :**  **{is_sudo}**
"""
botname = Config.BOT_USERNAME

@bot.on(Speedo_cmd(pattern="speedo$"))
@bot.on(sudo_cmd(pattern="speedo$", allow_sudo=True))
async def speedo_a(event):
    try:
        speedo = await bot.inline_query(botname, "alive")
        await speedo[0].click(event.chat_id)
        if event.sender_id == ForGo10God:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "speedo", None, "Shows Inline Alive Menu with more details."
).add_warning(
  "β Harmless Module"
).add()
