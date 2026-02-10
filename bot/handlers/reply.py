from sqlalchemy import select

from telegram.ext import ContextTypes,ConversationHandler
from telegram import Update
from telegram import (
    KeyboardButton,ReplyKeyboardMarkup,
    InlineKeyboardButton, InlineKeyboardMarkup
)

from database.session import SessionLocal
from repositories.user_repo import UserRepository
from models import Product,Cart,CartItem,User,Status,Order,OrderItem



async def start_handler(update:Update,context:ContextTypes):
    
    session = SessionLocal()
    repo = UserRepository(session)
    
    telegram_id = update.effective_user.id
    full_name = update.effective_user.full_name
    
    repo.get_or_create_user(telegram_id,full_name)
    
    
    keyboard = [
        [
            KeyboardButton("🛍 Mahsulotlar"),
            KeyboardButton("🛒 Savat")
        ],
        [KeyboardButton("📦 Buyurtmalarim")],
        [KeyboardButton("📞 Bog‘lanish")]
    ]
    
    reply_kb = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    
    
    await update.message.reply_text("""Assalomu alaykum! 🛍

Bizning online do‘konga xush kelibsiz. Bu yerda siz turli mahsulotlarni ko‘rishingiz, narxlarni solishtirishingiz va oson buyurtma berishingiz mumkin.

Quyidagi menyudan kerakli bo‘limni tanlang 👇
""",reply_markup = reply_kb),
    
    session.close()
    
    
async def helping(update,context):
    
    await update.message.reply_text("""ℹ️ Yordam

Bu bot orqali siz:
🛍 Mahsulotlarni ko‘rishingiz
🛒 Savatga qo‘shishingiz
📦 Buyurtma berishingiz mumkin

Asosiy bo‘limlar:
• 🛍 Mahsulotlar — katalogni ko‘rish
• 🛒 Savat — tanlangan mahsulotlar
• 📦 Buyurtmalarim — buyurtma holati

Savollar bo‘lsa, 📞 Bog‘lanish bo‘limidan foydalaning.
""")
    
    
async def products_handler(update,context):
    
    keyboard = [
        [
            KeyboardButton('👕 Kiyimlar'),
            KeyboardButton('👟 Oyoq kiyim')
        ],
        [
            KeyboardButton('📱 Elektronika'),
            KeyboardButton('🎒 Aksessuarlar')
        ],
        [
            KeyboardButton('🏘 Bosh meniu')
        ]
    ]
    
    reply_kb = ReplyKeyboardMarkup(
        keyboard,resize_keyboard=True
    )
    
    await update.message.reply_text("""🛍 Mahsulotlar katalogi

Kerakli kategoriyani tanlang 👇
""",reply_markup=reply_kb)
    

async def show_menu_handler(update: Update, context:ContextTypes.DEFAULT_TYPE):
    
    keyboard = [
        [
            KeyboardButton("🛍 Mahsulotlar"),
            KeyboardButton("🛒 Savat")
        ],
        [KeyboardButton("📦 Buyurtmalarim")],
        [KeyboardButton("📞 Bog‘lanish")]
    ]
    
    reply_kb = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    
    await update.message.reply_text("🏘 Siz Bosh Menyudasz \n Quyidagi menyudan kerakli bo‘limni tanlang 👇",reply_markup=reply_kb)
    
    
async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[1])
    telegram_id = update.effective_user.id

    with SessionLocal() as session:

        user = session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()

        cart = session.query(Cart).filter(
            Cart.user_id == user.id
        ).first()

        if not cart:
            cart = Cart(user_id=user.id)
            session.add(cart)
            session.commit()
            session.refresh(cart)

        cart_item = session.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        ).first()

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=1
            )
            session.add(cart_item)

        session.commit()

    await query.message.reply_text("🛒 Mahsulot savatchaga qo‘shildi")


async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id

    with SessionLocal() as session:

        user = session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()

        if not user:
            await update.message.reply_text("Savatcha bo‘sh")
            return

        cart = session.query(Cart).filter(
            Cart.user_id == user.id
        ).first()

        if not cart:
            await update.message.reply_text("Savatcha bo‘sh")
            return

        items = session.query(CartItem).filter(
            CartItem.cart_id == cart.id
        ).all()

        if not items:
            await update.message.reply_text("Savatcha bo‘sh")
            return

        text = "🛒 <b>Savatchangiz:</b>\n\n"
        total = 0

        for item in items:

            product = session.get(Product, item.product_id)

            subtotal = product.price * item.quantity
            total += subtotal

            text += f"""
🛍 {product.name}
💰 {product.price:,} so'm
📦 {item.quantity} dona
--------------------
"""

        text += f"\n<b>Jami:</b> {total:,} so'm"

        keyboard = [
            [InlineKeyboardButton("💳 Buyurtma berish", callback_data="checkout")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
 

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

        # 🔚 session.begin() chiqishi → avtomatik commit

    await update.message.reply_text("✅ Buyurtma qabul qilindi!")
    return ConversationHandler.END
