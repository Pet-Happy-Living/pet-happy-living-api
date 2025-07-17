#!/bin/bash

CONTAINER_NAME="pet-happy-api"

echo "🛑 Stopping container: $CONTAINER_NAME"

# 컨테이너 실행 중이면 중지
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    docker stop $CONTAINER_NAME
fi

# 중지된 컨테이너 제거
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    docker rm $CONTAINER_NAME
fi

echo "✅ Container $CONTAINER_NAME has been stopped and removed."
