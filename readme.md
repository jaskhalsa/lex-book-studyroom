Guide to the application:

Slack credentials:
Use the dummy credentials provided below to login into the channel and use the application

username: bookstudy2019@gmail.com
password: cloud@2019

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

1. API Endpoint: https://tim57d9gge.execute-api.us-east-1.amazonaws.com
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

roomLocation and sessions can be any of the specified locations and session types as mentioned above.

If load testing with locust, use the locustfile in this repository and run with the following:
locust --host=https://tim57d9gge.execute-api.us-east-1.amazonaws.com
