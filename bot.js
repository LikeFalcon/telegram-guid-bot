const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();

const PORT = process.env.PORT || 8080;
const bot = new TelegramBot(process.env.BOT_TOKEN, {
    polling: true
});

const adminId = parseInt(process.env.ADMIN_ID);

const guides = new Map();
let userLastGuide = new Map();

bot.onText(/\/start/, async (msg) => {
    try {
        const keyboard = {
            reply_markup: {
                keyboard: [['📚 Посмотреть гайды']],
                resize_keyboard: true
            }
        };
        await bot.sendMessage(msg.chat.id, 'Привет! Я бот с гайдами. Выбери действие:', keyboard);
    } catch (error) {
        console.error('Ошибка в команде start:', error);
    }
});

bot.onText(/\/add_guide (.+) (.+)/, async (msg, match) => {
    try {
        if (msg.from.id !== adminId) {
            await bot.sendMessage(msg.chat.id, 'У вас нет прав для добавления гайдов');
            return;
        }

        const guideName = match[1];
        const guideContent = match[2];
        guides.set(guideName, guideContent);
        await bot.sendMessage(msg.chat.id, `Гайд "${guideName}" успешно добавлен!`);
    } catch (error) {
        console.error('Ошибка в команде add_guide:', error);
    }
});

bot.on('message', async (msg) => {
    try {
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

        const inlineKeyboard = Array.from(guides.keys()).map(name => [{
            text: name,
            callback_data: name.substring(0, 32) // Ограничиваем длину callback_data
        }]);

        const keyboard = {
            reply_markup: {
                inline_keyboard: inlineKeyboard
            }
        };

        await bot.sendMessage(chatId, 'Выберите гайд:', keyboard);
    } catch (error) {
        console.error('Ошибка при показе гайдов:', error);
    }
});

bot.on('callback_query', async (query) => {
    try {
        const chatId = query.message.chat.id;
        const userId = query.from.id;
        const guideName = query.data;

        if (guides.has(guideName)) {
            userLastGuide.set(userId, Date.now());
            await bot.sendMessage(chatId, guides.get(guideName));
        }
        
        await bot.answerCallbackQuery(query.id);
    } catch (error) {
        console.error('Ошибка при выборе гайда:', error);
    }
});

// Обработка ошибок
bot.on('polling_error', (error) => {
    console.error('Ошибка polling:', error);
});

// Запуск сервера Express для поддержания работы бота
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Бот работает!');
});

app.listen(PORT, () => {
    console.log(`Сервер запущен на порту ${PORT}`);
    console.log('Бот запущен...');
});
Также нужно обновить package.json. Замените его содержимое на:
JSON

{
  "name": "telegram-guide-bot",
  "version": "1.0.0",
  "description": "Telegram Bot for Guides",
  "main": "bot.js",
  "dependencies": {
    "node-telegram-bot-api": "^0.61.0",
    "dotenv": "^16.0.3",
    "express": "^4.18.2"
  },
  "scripts": {
    "start": "node bot.js"
  },
  "engines": {
    "node": "16.x"
  }
}
