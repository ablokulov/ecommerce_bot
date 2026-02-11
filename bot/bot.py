from telegram.ext import Application,CommandHandler,MessageHandler,filters,CallbackQueryHandler,ConversationHandler

from bot.handlers.start import start_handler,helping,show_menu_handler
from bot.handlers.cart import show_cart,add_to_cart
from bot.handlers.product import product_detail,product_inlene_handler,products_handler
from bot.handlers.order import show_orders,order_detail
from bot.handlers.support import send_to_admin,contact_start,CONTACT,checkout_conv


from config import TOKEN

from telegram.ext import ConversationHandler, MessageHandler, filters




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
        filters.TEXT & filters.Regex("👕 Kiyimlar"),product_inlene_handler
    ))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("👟 Oyoq kiyim"),product_inlene_handler
    ))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("📱 Elektronika"),product_inlene_handler
    ))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("🎒 Aksessuarlar"),product_inlene_handler
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
    contact_conv = ConversationHandler(

        entry_points=[
            MessageHandler(
                filters.TEXT & filters.Regex("^📞 Bog‘lanish$"),
                contact_start
            )
        ],

        states={
            CONTACT: [
                MessageHandler(filters.TEXT , send_to_admin)
            ]
        },

        fallbacks=[]
    )
    


    app.add_handler(contact_conv)
    app.add_handler(checkout_conv)


    

    app.run_polling()
    
    
