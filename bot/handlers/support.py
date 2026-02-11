from sqlalchemy import select

from telegram.ext import ContextTypes,ConversationHandler,MessageHandler,filters,CallbackQueryHandler,ConversationHandler
from telegram import Update

from database.session import SessionLocal
from models import Product,Cart,CartItem,User,Status,Order,OrderItem

from config import ADMIN

ADMIN_ID = ADMIN
PHONE, ADDRESS = range(2)
CONTACT = 1


async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    address = update.message.text
    phone = context.user_data["phone"]

    with SessionLocal() as session:
        
        with session.begin():
            
            user = session.execute(
                select(User).where(User.telegram_id == telegram_id)
            ).scalar_one_or_none()
            
            if not user:
                await update.message.reply_text("Foydalanuvchi topilmadi.")
                return

            cart = session.execute(
                select(Cart).where(Cart.user_id == user.id)
            ).scalar_one_or_none()
            if not cart:
                await update.message.reply_text("Savatcha bo‘sh.")
                return

           
            items = session.execute(
                select(CartItem).where(CartItem.cart_id == cart.id)
            ).scalars().all()
            if not items:
                await update.message.reply_text("Savatcha bo‘sh.")
                return

    
            total = 0
            products_map = {}  
            for ci in items:
                product = session.get(Product, ci.product_id)
                if not product or not product.is_active:
                    raise ValueError("Mahsulot mavjud emas yoki aktiv emas.")
                if product.stock < ci.quantity:
                    raise ValueError(f"{product.name} uchun stock yetarli emas.")

                products_map[ci.product_id] = product
                total += product.price * ci.quantity

          
            order = Order(
                user_id=user.id,
                total_price=total,
                phone_number=phone,
                delivery_address=address,
                status=Status.PENDING,  
            )
            session.add(order)
            session.flush()  
           
            for ci in items:
                product = products_map[ci.product_id]

                oi = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=ci.quantity,
                    price_snapshot=product.price,  
                )
                session.add(oi)

                product.stock -= ci.quantity

            session.query(CartItem).filter(
                CartItem.cart_id == cart.id
            ).delete(synchronize_session=False)
    
    

            admin_text = f"""
            🆕 YANGI BUYURTMA

            📦 Order ID: #{order.id}

            👤 {user.full_name}
            🆔 {user.telegram_id}

            📞 {phone}
            📍 {address}

            💰 {total:,} so'm
            """

            for ci in items:
                product = products_map[ci.product_id]

                admin_text += f"""
            🛍 {product.name}
            📦 {ci.quantity} dona
            💵 {product.price:,} so'm
            """

            await context.bot.send_message(
                chat_id=ADMIN,
                text=admin_text
            )

            await update.message.reply_text("✅ Buyurtma qabul qilindi!")
            return ConversationHandler.END


    # await update.message.reply_text("✅ Buyurtma qabul qilindi!")
    # return ConversationHandler.END

async def contact_start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(
        "✍ Muammoingizni yozing. Operatorga yuboriladi."
    )
    return CONTACT
    


async def send_to_admin(update, context):

    user = update.effective_user
    message = update.message.text

    # Metadata text
    text = f"""
📩 Yangi murojaat

👤 {user.full_name}
🆔 {user.id}
🔗 @{user.username if user.username else "username yo‘q"}

💬 Xabar:
{message}
"""

    # Admin chatga yuborish
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )

    # Original xabarni forward qilish 
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    await update.message.reply_text(
        "✅ Xabaringiz adminga yuborildi."
    )

    return ConversationHandler.END



async def checkout_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(
        "📱 Telefon raqamingizni kiriting \n Masalan: +998912345678:"
    )
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("📍 Yetkazib berish manzilini kiriting:")
    return ADDRESS


checkout_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(checkout_start, pattern="^checkout$")
    ],
    states={
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
    },
    fallbacks=[],
)
