"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import json
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,CallbackContext, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update:update ,context:CallbackContext) -> None:
    update.message.reply_text('Hi! This will give you sumary of Test wikibot')


def button(update:update ,context:CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))


def help_command(update:update ,context:CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")

def test_wikibot(update:update ,context:CallbackContext):

    query = update.message.text

    url = "https://wikipenapi.herokuapp.com/page/?q="

    r = requests.get(url+query)

    ans = r.text
    result = json.loads(ans)

    a = result["details"]
    b = a["tittle"]
    c = a["url"]
    detailes = f"The details of the are as follows\nTittle of the page is: {b}\nUrl of the page is: {c}"
    update.message.reply_text(detailes)

    d = result["page"]
    e = d["summary"]
    update.message.reply_text(e)
    keyboard = [[InlineKeyboardButton("Url to the page", url=c)]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1479454800:AAE8yLKQJAIFGAV3iRxt6cCuHLkizyFjIbA", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, test_wikibot))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
