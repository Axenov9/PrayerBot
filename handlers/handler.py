import abc

from database.dbalchemy import DBManager

class Handler(metaclass=abc.ABCMeta):

    def __int__(self, bot):

        self.bot = bot

        self.DB = DBManager()



    @abc.abstractmethod
    def handle(self):
        pass

