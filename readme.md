Guide to the Slack application:

1. Download Slack from Android/Apple Store or Visit https://slack.com/ from a browser.
2. Click on Sign in.
3. Enter bristolstudents.slack.com as the workspace's Slack URL. (Just type in bristolstudents in the textbox on the page/app).
4. Use the below mentioned dummy Slack credentials to login into the channel and use the application:
    username: bookstudy2019@gmail.com
    password: cloud@2019
5. After sign in, go to Apps hosted in Slack (bottom of the left panel in the Slack app/web-page). Find book_study_room in the apps section.
6. Click on book_study_room app and follow the below instructions to start a text-based chat with the bot.

#####
Slack credentials:
Use the dummy credentials provided below to login into the channel and use the application

username: bookstudy2019@gmail.com
password: cloud@2019

#####

Instructions for booking the room through Slack as well as API endpoint:
Kindly use the following example chat phrases with the book study room bot in order to help us with the testing:
.
Sample Data:
1. Locations : queens, senate house, merchant ventures, hawthorns
2. Sessions: session one , session two

Sample Utterances:
1. Book a room near queens for session one
2. Book a room for session two near senate house
3. Session one at queens
4. Hawthorns for session two

To test the application for load testing etc:

1. API Endpoint: https://tim57d9gge.execute-api.us-east-1.amazonaws.com/external_test/
2. Example JSON payload:
{
  "currentIntent": {
    "name": "BookStudyRoom",
    "slots": {
      "roomLocation": "senate house",
      "sessions": "session one"
    }
  },
  "sessionAttributes": {},
  "invocationSource": "DialogCodeHook"
}

The roomLocation and sessions can be any of the specified locations and session types as mentioned above.

If load testing with locust, use the locustfile in this repository and run with the following:
locust --host=https://tim57d9gge.execute-api.us-east-1.amazonaws.com
