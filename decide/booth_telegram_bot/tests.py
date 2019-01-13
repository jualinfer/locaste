from telethon import TelegramClient, sync

api_id = 627128
api_hash = 'b5033c8a72cf750833eeb12dced27266'

client = TelegramClient('testBot', api_id, api_hash).start()
bot = client.get_entity('DecideLocasteBoothBot')

print("Running test suite...")
import random
intrandom = random.randint(1,100000000000)
username = "testing_booth_telegram" + str(intrandom)
with client.conversation(bot) as conv:
    conv.send_message('/start') 
    welcome = conv.get_response().raw_text 
    assert welcome == "Welcome!", "Missing Welcome message"
    explanation = conv.get_response().raw_text
    assert explanation == "I'm DecideLocasteBoothBot, the Telegram virtual booth assistant for Decide Locaste", "Missing bot explanation message"
    first = conv.get_response()
    assert first.raw_text == "First of all, you need to sign up or to log in with your Decide Locaste credentials in order to access your votings", "Missing sign up or login message"
    assert first.reply_markup != None, "Not showing actions buttons with Sign up, Log in and Cancel"

    conv.send_message('Mensaje fuera de lo esperado') 
    catchall = conv.get_response().raw_text
    assert catchall == "Sorry It seems like I can not understand your petition", "Missing catch all message"

    conv.send_message('Sign up')
    work = conv.get_response().raw_text
    assert work == "Let's get to work", "Missing Let's get to work message"
    introduce_username_signup = conv.get_response().raw_text
    assert introduce_username_signup == "Introduce an username, please", "Missing introduce username message"

    conv.send_message('Cancel Sign up')
    aborting = conv.get_response().raw_text
    assert aborting == "Aborting sign up...", "Missing aborting message"
    now = conv.get_response().raw_text
    assert now == "What are we doing now?", "Missing what are we doing now message"
    
    conv.send_message('Sign up')
    work = conv.get_response().raw_text
    assert work == "Let's get to work", "Missing Let's get to work message"
    introduce_username_signup = conv.get_response().raw_text
    assert introduce_username_signup == "Introduce an username, please", "Missing introduce username message"

    conv.send_message(username)
    introduce_password_signup = conv.get_response().raw_text
    assert introduce_password_signup == "Introduce your password", "Missing introduce password message"

    conv.send_message('low')
    lowpassword = conv.get_response().raw_text
    assert lowpassword == "The password must contain at least 8 digits", "Missing password with at least 8 digits message"
    introduce_password_signup_again = conv.get_response().raw_text
    assert introduce_password_signup_again == "Introduce your password again", "Missing introduce password again message"

    conv.send_message('12345678')
    numericpassword = conv.get_response().raw_text
    assert numericpassword == "The password can't be entirely numeric", "Missing password not entirely numeric message"
    introduce_password_signup_again = conv.get_response().raw_text
    assert introduce_password_signup_again == "Introduce your password again", "Missing introduce password again message"

    conv.send_message('asdfghjk')
    simplepassword = conv.get_response().raw_text
    assert simplepassword == "The password is too common", "Missing too common password message"
    introduce_password_signup_again = conv.get_response().raw_text
    assert introduce_password_signup_again == "Introduce your password again", "Missing introduce password again message"

    conv.send_message('contraseña')
    confirmpassword = conv.get_response().raw_text
    assert confirmpassword == "Confirm your password again", "Missing confirm password message"

    conv.send_message('distinta')
    notmatchingpassword = conv.get_response().raw_text
    assert notmatchingpassword == "Confirmation doesn't match password", "Missing not matching password message"
    checkit = conv.get_response().raw_text
    assert checkit == "Check it", "Missing check it message"
    introduce_password_signup_again = conv.get_response().raw_text
    assert introduce_password_signup_again == "Introduce your password again", "Missing introduce password again message"

    conv.send_message('contraseña')
    confirmpassword = conv.get_response().raw_text
    assert confirmpassword == "Confirm your password again", "Missing confirm password message"

    conv.send_message('contraseña')
    birthdate = conv.get_response().raw_text
    assert birthdate == "Introduce your birthdate in the following format: yyyy-mm-dd", "Missing introduce birthdate message"

    conv.send_message('asdf')
    notmatchingbirthdate = conv.get_response().raw_text
    assert notmatchingbirthdate == "The birthdate introduced doesn't follow the restricted format", "Missing not matching birthdate message"
    checkit = conv.get_response().raw_text
    assert checkit == "Check it", "Missing check it message"
    introduce_birthdate_signup_again = conv.get_response().raw_text
    assert introduce_birthdate_signup_again == "Introduce your birthdate again", "Missing introduce birthdate again message"

    conv.send_message('2045-09-19')
    futurebirthdate = conv.get_response().raw_text
    assert futurebirthdate == "You can't be born in the future!!", "Missing future birthdate message"
    checkit = conv.get_response().raw_text
    assert checkit == "Check it", "Missing check it message"
    introduce_birthdate_signup_again = conv.get_response().raw_text
    assert introduce_birthdate_signup_again == "Introduce your birthdate again", "Missing introduce birthdate again message"

    conv.send_message('2004-09-19')
    introduce_gender = conv.get_response().raw_text
    assert introduce_gender == "Introduce your gender with the menu options", "Missing introduce gender message"

    conv.send_message('asdf')
    notmatchinggender = conv.get_response().raw_text
    assert notmatchinggender == "The gender introduced doesn't follow the restricted format", "Missing not matching gender message"
    checkit = conv.get_response().raw_text
    assert checkit == "Check it", "Missing check it message"
    introduce_gender_signup_again = conv.get_response().raw_text
    assert introduce_gender_signup_again == "Introduce your gender again", "Missing introduce gender again message"

    conv.send_message('Male')
    success = conv.get_response().raw_text
    assert success == "Sign up performed succesfully!", "Missing success message"
    cantry = conv.get_response().raw_text
    assert cantry == "You can try to log in with the created credentials now", "Missing try with credentials message"
    
    conv.send_message('Cancel')
    success = conv.get_response().raw_text
    success = conv.get_response().raw_text

import time
time.sleep(10)
with client.conversation(bot) as conv:
    conv.send_message('/start') 
    welcome = conv.get_response().raw_text 
    assert welcome == "Welcome!", "Missing Welcome message"
    explanation = conv.get_response().raw_text
    assert explanation == "I'm DecideLocasteBoothBot, the Telegram virtual booth assistant for Decide Locaste", "Missing bot explanation message"
    first = conv.get_response()
    assert first.raw_text == "First of all, you need to sign up or to log in with your Decide Locaste credentials in order to access your votings", "Missing sign up or login message"
    assert first.reply_markup != None, "Not showing actions buttons with Sign up, Log in and Cancel"

    conv.send_message('Log in')
    good = conv.get_response().raw_text
    assert good == "Good choice!", "Missing good choice message"
    introduce_username_login = conv.get_response().raw_text
    assert introduce_username_login == "Introduce your username, please", "Missing introduce username login message"

    conv.send_message('noexistosegurisimoqueno')
    gotit = conv.get_response().raw_text
    assert gotit == "Got it", "Missing got it message"
    introduce_password_login = conv.get_response().raw_text
    assert introduce_password_login == "Now, introduce your password", "Missing introduce password login message"

    conv.send_message('contraseña')
    oops = conv.get_response().raw_text
    assert oops == "Oops, something went wrong", "Missing oops message"
    check = conv.get_response().raw_text
    assert check == "Check your credentials and try it again", "Missing check credentials message"

    conv.send_message('Try again')
    good = conv.get_response().raw_text
    assert good == "Good choice!", "Missing good choice message"
    introduce_username_login = conv.get_response().raw_text
    assert introduce_username_login == "Introduce your username, please", "Missing introduce username login message"

    conv.send_message(username)
    gotit = conv.get_response().raw_text
    assert gotit == "Got it", "Missing got it message"
    introduce_password_login = conv.get_response().raw_text
    assert introduce_password_login == "Now, introduce your password", "Missing introduce password login message"

    conv.send_message('contraseña')
    great = conv.get_response().raw_text
    assert great == "Great!", "Missing great message"
    success = conv.get_response().raw_text
    assert success == "Logged succesfully", "Missing success login message"
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Show votings in which I'm registered to vote")
    ok = conv.get_response().raw_text
    assert ok == "Ok", "Missing ok message"
    sorry = conv.get_response().raw_text
    assert sorry == "Sorry... It seems like you are not registered in any census yet", "Missing not registered in any census yet message"
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Show all votings")
    showing = conv.get_response().raw_text
    assert showing == "Showing all votings stored in Decide Locaste system...", "Missing showing all message"
    all = conv.get_response().raw_text
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Access to a voting")
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "Please "+username+", introduce the voting id you want to access in", "Missing introduce voting id message"

    conv.send_message("asdf")
    gotit = conv.get_response().raw_text
    assert gotit == "Got it", "Missing got it message"
    search = conv.get_response().raw_text
    assert search == "Let's search for the voting...", "Missing search message"
    sorry = conv.get_response().raw_text
    assert sorry == "Sorry, It seems like the voting doesn't exist in Decide Locaste system", "Missing voting not exists message"
    check = conv.get_response().raw_text
    assert check == "Check the id introduced or contact with the admin", "Missing check voting id introduced message"
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Access to a voting")
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "Please "+username+", introduce the voting id you want to access in", "Missing introduce voting id message"
    
    conv.send_message("3")
    gotit = conv.get_response().raw_text
    assert gotit == "Got it", "Missing got it message"
    search = conv.get_response().raw_text
    assert search == "Let's search for the voting...", "Missing search message"
    title = conv.get_response().raw_text
    sorry = conv.get_response().raw_text
    assert sorry == "Sorry, I can't let you access this voting since you are not registered to vote", "Missing cant access message"
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Register in a census")
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "You must provide me the voting id in which you want to register", "Missing introduce voting id message"
    remember = conv.get_response().raw_text
    assert remember == "Remember that finished votings are not accepting additional votes", "Missing remember message"
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "Introduce the voting id please", "Missing introduce voting id message"

    conv.send_message("6")
    title = conv.get_response().raw_text
    sorry = conv.get_response().raw_text
    assert sorry == "Sorry you are not allowed to register in this voting census because:", "Missing sorry message"
    why = conv.get_response().raw_text
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Register in a census")
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "You must provide me the voting id in which you want to register", "Missing introduce voting id message"
    remember = conv.get_response().raw_text
    assert remember == "Remember that finished votings are not accepting additional votes", "Missing remember message"
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "Introduce the voting id please", "Missing introduce voting id message"

    conv.send_message("5")
    title = conv.get_response().raw_text
    sorry = conv.get_response().raw_text
    assert sorry == "Sorry you are not allowed to register in this voting census because:", "Missing sorry message"
    why = conv.get_response().raw_text
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Register in a census")
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "You must provide me the voting id in which you want to register", "Missing introduce voting id message"
    remember = conv.get_response().raw_text
    assert remember == "Remember that finished votings are not accepting additional votes", "Missing remember message"
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "Introduce the voting id please", "Missing introduce voting id message"

    conv.send_message("3")
    title = conv.get_response().raw_text
    success = conv.get_response().raw_text
    assert success == "Registered in census successfully!", "Missing success message"
    can = conv.get_response().raw_text
    assert can == "You can access to the voting now", "Missing you can access message"
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Register in a census")
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "You must provide me the voting id in which you want to register", "Missing introduce voting id message"
    remember = conv.get_response().raw_text
    assert remember == "Remember that finished votings are not accepting additional votes", "Missing remember message"
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "Introduce the voting id please", "Missing introduce voting id message"

    conv.send_message("3")
    title = conv.get_response().raw_text
    already = conv.get_response().raw_text
    assert already == "You are already registered in this voting census!", "Missing already message"
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Register in a census")
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "You must provide me the voting id in which you want to register", "Missing introduce voting id message"
    remember = conv.get_response().raw_text
    assert remember == "Remember that finished votings are not accepting additional votes", "Missing remember message"
    introduce_voting = conv.get_response().raw_text
    assert introduce_voting == "Introduce the voting id please", "Missing introduce voting id message"
    
    conv.send_message("2")
    title = conv.get_response().raw_text
    late = conv.get_response().raw_text
    assert late == "Too late...", "Missing late message"
    finished = conv.get_response().raw_text
    assert finished == "This voting is already finished", "Missing finished message"
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"

    conv.send_message("Access to a voting")
    access = conv.get_response().raw_text
    assert access == "Please "+username+", introduce the voting id you want to access in", "Missing access message"

    conv.send_message("3")
    gotit = conv.get_response().raw_text
    assert gotit == "Got it", "Missing got it message"
    search = conv.get_response().raw_text
    assert search == "Let's search for the voting...", "Missing search message"
    here = conv.get_response().raw_text
    assert here == "Here It is:", "Missing here message"
    voting = conv.get_response().raw_text
    question = conv.get_response().raw_text
    assert question == "What option are you voting, "+username+"?", "Missing what option are you voting message"
    
    conv.send_message("1")
    voted = conv.get_response().raw_text
    assert voted == "You have voted option: 1. opción 1", "Missing voted message"
    congratulations = conv.get_response().raw_text
    assert congratulations == "Congratulations! The vote was send to decide system succesfully", "Missing congratulations message"
    remember = conv.get_response().raw_text
    assert remember == "Remember that you can modify your vote until the voting is finished by his owner", "Missing remember message"
    wnext = conv.get_response().raw_text
    assert wnext == "What are we doing next "+username+"?", "Missing what are we doing next message"
    
    conv.send_message('Log out')
    bye = conv.get_response().raw_text
    assert bye == "Bye "+username+", have a nice day!", "Missing bye message"
    remember = conv.get_response().raw_text
    assert remember == "Don't forget I'm still here, just wake me up by introducing /start if you need me", "Missing remember message"

    print("-------------------------------------------")
    print("Test suite completed successfully!")
    print("DecideLocasteBoothBot works completely as expected")

