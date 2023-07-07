from database.dbalchemy import DBManager
from functions.admin_func import op, skip, add_level, add_purse, send_error
from functions.check_player import check_player
from functions.me import me
from functions.pray import pray
from functions.relics import relics, buy_relics, buy_relic_by_id
from handlers.handler import Handler
from settings.messages import messages

from json import dumps
class HandlerCommands(Handler):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.DB = DBManager()

    def handle(self):
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            text = messages['start']
            self.bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=message.message_id)

        @self.bot.message_handler(commands=['create'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            if not check_player(message.from_user.id, message.chat.id, self.DB, self.bot, message):
                try:
                    text = messages['create'].format(message.from_user.first_name)
                    self.DB.add_new_player(message.from_user.id, message.chat.id, message.from_user.first_name)
                    self.bot.send_message(message.chat.id, text, parse_mode='Markdown',
                                          reply_to_message_id=message.message_id)
                except:
                    send_error(message, self.bot)
            else:
                text = 'Такой игрок *уже существует*'
                self.bot.send_message(message.chat.id, text, parse_mode='Markdown',
                                      reply_to_message_id=message.message_id)

        @self.bot.message_handler(commands=['pray'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            # try:
            if check_player(message.from_user.id, message.chat.id, self.DB, self.bot, message):
                pray(message.from_user.id, message.chat.id, message.message_id, self.bot, self.DB)
            # except:
            #     send_error(message, self.bot)
            # self.bot.send_message(message.chat.id, 'Не молись тут нахуй, нет еще этой функции')

        @self.bot.message_handler(commands=['me'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            try:
                me(message.from_user.id, message.chat.id, message.message_id, self.bot, self.DB)
            except:
                send_error(message, self.bot)
                # self.bot.send_message(message.chat.id, 'Че ме, баран чтоли?')

        @self.bot.message_handler(commands=['op'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            if message.reply_to_message:
                try:
                    op(message.from_user.id, message.chat.id, message.message_id, message.reply_to_message.from_user.id,
                       message.reply_to_message.from_user.first_name, self.bot, self.DB)
                except:
                    send_error(message, self.bot)
            else:
                text = 'Ответьте на сообщение того, кого хотите сделать админом'
                self.bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)

        @self.bot.message_handler(commands=['skip'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            try:
                skip(message.from_user.id, message.chat.id, message, self.bot, self.DB)
            except:
                send_error(message, self.bot)

        @self.bot.message_handler(commands=['add'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            try:
                if len(message.text.split()) >= 3:
                    if message.text.split()[1] == 'level':
                        count = message.text.split()[2]
                        # print(count)
                        add_level(message, count, self.bot, self.DB)

                    if message.text.split()[1] == 'balance':
                        count = message.text.split()[2]
                        # print(count)
                        add_purse(message, count, self.bot, self.DB)

                else:
                    text = messages['inc_args']
                    self.bot.send_message(message.chat.id, text, parse_mode='Markdown',
                                          reply_to_message_id=message.message_id)
            except:
                send_error(message, self.bot)

        @self.bot.message_handler(commands=['relics'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            # try:
            if check_player(message.from_user.id, message.chat.id, self.DB, self.bot, message):
                relics(message, self.bot, self.DB)
            # except:
            #     send_error(message, self.bot)

        @self.bot.callback_query_handler(func = lambda call: call.data == 'buy_relics')
        def handle(call):
            print(call.from_user.username + ": " + call.data)
            # print(call)
            if call.from_user.id == call.message.reply_to_message.from_user.id:
                buy_relics(call, self.bot, self.DB)
            else:
                self.bot.answer_callback_query(call.id, text=messages['not_sender_call'], show_alert=True)

        @self.bot.callback_query_handler(func=lambda call: 'buy' in call.data)
        def handle(call):
            print(call.from_user.username + ": " + call.data)
            if call.from_user.id == call.message.reply_to_message.from_user.id:
                buy_relic_by_id(call, self.bot, self.DB)
            else:
                self.bot.answer_callback_query(call.id, text=messages['not_sender_call'], show_alert=True)


            # self.bot.send_message(call.message.chat.id, call.data)
        # @self.bot.message_handler()
        # def handle(message):
        # print(message.from_user.username + ": " + message.text)
        # self.bot.send_message(message.chat.id, 'Нихуя не понял, можешь не повторять, иди нахуй')
