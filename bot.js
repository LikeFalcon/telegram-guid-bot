const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();

const bot = new TelegramBot(process.env.BOT_TOKEN, {polling: true});
const adminId = parseInt(process.env.ADMIN_ID);

const guides = new Map();
let userLastGuide = new Map();

bot.onText(/\/start/, async (msg) => {
    const keyboard = {
        reply_markup: {
            keyboard: [['📚 Посмотреть гайды']],
            resize_keyboard: true
        }
    };
    await bot.sendMessage(msg.chat.id, 'Привет! Я бот с гайдами. Выбери действие:', keyboard);
});

bot.onText(/\/add_guide (.+) (.+)/, async (msg, match) => {
    if (msg.from.id !== adminId) {
        await bot.sendMessage(msg.chat.id, 'У вас нет прав для добавления гайдов');
        return;
    }

    const guideName = match[1];
    const guideContent = match[2];
    guides.set(guideName, guideContent);
    await bot.sendMessage(msg.chat.id, `Гайд "${guideName}" успешно добавлен!`);
});

bot.on('message', async (msg) => {
    if (msg.text !== '📚 Посмотреть гайды') return;

    const chatId = msg.chat.id;
    const userId = msg.from.id;

    const now = Date.now();
    const lastGuideTime = userLastGuide.get(userId);
    
    if (lastGuideTime && now - lastGuideTime < 24 * 60 * 60 * 1000) {
        const timeLeft = 24 * 60 * 60 * 1000 - (now - lastGuideTime);
        const hoursLeft = Math.floor(timeLeft / (60 * 60 * 1000));
        const minutesLeft = Math.floor((timeLeft % (60 * 60 * 1000)) / (60 * 1000));
        await bot.sendMessage(chatId, `Вы уже получили гайд сегодня. Следующий гайд будет доступен через ${hoursLeft} часов ${minutesLeft} минут`);
        return;
    }

    if (guides.size === 0) {
        await bot.sendMessage(chatId, 'Пока нет доступных гайдов');
        return;
    }

    const keyboard = {
        reply_markup: {
            inline_keyboard: Array.from(guides.keys()).map(name => [{
                text: name,
                callback_data: name.substring(0, 64)
            }])
        }
    };

    await bot.sendMessage(chatId, 'Выберите гайд:', keyboard);
});

bot.on('callback_query', async (query) => {
    const chatId = query.message.chat.id;
    const userId = query.from.id;
    const guideName = query.data;

    if (guides.has(guideName)) {
        userLastGuide.set(userId, Date.now());
        await bot.sendMessage(chatId, guides.get(guideName));
    }
    
    await bot.answerCallbackQuery(query.id);
});

console.log('Бот запущен...');
