import sys
import time

import log
from telegram_bot import WTelegramBot
from logs import Logs, Type


if __name__ == '__main__':

    # if 'log_control' in sys.argv:
    log.Logger('Wildberries_TelegramBot')
    log.Logger.start()

    while True:
        try:
            w_telegram_bot = WTelegramBot()
            w_telegram_bot.start_request_processing()
        except Exception as error:
            Logs.print(Type.ERROR, '', error)
            time.sleep(60)

