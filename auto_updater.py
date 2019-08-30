import const
import telebot
import os
from time import sleep

bot = telebot.TeleBot(const.bot_token)

while True:
    os.system("git add .; git commit -m 'Updating everithyng'; git push")
    sleep(5)

