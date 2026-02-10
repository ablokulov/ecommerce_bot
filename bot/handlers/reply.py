
from telegram import KeyboardButton,ReplyKeyboardMarkup

async def start(update,context):
    
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
            KeyboardButton('⌚ Aksessuarlar')
        ]
    ]
    
    reply_kb = ReplyKeyboardMarkup(
        keyboard,resize_keyboard=True
    )
    
    await update.message.reply_text("""🛍 Mahsulotlar katalogi

Kerakli kategoriyani tanlang 👇
""",reply_markup=reply_kb)