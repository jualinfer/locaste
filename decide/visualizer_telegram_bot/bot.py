#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler
import logging
import sys
import requests
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.io as pio
from PIL import Image
from io import BytesIO



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
    update.message.reply_text('/start       , obtain a greeting message\n\n'+
                                '/id       , obtain the ids of the voting created  \n\n'+
                                '/info     , obtain all the information regarding the votation, ie. /info 1\n\n'+
                                '/title voting_id      , obtain the title of the voting_id provided, ie. /title 1\n\n'+
                                '/date voting_id       , obtain the end date of the voting_id provided, ie. /date 1\n\n'+
                                '/options voting_id       , obtain the options of the voting_id provided, ie. /options 1\n\n'+
                                '/result voting_id      , obtain the result of the voting_id provided, ie. /result 1\n\n'+
                                '/login       , log in with your Decide credentials\n\n'+
                                '/logout      , log out with your Decide credentials')

#returns every votings id created
def id(bot, update):

    url = baseURL + "/voting/?id="
    r = requests.get(url).json()

    if r != []:
        cantidad = len(r)
        lista = []
        for i in range(cantidad):
            voting_id = r[i]['id']
            lista.append(voting_id)
            update.message.reply_text('The name associated to the id ' + str(voting_id) + ' is: ' + r[i]['name'] )
        update.message.reply_text('The created ids are: ' + str(lista))
    else:
        update.message.reply_text('Ohh, it looks like there are no votings-id created \n')

#Obtain all the info regarding a voting
def info(bot, update):
    received_voting_id = update.message.text
    voting_id = received_voting_id.split(' ')[1]
    update.message.reply_text('You are looking for voting_id: ' + voting_id)

    url = baseURL + "/voting/?id="+voting_id
    r = requests.get(url).json()
    present = datetime.now()

    if r != []:
        update.message.reply_text('The title for the voting_id' + voting_id + ' is: ' + r[0]['name'])
        update.message.reply_text('The description is: ' + r[0]['desc'])
        if r[0]['start_date'] != None:
            startdate = r[0]['start_date']
            startdDate = datetime.strptime(startdate, '%Y-%m-%dT%H:%M:%S.%fZ')
            update.message.reply_text('The start date for the voting_id' + voting_id + ' is: ' + str(startdDate))
        if r[0]['end_date'] != None:
            enddate = r[0]['end_date']
            enddDate = datetime.strptime(enddate, '%Y-%m-%dT%H:%M:%S.%fZ')
            update.message.reply_text('The end date for the voting_id' + voting_id + ' is: ' + str(enddDate))
            if(enddDate<present):
                update.message.reply_text('The voting is closed')
        else:
            update.message.reply_text('The voting is NOT closed yet')

        for option in r[0]['question']['options']:
            update.message.reply_text('The options for the voting_id' + voting_id + ' are: ' + str(option['option']))
        
    else:
        update.message.reply_text('Ohh, it looks like the provided voting_id was invalid \n' +
        'Please try a new search with a different voting_id')

# Voting title, end date and description function
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
        update.message.reply_text('Ohh, it looks like the provided voting_id was invalid \n' +
        'Please try a new search with a different voting_id')
  
def end_date(bot, update):
    received_voting_id = update.message.text
    voting_id = received_voting_id.split(' ')[1]
    update.message.reply_text('You are looking for voting_id: ' + voting_id)

    url = baseURL + "/voting/?id="+voting_id
    r = requests.get(url).json()
    #ts = time.time()
    #date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    present = datetime.now()
    if r != []:
        if r[0]['end_date'] != None:
            enddate = r[0]['end_date']
            enddDate = datetime.strptime(enddate, '%Y-%m-%dT%H:%M:%S.%fZ')
            update.message.reply_text('The end date for the voting_id' + voting_id + ' is: ' + str(enddDate))
        #update.message.reply_text('Actual date is: ' + date)
            if(enddDate<present):
                update.message.reply_text('The voting is closed')
        else:
            update.message.reply_text('The voting is NOT closed yet')
    else:
        update.message.reply_text('Ohh, it looks like the provided voting_id was invalid \n' +
        'Please try a new search with a different voting_id')

def options(bot, update):
    received_voting_id = update.message.text
    voting_id = received_voting_id.split(' ')[1]
    update.message.reply_text('You are looking for voting_id: ' + voting_id)

    url = baseURL + "/voting/?id="+voting_id
    r = requests.get(url).json()
    if r != []:
        for option in r[0]['question']['options']:
            update.message.reply_text('The options for the voting_id' + voting_id + ' are: ' + str(option['option']))
    else:
        update.message.reply_text('Ohh, it looks like the provided voting_id was invalid \n' +
        'Please try a new search with a different voting_id')

# Voting result function
def result(bot, update):
    parsedDate = ''
    received_voting_id = update.message.text
    voting_id = received_voting_id.split(' ')[1]
    update.message.reply_text('You are looking for voting_id: ' + voting_id)

    url = baseURL + "/voting/?id="+voting_id
    r = requests.get(url).json()
    if r != []:
        present = datetime.now()
        endDate = r[0]['end_date']
        if(r[0]['end_date'] != None and r[0]['end_date'] != ''):
            parsedDate = datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S.%fZ')
        if(parsedDate == '' or parsedDate>present):
            update.message.reply_text('This voting is still open! Please use the /date command to know when it ends')
        else:
            if r[0]['postproc'] != None and r[0]['postproc'] != []:
                for item in r[0]['postproc']:
                    update.message.reply_text('Option: '+item['option']+'\n'+
                    'Votes: '+str(item['votes']), quote = False)
                
                tally = str(r[0]['tally'])
                tally_number = tally.split('[')[1].split(']')[0]
                update.message.reply_text('Final tally: '+tally_number, quote = False)

                # Sending results images from server
                x = []
                y = []

                # Generate data for bars and pie
                for item in r[0]['postproc']:
                    x.append(item['option'])
                    y.append(item['postproc'])
           
                dataBars = [go.Bar(x = x, y = y)]
                dataPie  = [go.Pie(labels = x, values = y)]

                # Establish layout
                layout = go.Layout(title = 'Result of voting after being processed')

                # Create bar figure
                fig = go.Figure(data= dataBars, layout = layout)
                img_bytes = pio.to_image(fig, format='jpeg')
                bars = Image.open(BytesIO(img_bytes))
            
                buf = BytesIO()
                buf.name = 'bar.jpeg'
                bars.save(buf, 'JPEG')
                buf.seek(0)

                # Create pie figure
                fig = go.Figure(data= dataPie, layout = layout)
                img_bytes = pio.to_image(fig, format='jpeg')
                pie = Image.open(BytesIO(img_bytes))
            
                buf1 = BytesIO()
                buf1.name = 'pie.jpeg'
                pie.save(buf1, 'JPEG')
                buf1.seek(0)

                # Send figures
                update.message.reply_photo(buf, quote = False)
                update.message.reply_photo(buf1, quote = False)

                # Cleaning
                buf.close()
                buf1.close()
                bars.close()
                pie.close()
            else:
                update.message.reply_text('This voting is being processed. Please retry later')
    else:
        update.message.reply_text('Ohh, it looks like the provided voting_id was invalid \n' +
        'Please try a new search with a different voting_id')

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
    dispatcher.add_handler(CommandHandler('id', id))
    dispatcher.add_handler(CommandHandler('info', info))
    dispatcher.add_handler(CommandHandler('title', title_desc))
    dispatcher.add_handler(CommandHandler('date', end_date))
    dispatcher.add_handler(CommandHandler('options', options))
    dispatcher.add_handler(CommandHandler('result', result))
    dispatcher.add_handler(CommandHandler('login', login))
    dispatcher.add_handler(CommandHandler('logout', logout))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()