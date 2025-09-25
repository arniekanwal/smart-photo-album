# Smart Photo Album

Cloud based web application developed with AWS to host photo albums and perform "smart" search lookups through voice or text. API Gateway facilitates
two Lambda (serverless functions) to execute user requests.

## Architecture

![](/frontend/assets/images/smartphoto-arch.png)

### Index Photos (LF1):
1. User uploads photo
2. uploaded file is verified and sent to S3
3. photo is then forwarded to AWS Rekognition for label generation
4. Labels are parsed/cleaned and indexed in ElasticSearch instance

### Search Photos (LF2):
1. User submits voice/text query
2. Lambda forwards search to Lex chatbot for disambiguation
3. Labels are processed by ElasticSearch and S3 photo ids are returned
4. Retrieve all related photos from S3 and return to user
