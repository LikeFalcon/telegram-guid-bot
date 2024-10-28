> God's shooter [пишу контент]:
Вот подробная инструкция с вашим токеном для создания и запуска бота.

Шаг 1: Подготовка проекта

 1. Создайте новый проект на Replit или локально на своем компьютере.
 2. Создайте файл main.py. Это будет основной файл, в котором будет содержаться код бота.
 3. Создайте файл requirements.txt для указания зависимостей.

Шаг 2: Настройка requirements.txt

Добавьте в requirements.txt следующие зависимости:

python-telegram-bot==20.0

Шаг 3: Код для main.py

Вставьте следующий код в main.py. В нем уже добавлен ваш токен бота.

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta
import os

# Токен бота
BOT_TOKEN = "7155864496:AAEyQTktFlNXiio7OeobSgAkL7mVJoiopro"

# ID администратора (замените на ваш ID, если потребуется)
ADMIN_ID = 123456789  # Замените на ваш ID

# Словарь для хранения гайдов
guides = {}
# Словарь для хранения времени последнего получения гайда пользователем
user_last_guide = {}

# Приветственное сообщение
WELCOME_MESSAGE = "👋 Приветствую, бро! Это твоя зона прокачки 💪. Готов стать сильнее, умнее и увереннее? Жми на кнопки ниже и выбирай гайд! 📚🔥"

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

> God's shooter [пишу контент]:
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

Объяснение функций и команд

 1. Приветственное сообщение: Бот приветствует пользователя молодежным сленгом.
 2. Команда /add_guide: Администратор может добавить новый гайд с помощью команды /add_guide <название> <текст_гайда>.
 3. Команда /start: Приветствует пользователя и показывает кнопку для просмотра гайдов.
 4. Команда /random_tip: Отправляет случайный мотивационный совет.
 5. Кнопка “📚 Посмотреть гайды”: Показывает список доступных гайдов, но только если с момента последнего просмотра прошло 24 часа.

Шаг 4: Запуск бота

 1. Установите зависимости:
Если вы работаете на Replit, запустите проект, и зависимости установятся автоматически. Если локально, выполните команду:

pip install -r requirements.txt


 2. Запустите бота:
На Replit просто нажмите Run, локально выполните:

python3 main.py


 3. Проверка:
Откройте Telegram и отправьте команду /start вашему боту.

