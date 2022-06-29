

class Settings:
    def __init__(self):
        self.__TOKEN = 'ТОКЕН БОТА'
        self.__BOT_NAME = 'НАЗВАНИЕ БОТА'

    def get_token(self):
        return self.__TOKEN

    def get_bot_name(self):
        return self.__BOT_NAME