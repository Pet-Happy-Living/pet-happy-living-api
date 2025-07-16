#!/bin/bash

CONTAINER_NAME="pet-happy-api"
IMAGE_NAME="pet-happy-api"

echo "✅ Starting container: $CONTAINER_NAME"

# 기존 컨테이너가 있으면 삭제
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🗑️ Removing existing container..."
    docker rm -f $CONTAINER_NAME
fi

# 새 컨테이너 실행
docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME

# 상태 확인
docker ps -f name=$CONTAINER_NAME
