from configs import Config
from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .Fsub import get_fsub
import asyncio
import os
from .database import data

User = Client(
    Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.USER_SESSION_STRING
)

@Client.on_message(filters.text & (filters.private | filters.group))
async def inline_handlers(client, event: Message):
    if Config.IS_FSUB and not await get_fsub(client, event):return
    if event.text.startswith('/'):
        return
    try:
        s = await event.reply_text(
            f"**🔍 Searching for:** {event.text}", disable_web_page_preview=True
        )
        answers = ""
        found_results = False

        async for message in User.search_messages(
            chat_id=Config.CHANNEL_ID, limit=50, query=event.text.strip()
        ):
            found_results = True
            if message.text:
                f_text = message.text.split(
                    "|||", 1)[0] if "|||" in message.text else message.text
                title = f_text.split("\n", 1)[0].strip()
                content = f_text.split("\n", 2)[-1].strip()
                answers += f"**🎬 {title}\n\n{content}**\n\n"
            elif message.photo and message.caption:
                f_text = message.caption.split(
                    "|||", 1)[0] if "|||" in message.caption else message.caption
                title = f_text.split("\n", 1)[0].strip()
                content = f_text.split("\n", 2)[-1].strip()
                answers += f"**🎬 {title}\n\n{content}**\n\n"

        await asyncio.sleep(1.5)
        await s.delete()

        if not found_results:
            google = f"https://www.google.com/search?q={event.text}+movie"
            q = await event.reply_text(
                f"<b><blockquote>No results found for: {event.text}</blockquote></b>\n\n"
                "<b>It seems this movie isn't in my database yet. This could be due to an incorrect name, or the movie hasn't been released or added by the admin.</b>\n\n"
                "🔎 <i>You can use Google to check the correct movie name and try searching again:</i>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔍 Google", url=google)]
                ])
            )
            await asyncio.sleep(Config.AUTO_DELETE)
            await q.delete()
            return

        # Promo button logic
        promo = await data.get_active_promo()
        if promo:
            promo_buttons = [
                [InlineKeyboardButton(f"[AD] {promo['button_text']}", callback_data=f"promo_{promo['reply_msg_id']}")]
            ]
            try:
                msg = await event.reply_text(
                    answers,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(promo_buttons)
                )
                await asyncio.sleep(Config.AUTO_DELETE)
                await msg.delete()

            except MessageTooLong:
                file_path = f"{event.text.strip()}.txt"
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(answers)

                msg = await event.reply_document(
                    file_path,
                    caption=f"Showing the Search result for **{event.text.strip()}**",
                    reply_markup=InlineKeyboardMarkup(promo_buttons)
                )
                os.remove(file_path)
                await asyncio.sleep(Config.AUTO_DELETE)
                await msg.delete()
        else:
            try:
                msg = await event.reply_text(
                    answers,
                    disable_web_page_preview=True
                )
                await asyncio.sleep(Config.AUTO_DELETE)
                await msg.delete()
            except MessageTooLong:
                file_path = f"{event.text.strip()}.txt"
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(answers)
                msg = await event.reply_document(
                    file_path,
                    caption=f"Showing the Search result for **{event.text.strip()}**"
                )
                os.remove(file_path)
                await asyncio.sleep(Config.AUTO_DELETE)
                await msg.delete()

    except Exception as e:
        await client.send_message(
            Config.REQUEST_CHNL,
            text=f"**[{Config.BOT_SESSION_NAME}] - Error in search - {str(e)}**"
        )
        g = await event.reply_text("**❌ No Results Found**", disable_web_page_preview=True)
        await asyncio.sleep(30)
        await g.delete()

# Promo callback handler
@Client.on_callback_query(filters.regex(r"^promo_"))
async def promo_callback_handler(client, callback_query):
    try:
        promo = await data.get_active_promo()
        if not promo:
            await callback_query.answer("Promo expired.", show_alert=True)
            return
        if f"promo_{promo['reply_msg_id']}" != callback_query.data:
            await callback_query.answer("Promo expired.", show_alert=True)
            return
        await callback_query.answer()
        user_id = callback_query.from_user.id
        try:
            dm_msg = await client.send_message(
                chat_id=user_id,
                text=f"{promo['promo_text']}\n\n<b>This msg will be deleted in 5 min.</b>",
                parse_mode="html"
            )
            await client.send_message(
                chat_id=user_id,
                text="This msg will be delete in 5 min."
            )
            await asyncio.sleep(300)
            await dm_msg.delete()
        except Exception as e:
            await callback_query.answer("Unable to send promo in DM. Please start the bot in private.", show_alert=True)
    except Exception as e:
        await callback_query.answer("Error showing promo.", show_alert=True)
