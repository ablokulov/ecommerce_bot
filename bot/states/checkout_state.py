from telegram.ext import ContextTypes
from telegram import Update



PHONE, ADDRESS = range(2)

async def checkout_start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("📱 Telefon raqamingizni kiriting:")
    return PHONE

async def get_phone(update, context):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("📍 Yetkazib berish manzilini kiriting:")
    return ADDRESS
