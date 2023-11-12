$IMAGE_TAG = 'core.harbor.domain:32100/library/veridion-api:latest'

docker build --tag $IMAGE_TAG .

docker push $IMAGE_TAG
