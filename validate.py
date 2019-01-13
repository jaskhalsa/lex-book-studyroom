import json
import datetime
import time
import os
import dateutil.parser
import logging
import boto3
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
db = boto3.resource('dynamodb')

# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Helper Functions ---


def safe_int(n):
    if n is not None:
        return int(n)
    return n


def try_ex(func):
    try:
        return func()
    except KeyError:
        return None

def isvalid_location(location):
    
    try:
        ## if item attribute exists, the location is valid
        table = db.Table("locations")
        response = table.get_item(
            Key={"location":location}
        )
        item = response['Item']
        return True
        
    except Exception:
        return False
        
sessionOneOptions = ['session one', 'session 1','SESSION 1','Session 1','Session One','SESSION ONE']
sessionTwoOption = ['session two', 'session 2','SESSION 2','Session 2','Session Two','SESSION TWO']


def attempt_booking(session_type, location, room_table, location_table):
    try:
        locationResponse = location_table.get_item(
                Key={"location":location}
            )
        location_item = locationResponse['Item']
        roomNumbers = location_item['roomNumbers']
        print(roomNumbers)
        for i in range(len(roomNumbers)):
            roomResponse = room_table.get_item(
                Key={"roomID":roomNumbers[i]}
            )
            room_item = roomResponse['Item']
            
            if(not room_item[session_type]):
                room_item[session_type] = True
                sessionString = "set {} = :r".format(session_type)
                room_table.update_item(Key={"roomID": roomNumbers[i]},
                    UpdateExpression=sessionString,
                    ExpressionAttributeValues={
                        ':r': True,
                    },
                    ReturnValues="UPDATED_NEW"
                )
                return True
        return False
    except Exception:
        return False

def book_session(sessions, location):
    sessionType = ''
    if (sessions in sessionOneOptions):
        sessionType = 'session1'
    elif(sessions in sessionTwoOption):
        sessionType = 'Session2'
    else:
        return False
    
    locationTable = db.Table("locations")
    roomTable = db.Table("rooms")
    
    return attempt_booking(sessionType, location, roomTable, locationTable)
    
    
    
def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }



def validate_room(location, sessions):
    if location == None or not isvalid_location(location.lower()):
        return build_validation_result(
            False,
            'roomLocation',
            'We currently do not support that building.  Can you try a different building?'
        )
    if sessions == None or not book_session(sessions.lower(), location.lower()):
        return build_validation_result(
            False,
            'sessions',
            'That session is unavailable at requested location. Please try with the other session.'
        )

    return {'isValid': True}


""" --- Functions that control the bot's behavior --- """


def book_room(intent_request):

    ## get location and session
    location = try_ex(lambda: intent_request['currentIntent']['slots']['roomLocation'])
    sessions = try_ex(lambda: intent_request['currentIntent']['slots']['sessions'])

    
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    # create reservation json object
    reservation = json.dumps({
        'ReservationType': 'StudyRoom',
        'Location': location,
        'sessions': sessions,
    })

    session_attributes['currentReservation'] = reservation

    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_room(location, sessions)
        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        session_attributes['currentReservation'] = reservation

        ## comment unless we require confirmation prompt
        # return delegate(session_attributes, intent_request['currentIntent']['slots'])

    try_ex(lambda: session_attributes.pop('currentReservation'))
    session_attributes['lastConfirmedReservation'] = reservation

    ## generate random room number, actual room number not important for the purpose of this task
    randomNumber = random.randint(1, 28)
    confirmationString = 'Room {} has been successfully booked at {} for {}'.format(randomNumber, location, sessions)

    if (intent_request['invocationSource'] == 'FulfillmentCodeHook'):
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': confirmationString
            }
        )

# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to bot's intent handlers
    if intent_name == 'BookStudyRoom':
        return book_room(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()

    return dispatch(event)
