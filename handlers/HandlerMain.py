
from handlers.handlerCommands import HandlerCommands
class HandlerMain:

    def __init__(self, bot):

        self.bot = bot
        self.handlercommands = HandlerCommands(self.bot)

    def handle(self):
        self.handlercommands.handle()