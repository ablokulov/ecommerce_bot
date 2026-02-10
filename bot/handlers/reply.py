

from telegram.ext import ContextTypes
from telegram import Update
from telegram import (
    KeyboardButton,ReplyKeyboardMarkup
)

from database.session import SessionLocal
from repositories.user_repo import UserRepository
from models import Product



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