from telegram.ext import Application,CommandHandler,MessageHandler,filters,CallbackQueryHandler

from config import TOKEN
from bot.handlers.reply import (
    start_handler,helping,products_handler,
    show_menu_handler
)

from bot.handlers.inline import clothes_handler,product_detail

    

def run():
    
    app = Application.builder().token(TOKEN).build()
    
    # Command handler
    app.add_handler(CommandHandler('start',start_handler))
    app.add_handler(CommandHandler('help',helping))
    
    # Message Handler
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("🛍 Mahsulotlar"),products_handler
    ))
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("👕 Kiyimlar"),clothes_handler
    ))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("👟 Oyoq kiyim"),clothes_handler
    ))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("📱 Elektronika"),clothes_handler
    ))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("🎒 Aksessuarlar"),clothes_handler
    ))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("🏘 Bosh meniu"),show_menu_handler
    ))
    
    # Callback query Handler
    
    app.add_handler(
    CallbackQueryHandler(product_detail, pattern="^product_")
)

    
    
    app.run_polling()
    
