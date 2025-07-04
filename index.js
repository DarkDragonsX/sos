const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');

const TOKEN = '7762777684:AAFngHPgagA7-IurRcOWf1ZjiW7OlpnSxfM';
const bot = new TelegramBot(TOKEN, { polling: true });

const MAIN_ADMIN = 'darkdragonsx';
let moderators = [];

// /start
bot.onText(/\/start/, (msg) => {
  const user = msg.from.username || 'مستخدم';
  bot.sendMessage(msg.chat.id, `👋 مرحباً @${user}! هذا بوت سيده ${MAIN_ADMIN} 👑`);
});

// تحميل جميع ملفات الأوامر من مجلد commands
const commandsDir = path.join(__dirname, 'commands');
fs.readdirSync(commandsDir).forEach(file => {
  if (file.endsWith('.js')) {
    require(path.join(commandsDir, file))(bot, MAIN_ADMIN, moderators);
  }
});
