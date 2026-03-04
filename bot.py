import os
import asyncio
from telegram import (
    Update,
    ChatPermissions,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 6919025708
CHANNEL_USERNAME = "@myfirstchannel12"
CHANNEL_LINK = "https://t.me/myfirstchannel12"

warnings = {}

# ================= FORCE JOIN =================
async def is_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    joined = await is_joined(user_id, context)
    if not joined:
        button = [[InlineKeyboardButton("🔔 Join Channel", url=CHANNEL_LINK)]]
        await update.message.reply_text(
            "🚫 Please join our official channel first!",
            reply_markup=InlineKeyboardMarkup(button),
        )
        return

    await update.message.reply_text("🤖 Group Helper Bot is Active!")

# ================= WELCOME =================
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:

        photo_url = "https://i.ibb.co/mV1pwfGz/images.jpg"

        caption = f"""
🎉 <b>Welcome {member.mention_html()}!</b>

📌 <b>Group:</b> {update.effective_chat.title}

✨ Please follow rules:
1️⃣ No spam
2️⃣ No links
3️⃣ Respect everyone

👑 Owner: ꧁👑ḊÄṚḲ_ṖṚЇṄĊЁ👑꧂
"""

        buttons = [
            [InlineKeyboardButton("🌐 Developer Community BD", url="https://t.me/Developer_CommunityBD")],
            [InlineKeyboardButton("💬 Dev Community Chat", url="https://t.me/+QVSsvVBnzPgxNDBl")],
            [InlineKeyboardButton("👑 Owner Profile", url="https://t.me/dark_princes12")],
        ]

        sent = await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

        await asyncio.sleep(30)

        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=sent.message_id,
            )
        except:
            pass

# ================= RULES =================
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 Group Rules:\n1️⃣ No spam\n2️⃣ No links\n3️⃣ Respect everyone"
    )

# ================= WARN SYSTEM =================
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user
    user_id = user.id

    warnings[user_id] = warnings.get(user_id, 0) + 1

    if warnings[user_id] >= 3:
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False),
        )
        await update.message.reply_text(f"🔇 {user.first_name} muted (3 warnings).")
        warnings[user_id] = 0
    else:
        await update.message.reply_text(
            f"⚠ {user.first_name} warned ({warnings[user_id]}/3)"
        )

# ================= MUTE =================
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions=ChatPermissions(can_send_messages=False),
    )
    await update.message.reply_text("🔇 User muted.")

# ================= UNMUTE =================
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions=ChatPermissions(can_send_messages=True),
    )
    await update.message.reply_text("🔊 User unmuted.")

# ================= ADMIN CALL =================
async def admin_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user

    if message.text and "@admin" in message.text.lower():
        report = (
            f"🚨 Admin Call!\n\n"
            f"👤 {user.first_name}\n"
            f"🆔 {user.id}\n"
            f"💬 {message.text}\n"
            f"📍 {update.effective_chat.title}"
        )

        await context.bot.send_message(chat_id=OWNER_ID, text=report)
        await message.reply_text("📩 Admin notified.")

# ================= ANTI LINK =================
async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user
    chat_id = update.effective_chat.id

    member = await context.bot.get_chat_member(chat_id, user.id)

    if member.status in ["administrator", "creator"]:
        return

    if message.text and "http" in message.text:
        await message.delete()

# ================= RUN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_call))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_link))

app.run_polling()
