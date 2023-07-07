from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb

bot = TeleBot('6086808949:AAE9vyl1WKgQa_A2beWYqzf4Ct32bjkJSu0')

markup = ikm()
markup.max_row_keys = 3
markup.add(ikb('Хуй', callback_data='a'))
markup.add(ikb('Пизда', callback_data='b'))



bot.send_message(-1001783889173, 'Ауе', parse_mode='Markdown', reply_markup=markup)
