from hellbot import *
from hellbot.config import Config
from hellbot.helpers import *
from hellbot.utils import *
from hellbot.random_strings import *
from hellbot.version import __hell__


HELL_USER = Config.YOUR_NAME or "Hêll"
ForGo10God = bot.uid
hell_mention = f"[{HELL_USER}](tg://user?id={ForGo10God})"
hell_logo = "./hellbot/resources/pics/hellbot_logo.jpg"
cjb = "./hellbot/resources/pics/cjb.jpg"
restlo = "./hellbot/resources/pics/rest.jpeg"
shuru = "./hellbot/resources/pics/shuru.jpg"
hl = Config.HANDLER
shl = Config.SUDO_HANDLER
hell_ver = __hell__

async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await bot.get_entity(ids)).id
    return userid

sudos = Config.SUDO_USERS

if sudos:
    is_sudo = "True"
else:
    is_sudo = "False"

chnl_link = "https://t.me/its_hellbot"
hell_channel = f"[†hê Hêllẞø†]({chnl_link})"
grp_link = "https://t.me/HellBot_Chat"
hell_grp = f"[Hêllẞø† Group]({grp_link})"

WELCOME_FORMAT = """**Use these fomats in your welcome note to make them attractive.**

  {mention} :  To mention the user
  {title} : To get chat name in message
  {count} : To get group members
  {first} : To use user first name
  {last} : To use user last name
  {fullname} : To use user full name
  {userid} : To use userid
  {username} : To use user username
  {my_first} : To use my first name
  {my_fullname} : To use my full name
  {my_last} : To use my last name
  {my_mention} : To mention myself
  {my_username} : To use my username
"""
# will add more soon

# hellbot
