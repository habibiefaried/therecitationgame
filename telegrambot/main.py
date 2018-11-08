#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import pymongo
from pprint import pprint
import os
from cnnlib import cnnlib

#Mongo connector
f = open("../secrets/mongouser", "r")
mongouser = f.read().split('\n')[0]
f = open("../secrets/mongopass", "r")
mongopass = f.read().split('\n')[0]
f = open("../secrets/mongohost", "r")
mongohost = f.read().split('\n')[0]

print "Connecting to mongo"
mongostr = "mongodb://"+mongouser+":"+mongopass+"@"+mongohost+"/?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"
print "Target: "+mongostr
myclient = pymongo.MongoClient(mongostr)
print "Succeed! Accepting request..."

mydb = myclient["quran"]
myusers = mydb["users"]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def is_user_exist(telegram_id):
    if (myusers.find_one({"telegram_id": telegram_id})):
        return True
    else:
        return False

def start(bot, update):
    if (is_user_exist(update.message.from_user.id)):
        update.message.reply_text("You are already registered!")
    else:
        val = {"telegram_id" : update.message.from_user.id, "username" : update.message.from_user.username, "current_surah":1, "current_ayah":1}
        myusers.insert_one(val)
        update.message.reply_text("Welcome to Al-Quran recitation bot!")
        update.message.reply_text("This bot grades your voice whether you are correctly recite an ayah or not using Deep Learning algorithm")
        update.message.reply_text("By registering to our system, you agree that your telegram data (username, id) will be captured for our tracking system")
        update.message.reply_text("And also, your recorded voice will be stored for our deep learning research purposes")
        update.message.reply_text("If you do not agree terms above, then send /leave command to delete your data")
        update.message.reply_text("Feel free to DM me @habibiefaried if you have any questions")
        update.message.reply_text('In order to proceed, please issue a command /status')

def leave(bot, update):
    if (is_user_exist(update.message.from_user.id)):
        update.message.reply_text("Your data has been deleted from our system. Good bye!")
    else:
        update.message.reply_text("401 Unauthorized. Issue /start command to register")

def status(bot, update):
    x = myusers.find_one({"telegram_id": update.message.from_user.id})
    if (x):
        surah = x['current_surah']
        ayah = x['current_ayah']
        update.message.reply_text("Please recite surah "+str(surah)+" ayah "+str(ayah))
    else:
        update.message.reply_text("401 Unauthorized. Issue /start command to register")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def voice(bot, update):
    global C
    x = myusers.find_one({"telegram_id": update.message.from_user.id})
    if (x):
	target_file = "/audios/"+update.message.voice.file_id+".ogg"
	wav_file = target_file+".wav"

        print "From: "+str(update.message.from_user.id)+". Name: "+update.message.from_user.username
        update.message.voice.get_file().download(target_file)

        os.system("ffmpeg -i "+target_file+" -filter:a loudnorm -ar 22050 -y "+wav_file+" > /dev/null 2>&1")
	C = cnnlib()

	if (C.isCorrect(wav_file, str(x['current_ayah']))):
		update.message.reply_text("Correct! please go to the next ayah")
		myusers.update_one({"telegram_id": update.message.from_user.id}, {"$set": { "current_ayah": x['current_ayah']+1 }})
	else:
		update.message.reply_text("It seems that you recited in wrong way. Please /status to make sure you recite the correct ayah or try again")

    else:
        update.message.reply_text("401 Unauthorized. Issue /start command to register")

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
