import telebot
from telebot import types
from const import token
import localize
from re import match
import random
from katakana import katakana
from hiragana import hirogana

bot = telebot.TeleBot(token)

users_stat = {} #format user_id: {'answer': '', streak: 0}

@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.from_user.language_code == 'ru':
        lang = 'ru'
    else:
        lang = 'en'
    markup = types.InlineKeyboardMarkup()
    if lang == 'ru':
        markup.row(
            types.InlineKeyboardButton('Хирагана', callback_data='hiragana_ru'),
            types.InlineKeyboardButton('Вперемешку', callback_data='mixed_0_ru'),
            types.InlineKeyboardButton('Катакана', callback_data='katakana_ru'),
        )
    else:
        markup.row(
            types.InlineKeyboardButton('Hiragana', callback_data='hiragana_en'),
            types.InlineKeyboardButton('Mixed', callback_data='mixed_0_en'),
            types.InlineKeyboardButton('Katakana', callback_data='katakana_en'),
        )
    bot.send_message(message.from_user.id, localize.start_message[lang], reply_markup=markup)


@bot.callback_query_handler(func=lambda call:match('mixed', call.data))
def mixed(call):
    t, streak, lang = call.data.split('_')
    alph = random.choice(['h', 'k'])
    if alph = 'h':
        symb = random.choice(list(hirogana.items()))
    else:
        symb = random.choice(list(katakana.items()))
    

    bot.send_message()




bot.polling(none_stop=True)