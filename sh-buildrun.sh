#/bin/bash
docker build -t iamrich-app-v2 .
docker run -v apikey.json:/apikey.json -e GOOGLE_APPLICATION_CREDENTIALS=apikey.json -p 8080:8080 iamrich-app-v2
