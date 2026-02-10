from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal
from models import Order, OrderItem, User, Product
from telegram import InlineKeyboardButton, InlineKeyboardMarkup



async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id

    with SessionLocal() as session:

        user = session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()

        if not user:
            await update.message.reply_text("Buyurtmalar topilmadi")
            return

        orders = session.query(Order).filter(
            Order.user_id == user.id
        ).all()

        if not orders:
            await update.message.reply_text("Buyurtmalar mavjud emas")
            return

        keyboard = []

        for order in orders:
            keyboard.append([
                InlineKeyboardButton(
                    f"📦 Buyurtma #{order.id}",
                    callback_data=f"order_{order.id}"
                )
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "📦 Buyurtmalaringiz:",
            reply_markup=reply_markup
        )



async def order_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    order_id = int(query.data.split("_")[1])

    with SessionLocal() as session:

        order = session.get(Order, order_id)

        items = session.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        text = f"""
📦 Buyurtma #{order.id}

📱 Tel: {order.phone_number}
📍 Manzil: {order.delivery_address}
📌 Status: {order.status.value}

---------------------
"""

        total = 0

        for item in items:

            product = session.get(Product, item.product_id)

            subtotal = item.price_snapshot * item.quantity
            total += subtotal

            text += f"""
🛍 {product.name}
📦 {item.quantity} dona
💰 {subtotal:,} so'm
"""

        text += f"\n<b>Jami:</b> {total:,} so'm"

        await query.message.reply_text(text, parse_mode="HTML")
