from dotenv import load_dotenv
load_dotenv()
import os

TOKEN = os.getenv("TOKEN")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send welcome messages when the command /start is issued."""
    update.message.reply_text('Welcome!')
    update.message.reply_text("I'm DecideLocasteBoothBot, the Telegram virtual booth assistant for Decide Locaste")
    



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command - Answer
    dp.add_handler(CommandHandler("start", start))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    #Block the bot until you decide to stop it with Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()