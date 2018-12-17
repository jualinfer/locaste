from dotenv import load_dotenv
load_dotenv()
import os
import requests


TOKEN = os.getenv("TOKEN")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup, ParseMode, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['Log in', 'Cancel']]
reply_keyboard_tryagain = [['Try again', 'Cancel']]
reply_keyboard_logged = [['Access to a voting', 'Log out']]
markup = ReplyKeyboardMarkup(reply_keyboard )
markup_tryagain = ReplyKeyboardMarkup(reply_keyboard_tryagain)
markup_logged = ReplyKeyboardMarkup(reply_keyboard_logged)
markup_quit = ReplyKeyboardRemove()

CHOOSING, TYPING_USERNAME, TYPING_PASSWORD, TYPING_VOTING_ID  = range(4)

def start(bot, update):
    """Send welcome messages when the command /start is issued."""
    update.message.reply_text('Welcome!')
    update.message.reply_text("I'm DecideLocasteBoothBot, the Telegram virtual booth assistant for Decide Locaste")
    update.message.reply_text("First of all, you need to log in with your Decide Locaste credentials in order to access your votings",
    reply_markup=markup)

    return CHOOSING
    
def introduce_username(bot, update):
    update.message.reply_text("Good choice!", reply_markup=markup_quit)
    update.message.reply_text("Introduce your username, please")

    return TYPING_USERNAME

def introduce_password(bot, update, user_data):
    text = update.message.text
    user_data['username'] = text
    update.message.reply_text("Got it")
    update.message.reply_text("Now, introduce your password")

    return TYPING_PASSWORD

def login(bot, update, user_data):
    text = update.message.text
    user_data['password'] = text

    url = "http://localhost:8000/rest-auth/login/"
    r = requests.post(url, data={'username': user_data['username'], 'password': user_data['password']})
    
    if r.status_code == 200:
        update.message.reply_text("Great!")
        update.message.reply_text("Logged succesfully")
        del user_data['password']
        user_data['token'] = r.json()['key']

        #Now we have the token, so we can request the user id to the Decide Locaste API
        url = "http://localhost:8000/authentication/getuser/"
        r = requests.post(url, data={'token': user_data['token'], })
        user_data['user_id'] = r.json()['id']

        update.message.reply_text("What are we doing next " + user_data['username'] + "?",
        reply_markup=markup_logged)
    
    else:
        update.message.reply_text("Oops, something went wrong")
        update.message.reply_text("Check your credentials and try it again",
        reply_markup=markup_tryagain)

    return CHOOSING

def introduce_voting_id(bot, update, user_data):
    update.message.reply_text("Please "+user_data['username']+ ", introduce the voting id you want to access in", reply_markup=markup_quit)

    return TYPING_VOTING_ID

def get_voting(bot, update, user_data):
    update.message.reply_text("Got it")
    update.message.reply_text("Let's search for the voting...")
    id = update.message.text

    url = "http://localhost:8000/voting/?id="+id
    r = requests.get(url)
    if r.json() != []:
        update.message.reply_text("Here It is:")
        msg = "------------------------------------------------------------\n*"+str(r.json()[0]['id']) + " - " + r.json()[0]['name'] + "*\n\n*" + r.json()[0]['question']['desc'] + "*\n\n"
        reply_keyboard_logged = []
        options_dict = {}
        for option in r.json()[0]['question']['options']:
            options_dict[option['number']-1] = option['option']
            msg += str(option['number']-1) + ". " + option['option'] + "\n"
        update.message.reply_text(msg + "\n" + 
            "------------------------------------------------------------", parse_mode=ParseMode.MARKDOWN)
        if r.json()[0]['end_date'] != None:
            update.message.reply_text("This voting has already ended, exactly at " + r.json()[0]['end_date'].split('.')[0].replace('T',' '))
            update.message.reply_text("Votes are not allowed for this voting anymore")
            update.message.reply_text("What are we doing next " + user_data['username'] + "?",
            reply_markup=markup_logged)
            
            return CHOOSING
    else:
        update.message.reply_text("Sorry, It seems like the voting doesn't exist in Decide Locaste system")
        update.message.reply_text("Check the id introduced or contact with the admin")
        update.message.reply_text("What are we doing next " + user_data['username'] + "?",
        reply_markup=markup_logged)

        return CHOOSING


def logout(bot, update, user_data):
    update.message.reply_text('Bye ' + user_data['username'] + ", have a nice day!", reply_markup=markup_quit)
    update.message.reply_text("Don't forget I'm still here, just wake me up by introducing /start if you need me")
    del user_data['username']
    del user_data['token']
    del user_data['user_id']

    return ConversationHandler.END

def cancel(bot, update):
    update.message.reply_text('I just wanted to be useful, but another time maybe!', reply_markup=markup_quit)
    update.message.reply_text('If you need me again you can call me by introducing /start. See you!')
    
    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def unknown_command(bot, update,  user_data):
    update.message.reply_text('Sorry It seems like I can not understand your petition')
    

def main():
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CommandHandler('start', start),],

        states={
            CHOOSING: [RegexHandler('^(Log\s+in|Try\s+again)$',introduce_username),
                       RegexHandler('^Cancel$',cancel),
                       RegexHandler('^Log\s+out$',logout, pass_user_data=True),
                       RegexHandler('^Access\s+to\s+a\s+voting$',introduce_voting_id, pass_user_data=True),
                       ],

            TYPING_USERNAME: [MessageHandler(Filters.text,introduce_password,pass_user_data=True),
                           ],

            TYPING_PASSWORD: [MessageHandler(Filters.text, login, pass_user_data=True),
                           ],

            TYPING_VOTING_ID: [MessageHandler(Filters.text, get_voting, pass_user_data=True),
                           ],
        },
        fallbacks=[MessageHandler(Filters.text, unknown_command, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    #Block the bot until you decide to stop it with Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()