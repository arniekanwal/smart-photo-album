import boto3
import os
import time
import urllib.parse
import base64
from opensearchpy import OpenSearch, RequestsHttpConnection    

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Grab bucket and object-key
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # retrieve the object
    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj['Body'].read().decode('utf-8')
    image = base64.b64decode(body)   

    s3.delete_object(Bucket=bucket,Key=key)
    s3.put_object(Bucket=bucket, Body=image, Key=key,ContentType='image/jpeg')

    # update key
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    metadata = time.time()

    # Collect labels from Rekognition 
    labels = detect_labels(key, bucket)
    
    photo_object = {
        "objectKey": key,
        "bucket": bucket,
        "createdTimestamp": metadata,
        "labels": labels,
    }

    # Add labels to photos index in OpenSearch instance
    add_to_opensearch(photo_object, key)

def detect_labels(photo, bucket) -> list[str]:
    rekognition_client = boto3.client("rekognition")

    response = rekognition_client.detect_labels(
        Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10,
        # Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        # Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
        # "ImageProperties": {"MaxDominantColors":10}}
    )

    detected_labels = []
    for label in response['Labels']:
        detected_labels.append(label['Name'].lower())
    
    print("Labels: ", detected_labels)
    return detected_labels


def add_to_opensearch(body, key) -> None:
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

