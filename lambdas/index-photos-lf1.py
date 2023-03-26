import boto3
import urllib.parse
import os
from opensearchpy import OpenSearch, RequestsHttpConnection    

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Grab bucket and object-key
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    # Use head_object to retrieve S3 Metadata
    response = s3.head_object(Bucket=bucket, Key=key)
    metadata = response['ResponseMetadata']['HTTPHeaders']['date'] # retrieve creation date (x-amz-meta-customLabels)

    # Collect labels from Rekognition 
    labels = detect_labels(key, bucket)
    
    photo_object = {
        "objectKey": key,
        "bucket": bucket,
        "createdTimestamp": metadata,
        "labels": labels,
    }

    add_to_opensearch(photo_object, key)


def detect_labels(photo, bucket):
    rekognition_client = boto3.client("rekognition")

    response = rekognition_client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
    MaxLabels=10,
    # Uncomment to use image properties and filtration settings
    #Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
    #Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
    # "ImageProperties": {"MaxDominantColors":10}}
    )

    detected_labels = []
    for label in response['Labels']:
        detected_labels.append(label['Name'].lower())
        
    return detected_labels


def add_to_opensearch(body, key):
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

    response = client.index(
        index = "photos",
        body = body,
        id = key,
        refresh = True
    )
    print("Add document: ", response)

    

    




