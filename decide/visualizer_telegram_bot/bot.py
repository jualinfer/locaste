#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Basic function
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome! I'm the Locaste Visualization Bot.")

def main():
    print("Starting Telegram visualizer bot")

    updater = Updater('744386955:AAHXNjNeK1T0ryD95v5m5emk-3ifg-umleo')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()