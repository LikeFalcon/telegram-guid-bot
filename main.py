
like devil
23:43 (0 минут назад)
кому: мне

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta
import os

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Словарь для хранения гайдов
guides = {}
# Словарь для хранения времени последнего получения гайда пользователем
user_last_guide = {}

# Приветственное сообщение
WELCOME_MESSAGE = "👋 Yo, бро! Добро пожаловать! Это твоя зона прокачки 💪. Готов стать сильнее, умнее и увереннее? Жми на кнопки ниже и выбирай гайд! 📚🔥"

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📚 Посмотреть гайды", callback_data="view_guides")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

# Функция для добавления гайда (только для администратора)
async def add_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ У тебя нет прав для добавления гайдов, бро.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Используй команду так: /add_guide <название> <текст_гайда>")
        return

    guide_name = context.args[0]
    guide_content = " ".join(context.args[1:])
    guides[guide_name] = guide_content
    await update.message.reply_text(f'✅ Гайд "{guide_name}" успешно добавлен!')

# Функция для показа доступных гайдов
async def view_guides(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Проверяем, прошло ли 24 часа с момента последнего получения гайда
    last_guide_time = user_last_guide.get(user_id)
    if last_guide_time and datetime.now() - last_guide_time < timedelta(days=1):
        time_left = timedelta(days=1) - (datetime.now() - last_guide_time)
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes = remainder // 60
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⏳ Ты уже получал гайд сегодня. Возвращайся через {hours} ч и {minutes} мин, чтобы получить новый!"
        )
        return

    # Проверяем, есть ли гайды
    if not guides:
        await context.bot.send_message(chat_id=chat_id, text="😕 Пока нет доступных гайдов.")
        return

    # Создаем клавиатуру с гайдами
    keyboard = [[InlineKeyboardButton(f"📖 {name}", callback_data=name)] for name in guides.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="👉 Выбирай гайд, который тебя интересует:", reply_markup=reply_markup)

# Обработчик выбора гайда
async def guide_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    guide_name = query.data
    user_id = query.from_user.id

    # Отправляем текст выбранного гайда и обновляем время последнего получения гайда
    if guide_name in guides:
        user_last_guide[user_id] = datetime.now()
        await query.message.reply_text(f"📝 {guides[guide_name]}")
    await query.answer()

# Функция для случайного совета
async def random_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tips = [
        "💡 Подумай на 10 шагов вперед, но живи в моменте.",
        "🔥 Никогда не сдавайся, даже если все идет против тебя.",
        "💪 Верь в свои силы. Твоя главная битва — внутри.",
        "📚 Учись, ведь знание — это сила.",
        "⚔️ Рискуй и развивайся — в комфорте нет побед."
    ]
    from random import choice
    await update.message.reply_text(choice(tips))

def main():
    # Инициализация приложения с токеном бота
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_guide", add_guide))
    application.add_handler(CommandHandler("random_tip", random_tip))
    
    # Обработчик сообщений с текстом "📚 Посмотреть гайды"
    application.add_handler(MessageHandler(filters.Text("📚 Посмотреть гайды"), view_guides))
    
    # Обработчик нажатий на кнопки
    application.add_handler(CallbackQueryHandler(guide_selection))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
