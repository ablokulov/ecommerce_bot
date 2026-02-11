# from telegram.ext import (
#     ContextTypes,
#     MessageHandler,
#     filters,
#     CallbackQueryHandler,
#     ConversationHandler
# )
# from telegram import Update
# from bot.handlers.support import get_address


# PHONE, ADDRESS = range(2)


# async def checkout_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     q = update.callback_query
#     await q.answer()
#     await q.message.reply_text(
#         "📱 Telefon raqamingizni kiriting \n Masalan: +998912345678:"
#     )
#     return PHONE


# async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["phone"] = update.message.text
#     await update.message.reply_text("📍 Yetkazib berish manzilini kiriting:")
#     return ADDRESS


# checkout_conv = ConversationHandler(
#     entry_points=[
#         CallbackQueryHandler(checkout_start, pattern="^checkout$")
#     ],
#     states={
#         PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
#         ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
#     },
#     fallbacks=[],
# )
