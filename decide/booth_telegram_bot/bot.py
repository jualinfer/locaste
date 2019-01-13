from dotenv import load_dotenv
load_dotenv()
import os
import requests
import re
from datetime import datetime


TOKEN = os.getenv("TOKEN")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup, ParseMode, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import logging
import numpy



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['Sign up', 'Log in', 'Cancel']]
reply_keyboard_tryagain = [['Try again', 'Cancel']]
reply_keyboard_gender = [['Male', 'Female', 'Other'], ['Cancel Sign up']]
reply_keyboard_cancel_signup = [['Cancel Sign up']]
reply_keyboard_cancel = [['Cancel']]
reply_keyboard_logged = [["Show votings in which I'm registered to vote"], ['Show all votings', 'Register in a census'], [ 'Access to a voting', 'Log out']]
markup = ReplyKeyboardMarkup(reply_keyboard )
markup_tryagain = ReplyKeyboardMarkup(reply_keyboard_tryagain)
markup_gender = ReplyKeyboardMarkup(reply_keyboard_gender)
markup_cancel_signup = ReplyKeyboardMarkup(reply_keyboard_cancel_signup)
markup_cancel = ReplyKeyboardMarkup(reply_keyboard_cancel)
markup_logged = ReplyKeyboardMarkup(reply_keyboard_logged)
markup_quit = ReplyKeyboardRemove()

CHOOSING_NOT_LOGGED,CHOOSING_LOGGED,OPTION_VOTED, TYPING_USERNAME, TYPING_PASSWORD, TYPING_VOTING_ID, TYPING_USERNAME_SIGNUP, TYPING_PASSWORD_SINGUP, TYPING_CONFIRMATION_PASSWORD_SINGUP, TYPING_BIRTHDATE_SIGNUP, TYPING_GENDER_SINGUP, TYPING_VOTING_ID_CENSUS  = range(12)

def start(bot, update):
    """Send welcome messages when the command /start is issued."""
    update.message.reply_text('Welcome!')
    update.message.reply_text("I'm DecideLocasteBoothBot, the Telegram virtual booth assistant for Decide Locaste")
    update.message.reply_text("First of all, you need to sign up or to log in with your Decide Locaste credentials in order to access your votings",
    reply_markup=markup)

    return CHOOSING_NOT_LOGGED

#Sign up process
def introduce_username_signup(bot, update):
    update.message.reply_text("Let's get to work", reply_markup=markup_quit)
    update.message.reply_text('Introduce an username, please',
        reply_markup=markup_cancel_signup)

    return TYPING_USERNAME_SIGNUP

def introduce_password_signup(bot, update, user_data):
    text = update.message.text
    if(text == 'Cancel Sign up'):
        update.message.reply_text("Aborting sign up...")
        update.message.reply_text("What are we doing now?",
            reply_markup=markup)
        return CHOOSING_NOT_LOGGED
    user_data['username'] = text
    update.message.reply_text("Introduce your password",
        reply_markup=markup_cancel_signup)

    return TYPING_PASSWORD_SINGUP

def introduce_confirmation_password_signup(bot, update, user_data):
    text = update.message.text
    if(text == 'Cancel Sign up'):
        update.message.reply_text("Aborting sign up...")
        update.message.reply_text("What are we doing now?",
            reply_markup=markup)
        return CHOOSING_NOT_LOGGED
    user_data['password'] = text
    if(len(text) < 8):
        update.message.reply_text("The password must contain at least 8 digits")
        update.message.reply_text("Introduce your password again",
            reply_markup=markup_cancel_signup)

        return TYPING_PASSWORD_SINGUP
    elif(re.search("\d+",text)):
        update.message.reply_text("The password can't be entirely numeric")
        update.message.reply_text("Introduce your password again",
            reply_markup=markup_cancel_signup)

        return TYPING_PASSWORD_SINGUP
    elif(re.match("^asdfghjk|asdfghjkl|asdfghjklñ$",text)):
        update.message.reply_text("The password is too common")
        update.message.reply_text("Introduce your password again",
            reply_markup=markup_cancel_signup)

        return TYPING_PASSWORD_SINGUP
    else:
        update.message.reply_text("Confirm your password again",
            reply_markup=markup_cancel_signup)

        return TYPING_CONFIRMATION_PASSWORD_SINGUP

def introduce_birthdate(bot, update, user_data):
    text = update.message.text
    if(text == 'Cancel Sign up'):
        update.message.reply_text("Aborting sign up...")
        update.message.reply_text("What are we doing now?",
            reply_markup=markup)
        return CHOOSING_NOT_LOGGED
    user_data['confirmation'] = text
    if(user_data['confirmation'] != user_data['password']):
        update.message.reply_text("Confirmation doesn't match password")
        update.message.reply_text("Check it")
        update.message.reply_text("Introduce your password again",
            reply_markup=markup_cancel_signup)

        return TYPING_PASSWORD_SINGUP
    else:
        update.message.reply_text("Introduce your birthdate in the following format: yyyy-mm-dd",
            reply_markup=markup_cancel_signup)

        return TYPING_BIRTHDATE_SIGNUP

def introduce_gender_signup(bot, update, user_data):
    text = update.message.text
    if(text == 'Cancel Sign up'):
        update.message.reply_text("Aborting sign up...")
        update.message.reply_text("What are we doing now?",
            reply_markup=markup)
        return CHOOSING_NOT_LOGGED
    user_data['birthdate'] = text
    if(re.match("^\d{4}-\d{2}-\d{2}$",text) == None):
        update.message.reply_text("The birthdate introduced doesn't follow the restricted format")
        update.message.reply_text("Check it")
        update.message.reply_text("Introduce your birthdate again",
            reply_markup=markup_cancel_signup)

        return TYPING_BIRTHDATE_SIGNUP
    else:
        try:
            birthdate = datetime.strptime(text, '%Y-%m-%d')
            if(birthdate > datetime.now()):
                update.message.reply_text("You can't be born in the future!!")
                update.message.reply_text("Check it")
                update.message.reply_text("Introduce your birthdate again",
                    reply_markup=markup_cancel_signup)

                return TYPING_BIRTHDATE_SIGNUP
            else:
                update.message.reply_text("Introduce your gender with the menu options",
                    reply_markup=markup_gender)

                return TYPING_GENDER_SINGUP
        except:
            update.message.reply_text("The birthdate introduced doesn't follow the restricted format or doesn't make sense")
            update.message.reply_text("Check it")
            update.message.reply_text("Introduce your birthdate again",
                reply_markup=markup_cancel_signup)

            return TYPING_BIRTHDATE_SIGNUP
        
def signup(bot, update, user_data):
    text = update.message.text
    if(text == 'Cancel Sign up'):
        update.message.reply_text("Aborting sign up...")
        update.message.reply_text("What are we doing now?",
            reply_markup=markup)
        return CHOOSING_NOT_LOGGED
    user_data['gender'] = text

    if(re.match("^Male|Female|Other$",text) == None):
        update.message.reply_text("The gender introduced doesn't follow the restricted format")
        update.message.reply_text("Check it")
        update.message.reply_text("Introduce your gender again",
            reply_markup=markup_gender)

        return TYPING_GENDER_SINGUP
    else:
        url = "https://locaste-decide.herokuapp.com/authentication/signup/"
        #url = "http://localhost:8000/authentication/signup/"
        r = requests.post(url, data={'username': user_data['username'], 'password1': user_data['password'], 'password2': user_data['confirmation'], 'birthdate': user_data['birthdate']+"T00:00",'gender': user_data['gender']})
        if r.status_code == 201:
            update.message.reply_text("Sign up performed succesfully!")
            update.message.reply_text("You can try to log in with the created credentials now",
                reply_markup=markup)
        elif r.status_code == 400:
            update.message.reply_text("Sorry...")
            update.message.reply_text("Username is already in use")
            update.message.reply_text("Try another one",
                reply_markup=markup)
        else:
            update.message.reply_text("There is a problem with decide system try again later",
                reply_markup=markup)

        return CHOOSING_NOT_LOGGED
    
    
#Log in process    
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

    url = "https://locaste-decide.herokuapp.com/rest-auth/login/"
    #url = "http://localhost:8000/rest-auth/login/"
    r = requests.post(url, data={'username': user_data['username'], 'password': user_data['password']})
    
    if r.status_code == 200:
        update.message.reply_text("Great!")
        update.message.reply_text("Logged succesfully")
        user_data['token'] = r.json()['key']

        #Now we have the token, so we can request the user id to the Decide Locaste API
        url = "https://locaste-decide.herokuapp.com/authentication/getuser/"
        #url = "http://localhost:8000/authentication/getuser/"
        r = requests.post(url, data={'token': user_data['token'], })
        user_data['user_id'] = r.json()['id']

        update.message.reply_text("What are we doing next " + user_data['username'] + "?",
        reply_markup=markup_logged)

        return CHOOSING_LOGGED
    
    else:
        update.message.reply_text("Oops, something went wrong")
        update.message.reply_text("Check your credentials and try it again",
        reply_markup=markup_tryagain)
        
        return CHOOSING_NOT_LOGGED

def get_census_logged_user(bot, update, user_data):
    update.message.reply_text("Ok")

    url = "https://locaste-decide.herokuapp.com/census/?voter_id="+str(user_data['user_id'])
    #url = "http://localhost:8000/census/?voter_id="+str(user_data['user_id'])
    r = requests.get(url, auth=(user_data['username'], user_data['password']))
    if len(r.json()['voting']) != 0:
        update.message.reply_text("You are registered to vote in the following votings:")
        msg=""
        for voting_id in r.json()['voting']:
            url = "https://locaste-decide.herokuapp.com/voting/?id="+str(voting_id)
            #url = "http://localhost:8000/voting/?id="+str(voting_id)
            r = requests.get(url)
            voting = r.json()[0]
            msg+= "*ID = " + str(voting['id']) + "* | " + voting['name']
            if voting['end_date'] == None and voting['start_date'] != None:
                msg+= " | *(ACTIVE)*\n"
            elif voting['start_date'] == None:
                msg+= " | *(NOT STARTED)*\n"
            else:
                msg+= " | *(FINISHED)*\n"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Sorry... It seems like you are not registered in any census yet")
    
    update.message.reply_text("What are we doing next " + user_data['username'] + "?",
    reply_markup=markup_logged)

    return CHOOSING_LOGGED

def introduce_voting_id(bot, update, user_data):
    update.message.reply_text("Please "+user_data['username']+ ", introduce the voting id you want to access in",
        reply_markup=markup_cancel)

    return TYPING_VOTING_ID

def get_voting(bot, update, user_data):
    id = update.message.text
    if(id == 'Cancel'):
        update.message.reply_text("Aborting...")
        update.message.reply_text("What are we doing next " + user_data['username'] + "?",
            reply_markup=markup_logged)
        return CHOOSING_LOGGED
    update.message.reply_text("Got it")
    update.message.reply_text("Let's search for the voting...")

    url = "https://locaste-decide.herokuapp.com/voting/?id="+id
    #url = "http://localhost:8000/voting/?id="+id
    r = requests.get(url)
    if r.json() != []:
        #Check first if the user is registered to vote in this voting, that's has a census object
        url = "https://locaste-decide.herokuapp.com/census/?voter_id="+str(user_data['user_id'])
        #url = "http://localhost:8000/census/?voter_id="+str(user_data['user_id'])
        r2 = requests.get(url, auth=(user_data['username'], user_data['password']))
        #if the user is registered to vote
        if int(id) in r2.json()['voting']:
            update.message.reply_text("Here It is:")
            msg = "------------------------------------------------------------\n*"+str(r.json()[0]['id']) + " - " + r.json()[0]['name'] + "*\n\n*" + r.json()[0]['question'][0]['desc'] + "*\n\n"
            reply_keyboard_options = []
            options_dict = {}
            for option in r.json()[0]['question'][0]['options']:
                options_dict[str(option['number']-1)] = option['option']
                msg += str(option['number']-1) + ". " + option['option'] + "\n"
            user_data['options_dict'] = options_dict
            update.message.reply_text(msg + "\n" + 
                "------------------------------------------------------------", parse_mode=ParseMode.MARKDOWN)
            if r.json()[0]['end_date'] != None:
                update.message.reply_text("This voting has already ended, exactly at " + r.json()[0]['end_date'].split('.')[0].replace('T',' '))
                update.message.reply_text("Votes are not allowed for this voting anymore")
            elif r.json()[0]['start_date'] == None:  
                update.message.reply_text("This voting is not started yet, accessing to a voting is only permitted when it is started")
            else:
                #If the user can vote for this voting we need to store voting pub_key in order to encrypt the user vote
                user_data['pub_key'] = r.json()[0]['pub_key']
                #And also the voting_id
                user_data['voting_id'] = id

                reply_keyboard_options.append(numpy.asarray(list(options_dict.keys())))
                reply_keyboard_options.append(['Cancel'])
                markup_options = ReplyKeyboardMarkup(reply_keyboard_options)
                update.message.reply_text("What option are you voting, " + user_data['username'] + "?",
                reply_markup=markup_options)

                return OPTION_VOTED
        #if the user is not registered to vote       
        else:
            msg= "*ID = " + str(r.json()[0]['id']) + "* | " + r.json()[0]['name']
            if r.json()[0]['end_date'] == None and r.json()[0]['start_date'] != None:
                msg+= " | *(ACTIVE)*\n"
            elif r.json()[0]['start_date'] == None:
                msg+= " | *(NOT STARTED)*\n"
            else:
                msg+= " | *(FINISHED)*\n"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text("Sorry, I can't let you access this voting since you are not registered to vote")

    #If id introduced doesn't correspond to any voting_id in decide system        
    else:
        update.message.reply_text("Sorry, It seems like the voting doesn't exist in Decide Locaste system")
        update.message.reply_text("Check the id introduced or contact with the admin")
    
    update.message.reply_text("What are we doing next " + user_data['username'] + "?",
    reply_markup=markup_logged)

    return CHOOSING_LOGGED

def option_voted(bot, update, user_data):
    options_dict = user_data['options_dict']
    if(update.message.text in list(options_dict.keys())):
        update.message.reply_text("You have voted option: " + update.message.text + ". " + options_dict[update.message.text], reply_markup=markup_quit)
        #Here encrypt the vote
        vote_number_for_decide = int(update.message.text)
        vote_number_for_decide += 1
        import elgamal
        tupla = (user_data['pub_key']['p'],user_data['pub_key']['g'],user_data['pub_key']['y'])
        key = elgamal.construct(tupla)
        import random
        cifrado = key.encrypt(vote_number_for_decide, random.getrandbits(256))
        url = "https://locaste-decide.herokuapp.com/store/"
        #url = "http://localhost:8000/store/"
        r = requests.post(url, auth=(user_data['username'], user_data['password']), json={'voting': user_data['voting_id'], 'voter': user_data['user_id'],'vote': {'a':str(cifrado[0]), 'b':str(cifrado[1])} })
        if r.status_code == 200:
            update.message.reply_text("Congratulations! The vote was send to decide system succesfully")
            update.message.reply_text("Remember that you can modify your vote until the voting is finished by his owner")
            
        else:
            update.message.reply_text("Oops something went wrong. Try it again later")
        update.message.reply_text("What are we doing next " + user_data['username'] + "?",
                reply_markup=markup_logged)

        return CHOOSING_LOGGED
    else:
        update.message.reply_text("There is no option " + update.message.text + " in the possible options")

def cancel_vote(bot, update, user_data):
    update.message.reply_text("Ok, vote cancelled")
    update.message.reply_text("What are we doing next " + user_data['username'] + "?",
    reply_markup=markup_logged)
    
    return CHOOSING_LOGGED

def show_all_votings(bot, update, user_data):
    update.message.reply_text("Showing all votings stored in Decide Locaste system...")

    url = "https://locaste-decide.herokuapp.com/voting/"
    #url = "http://localhost:8000/voting/"
    r = requests.get(url)
    if len(r.json()) != 0:
        msg=""
        for voting in r.json():
            msg+= "*ID = " + str(voting['id']) + "* | " + voting['name']
            if voting['end_date'] == None and voting['start_date'] != None:
                msg+= " | *(ACTIVE)*\n"
            elif voting['start_date'] == None:
                msg+= " | *(NOT STARTED)*\n"
            else:
                msg+= " | *(FINISHED)*\n"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Whoa")
        update.message.reply_text("There are no votings stored in Decide Locaste yet")
    
    update.message.reply_text("What are we doing next " + user_data['username'] + "?",
    reply_markup=markup_logged)

    return CHOOSING_LOGGED

def introduce_voting_id_register_census(bot, update, user_data):
    update.message.reply_text('You must provide me the voting id in which you want to register', reply_markup=markup_quit)
    update.message.reply_text('Remember that finished votings are not accepting additional votes')
    update.message.reply_text('Introduce the voting id please',
        reply_markup=markup_cancel)

    return TYPING_VOTING_ID_CENSUS

def register_census(bot, update, user_data):
    id = update.message.text
    if(id == 'Cancel'):
        update.message.reply_text("Aborting...")
        update.message.reply_text("What are we doing next " + user_data['username'] + "?",
            reply_markup=markup_logged)
        return CHOOSING_LOGGED

    url = "https://locaste-decide.herokuapp.com/voting/?id="+id
    #url = "http://localhost:8000/voting/?id="+id
    r = requests.get(url,auth=(user_data['username'], user_data['password']))
    #Check if voting exists or not
    if r.json() != []:
        msg= "*ID = " + str(r.json()[0]['id']) + "* | " + r.json()[0]['name']
        if r.json()[0]['end_date'] == None and r.json()[0]['start_date'] != None:
            msg+= " | *(ACTIVE)*\n"
        elif r.json()[0]['start_date'] == None:
            msg+= " | *(NOT STARTED)*\n"
        else:
            msg+= " | *(FINISHED)*\n"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        #Check first if voting is finished or not
        if(r.json()[0]['end_date'] == None):
            #Then check if the user is registered to vote in this voting, that's has a census object
            url = "https://locaste-decide.herokuapp.com/census/?voter_id="+str(user_data['user_id'])
            #url = "http://localhost:8000/census/?voter_id="+str(user_data['user_id'])
            r2 = requests.get(url,auth=(user_data['username'], user_data['password']))
            #if the user is registered to vote
            if int(id) in r2.json()['voting']:
                update.message.reply_text('You are already registered in this voting census!')

            #if the user is not registered to vote       
            else:
                #Register in census
                url = "https://locaste-decide.herokuapp.com/census/"
                #url = "http://localhost:8000/census/"
                r3 = requests.post(url, auth=(user_data['username'], user_data['password']), json={'voting_id' : id, 'voters' : [user_data['user_id']]})
                if(r3.status_code == 201):
                    update.message.reply_text('Registered in census successfully!')
                    update.message.reply_text('You can access to the voting now')
                elif(r3.status_code == 400):
                    update.message.reply_text('Sorry you are not allowed to register in this voting census because:')
                    msg = r3.json().split("'")
                    update.message.reply_text(msg[1])
                elif(r3.status_code == 403):
                    update.message.reply_text('Sorry you are not allowed to register in this voting census because:')
                    update.message.reply_text('This voting is private and you are not a staff member')
                else:
                    update.message.reply_text('There was a problem try it again later please')
        else:
            update.message.reply_text('Too late...')
            update.message.reply_text('This voting is already finished')

    #If id introduced doesn't correspond to any voting_id in decide system        
    else:
        update.message.reply_text("Sorry, It seems like the voting doesn't exist in Decide Locaste system")
        update.message.reply_text("Check the id introduced or contact with the admin")
    
    update.message.reply_text("What are we doing next " + user_data['username'] + "?",
    reply_markup=markup_logged)

    return CHOOSING_LOGGED



def logout(bot, update, user_data):
    update.message.reply_text('Bye ' + user_data['username'] + ", have a nice day!", reply_markup=markup_quit)
    update.message.reply_text("Don't forget I'm still here, just wake me up by introducing /start if you need me")
    del user_data['username']
    del user_data['password']
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
            CHOOSING_NOT_LOGGED: [RegexHandler('^(Sign\s+up)$',introduce_username_signup),
                        RegexHandler('^(Log\s+in|Try\s+again)$',introduce_username),
                        RegexHandler('^Cancel$',cancel),
                        ],

            CHOOSING_LOGGED: [RegexHandler('^Log\s+out$',logout, pass_user_data=True),
                        RegexHandler('^Access\s+to\s+a\s+voting$',introduce_voting_id, pass_user_data=True),
                        RegexHandler("^Show\s+votings\s+in\s+which\s+I'm\s+registered\s+to\s+vote$",get_census_logged_user, pass_user_data=True),
                        RegexHandler("^Show\s+all\s+votings$",show_all_votings, pass_user_data=True),
                        RegexHandler("^Register\s+in\s+a\s+census$",introduce_voting_id_register_census, pass_user_data=True),
                        ],

            OPTION_VOTED: [RegexHandler('^\d+$',option_voted, pass_user_data=True),
                        RegexHandler('^Cancel$',cancel_vote, pass_user_data=True),
                        ],

            TYPING_USERNAME: [MessageHandler(Filters.text,introduce_password,pass_user_data=True),
                           ],

            TYPING_PASSWORD: [MessageHandler(Filters.text, login, pass_user_data=True),
                           ],

            TYPING_USERNAME_SIGNUP: [MessageHandler(Filters.text,introduce_password_signup,pass_user_data=True),
                           ],

            TYPING_PASSWORD_SINGUP: [MessageHandler(Filters.text, introduce_confirmation_password_signup, pass_user_data=True),
                           ],

            TYPING_CONFIRMATION_PASSWORD_SINGUP: [MessageHandler(Filters.text,introduce_birthdate,pass_user_data=True),
                           ],

            TYPING_BIRTHDATE_SIGNUP: [MessageHandler(Filters.text, introduce_gender_signup, pass_user_data=True),
                           ],
            
            TYPING_GENDER_SINGUP: [MessageHandler(Filters.text,signup,pass_user_data=True),
                           ],

            TYPING_VOTING_ID: [MessageHandler(Filters.text, get_voting, pass_user_data=True),
                           ],
            
            TYPING_VOTING_ID_CENSUS: [MessageHandler(Filters.text, register_census, pass_user_data=True),
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