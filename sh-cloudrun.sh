#/bin/bash
docker tag iamrich-app-v2 gcr.io/work-mylab-machinelearning/iamrich-app-v2
gcloud auth configure-docker
docker push gcr.io/work-mylab-machinelearning/iamrich-app-v2
gcloud run deploy iamrich-app-v2 \
  --image gcr.io/work-mylab-machinelearning/iamrich-app-v2 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated