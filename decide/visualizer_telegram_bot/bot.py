#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler
import logging
import sys
import settings
import requests

sys.path.insert(1, '../decide')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Basic start function
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome! I'm the Locaste Visualization Bot.")
    bot.send_message(chat_ud=update.message.chat_id, text="Type /help for a list of things I can do!")

# Help function
def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=[
        "/start         obtain a greeting message",
        "/login         log in with your Decide credentials",
        "/logout        log out with your Decide credentials"
    ])

# Login and logout
def login(bot, update, user_data):
    user_data['password'] = update.message.text
    url = settings.BASEURL + "/rest-auth/login/"
    request = requests.post(url, data={'username': user_data['username'], 'password': user_data['password']})
    
    if request.status_code == 200:
        del user_data['password']
        user_data['token'] = request.json()['key']
        url = settings.BASEURL +"/authentication/getuser/"
        request2 = requests.post(url, data={'token': user_data['token'], })
        user_data['user_id'] = request2.json()['id']

        bot.send_message(chat_id=update.message.chat_id, text="Logged in as" + user_data['username'] + "!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Login unsuccessful. Please verify your credentials.")

def logout(bot, update, user_data):
    del user_data['username']
    del user_data['token']
    del user_data['user_id']
    bot.send_message(chat_id=update.message.chat_id, text="Logged out.")

def main():
    print("Starting Telegram visualizer bot")

    # TODO: Store token somewhere accesible by any OS configuration
    updater = Updater('744386955:AAHXNjNeK1T0ryD95v5m5emk-3ifg-umleo')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('login', login))
    dispatcher.add_handler(CommandHandler('logout', logout))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()