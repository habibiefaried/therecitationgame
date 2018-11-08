#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from pprint import pprint

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Welcome to Al-Quran recitation bot!")
    update.message.reply_text("This bot grades your voice whether you are correctly recite an ayah or not using Deep Learning algorithm")
    update.message.reply_text("By registering to our system, you agree that your telegram data (username, id) will be captured for our tracking system")
    update.message.reply_text("And also, your recorded voice will be stored for our deep learning research purposes")
    update.message.reply_text("If you do not agree terms above, then send /leave command to delete your data")
    update.message.reply_text("Feel free to DM me @habibiefaried if you have any questions")
    update.message.reply_text('In order to proceed, please issue a command /status')

def leave(bot, update):
    update.message.reply_text("Your data has been deleted from our system. Good bye!")

def status(bot, update):
    surah = 1
    ayah = 1
    update.message.reply_text("Please recite surah "+str(surah)+" ayah "+str(ayah))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def voice(bot, update):
    print "From: "+str(update.message.from_user.id)+". Name: "+update.message.from_user.username
    print "File ID: "+update.message.voice.file_id
    update.message.voice.get_file().download("/tmp/audio.something")
    update.message.reply_text("Received!")

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    tok = ""
    with open('../secrets/telegramtoken', 'r') as myfile:
        tok=myfile.read().replace('\n', '')

    updater = Updater(tok)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("leave", leave))
    dp.add_handler(CommandHandler("status", status))

    # Audio command
    dp.add_handler(MessageHandler(Filters.voice, voice))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
