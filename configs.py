import os
class Config(object):

    API_ID = int(os.environ.get("API_ID", "13708534"))
    API_HASH = os.environ.get("API_HASH", "51b384fee3c86840ee2ba7938f0beff4")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7784529867:AAG9-hYNVY_g1bH28yCOxX_uavCNiehBXd8")
    BOT_SESSION_NAME = os.environ.get("BOT_SESSION_NAME", "DypixxSearchbot")
    USER_SESSION_STRING = os.environ.get("USER_SESSION_STRING", "BQDRLPYAOJmP9kpJUhtVbpFydyFh_tEO9w7XxYj4quGRXd6bytl-_FhV2IicCOA2uHhB71DqBjuVevq6czcbVZoG3-TJQcvA0hDHELFX85hCBCVEEHKfsvOCtDtT4uIkoT-j5mbUVG_ZOSVSf5nS566ISi-RcpMauByE7ouzrN63r2U12bduuK2hoKZiyi2TS2d23gwGVmBLYbVOL5YIg-wWe5Bs3ShJ0D4ZVL7aOMnC5-bL7SOtXyTq4O56997t0sJIOLsTFZaa_GvvlTpu4LNCsS0IyhId7Fq0OssNM9RX5P9Rn5l9SB-NbkfVUGhLjR80G0N5Rr5brkth75Z50ww5KfXZ8AAAAABqQ-a6AA")
    CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002147456374")) # Database Channel
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "SharediskSearchingRobot")
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "1782834874"))
    IS_FSUB = bool(os.environ.get("FSUB", True)) # Set "True" For Enable Force Subscribe
    AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1002421861644").split())) # Add Multiple channel id
    DATABASE_URL = os.environ.get("DATABASE_URL",  "mongodb+srv://starcinebot:mkooaa@werdeveloper.vxfam.mongodb.net/?retryWrites=true&w=majority&appName=werdeveloper")
    AUTO_DELETE = int(os.environ.get("AUTO_DELETE", "300")) # 5 min


    # Texts................

    ABOUT_BOT_TEXT = """<b>🔍 About Mdisk Search Bot</b>

<b>🚀 Powered By:</b>  
<b>• Language: <a href="https://www.python.org">Python 3</a>  
• Library: <a href="https://docs.pyrogram.org">Pyrogram v2.0.106</a>  
• Hosting: <a href="https://app.koyeb.com/">Koyeb</a></b>

<b>👨‍💻 Developed & Maintained By:</b>
<b><a href="https://t.me/dypixx">Dypixx</a></b>

<b>Have questions or suggestions?
Reach out to the developer anytime!</b>"""

    ABOUT_HELP_TEXT = """<b>❗ How to Use:</b>

<b>Just send me the movie or series name in a simple format. I will search that name in my database. If I find it, I will provide you with direct streaming and download links.</b>

<b>If I don't find anything about your movie or series, I will automatically send a request to my admins so they can add it as soon as possible.</b>

<blockquote>
  <b>Please take responsibility:</b><br>
  <b>Double-check your spelling because I cannot verify it. I will search exactly what you send me, so be careful!</b>
</blockquote>

<b><br>Format should be:<br>
Avengers Endgame 2019</b>

<blockquote>
  <b>Do NOT add words like "movie" or "series" along with the name,<br>
  otherwise, I won’t be able to give you proper results!</b>
</blockquote>"""

    HOME_TEXT = """<b>👋 {}, Welcome to the Movie & Series Finder Bot.</b>

<b>Send me the name of any movie or series, and I’ll find it for you instantly!</b>

<b>Go ahead, type a name to get started! 🎬</b>

<b><blockquote>Made With ❤ By @Dypixx</blockquote></b>"""
