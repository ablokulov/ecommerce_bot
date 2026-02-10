from telegram.ext import Application,CommandHandler,MessageHandler,filters

from config import TOKEN
from bot.handlers.reply import start,helping,products_handler



    

def run():
    
    app = Application.builder().token(TOKEN).build()
    
    # Command handler
    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('help',helping))
    
    # Message Handler
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("🛍 Mahsulotlar"),products_handler
    ))
    
    
    
    
    
    
    
    app.run_polling()
    