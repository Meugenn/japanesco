import telebot
from const import token
import localize

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.from_user.language_code == 'ru':
        lang = 'ru'
    else:
        lang = 'en'
    bot.send_message(message.from_user.id, localize.start_message[lang])

bot.polling(none_stop=True)