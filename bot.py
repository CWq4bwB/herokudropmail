# Импортируем необходимые классы.
import logging
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import ReplyKeyboardMarkup
from based_requests import fetch_users_messages, new_address
import os


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR
)

logger = logging.getLogger(__name__)

TOKEN = os.environ["TOKEN_BOT"]
APP_NAME = os.environ["APP_NAME"]

reply_keyboard = [['Новый адрес', 'Активные адреса'], ['Проверить входящие'],
                  ['Восстановить адрес', 'Доп. функции']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)


def echo(update, context):
    result = fetch_users_messages(update.message.from_user.id, update.message.text)
    if type(result) == list and len(result) == 2:
        update.message.reply_text(result[0], reply_markup=result[1])
    else:
        update.message.reply_text(result, reply_markup=markup)


def button(update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    uid = query.message.chat.id
    query.answer()
    returned = new_address(uid, query.data)
    query.edit_message_text(text=returned)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dp.add_handler(text_handler)
    updater.start_webhook(listen="0.0.0.0", port=1337, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
