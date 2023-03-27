import boto3
import dateutil.parser
import datetime
import time
import os
import logging
from opensearchpy import OpenSearch, RequestsHttpConnection 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def opensearch_query(host, query):
    host = 'search-photos-x5sreqhncdhwvdz35exej4owri.us-east-1.es.amazonaws.com' 
    auth = (os.getenv("opensearch_user"), os.getenv("opensearch_pwd"))

    client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    print("Client Info: ", client.info())
    
    es_result=client.search(index="photos", body=query)    # response=es.get()
    return es_result


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


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


""" --- Validation Functions --- """

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def validate_dining(searchterm):
    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """

def disambiguate_search(intent_request):
    source = intent_request['invocationSource']    
    slots = get_slots(intent_request)
    
    searchterm = slots["searchterm"]
    slot_dict = { 'searchterm': searchterm }

    if source == 'DialogCodeHook':
        validation_result = validate_dining()
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # continue to elicit slots if needed
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return delegate(output_session_attributes, get_slots(intent_request))

    # Fulfillment code hook, send information to queue
    request_id='myuser'
    print(intent_request)
    print(slot_dict)
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Thanks, your recommendations will be texted to you shortly!!'})


""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'SearchIntent':
        return disambiguate_search(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    # logger.debug('event.bot.name={}'.format(event['bot']['name']))

    dispatch(event)
    es_host = 'search-diningsearch-hgalbkaccpydlhouymrgk3k23a.us-east-1.es.amazonaws.com' 
    

    
    




