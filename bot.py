import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

WELCOME_TEXT = """
👋 Welcome to the Group!

📌 Please follow the rules.
🚫 No spam
🚫 No bad links

🔗 Join our communities:

Developer Community BD:
https://t.me/Developer_CommunityBD

Dev Community BD Chat:
https://t.me/+QVSsvVBnzPgxNDBl

Owner:
https://t.me/dark_princes12
"""

# Welcome message
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        msg = await update.message.reply_text(
            f"👋 Welcome {member.mention_html()}!\n\n{WELCOME_TEXT}",
            parse_mode="HTML"
        )

        # Auto delete after 30 sec
        await asyncio.sleep(30)
        await msg.delete()

# Admin call system
async def admin_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "@admin" in update.message.text.lower():
        await update.message.reply_text(
            "🚨 Admin has been called!\n@KShakilRana2025 please check."
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
