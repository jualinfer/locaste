const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const app = express();
const BootBot = require('bootbot');
const axios = require('axios');


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

bot.deletePersistentMenu();
bot.setGreetingText("Hello, I'm Decide-Locaste-Booth Bot. I'm here to help you vote with Decide. Click on the 'Get Started' button to begin.")


bot.setGetStartedButton((payload, chat) => {
  chat.getUserProfile().then((user) => {
    const welcome1 = `Hello ${user.first_name} !`;
    const welcome2 = `I'm Decide-Locaste-Booth Bot, the Facebook Messenger virtual assistant for Decide.`;
    const welcome3 = {
      text: 'In order to vote, first you need to log in with your Decide username and password.',
      buttons: [
        { type: 'postback', title: 'Log in', payload: 'BOT_LOG_IN' },
        { type: 'postback', title: 'Help', payload: 'BOT_HELP' },
        { type: 'web_url', url: "https://github.com/wadobo/decide/wiki/Como-funciona-Decide", title: "¿Cómo funciona Decide?" }
      ]
    };
    const options = { typing: true };
    chat.say([welcome1, welcome2, welcome3], options);
  });
});


bot.on('postback:BOT_RESTART', (payload, chat) => {
  const options = { typing: true };

  async function restart() {

    async function logout() {
      if (config.login === true) {
        chat.say("Logging out...", options);
        await axios.get('http://localhost:8000/rest-auth/logout/')
          .then((res) => {
            config.login = false;
            config.token = null;
            config.userId = null;
            config.allowedVotings = null;
            config.actualVoting = null;
            chat.say("Logged out successfully!", options);
          })
          .catch((err) => {
            console.log(err.message);
            const errorMessage1 = `An error was produced while logging out...`;
            const errorMessage2 = {
              text: 'Do you want to try again?',
              buttons: [
                { type: 'postback', title: 'Try again', payload: 'BOT_RESTART' },
                { type: 'postback', title: 'Help', payload: 'BOT_HELP' }
              ]
            };
            chat.say([errorMessage1, errorMessage2], options);
          });
      }
    };

    await logout();
    chat.say("Starting a new conversation ...", options);
    chat.getUserProfile().then((user) => {
      const welcome1 = `Hello again ${user.first_name} !`;
      const welcome2 = `I'm Decide-Locaste-Booth Bot, the Facebook Messenger virtual assistant for Decide.`;
      const welcome3 = {
        text: 'In order to vote, first you need to log in with your Decide username and password.',
        buttons: [
          { type: 'postback', title: 'Log in', payload: 'BOT_LOG_IN' },
          { type: 'postback', title: 'Help', payload: 'BOT_HELP' },
          { type: 'web_url', url: "https://github.com/wadobo/decide/wiki/Como-funciona-Decide", title: "¿Cómo funciona Decide?" }
        ]
      };
      const options = { typing: true };
      chat.say([welcome1, welcome2, welcome3], options);
    });

  }
  restart();
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
                    { type: 'postback', title: 'Log out', payload: 'BOT_LOG_OUT' }, 
                    { type: 'postback', title: 'Restart bot', payload: 'BOT_RESTART' }
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



bot.on('postback:BOT_LOG_OUT', (payload, chat) => {
  const options = { typing: true };
  if (config.login === true) {
    request.get('http://localhost:8000/rest-auth/logout/', function (error, response, body) {
      if (!error && response.statusCode == 200) {
        config.login = false;
        config.token = null;
        config.userId = null;
        config.allowedVotings = null;
        config.actualVoting = null;
        chat.getUserProfile().then((user) => {
          const logoutMessage1 = `Logged out successfully!`;
          const logoutMessage2 = `Well, ${user.first_name} , I hope I have been helpful.`;
          const logoutMessage3 = {
            text: 'If you need me again, just let me know!',
            buttons: [
              { type: 'postback', title: 'Restart bot', payload: 'BOT_RESTART' }
            ]
          };
          chat.say([logoutMessage1, logoutMessage2, logoutMessage3], options);
        });
      } else {
        const errorMessage1 = `An error was produced while logging out...`;
        const errorMessage2 = {
          text: 'Do you want to try again?',
          buttons: [
            { type: 'postback', title: 'Try again', payload: 'BOT_LOG_OUT' },
            { type: 'postback', title: 'Help', payload: 'BOT_HELP' }
          ]
        };
        chat.say([errorMessage1, errorMessage2], options);
      }
    });
  } else {
    chat.say("You are not logged in!", options);
  }
});




bot.on('postback:BOT_GET_VOTING', (payload, chat) => {
  const options = { typing: true };
  if (config.login === true) {

    async function getAllowedVotings() {

      if (config.userId === null || config.userId === undefined) {

        await axios.post('http://localhost:8000/authentication/getuser/', { 'token': config.token })
          .then((res) => {
            config.userId = res.data.id;
            return axios.get('http://localhost:8000/census/?voter_id=' + config.userId);
          })
          .then((res) => {
            config.allowedVotings = res.data.voting;
          })
          .catch((err) => {
            console.log(err.message);
          });


      } else {

        await axios.get('http://localhost:8000/census/?voter_id=' + config.userId)
          .then((res) => {
            config.allowedVotings = res.data.voting;
          })
          .catch((err) => {
            console.log(err.message);
          });
      }
    };

    async function conversation() {
      await getAllowedVotings();


      if (config.allowedVotings === undefined || config.allowedVotings === null) {
        const errorMessage1 = `An error was produced while performing this operation...`;
        const errorMessage2 = {
          text: 'Do you want to try again?',
          buttons: [
            { type: 'postback', title: 'Try again', payload: 'BOT_GET_VOTING' },
            { type: 'postback', title: 'Help', payload: 'BOT_HELP' },
            { type: 'postback', title: 'Restart bot', payload: 'BOT_RESTART' }
          ]
        };
        chat.say([errorMessage1, errorMessage2], options);
      } else if (config.allowedVotings.length === 0) {
        const message1 = `I'm sorry. There aren't votings in which you can participate.`;
        const message2 = {
          text: 'What would you want to do now?',
          buttons: [
            { type: 'postback', title: 'Help', payload: 'BOT_HELP' },
            { type: 'postback', title: 'Restart bot', payload: 'BOT_RESTART' }
          ]
        };
        chat.say([message1, message2], options);
      } else {
        const votingsIds = config.allowedVotings.map(String);
        const replies = [];
        const votings = [];
        const activeVotings = [];


        for (i = 0; i < votingsIds.length; i++) {

          await axios.get('http://localhost:8000/voting/?id=' + votingsIds[i].toString())
            .then((res) => {
              var title = res.data[0].name;
              var isActive = (res.data[0].start_date !== null && res.data[0].end_date === null) ? true : false;
              var image = (!isActive) ? "https://http2.mlstatic.com/adventure-kidz-banz-age-2-5-gafas-de-sol-rockin-red-D_NQ_NP_638979-MLM26845819305_022018-O.jpg" :
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHsXY1PIZ4MgKi0XWj0uIOUks9TuP75Lkphk2bNLHNE2leQVF2BQ";

              reply = {
                "content_type": "text",
                "title": title,
                "image_url": image,
                "payload": "BOT_PICK_VOTING_" + votingsIds[i].toString()
              };
              replies.push(reply);

              votings[title] = votingsIds[i];

              if (isActive) {
                activeVotings.push(title);
              }

            })
            .catch((err) => {
              console.log(err.message);
            })
          

        }
        const chooseVoting = (convo) => {


          const question = {
            text: `Here's a list of the votings in which you can participate. The active votings are marked in green, while the inactive are marked in red. Please, choose an active voting!`,
            quickReplies: replies
          };

          const answer = (payload, convo) => {
            const voting = payload.message.text;
            const allVotings = Object.keys(votings);

            if (!allVotings.includes(voting)) {
              const errorMessage1 = `This voting does not exist!!!`;
              const errorMessage2 = {
                text: 'What would you want to do now?',
                buttons: [
                  { type: 'postback', title: 'See the votings again', payload: 'BOT_GET_VOTING' },
                  { type: 'postback', title: 'Help', payload: 'BOT_HELP' },
                  { type: 'postback', title: 'Restart bot', payload: 'BOT_RESTART' }
                ]
              };
              convo.say([errorMessage1, errorMessage2], options);
            } else if (!activeVotings.includes(voting)) {
              const errorMessage1 = `You have chosen an inactive voting.`;
              const errorMessage2 = `I told you not to do that!`;
              const errorMessage3 = {
                text: 'What would you want to do now?',
                buttons: [
                  { type: 'postback', title: 'See the votings again', payload: 'BOT_GET_VOTING' },
                  { type: 'postback', title: 'Help', payload: 'BOT_HELP' },
                  { type: 'postback', title: 'Restart bot', payload: 'BOT_RESTART' }
                ]
              };
              convo.say([errorMessage1, errorMessage2, errorMessage3], options);
            } else {
              convo.set('votingName', voting);
              votingId = votings[convo.get('votingName')];
              convo.set('votingId', votingId);

              convo.say(`Good choice!`, options).then(() => askConfirmation(convo));
            }

          };

          convo.ask(question, answer, options);
        };

        const askConfirmation = (convo) => {

          convo.getUserProfile().then((user) => {
            const question = {
              text: `So ${user.first_name} , do you want to participate in the voting '` + convo.get('votingName') + "'?",
              quickReplies: ["Yes", "No"]
            };


            const answer = (payload, convo) => {
              const reply = payload.message.text;

              if (reply == "Yes" || reply == 'yes' || reply == 'YES') {
                config.actualVoting = convo.get('votingId');
                const message1 = `Ok, ${user.first_name}. `;
                convo.sendButtonTemplate(message1, [
                  { type: 'postback', title: 'Open the voting', payload: 'BOT_OPEN_VOTING' }], options).then(() => convo.end());
              }

              else if (reply == "No" || reply == 'no' || reply == 'NO') {
                const message1 = `Got it.`;
                const message2 = {
                  text: 'What would you want to do now?',
                  buttons: [
                    { type: 'postback', title: 'See the votings again', payload: 'BOT_GET_VOTING' },
                    { type: 'postback', title: 'Restart bot', payload: 'BOT_RESTART' }
                  ]
                };
                convo.say([message1, message2], options).then(() => convo.end());
              } else {
                const message1 = `I didn't understand that.`;
                convo.sendButtonTemplate(message1, [
                  { type: 'postback', title: 'Help', payload: 'BOT_HELP' }], options).then(() => convo.end());
              }

            }

            convo.ask(question, answer, options);
          });
        };


        const message = `Ok`;
        chat.say(message, options)
          .then(() => chat.conversation((convo) => {
            chooseVoting(convo);
          }));

      }

    };
    conversation();
  } else {
    const errorMessage = {
      text: 'You must be logged in in order to access a voting.',
      buttons: [
        { type: 'postback', title: 'Log in', payload: 'BOT_LOG_IN' },
        { type: 'postback', title: 'Help', payload: 'BOT_HELP' }
      ]
    };
    chat.say(errorMessage, options);

  }
});



bot.start()