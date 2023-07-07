from telebot import TeleBot

from handlers.HandlerMain import HandlerMain
from settings import config


class RunBot:
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        self.token = config.TOKEN

        self.bot = TeleBot(self.token)

        self.handler = HandlerMain(self.bot)

    def start(self):
        self.handler.handle()

    def run_bot(self):
        self.start()
        # self.bot.send_message(249562441, 'started')
        self.bot.polling(non_stop=True)
        # self.bot.send_message(249562441, 'finished')


if __name__ == '__main__':
    # try:
    bot = RunBot()
    bot.run_bot()
    # except:
    #     bot = TeleBot(config.TOKEN)
    #     bot.send_message(249562441, 'Бот завершил работу *из-за ошибки*', parse_mode='Markdown')
