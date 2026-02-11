
from telegram.ext import ContextTypes
from telegram import Update
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup
)

from database.session import SessionLocal
from models import Product,Cart,CartItem,User



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
 