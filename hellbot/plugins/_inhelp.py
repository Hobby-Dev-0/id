from math import ceil
from re import compile
import asyncio
import html
import os
import re
import sys

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from . import *

speedo_row = Config.BUTTONS_IN_HELP
speedo_emoji = Config.EMOJI_IN_HELP
speedo_pic = Config.PMPERMIT_PIC or "https://telegra.ph/file/58df4d86400922aa32acd.jpg"
cstm_pmp = Config.CUSTOM_PMPERMIT
ALV_PIC = Config.ALIVE_PIC
help_pic = Config.HELP_PIC or "https://telegra.ph/file/62b0f29c8887887f259ac.jpg"
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Config.LOGGER_ID
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
)

USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**ð« Blocked and Reported**"

HELL_FIRST = (
    "**ð¥ SPEEDOBOT PrÃ®vÃ£â Ã© SÃªÃ§Ã¼rÃ¯ty PrÃ¸â Ã¶Ã§Ãµl ð¥**\n\nThis is to inform you that "
    "{} is currently unavailable.\nThis is an automated message.\n\n"
    "{}\n\n**Please Choose Why You Are Here!!**"
)

alive_txt = """
**âï¸ Ð½ÑââÐ²ÏÑ Î¹Ñ ÏÐ¸âÎ¹Ð¸Ñ âï¸**
{}
**ð ð±ðð ðððððð ð**

**Telethon :**  `{}`
**SPEEDOBOT  :**  **{}**
**Abuse    :**  **{}**
**Sudo      :**  **{}**
"""

def button(page, modules):
    Row = speedo_row
    Column = 3

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(f"{speedo_emoji} " + pair + f" {speedo_emoji}", data=f"Information[{page}]({pair})")
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
               f"âï¸ Back {speedo_emoji}", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"â¢ â â¢", data="close"
            ),
            custom.Button.inline(
               f"{speedo_emoji} Next â¶ï¸", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]


    modules = CMD_HELP
if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query == "Speedo_help":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            help_msg = f"ð° **{speedo_mention}**\n\nð __No.of Plugins__ : `{len(CMD_HELP)}` \nðï¸ __Commands__ : `{len(apn)}`\nðï¸ __Page__ : 1/{veriler[0]}"
            if help_pic and help_pic.endswith((".jpg", ".png")):
                result = builder.photo(
                    help_pic,
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic:
                result = builder.document(
                    help_pic,
                    text=help_msg,
                    title="HellBot Alive",
                    buttons=veriler[1],
                    link_preview=False,
                )
            else:
                result = builder.article(
                    f"Hey! Only use .help please",
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
        elif event.query.user_id == bot.uid and query.startswith("fsub"):
            hunter = event.pattern_match.group(1)
            speedo = hunter.split("+")
            user = await bot.get_entity(int(speedo[0]))
            channel = await bot.get_entity(int(speedo[1]))
            msg = f"**ð Welcome** [{user.first_name}](tg://user?id={user.id}), \n\n**ð You need to Join** {channel.title} **to chat in this group.**"
            if not channel.username:
                link = (await bot(ExportChatInviteRequest(channel))).link
            else:
                link = "https://t.me/" + channel.username
            result = [
                await builder.article(
                    title="force_sub",
                    text = msg,
                    buttons=[
                        [Button.url(text="Channel", url=link)],
                        [custom.Button.inline("ð Unmute Me", data=unmute)],
                    ],
                )
            ]

        elif event.query.user_id == bot.uid and query == "alive":
            he_ll = alive_txt.format(Config.ALIVE_MSG, tel_ver, speedo_ver, abuse_m, is_sudo)
            alv_btn = [
                [Button.url(f"{HELL_USER}", f"tg://openmessage?user_id={ForGo10God}")],
                [Button.url("My Channel", f"https://t.me/{my_channel}"), 
                Button.url("My Group", f"https://t.me/{my_group}")],
            ]
            if ALV_PIC and ALV_PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    ALV_PIC,
                    text=he_ll,
                    buttons=alv_btn,
                    link_preview=False,
                )
            elif ALV_PIC:
                result = builder.document(
                    ALV_PIC,
                    text=he_ll,
                    title="HellBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=he_ll,
                    title="HellBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                )

        elif event.query.user_id == bot.uid and query == "pm_warn":
            hel_l = HELL_FIRST.format(speedo_mention, mssge)
            result = builder.photo(
                file=speedo_pic,
                text=hel_l,
                buttons=[
                    [
                        custom.Button.inline("ð Request ð", data="req"),
                        custom.Button.inline("ð¬ Chat ð¬", data="chat"),
                    ],
                    [custom.Button.inline("ð« Spam ð«", data="heheboi")],
                    [custom.Button.inline("Curious â", data="pmclick")],
                ],
            )

        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**â¡ ÊÉÉ¢ÉÕ¼ÉaÊÊ á´Ò Speedo â¡**",
                buttons=[
                    [Button.url("ð Repo ð", "https://github.com/The-HellBot/HellBot")],
                    [Button.url("ð Deploy ð", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FThe-HellBot%2FHellBot&template=https%3A%2F%2Fgithub.com%2Fthe-Speedo%2FSpeedo")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[âââ â]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@Its_HellBot",
                text="""**Hey! This is [SPEEDOBOT](https://t.me/its_Speedo) \nYou can know more about me from the links given below ð**""",
                buttons=[
                    [
                        custom.Button.url("ð¥ CHANNEL ð¥", "https://t.me/Its_HellBot"),
                        custom.Button.url(
                            "â¡ GROUP â¡", "https://t.me/Speedo_chat"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "â¨ REPO â¨", "https://github.com/The-HellBot/HellBot"),
                        custom.Button.url
                    (
                            "ð° TUTORIAL ð°", "https://youtu.be/M2FQJq_sHp4"
                    )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for Other Users..."
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"ð° This is SPEEDOBOT PM Security for {speedo_mention} to keep away unwanted retards from spamming PM..."
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"â **Request Registered** \n\n{speedo_mention} will now decide to look for your request or not.\nð Till then wait patiently and don't spam!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**ð Hey {speedo_mention} !!** \n\nâï¸ You Got A Request From [{first_name}](tg://user?id={ok}) In PM!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"chat")))
    async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Ahh!! You here to do chit-chat!!\n\nPlease wait for {speedo_mention} to come. Till then keep patience and don't spam."
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**ð Hey {speedo_mention} !!** \n\nâï¸ You Got A PM from  [{first_name}](tg://user?id={ok})  for random chats!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"ð¥´ **Nikal lawde\nPehli fursat me nikal**"
            )
            await bot(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await bot.send_message(
                LOG_GP,
                f"**Blocked**  [{first_name}](tg://user?id={ok}) \n\nReason:- Spam",
            )


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"unmute")))
    async def on_pm_click(event):
        hunter = (event.data_match.group(1)).decode("UTF-8")
        speedo = hunter.split("+")
        if not event.sender_id == int(speedo[0]):
            return await event.answer("This Ain't For You!!", alert=True)
        try:
            await bot(GetParticipantRequest(int(speedo[1]), int(speedo[0])))
        except UserNotParticipantError:
            return await event.answer(
                "You need to join the channel first.", alert=True
            )
        await bot.edit_permissions(
            event.chat_id, int(speedo[0]), send_message=True, until_date=None
        )
        await event.edit("Yay! You can chat now !!")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
            if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
                current_page_number=0
                simp = button(current_page_number, CMD_HELP)
                veriler = button(0, sorted(CMD_HELP))
                apn = []
                for x in CMD_LIST.values():
                    for y in x:
                        apn.append(y)
                await event.edit(
                    f"ð° **{speedo_mention}**\n\nð __No.of Plugins__ : `{len(CMD_HELP)}` \nðï¸ __Commands__ : `{len(apn)}`\nðï¸ __Page__ : 1/{veriler[0]}",
                    buttons=simp[1],
                    link_preview=False,
                )
            else:
                reply_pop_up_alert = "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. Â© SPEEDOBOT â¢"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            veriler = custom.Button.inline(f"{speedo_emoji} Re-Open Menu {speedo_emoji}", data="reopen")
            await event.edit(f"**âï¸ SPEEDOBOT MÃªÃ±Ã» PrÃµvÃ®dÃªr Ã¬s Ã±Ã´w ÃlÃ¶sÃ«d âï¸**\n\n**Bot Of :**  {speedo_mention}\n\n        [Â©ï¸ SPEEDOBOT â¢ï¸]({chnl_link})", buttons=veriler, link_preview=False)
        else:
            reply_pop_up_alert = "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. Â© SPEEDOBOT â¢"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
   

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f"ð° **{speedo_mention}**\n\nð __No.of Plugins__ : `{len(CMD_HELP)}`\nðï¸ __Commands__ : `{len(apn)}`\nðï¸ __Page__ : {page + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. Â© SPEEDOBOT â¢",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "â¡ " + cmd[0] + " â¡", data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "No Description is written for this plugin", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{speedo_emoji} Main Menu {speedo_emoji}", data=f"page({page})")])
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f"**ð File :**  `{commands}`\n**ð¢ Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. Â© SPEEDOBOT â¢",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**ð File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**â ï¸ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**â ï¸ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**â¹ï¸ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**ð  Commands :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**ð  Commands :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**ð¬ Explanation :**  `{command['usage']}`\n\n"
        else:
            result += f"**ð¬ Explanation :**  `{command['usage']}`\n"
            result += f"**â¨ï¸ For Example :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                result,
                buttons=[
                    custom.Button.inline(f"{speedo_emoji} Return {speedo_emoji}", data=f"Information[{page}]({cmd})")
                ],
                link_preview=False,
            )
        else:
            return await event.answer(
                "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. Â© SPEEDOBOT â¢",
                cache_time=0,
                alert=True,
            )


# Speedo
