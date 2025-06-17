# Smart Photo Album

Cloud based web application developed with AWS to host photo albums and perform "smart" search lookups through voice or text. It uses services such as AWS Lex Chatbot, ElasticSearch, Rekognition, and Transcribe. After uploading photos to an album, image labels will be automatically processed and stored to an ElasticSearch instance and queries are dismantled with Lex Chatbot to match key words
and perform "smart" photo lookups.