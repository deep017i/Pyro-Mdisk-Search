from configs import Config
from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .Fsub import get_fsub
from .database import data
import asyncio
from extraa import verify_user, check_token

# @Client.on_message(filters.private & filters.command("start"))
# async def start_handler(client: Client, event: Message):

#     data = event.command[1]
#     if data.split("-", 1)[0] == "verify":
#         userid = data.split("-", 2)[1]
#         token = data.split("-", 3)[2]
#         if str(event.from_user.id) != str(userid):return await event.reply_text(text="<b>Invalid link or Expired link !</b>",protect_content=True)
#         is_valid = await check_token(client, userid, token)
#         if is_valid == True:
#             await event.reply_text(text=f"<b>👋 {event.from_user.mention},\n\n🎉 Verification Successful! 🎉\n\n<blockquote>⏰ You now have unlimited access for the next 24 hours.</blockquote></b>",protect_content=True)
#             await verify_user(client, userid, token)
#         else:
#             return await event.reply_text(text="<b>Invalid link or Expired link !</b>",protect_content=True)

#     if await data.get_user(event.from_user.id) is None:
#         await data.addUser(event.from_user.id, event.from_user.first_name)
#     if Config.IS_FSUB and not await get_fsub(client, event):return
#     await event.reply(
#         text=Config.HOME_TEXT.format(event.from_user.mention),
#         reply_markup=InlineKeyboardMarkup([
#             [InlineKeyboardButton("• Updates Channel •", url="https://telegram.me/DypixxTech")],
#             [InlineKeyboardButton("• Help •", callback_data="help"),
#              InlineKeyboardButton("• About •", callback_data="about")],
#             [InlineKeyboardButton("• Developer •", user_id=int(Config.BOT_OWNER))]]))

@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, event: Message):
    data = event.command[1] if len(event.command) > 1 else None
    if data and data.startswith("verify-"):
        try:
            _, userid, token = data.split("-", 2)
        except ValueError:
            return await event.reply_text("<b>Invalid verification link format!</b>", protect_content=True)
        if str(event.from_user.id) != str(userid):
            return await event.reply_text("<b>Invalid or expired link!</b>", protect_content=True)
        is_valid = await check_token(client, userid, token)
        if is_valid:
            await event.reply_text(
                f"<b>👋 {event.from_user.mention},\n\n🎉 Verification Successful! 🎉\n\n"
                "<blockquote>⏰ You now have unlimited access for the next 24 hours.</blockquote></b>",
                protect_content=True
            )
            await verify_user(client, userid, token)
            return
        else:
            return await event.reply_text("<b>Invalid or expired link!</b>", protect_content=True)
    if await data.get_user(event.from_user.id) is None:
        await data.addUser(event.from_user.id, event.from_user.first_name)
    if Config.IS_FSUB and not await get_fsub(client, event):return
    await event.reply(
        text=Config.HOME_TEXT.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Updates Channel •", url="https://telegram.me/DypixxTech")],
            [InlineKeyboardButton("• Help •", callback_data="help"),
             InlineKeyboardButton("• About •", callback_data="about")],
            [InlineKeyboardButton("• Developer •", user_id=int(Config.BOT_OWNER))]
        ])
    )


@Client.on_message(filters.command("broadcast") & (filters.private) & filters.user(Config.BOT_OWNER))
async def broadcasting_func(client : Client, message: Message):
    msg = await message.reply_text("Wait a second!")
    if not message.reply_to_message:
        return await msg.edit("<b>Please reply to a message to broadcast.</b>")
    await msg.edit("Processing ...")
    completed = 0
    failed = 0
    to_copy_msg = message.reply_to_message
    users_list = await data.get_all_users()
    for i , userDoc in enumerate(users_list):
        if i % 20 == 0:
            await msg.edit(f"Total : {i} \nCompleted : {completed} \nFailed : {failed}")
        user_id = userDoc.get("user_id")
        if not user_id:
            continue
        try:
            await to_copy_msg.copy(user_id)
            completed += 1
        except FloodWait as e:
            if isinstance(e.value , int | float):
                await asyncio.sleep(e.value)
                await to_copy_msg.copy(user_id)
                completed += 1
        except Exception as e:
            print("Error in broadcasting:", e) 
            failed += 1
            pass
    await msg.edit(f"Successfully Broadcasted\nTotal : {len(users_list)} \nCompleted : {completed} \nFailed : {failed}")
