from telegram.ext import ContextTypes

from telegram import (
    Update,InlineKeyboardButton,InlineKeyboardMarkup,
    KeyboardButton,ReplyKeyboardMarkup
)

from database.session import SessionLocal
from models import Product


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
    

async def product_inlene_handler(update:Update,context: ContextTypes):
    
    text = update.message.text
    
    with SessionLocal() as session:
        

        if text == "👕 Kiyimlar":
            category_id = 1
        elif text == "👟 Oyoq kiyim":
            category_id = 2
        elif text == "📱 Elektronika":
            category_id = 3
        elif text == "🎒 Aksessuarlar":
            category_id = 4
        else:
            return
        
        products = session.query(Product).filter(Product.category_id == category_id).all()
        
        if not products:
            await update.message.reply_text("Mahsulot topilmadi")
            return
        
        keyboard = [
            [InlineKeyboardButton(text=product.name,callback_data=f"product_{product.id}")]
            for product in products
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
            
        await update.message.reply_text(
            "Kerakli Tovarni  tanlang 👇:",
            reply_markup=reply_markup
        )
        
        
async def product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[1])

    with SessionLocal() as session:
        product = session.get(Product, product_id)

        caption = f"""
    🛍 <b>{product.name}</b>

    💰 <b>{product.price:,} so'm</b>

    📄 {product.description}

    🚚 24 soatda yetkazib beriladi
    """

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Savatchaga qo‘shish",
                    callback_data=f"addcart_{product.id}"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_photo(
            photo=product.image_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

