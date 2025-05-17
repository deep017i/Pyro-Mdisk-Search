import pytz, random, string
from configs import Config
from shortzy import Shortzy
from datetime import datetime, timedelta

TOKENS = {}
VERIFIED = {}

async def get_verify_shorted_link(link):
    shortzy = Shortzy(api_key=Config.SHORTNER_API, base_site=Config.SHORTNER_URL)
    link = await shortzy.convert(link)
    return link

async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    if user.id in TOKENS.keys():
        TKN = TOKENS[user.id]
        if token in TKN.keys():
            is_used = TKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False

async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    link = f"{link}verify-{user.id}-{token}"
    shortened_verify_url = await get_verify_shorted_link(link)
    return str(shortened_verify_url)

# async def verify_user(bot, userid, token):
#     user = await bot.get_users(userid)
#     TOKENS[user.id] = {token: True}
#     tz = pytz.timezone('Asia/Kolkata')
#     today = date.today()
#     VERIFIED[user.id] = str(today)

async def verify_user(bot, userid, token):
    user = await bot.get_users(userid)
    TOKENS[user.id] = {token: True}
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    VERIFIED[user.id] = now.isoformat()

# async def check_verification(bot, userid):
#     user = await bot.get_users(userid)
#     tz = pytz.timezone('Asia/Kolkata')
#     today = date.today()
#     if user.id in VERIFIED.keys():
#         EXP = VERIFIED[user.id]
#         years, month, day = EXP.split('-')
#         comp = date(int(years), int(month), int(day))
#         if comp<today:
#             return False
#         else:
#             return True
#     else:
#         return False

async def check_verification(bot, userid):
    user = await bot.get_users(userid)
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    if user.id in VERIFIED.keys():
        exp_str = VERIFIED[user.id]
        exp_datetime = datetime.fromisoformat(exp_str)
        if now - exp_datetime > timedelta(hours=Config.VERIFIED_HOUR):
            return False
        else:
            return True
    else:
        return False
