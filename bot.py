from configs import Config
from pyrogram.client import Client
from pyrogram import idle
from plugins.search import User

class Bot(Client):
    def __init__(self):
        super().__init__(
            "MdiskSearchBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")
        print("""           
██████╗░██╗░░░██╗██████╗░██╗██╗░░██╗██╗░░██╗   ████████╗███████╗░█████╗░██╗░░██╗
██╔══██╗╚██╗░██╔╝██╔══██╗██║╚██╗██╔╝╚██╗██╔╝   ╚══██╔══╝██╔════╝██╔══██╗██║░░██║
██║░░██║░╚████╔╝░██████╔╝██║░╚███╔╝░░╚███╔╝░   ░░░██║░░░█████╗░░██║░░╚═╝███████║
██║░░██║░░╚██╔╝░░██╔═══╝░██║░██╔██╗░░██╔██╗░   ░░░██║░░░██╔══╝░░██║░░██╗██╔══██║
██████╔╝░░░██║░░░██║░░░░░██║██╔╝╚██╗██╔╝╚██╗   ░░░██║░░░███████╗╚█████╔╝██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝   ░░░╚═╝░░░╚══════╝░╚════╝░╚═╝░░╚═╝""")
        
    async def stop(self, *args):
        await super().stop()
        print("Bᴏᴛ Iꜱ Sᴛᴏᴘᴘᴇᴅ....")

async def main():
    app = Bot()
    await app.start()
    await User.start()
    await idle()
    await app.stop()
    await User.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())