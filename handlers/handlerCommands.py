from handlers.handler import Handler
from functions.pray import pray
from functions.me import me
from functions.check_player import check_player
from functions.admin_func import op, skip

from database.dbalchemy import DBManager


class HandlerCommands(Handler):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.DB = DBManager()

    def command_start(self, message):
        self.bot.send_message(message.chat.id, 'Иди нахуй, нет никакого старта')

    def handle(self):
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            if message.text == '/start':
                self.command_start(message)

        @self.bot.message_handler(commands=['pray'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)

            if message.text == '/pray' or message.text == '/pray@PriestPrayerBot':
                check_player(message.from_user.id, message.chat.id, self.DB, message)
                pray(message.from_user.id, message.chat.id,message.message_id , self.bot, self.DB)
                # self.bot.send_message(message.chat.id, 'Не молись тут нахуй, нет еще этой функции')

        @self.bot.message_handler(commands=['me'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            if message.text == '/me' or message.text == '/me@PriestPrayerBot':
                me(message.from_user.id, message.chat.id,message.message_id , self.bot, self.DB)
                # self.bot.send_message(message.chat.id, 'Че ме, баран чтоли?')

        @self.bot.message_handler(commands=['op'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            if message.text == '/op' or message.text == '/op@PriestPrayerBot':
                if message.reply_to_message:
                    op(message.from_user.id, message.chat.id,message.message_id, message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name, self.bot, self.DB)
                else:
                    self.bot.send_message(message.chat.id, 'Ответьте на сообщение того, кого хотите сделать админом', reply_to_message_id=message.message_id)


        @self.bot.message_handler(commands=['skip'])
        def handle(message):
            print(message.from_user.username + ": " + message.text)
            if message.text == '/skip' or message.text == '/skip@PriestPrayerBot':
                skip(message.from_user.id, message.chat.id,message.message_id, self.bot, self.DB)


        # @self.bot.message_handler()
        # def handle(message):
            # print(message.from_user.username + ": " + message.text)
            # self.bot.send_message(message.chat.id, 'Нихуя не понял, можешь не повторять, иди нахуй')
