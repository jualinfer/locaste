#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler
import logging
import sys
import requests
from dotenv import load_dotenv
import os

sys.path.insert(0, '../decide')
import settings

load_dotenv()
TOKEN = os.getenv("TOKEN")


# The base URL needs to be changed when pushed it will use locaste-decide.herokuapp
# for local development I use localhost

# baseURL = settings.BASEURL
baseURL = 'http://127.0.0.1:8000'



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Basic start function
def start(bot, update):
    update.message.reply_text("Welcome! I'm the Locaste Visualization Bot.")
    update.message.reply_text('Type /help for a list of things I can do!')

# Help function
def help(bot, update):
    update.message.reply_text('/start       , obtain a greeting message')
    update.message.reply_text('/title voting_id      , obtain the title of the voting_id provided, ie. /title 1')

    update.message.reply_text('/login       , log in with your Decide credentials')
    update.message.reply_text('/logout      , log out with your Decide credentials')


# voting title and description function
def title_desc(bot, update):
    received_voting_id = update.message.text
    voting_id = received_voting_id.split(' ')[1]
    update.message.reply_text('You are looking for voting_id: ' + voting_id)

    url = baseURL + "/voting/?id="+voting_id
    r = requests.get(url).json()
    if r != []:
        update.message.reply_text('The title for the voting_id' + voting_id + ' is: ' + r[0]['name'])
        update.message.reply_text('Also the provided description is: ' + r[0]['desc'])
    else:
        update.message.reply_text('Ohh it looks like the provided voting_id was invalid \n' +
        'Please try a new title search with a different voting_id')
  


# Login and logout
def login(bot, update, user_data):
    user_data['password'] = update.message.text
    url = baseURL + "/rest-auth/login/"
    request = requests.post(url, data={'username': user_data['username'], 'password': user_data['password']})
    
    if request.status_code == 200:
        del user_data['password']
        user_data['token'] = request.json()['key']
        url = baseURL + "/authentication/getuser/"
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
    print('Base URL', baseURL)

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('title', title_desc))
    dispatcher.add_handler(CommandHandler('login', login))
    dispatcher.add_handler(CommandHandler('logout', logout))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()