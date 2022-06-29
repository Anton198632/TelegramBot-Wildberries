from enum import Enum
from colorama import Fore
import datetime


class Type(Enum):
    ERROR = -1
    SERVICE = 0
    FROM_BOT = 1
    FROM_USER = 2


class Logs:
    __SOURCE_LEN = 20
    __COLOR_DICT = {
        Type.ERROR: Fore.RED,
        Type.SERVICE: Fore.GREEN,
        Type.FROM_BOT: Fore.LIGHTBLUE_EX,
        Type.FROM_USER: Fore.YELLOW}

    @staticmethod
    def print(type: Type, source: str, message: str):
        color = Logs.__COLOR_DICT.get(type)

        if type == Type.ERROR or type == Type.SERVICE:
            source = 'SERVICE'

        count_added = Logs.__SOURCE_LEN - len(source)
        added_str = " " * count_added

        current_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print_mess = message
        # if len(print_mess) > 40:
        #     print_mess = print_mess[:40:] + '...'
        # print_mess = print_mess.replace('\n', '\\n')
        # print('{5} {0}: {1}{2}{3}{4}' \
        #     .format(source, added_str, color, print_mess.replace('\n', '\\n'), Fore.RESET, current_date))

        print(print_mess)

        message = '{0} {1}: {2}{3}\n' \
            .format(current_date, source, added_str, message.replace('\n', '\\n'))
        with open('log.txt', 'a') as f:
            f.write(message)
