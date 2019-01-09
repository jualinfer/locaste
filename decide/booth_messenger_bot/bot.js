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


const bot = new BootBot({
  accessToken: process.env.ACCESS_TOKEN,
  verifyToken: process.env.VERIFY_TOKEN,
  appSecret: process.env.APP_SECRET
})


bot.setGreetingText("Hello, I'm Decide-Locaste-Booth Bot. I'm here to help you vote with Decide. Click on the 'Get Started' button to begin.")


bot.setGetStartedButton((payload, chat) => {
  chat.getUserProfile().then((user) => {
    const welcome1 = `Hello ${user.first_name} !`;
    const welcome2 = `I'm Decide-Locaste-Booth Bot, the Facebook Messenger virtual assistant for Decide.`;
    const welcome3 = {
      text: 'In order to vote, first you need to log in with your Decide username and password.',
      buttons: [
        { type: 'postback', title: 'Log in', payload: 'BOT_LOG_IN' },
        { type: 'postback', title: 'Cancel', payload: 'BOT_CANCEL' }
      ]
    };
    const options = { typing: true };
    chat.say([welcome1, welcome2, welcome3], options);
  });
});






bot.start()