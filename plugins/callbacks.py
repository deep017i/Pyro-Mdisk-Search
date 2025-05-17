from pyrogram import Client
from pyrogram.types import *
from configs import Config
import asyncio

@Client.on_callback_query()
async def button(client, cmd: CallbackQuery):
    data = cmd.data
    if data == "about":
        await cmd.message.edit(
            text=Config.ABOUT_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Back •", callback_data="back")
                ]
            ])
        )

    elif data == "help":
        await cmd.message.edit(
            text=Config.ABOUT_HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Back •", callback_data="back")
                ]
            ])
        )
        
    elif data == "back":
        await cmd.message.edit(
            text=Config.HOME_TEXT.format(cmd.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Updates Channel •", url="https://telegram.me/DypixxTech")],
            [InlineKeyboardButton("• Help •", callback_data="help"),
             InlineKeyboardButton("• About •", callback_data="about")],
            [InlineKeyboardButton("• Developer •", user_id=int(Config.BOT_OWNER))]]))
        
    elif data == "send_tutorial":
        i = await client.copy_message(
            chat_id=data.message.chat.id,
            from_chat_id=-1002147456374,
            message_id=104,
            caption="<b>✅ Wᴀᴛᴄʜ ᴛʜɪs ᴛᴜᴛᴏʀɪᴀʟ ᴠɪᴅᴇᴏ ᴛᴏ ᴠᴇʀɪғʏ ʏᴏᴜʀsᴇʟғ...\n\n<blockquote>Yᴏᴜ ᴄᴀɴ ᴀʟsᴏ ʙᴜʏ ᴀ ᴏɴᴇ ᴍᴏɴᴛʜ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀsʜɪᴘ ᴀᴛ ᴛʜᴇ ᴄʜᴇᴀᴘᴇsᴛ ᴘʀɪᴄᴇ ᴛᴏ sᴋɪᴘ ᴛʜᴇ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss.</blockquote></b>")
        await asyncio.sleep(360)
        await i.delete()

    elif data == "delete_msg":
        await cmd.answer("🚨 This message will delete itself in 5 minutes\n\nBetter check it before it’s gone! 👀\n\nJoin : @DypixxTech", show_alert=True)