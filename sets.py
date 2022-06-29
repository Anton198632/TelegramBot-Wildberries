

class Settings:
    def __init__(self):
        self.__TOKEN = ''
        self.__BOT_NAME = ''

    def get_token(self):
        return self.__TOKEN

    def get_bot_name(self):
        return self.__BOT_NAME