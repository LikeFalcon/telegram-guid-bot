const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();

const token = process.env.BOT_TOKEN;
const adminId = parseInt(process.env.ADMIN_ID);

const bot = new TelegramBot(token, {polling: true});

let guides = {};
let userLastGuide = {};

bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  const opts = {
    reply_markup: {
      keyboard: [
        ['📚 Посмотреть гайды']
      ],
      resize_keyboard: true
    }
  };
  bot.sendMessage(chatId, 'Привет! Я бот с гайдами. Выбери действие:', opts);
});

bot.onText(/\/add_guide (.+) (.+)/, (msg, match) => {
  const chatId = msg.chat.id;
  
  if (msg.from.id !== adminId) {
    bot.sendMessage(chatId, 'У вас нет прав для добавления гайдов');
    return;
  }

  const guideName = match[1];
  const guideContent = match[2];
  guides[guideName] = guideContent;
  
  bot.sendMessage(chatId, `Гайд "${guideName}" успешно добавлен!`);
});

bot.on('message', (msg) => {
  if (msg.text !== '📚 Посмотреть гайды') return;
  
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  
  const now = Date.now();
  if (userLastGuide[userId] && now - userLastGuide[userId] < 24 * 60 * 60 * 1000) {
    const timeLeft = 24 * 60 * 60 * 1000 - (now - userLastGuide[userId]);
    const hoursLeft = Math.floor(timeLeft / (60 * 60 * 1000));
    const minutesLeft = Math.floor((timeLeft % (60 * 60 * 1000)) / (60 * 1000));
    bot.sendMessage(chatId, `Вы уже получили гайд сегодня. Следующий гайд будет доступен через ${hoursLeft} часов ${minutesLeft} минут`);
    return;
  }

  if (Object.keys(guides).length === 0) {
    bot.sendMessage(chatId, 'Пока нет доступных гайдов');
    return;
  }

  const opts = {
    reply_markup: {
      inline_keyboard: Object.keys(guides).map(name => [{
        text: name,
        callback_data: name
      }])
    }
  };
  
  bot.sendMessage(chatId, 'Выберите гайд:', opts);
});

bot.on('callback_query', (query) => {
  const chatId = query.message.chat.id;
  const userId = query.from.id;
  const guideName = query.data;

  if (guides[guideName]) {
    userLastGuide[userId] = Date.now();
    bot.sendMessage(chatId, guides[guideName]);
  }
  
  bot.answerCallbackQuery(query.id);
});

console.log('Бот запущен...');
