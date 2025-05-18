from configs import Config
from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .Fsub import get_fsub
from .database import data
import asyncio
import re
import time

@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, event: Message):
    if (ban_info := await data.is_banned(message.from_user.id)):return await message.reply(f"You are banned to use me. Reason: {ban_info.get('reason', 'No reason provided') if isinstance(ban_info, dict) else 'No reason provided'}")
    if await data.get_user(event.from_user.id) is None:
        await data.addUser(event.from_user.id, event.from_user.first_name)
    if Config.IS_FSUB and not await get_fsub(client, event):return
    await event.reply(
        text=Config.HOME_TEXT.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Updates Channel •", url="https://telegram.me/DypixxTech")],
            [InlineKeyboardButton("• Help •", callback_data="help"),
             InlineKeyboardButton("• About •", callback_data="about")],
            [InlineKeyboardButton("• Developer •", user_id=int(Config.BOT_OWNER))]]))


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


@Client.on_message(filters.command(["ban"]) & filters.user(Config.BOT_OWNER))
async def ban_user_handler(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Ban command ka use: /ban user_id [reason]")
        return
    try:
        user_id = int(message.command[1])
        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason"
        if await data.ban_user(user_id, reason):
            await message.reply(f"User {user_id} ban ho gaya. Reason: {reason}")
        else:
            await message.reply(f"User {user_id} pehle se ban hai ya error aayi.")
    except Exception as e:
        await message.reply(f"Ban karte waqt error: {e}")

@Client.on_message(filters.command(["unban"]) & filters.user(Config.BOT_OWNER))
async def unban_user_handler(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Unban command ka use: /unban user_id")
        return
    try:
        user_id = int(message.command[1])
        if await data.unban_user(user_id):
            await message.reply(f"User {user_id} unban ho gaya.")
        else:
            await message.reply(f"User {user_id} ban list me nahi tha ya error aayi.")
    except Exception as e:
        await message.reply(f"Unban karte waqt error: {e}")

@Client.on_message(filters.command(["banlist"]) & filters.user(Config.BOT_OWNER))
async def banlist_handler(client, message: Message):
    banlist = await data.get_banlist()
    if not banlist:
        await message.reply("Koi bhi user ban nahi hai.")
        return
    text = "<b>Ban List:</b>\n"
    for user in banlist:
        text += f"<code>{user['user_id']}</code> - {user.get('reason','No reason')}\n"
    await message.reply(text, parse_mode="html")

@Client.on_message(filters.command("addpromo") & filters.user(Config.BOT_OWNER))
async def add_promo_handler(client, message):
    if not message.reply_to_message or not message.reply_to_message.text:
        await message.reply("Reply to a text message to add promo.")
        return
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.reply("Usage: /addpromo [Button Text] [Duration, e.g. 2d or 5h]")
        return
    button_text = args[1]
    duration_arg = args[2].strip().lower()
    duration_seconds = 0
    match = re.match(r"(\d+)([dh])", duration_arg)
    if match:
        num = int(match.group(1))
        unit = match.group(2)
        if unit == "d":
            duration_seconds = num * 86400
        elif unit == "h":
            duration_seconds = num * 3600
    if duration_seconds == 0:
        await message.reply("Invalid duration. Use d for days, h for hours. Example: 2d or 5h")
        return
    promo_text = message.reply_to_message.text
    reply_msg_id = message.reply_to_message.id
    promo = await data.add_promo(button_text, reply_msg_id, promo_text, duration_seconds)
    if promo:
        expire_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(promo['expire_at']))
        await message.reply(f"Promo added!\nButton: {button_text}\nExpires at: {expire_time}")
    else:
        await message.reply("Failed to add promo.")
