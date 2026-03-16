IMAGE_NAME=
IMAGE_TAG=
ACCOUNT_ID=586639730662
REGION_ID=ap-northeast-2
aws ecr get-login-password --region ${REGION_ID} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION_ID}.amazonaws.com
docker build -t ${IMAGE_NAME} .
docker tag ${IMAGE_NAME}:latest ${ACCOUNT_ID}.dkr.ecr.${REGION_ID}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}
docker push ${ACCOUNT_ID}.dkr.ecr.${REGION_ID}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}