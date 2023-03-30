import boto3
import time
import os
from opensearchpy import OpenSearch, RequestsHttpConnection 

'''
Sends search query to Lex bot and disambiguates the responses.
Returns the slots/labels for SearchIntent which are used
for returning results from OpenSearch
'''
def disambiguate_search(event):
    client = boto3.client('lex-runtime')

    response = client.post_text(botName='PhotoSearchBot', botAlias='dev', userId='myuser',
                                inputText=event['messages'][0]['unstructured']['text'])
    
    bot_response = response['message']

    return {
        'statusCode': 200,
        'messages': [{
            'type': 'unstructured',
            'unstructured': {
                'text': bot_response
            }
        }]
    }    
    


'''
Take provided labels and query for matching results/photos
from our OpenSearch instance
'''
def opensearch_query(host, query):
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


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()

    # Initialize endpoint for OpenSearch instance
    es_host = 'search-photos-x5sreqhncdhwvdz35exej4owri.us-east-1.es.amazonaws.com'  

    # Build an OpenSearch Query
    labels = disambiguate_search(event)
    print("Labels found: ", labels)
    query = ""

    opensearch_query(es_host, query)
           




