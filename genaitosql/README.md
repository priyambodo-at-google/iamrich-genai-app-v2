### https://source.cloud.google.com/cloud-ce-shared-csr/szanevra-streamlit-bq-q-and-a-app/+/main:README.md

# BigQuery Question and Answer Bot

### What Problem does the app solve
This application is aimed at unlocking insights from structured data stored in BigQuery using natural language.

### Why is the value in solving this problem
Interacting with databases using natural language is important to people for a number of reasons.

* **It makes it easier for people to access and use information.** Natural language is the way that people naturally communicate, so it makes sense that people would prefer to interact with databases using natural language. This is especially true for people who do not have a lot of experience with database query languages.
* **It makes it possible to build more user-friendly applications.** When people can interact with databases using natural language, it is possible to build applications that are more user-friendly and intuitive. This can make it easier for people to use the applications and get the information they need.
* **It can improve the efficiency of data analysis.** Natural language processing can be used to analyze large amounts of data and extract insights that would be difficult or impossible to extract using traditional methods. This can help people to make better decisions and improve the efficiency of their data analysis processes.
* **It can open up new possibilities for data-driven applications.** Natural language processing can be used to build new types of data-driven applications that were not possible before. This can lead to new ways of interacting with data and new ways of solving problems.


### How does this application work? What does it use?
LLMs are capable of understanding and responding to natural language, but they can sometimes struggle to 
understand natural language queries that are not well-formed or that do not contain all the necessary information. 
LangChain (the library used in this demo) solves this problem by providing a framework for building applications 
that can interact with databases using natural language.

### What does the GUI look like
![alt text](imgs/app_gui.png)

### How are Responses played back to the users
![alt text](imgs/app_gui_q_and_a.png)

# Prerequisites
The assumption is made that you have set up a google cloud project and activated billing for this project.

#### The following Google Cloud Project APIs need to be enabled
* IAM
* BigQuery
* Vertex AI
* Cloud Run

#### Authentication
1) Create a service account, with the following Bigquery Roles:
* BigQuery User 
* BigQuery Data Viewer 
* BigQuery Job User
* Vertex AI User

Note: Additional roles may be required

#### gcloud Setup
To initialize the gcloud CLI:
```shell
gcloud init
```

If you want o use a service account run this command
```shell
gcloud auth login --cred-file=KEY_FILE
```
Replace KEY_FILE with the path to a service account key file.

Follow the prompt to authorise your local terminal

## If running the code locally within the IDE
## Option One - Via the IDE

Create the virtual environment
```
$ python3 -m venv env
```
Activate the virtual environment
```
$ source env/bin/activate
```
Install dependencies using
```
$ pip install -r requirements.txt
```

Set Environment Variables
```shell
export CONFIG_FILE = <PATH TO CONFIG_FILE>
eg. /Users/xxx/PycharmProjects/GenAIProject/config.yml
```

Update the required fields in the config.yml file
```shell
gcp:
  project_id: <PROJECT ID>
  region: <REGION>
```

Set Project Root Directory
```
GenAIProject
eg. /Users/xxx/PycharmProjects/GenAIProject/
```

11) Run Streamlit (from the project root directory)
```
$ streamlit run app.py
```

Note: For this application to run locally, you must have gcloud installed and authorised

## Deploy Container to GCP Container Register

### Set an environment variables
```shell
export GOOGLE_CLOUD_PROJECT="<enter project id>"
export CONTAINER_NAME='streamlit-bigquery-q-and-a'
export APP_NAME='streamlit-bigquery-q-and-a'
export REGION="us-central1"
export AR_NAME="streamlit" 
export AR_URI=${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${AR_NAME}
export SERVICE_ACCOUNT="<enter service account for cloud run"
```

```shell
gcloud auth application-default login
gcloud auth login
gcloud config set project ${GOOGLE_CLOUD_PROJECT}
```

### Create a repository in Artifact Registry
```shell
gcloud artifacts repositories create ${AR_NAME} --location=${REGION} --repository-format=docker
```
**Note**: If this command fails, run the below and try again: 
```shell
gcloud components update
```

### Create Docker file
Copy the following into a Dockerfile (if not exists)
```shell
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py","--server.port=8501"]
```

### Setup Docker auth
gcloud auth configure-docker us-central1-docker.pkg.dev

### Create and tag docker image
```shell
docker build -t ${AR_URI}/${CONTAINER_NAME} .
```

### Push to Artifact Registry
```shell
docker push ${AR_URI}/${CONTAINER_NAME}
```

### Cloud from Service Identity
By default, Cloud Run revisions and jobs execute as the Compute Engine default service account. The Compute Engine default service account has the Project Editor IAM role which grants read and write permissions on all resources in your Google Cloud project.
While this may be convenient, rather than use the default service account, Google recommends creating your own user-managed service account with the most granular permissions and assigning that service account as your Cloud Run service or job identity. 

See the doce here for details [here](https://cloud.google.com/run/docs/securing/service-identity#gcloud)

### Deploy to Cloud Run
```shell
gcloud run deploy ${APP_NAME} \
--image=${AR_URI}/${CONTAINER_NAME} \
--platform=managed \
--port 8501 \
--service-account=${SERVICE_ACCOUNT} \
--region=${REGION} \
--cpu=2 --memory=1Gi \
--max-instances=2 \
--allow-unauthenticated
```

Note, remove this flag if you don't want to allow unauthenticated access:
```shell
--allow-unauthenticated
```

See the details [here](https://cloud.google.com/run/docs/authenticating/public#gcloud)


