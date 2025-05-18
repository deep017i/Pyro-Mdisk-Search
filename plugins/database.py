from typing import Any
from configs import Config
from motor import motor_asyncio
client: motor_asyncio.AsyncIOMotorClient[Any] = motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URL)
db = client["MdiskSearchBot"]

class data:
    def __init__(self):
        self.users = db["users"]
        self.cache : dict[int, dict[str, Any]] = {}
        self.promos = db["promos"]

    async def addUser(self, user_id: int, name: str) -> dict[str, Any] | None:
        try:
            user: dict[str, Any] = {"user_id": user_id, "name": name}
            await self.users.insert_one(user)
            self.cache[user_id] = user      
            return user
        except Exception as e:
            print("Error in addUser: ", e)
            

    async def get_user(self, user_id: int) -> dict[str, Any] | None:
        try:
            if user_id in self.cache:
                return self.cache[user_id]
            user = await self.users.find_one({"user_id": user_id})
            return user
        except Exception as e:
            print("Error in getUser: ", e)
            return None
    
    async def get_all_users(self) -> list[dict[str, Any]]:
        try:
            users : list[dict[str, Any]] = []
            async for user in self.users.find():
                users.append(user)
            return users
        except Exception as e:
            print("Error in getAllUsers: ", e)
            return []

    async def ban_user(self, user_id: int, reason: str = "") -> bool:
        try:
            banned = await db["banned_users"].find_one({"user_id": user_id})
            if banned:
                return False
            await db["banned_users"].insert_one({"user_id": user_id, "reason": reason})
            return True
        except Exception as e:
            print("Error in ban_user: ", e)
            return False

    async def unban_user(self, user_id: int) -> bool:
        try:
            result = await db["banned_users"].delete_one({"user_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print("Error in unban_user: ", e)
            return False

    async def is_banned(self, user_id: int) -> bool:
        try:
            banned = await db["banned_users"].find_one({"user_id": user_id})
            return banned is not None
        except Exception as e:
            print("Error in is_banned: ", e)
            return False

    async def get_banlist(self) -> list:
        try:
            banlist = []
            async for user in db["banned_users"].find():
                banlist.append(user)
            return banlist
        except Exception as e:
            print("Error in get_banlist: ", e)
            return []

    async def add_promo(self, button_text: str, reply_msg_id: int, promo_text: str, duration_seconds: int) -> dict[str, Any] | None:
        import time
        try:
            expire_at = int(time.time()) + duration_seconds
            promo = {
                "button_text": button_text,
                "reply_msg_id": reply_msg_id,
                "promo_text": promo_text,
                "expire_at": expire_at
            }
            await self.promos.insert_one(promo)
            return promo
        except Exception as e:
            print("Error in add_promo: ", e)
            return None

    async def get_active_promo(self) -> dict[str, Any] | None:
        import time
        try:
            now = int(time.time())
            promo = await self.promos.find_one({"expire_at": {"$gt": now}}, sort=[("expire_at", -1)])
            return promo
        except Exception as e:
            print("Error in get_active_promo: ", e)
            return None
data = data()