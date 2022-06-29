from typing import List
import re
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton, KeyboardButton
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import Dispatcher

import sets
from logs import Logs, Type
from wildberries import WildberriesParser, Socks, Product


class WTelegramBot:
    __DESCRIPTION_TEXT = 'Пришлите мне артикул товара Wildberries и я скажу сколько его осталось на складах.'
    __BOT_START_TEXT = 'Бот запущен'
    __NO_QWT_TEXT = 'нет в наличии\n'
    __NOT_FIND = 'товар не найден'
    __MAX_IDS = 20

    def __init__(self):
        self.settnings = sets.Settings()

        self.updater: Updater = Updater(token=self.settnings.get_token())
        self.dispatcher: Dispatcher = self.updater.dispatcher

        self.messages_handler: MessageHandler = MessageHandler(
            filters=Filters.text, callback=self.text_message_handler)
        self.dispatcher.add_handler(self.messages_handler)

        self.inline_button_handlers: CallbackQueryHandler = CallbackQueryHandler(
            callback=self.inline_button_handler)
        self.dispatcher.add_handler(self.inline_button_handlers)

    def start_request_processing(self):
        Logs.print(Type.SERVICE, '', self.__BOT_START_TEXT)
        self.updater.start_polling(poll_interval=2)
        self.updater.idle()

    def text_message_handler(self, update: Update, context: CallbackContext):
        if update.channel_post is not None:
            return

        mess = update.effective_message.text
        Logs.print(Type.FROM_USER, str(update.effective_message.chat_id), mess)

        ids = self.__get_only_numbers(mess)

        if len(ids) > 0:
            result_text = self.__build_result(ids)
            if result_text != '':
                self.send_inline_button(
                    update,
                    text=result_text,
                    context=context)
            else:
                self.send_message_text(
                    update,
                    text=self.__NOT_FIND,
                    context=context)

        elif mess == '/start':
            self.send_message_text(
                update,
                text=self.__DESCRIPTION_TEXT,
                context=context)
        else:
            Logs.print(Type.ERROR, '', 'Неверный артикул: {}'.format(mess))

    def inline_button_handler(self, update: Update, context: CallbackContext):

        Logs.print(Type.FROM_USER, str(update.effective_message.chat_id),
                   update.effective_message.text_html)

        ids = self.__get_ids_from_message(update.effective_message.text_html)
        result_text = self.__build_result(ids)

        self.send_inline_button(
            # chat_id=update.effective_message.chat_id,
            update,
            text=result_text,
            context=context)

    def __build_result(self, ids: List[int]):
        wildberries = WildberriesParser()
        parse_result: List[Product] = wildberries.parse(ids)
        result_text = ''
        for result in parse_result:
            if result == None:
                continue
            result_text += result.build_result()


        # result_text += '*' * 1000
        l = len(result_text)
        if l > 4096:
            result_text = result_text[0:4000]
            result_text += '\n* * * * * *\n\n!!!Запрос слишком большой.\nРазбейте запрос на несколько частей.'
        return result_text

    def send_inline_button(self, update: Update, text: str,
                           context: CallbackContext):
        if text == '':
            return

        mk_list = [
            [InlineKeyboardButton(text='Повторить', callback_data='pressB1')]
        ]
        Logs.print(Type.FROM_BOT, self.settnings.get_bot_name(), text)

        update.effective_message.reply_text(text=text, parse_mode='HTML',
                                            disable_web_page_preview=True,
                                            reply_markup=InlineKeyboardMarkup(
                                                mk_list))

    def send_message_text(self, update: Update, text: str,
                          context: CallbackContext):
        if text == '':
            return

        Logs.print(Type.FROM_BOT, self.settnings.get_bot_name(), text)

        update.effective_message.reply_text(text=text,
                                            parse_mode='HTML')

    def __get_only_numbers(self, text: str) -> List[int]:
        ids = re.split(',|\n', text)
        idss = []
        i = 0
        for id in ids:
            i += 1
            if i > self.__MAX_IDS:
                break
            number = ''.join(re.findall(r'\d+', id))
            if number != '':
                idss.append(int(number))

        return idss

    def __get_ids_from_message(self, html_text: str) -> List[int]:
        ids_text = html_text.split('catalog/')
        result = []
        for id_text in ids_text:
            index = id_text.find('/')
            if id_text[:index:].isdigit():
                result.append(int(id_text[:index:]))

        return result
