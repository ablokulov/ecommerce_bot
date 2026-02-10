from telegram.ext import Application,CommandHandler,MessageHandler,filters,CallbackQueryHandler,ConversationHandler

from config import TOKEN
from bot.handlers.reply import (
    start_handler,helping,products_handler,
    show_menu_handler,add_to_cart,show_cart,
    get_address
)

from bot.handlers.inline import clothes_handler,product_detail
from bot.handlers.order import show_orders,order_detail
from bot.states import checkout_start
from bot.states.checkout_state import PHONE,ADDRESS,get_phone

    
    
checkout_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(checkout_start, pattern="^checkout$")],
    states={
        PHONE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
    },
    fallbacks=[],
)



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
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("🛒 Savat"),show_cart
    ))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("📦 Buyurtmalarim"),show_orders
    ))
     
    # Callback query Handler
    
    app.add_handler(
    CallbackQueryHandler(product_detail, pattern="^product_")
)

    app.add_handler(
    CallbackQueryHandler(add_to_cart, pattern="^addcart_")
)

    app.add_handler(
    CallbackQueryHandler(order_detail, pattern="^order_")
)
    app.add_handler(checkout_conv)
    

    app.run_polling()