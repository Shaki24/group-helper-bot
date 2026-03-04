import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

WELCOME_TEXT = """
👋 <b>Welcome to the Group!</b>

📌 Please follow the rules.
🚫 No spam
🚫 No bad links

🔗 <b>Join Our Communities:</b>

Developer Community BD:
https://t.me/Developer_CommunityBD

Dev Community BD Chat:
https://t.me/+QVSsvVBnzPgxNDBl

Owner:
https://t.me/dark_princes12
"""

# Welcome new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        msg = await update.message.reply_text(
            f"👋 Welcome {member.mention_html()}!\n\n{WELCOME_TEXT}",
            parse_mode="HTML"
        )

        await asyncio.sleep(30)
        await msg.delete()


# Admin call system
async def admin_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        if "@admin" in update.message.text.lower():
            await update.message.reply_text(
                "🚨 <b>Admin has been called!</b>\n@KShakilRana2025 please check.",
                parse_mode="HTML"
            )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, admin_call)
    )

    print("Bot is running... 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
