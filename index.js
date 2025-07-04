const TelegramBot = require('node-telegram-bot-api');
const express = require('express');
const app = express();

const TOKEN = '7762777684:AAFngHPgagA7-IurRcOWf1ZjiW7OlpnSxfM';
const bot = new TelegramBot(TOKEN, { polling: false });

app.use(express.json());

app.post(`/bot${TOKEN}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

app.get('/', (req, res) => {
  res.send('✅ البوت يعمل الآن على Render');
});

// أوامر البوت
bot.onText(/\/start/, (msg) => {
  const name = msg.from.username || msg.from.first_name;
  bot.sendMessage(msg.chat.id, `👋 أهلاً بك @${name}, أنا بوت سيدك 👑 darkdragonsx`);
});

// استماع لأي رسالة
bot.on('message', (msg) => {
  if (!msg.text.startsWith('/')) {
    bot.sendMessage(msg.chat.id, 'أرسل /start أو /مساعد لرؤية الأوامر 🔧');
  }
});

// تشغيل السيرفر
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Bot server running on port ${PORT}`);

  // إعداد Webhook تلقائياً
  const url = `https://${process.env.RENDER_EXTERNAL_HOSTNAME}/bot${TOKEN}`;
  bot.setWebHook(url).then(() => {
    console.log(`✅ Webhook set to: ${url}`);
  }).catch((err) => {
    console.error('❌ خطأ في Webhook:', err.message);
  });
});
