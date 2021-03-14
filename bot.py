import telebot
from telebot import types
from const import token
import localize
from re import match
import random
from letters import katakana, hirogana

bot = telebot.TeleBot(token)

users_stat = {} #format user_id: {'answer': '', streak: 0}

return_to_main_markup = types.InlineKeyboardMarkup()
back_button = types.InlineKeyboardButton('Назад', callback_data='start')
skip = types.InlineKeyboardButton('Пропустить', callback_data='mixed_0_ru')
return_to_main_markup.row(back_button, skip)

@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.from_user.language_code == 'ru':
        lang = 'ru'
    else:
        lang = 'en'
    markup = types.InlineKeyboardMarkup()
    if lang == 'ru':
        markup.row(
            # types.InlineKeyboardButton('Хирагана', callback_data='hiragana_ru'),
            types.InlineKeyboardButton('На японский', callback_data='mixed_0_ru'),
            types.InlineKeyboardButton('С японского', callback_data='transcrypt_0_ru'),
            # types.InlineKeyboardButton('Катакана', callback_data='katakana_ru'),
        )
    else:
        markup.row(
            # types.InlineKeyboardButton('Hiragana', callback_data='hiragana_en'),
            types.InlineKeyboardButton('To jap', callback_data='mixed_0_en'),
            types.InlineKeyboardButton('From jap', callback_data='transcrypt_0_ru'),
            # types.InlineKeyboardButton('Katakana', callback_data='katakana_en'),
        )
    bot.send_message(message.from_user.id, localize.start_message[lang], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: match('transcrypt', call.data))
def to_transcrypt(call, right=False):
    print('Кто-то что-то тычет', call.from_user.username)
    t, streak, lang = call.data.split('_')
    print(call.data)
    streak = int(streak)
    alph = random.choice(['h', 'k'])
    if alph == 'h':
        symb = random.choice(list(hirogana.items()))
    else:
        symb = random.choice(list(katakana.items()))
    text = ''
    if right:
        text += '✅Правильно!\n'
    if streak > 0:
        text += f'Уже {streak} раз подряд правильно!\n'
    text += f'{symb[0]} ({alph})'
    symb_text = f'{symb[0]} ({alph})'
    bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=return_to_main_markup)
    bot.register_next_step_handler(call.message, transcrypt_checker, call, symb_text, symb[1], streak, lang)


def transcrypt_checker(message, main_call, text, answer, streak, lang):
    bot.delete_message(message.from_user.id, message.message_id)    
    if message.text == answer:
        main_call.data = f'transcrypt_{streak}_{lang}'
        mixed(main_call, right=True)
    else:
        bot.edit_message_text('❌Не правильно.\n'+text, main_call.message.chat.id, 
                              main_call.message.message_id, reply_markup=return_to_main_markup)
        bot.register_next_step_handler(main_call.message, transcrypt_checker, main_call, text, answer, 0, lang)


@bot.callback_query_handler(func=lambda call:match('mixed', call.data))
def mixed(call, right=False):
    print('Кто-то что-то тычет', call.from_user.username)
    t, streak, lang = call.data.split('_')
    print(streak)
    streak = int(streak)
    alph = random.choice(['h', 'k'])
    if alph == 'h':
        symb = random.choice(list(hirogana.items()))
    else:
        symb = random.choice(list(katakana.items()))
        
    text = ''
    if right:
        text += '✅Правильно!\n'
    if streak > 0:
        text += f'Уже {streak} раз подряд правильно!\n'
    text += f'{symb[1]} ({alph})'
    symb_text = f'{symb[1]} ({alph})'
    bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=return_to_main_markup)
    bot.register_next_step_handler(call.message, mixed_checker, call, symb_text, symb[0], streak, lang)

def mixed_checker(message, main_call, text, answer, streak, lang):
    bot.delete_message(message.from_user.id, message.message_id)    
    print(streak, 'vv checkere')
    if message.text == answer:
        main_call.data = f'mixed_{streak}_{lang}'
        mixed(main_call, right=True)
    else:
        bot.edit_message_text('❌Не правильно.\n'+text, main_call.message.chat.id, 
                              main_call.message.message_id, reply_markup=return_to_main_markup)
        bot.register_next_step_handler(main_call.message, mixed_checker, main_call, text, answer, 0, lang)


@bot.callback_query_handler(func=lambda call: call.data == 'start')
def start_cq(call):
    bot.clear_step_handler(call.message)
    if call.from_user.language_code == 'ru':
        lang = 'ru'
    else:
        lang = 'en'
    markup = types.InlineKeyboardMarkup()
    if lang == 'ru':
        markup.row(
            # types.InlineKeyboardButton('Хирагана', callback_data='hiragana_ru'),
            types.InlineKeyboardButton('Вперемешку', callback_data='mixed_0_ru'),
            # types.InlineKeyboardButton('Катакана', callback_data='katakana_ru'),
        )
    else:
        markup.row(
            # types.InlineKeyboardButton('Hiragana', callback_data='hiragana_en'),
            types.InlineKeyboardButton('Mixed', callback_data='mixed_0_en'),
            # types.InlineKeyboardButton('Katakana', callback_data='katakana_en'),
        )
    bot.edit_message_text(localize.start_message[lang], call.from_user.id, call.message.message_id, reply_markup=markup)


bot.polling(none_stop=True)