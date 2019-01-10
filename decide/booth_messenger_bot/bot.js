const express = require('express')
const bodyParser = require('body-parser')
const request = require('request')
const app = express()
const BootBot = require('bootbot')
require('dotenv').config()


app.set('port', (process.env.PORT || 5000))
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())


app.get('/', function (req, res) {
  res.send("This is a Facebook Messenger Bot for Decide.")
})


app.get('/webhook/', function (req, res) {
  if (req.query['hub.verify_token'] === process.env.VERIFY_TOKEN) {
    return res.send(req.query['hub.challenge'])
  }
  res.send('wrong token')
})

app.listen(app.get('port'), function () {
  console.log('Started on port', app.get('port'))
})

var config = {};

const bot = new BootBot({
  accessToken: process.env.ACCESS_TOKEN,
  verifyToken: process.env.VERIFY_TOKEN,
  appSecret: process.env.APP_SECRET
})


bot.setGreetingText("Hello, I'm Decide-Locaste-Booth Bot. I'm here to help you vote with Decide. Click on the 'Get Started' button to begin.")

bot.setPersistentMenu([
{ type: 'postback', title: 'Log in', payload: 'BOT_LOG_IN' },
{ type: 'web_url', url: "https://github.com/wadobo/decide/wiki/Como-funciona-Decide", title: "Info" },
{ type: 'postback', title: 'HELP', payload: 'BOT_HELP' }
]);

bot.setGetStartedButton((payload, chat) => {
  chat.getUserProfile().then((user) => {
    const welcome1 = `Hello ${user.first_name} !`;
    const welcome2 = `I'm Decide-Locaste-Booth Bot, the Facebook Messenger virtual assistant for Decide.`;
    const welcome3 = {
      text: 'In order to vote, first you need to log in with your Decide username and password.',
      buttons: [
        { type: 'postback', title: 'Log in', payload: 'BOT_LOG_IN' },
        { type: 'postback', title: 'Cancel', payload: 'BOT_HELP' }
      ]
    };
    const options = { typing: true };
    chat.say([welcome1, welcome2, welcome3], options);
  });
});

bot.on('postback:BOT_LOG_IN', (payload, chat) => {
  const options = { typing: true };
  if (config.login === true) {
    chat.say("You're already logged in.", options);
  } else {
    const askUsername = (convo) => {
      const question = "Please, introduce your username.";

      const answer = (payload, convo) => {
        const username = payload.message.text;
        convo.set('username', username);
        convo.say(`Got it!`, options).then(() => askPassword(convo));
      };

      convo.ask(question, answer, options);
    };

    const askPassword = (convo) => {
      const question = "Now introduce your password.";


      const answer = (payload, convo) => {
        const password = payload.message.text;
        convo.set('password', password);
        convo.say(`Ok!`, options);

        let requestBody = {
          "username": convo.get('username'),
          "password": convo.get('password')
        };

        request.post(
          'http://localhost:8000/rest-auth/login/',
          { json: requestBody },
          function (error, response, body) {
            if (!error && response.statusCode == 200) {
              convo.getUserProfile().then((user) => {
                const loginMessage1 = `Well done, ${user.first_name} !`;
                const loginMessage2 = 'You have logged in successfully as ' + convo.get('username') + '!';
                const loginMessage3 = {
                  text: 'What would you want to do now?',
                  buttons: [
                    { type: 'postback', title: 'Access to a voting', payload: 'BOT_GET_VOTING' },
                    { type: 'postback', title: 'Log out', payload: 'BOT_LOG_OUT' }
                  ]
                };
                convo.say([loginMessage1, loginMessage2, loginMessage3], options).then(() => convo.end());
              });
              config.login = true;
              config.token = body.key;
            } else {
              convo.say(`Ooops! Something went wrong.`, options);
              const errorMessage = {
                text: 'Please, make sure you typed your username and password correctly.',
                buttons: [
                  { type: 'postback', title: 'Try again', payload: 'BOT_LOG_IN' },
                  { type: 'postback', title: 'Help', payload: 'BOT_HELP' }
                ]
              };
              convo.say(errorMessage, options).then(() => convo.end());
            }
          }
        );

      };

      convo.ask(question, answer, options);
    };

    const message = `Perfect!`;
    chat.say(message, options)
      .then(() => chat.conversation((convo) => {
        askUsername(convo);
      }));
  }
});

bot.on('postback:BOT_CANCEL', (payload, chat) => {
  const options = { typing: true };
  const message1 = "If you need me again you can call me by typing 'Get Started'.";
  const message2 = "Bye!";
  chat.say([message1, message2], options);
});


bot.start()