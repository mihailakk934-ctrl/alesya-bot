import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import datetime
import random
import asyncio

# 🔧 НАСТРОЙКИ
BOT_TOKEN = "8453101752:AAHrrySbI3EkDtv0YK-ICwo-4iOnteBip_k"
ALESYA_CHAT_ID = "1683043954"
YOUR_CHAT_ID = "907066358"
START_DATE = datetime.datetime(2025, 1, 10)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Импортируем функции из messages.py
from messages import get_daily_message, get_surprise_message, get_compliment, get_secret_message, get_special_message, get_morning_message, get_evening_message

# Создаем клавиатуру с кнопками
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("💕 Почему я тебя люблю"), KeyboardButton("📅 Сколько дней вместе")],
        [KeyboardButton("🌟 Получить комплимент"), KeyboardButton("🔐 Тайное послание")],
        [KeyboardButton("📖 Послание дня"), KeyboardButton("🎁 Случайный сюрприз")],
        [KeyboardButton("ℹ️ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="Выбери действие...")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = f"""
💖 Привет, Алеся!

Этот бот создан специально для тебя! 
У него есть много уникальных посланий на каждый день! 📅

🎯 Доступные команды (можно выбрать кнопкой ниже):
• 💕 Почему я тебя люблю
• 📅 Сколько дней вместе  
• 🌟 Получить комплимент
• 🔐 Тайное послание
• 📖 Послание дня
• 🎁 Случайный сюрприз
• ℹ️ Помощь

⏰ Автоматически каждый день:
• Каждый день в 12:00 - уникальное послание дня!
• 3 раза в день - случайные сюрпризы! 🎁

Ты заслуживаешь всего самого прекрасного! 💝
    """
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📋 Помощь по командам:

💕 Почему я тебя люблю - случайная причина любви
📅 Сколько дней вместе - статистика наших отношений  
🌟 Получить комплимент - милый комплимент для тебя
🔐 Тайное послание - секретное сообщение
📖 Послание дня - уникальное послание на сегодня
🎁 Случайный сюрприз - неожиданный сюрприз
ℹ️ Помощь - это сообщение

Просто нажимай на кнопки ниже! 💖
    """
    await update.message.reply_text(help_text, reply_markup=get_main_keyboard())

async def love_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reasons = [
        "💕 За твою невероятную улыбку",
        "🌟 За твою доброту и отзывчивость", 
        "😊 За то, как ты поддерживаешь меня",
        "🎯 За твою целеустремленность",
        "🤣 За твое прекрасное чувство юмора",
        "💝 Просто за то, что ты - это ты!"
    ]
    reason = random.choice(reasons)
    message = f"Я тебя люблю, Алеся...\n\n{reason}"
    await update.message.reply_text(message, reply_markup=get_main_keyboard())

async def days_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.datetime.now()
    days_together = (today - START_DATE).days
    message = f"""
👩‍❤️‍💋‍👨 Алеся, мы вместе уже {days_together} дней!

Это:
• {days_together * 24} часов
• {days_together * 24 * 60} минут  
• {days_together * 24 * 60 * 60} секунд

И с каждой секундой я люблю тебя все сильнее! 💖
    """
    await update.message.reply_text(message, reply_markup=get_main_keyboard())

async def compliment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    compliment = get_compliment(day_of_year)
    await update.message.reply_text(compliment, reply_markup=get_main_keyboard())

async def secret_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    secret = get_secret_message(day_of_year)
    await update.message.reply_text(secret, reply_markup=get_main_keyboard())

async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    message = get_daily_message(day_of_year)
    await update.message.reply_text(f"📖 Послание дня ({day_of_year}/365):\n\n{message}", reply_markup=get_main_keyboard())

async def surprise_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    surprise = get_surprise_message(day_of_year)
    await update.message.reply_text(f"🎁 Сюрприз дня ({day_of_year}/365):\n\n{surprise}", reply_markup=get_main_keyboard())

# Обработчик текстовых сообщений (кнопок)
async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "💕 Почему я тебя люблю":
        await love_command(update, context)
    elif text == "📅 Сколько дней вместе":
        await days_command(update, context)
    elif text == "🌟 Получить комплимент":
        await compliment_command(update, context)
    elif text == "🔐 Тайное послание":
        await secret_command(update, context)
    elif text == "📖 Послание дня":
        await today_command(update, context)
    elif text == "🎁 Случайный сюрприз":
        await surprise_command(update, context)
    elif text == "ℹ️ Помощь":
        await help_command(update, context)
    else:
        await update.message.reply_text("Используй кнопки ниже для навигации 💖", reply_markup=get_main_keyboard())

# Функции для автоматической отправки ОБОИМ
async def send_to_both(context: ContextTypes.DEFAULT_TYPE, message: str, message_type: str):
    """Отправляет сообщение и Алесе, и тебе"""
    try:
        # Отправляем Алесе
        await context.bot.send_message(chat_id=ALESYA_CHAT_ID, text=message, reply_markup=get_main_keyboard())
        
        # Отправляем тебе (только если указан твой ID)
        if YOUR_CHAT_ID != "907066358":
            your_message = f"📨 Отправлено Алесе ({message_type}):\n\n{message}"
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=your_message)
        
        print(f"✅ {message_type} отправлен обоим! День {datetime.datetime.now().timetuple().tm_yday}")
    except Exception as e:
        print(f"❌ Ошибка отправки {message_type}: {e}")

async def send_morning_message(context: ContextTypes.DEFAULT_TYPE):
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    morning_message = get_morning_message(day_of_year)
    message = f"☀️ Доброе утро, Алеся!\n\n{morning_message}"
    await send_to_both(context, message, "Утреннее сообщение")

async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    day_of_year = now.timetuple().tm_yday
    
    # Проверяем особые случаи
    special_message = get_special_message(now)
    if special_message:
        message = special_message
    else:
        message = get_daily_message(day_of_year)
    
    full_message = f"💌 Послание дня ({day_of_year}/365):\n\n{message}"
    await send_to_both(context, full_message, "Ежедневное сообщение")

async def send_evening_message(context: ContextTypes.DEFAULT_TYPE):
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    evening_message = get_evening_message(day_of_year)
    message = f"🌙 Спокойной ночи, Алеся!\n\n{evening_message}"
    await send_to_both(context, message, "Вечернее сообщение")

async def send_random_surprise(context: ContextTypes.DEFAULT_TYPE):
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    surprise = get_surprise_message(day_of_year)
    message = f"🎁 Внезапный сюрприз! ({day_of_year}/365)\n\n{surprise}"
    await send_to_both(context, message, "Случайный сюрприз")

def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("today", today_command))
    application.add_handler(CommandHandler("love", love_command))
    application.add_handler(CommandHandler("days", days_command))
    application.add_handler(CommandHandler("compliment", compliment_command))
    application.add_handler(CommandHandler("secret", secret_command))
    application.add_handler(CommandHandler("surprise", surprise_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Обработчик текстовых сообщений (кнопок)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))
    
    # Настраиваем автоматическую отправку сообщений
    job_queue = application.job_queue
    
    # Ежедневные сообщения
    job_queue.run_daily(send_morning_message, time=datetime.time(hour=7, minute=0))  # 07:00
    job_queue.run_daily(send_daily_message, time=datetime.time(hour=12, minute=0))   # 12:00
    job_queue.run_daily(send_evening_message, time=datetime.time(hour=22, minute=0)) # 22:00
    
    # Случайные сюрпризы 3 раза в день (каждые 8 часов)
    job_queue.run_repeating(send_random_surprise, interval=28800, first=10)  # 28800 секунд = 8 часов
    
    print("=" * 70)
    print("🚀 РОМАНТИЧЕСКИЙ БОТ ДЛЯ АЛЕСИ ЗАПУЩЕН!")
    print("💖 365 уникальных посланий, сюрпризов, комплиментов и тайн!")
    print("🎹 Добавлено кнопочное меню для удобства!")
    print("👥 Автоматические сообщения настроены для ОБОИХ:")
    print("   • 07:00 - Доброе утро")
    print("   • 12:00 - Послание дня") 
    print("   • 22:00 - Спокойной ночи")
    print("   • 3 случайных сюрприза в течение дня")
    print("📍 Проверь бота в Telegram - напиши /start")
    print("=" * 70)
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()