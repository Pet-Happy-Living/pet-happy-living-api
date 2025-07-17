#!/bin/bash

CONTAINER_NAME="pet-happy-api"
IMAGE_NAME="pet-happy-api"
PORT=8000

echo "✅ Starting container: $CONTAINER_NAME"

# 🔍 1. 이미지 존재 여부 확인
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    echo "📦 Docker image '$IMAGE_NAME' not found. Building image..."
    docker build -t $IMAGE_NAME .
else
    echo "✅ Docker image '$IMAGE_NAME' already exists."
fi

# 🧹 2. 기존 컨테이너가 있으면 삭제
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🗑️ Removing existing container..."
    docker rm -f $CONTAINER_NAME
fi

# 🚀 3. 컨테이너 실행
echo "🐳 Running container..."
docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $IMAGE_NAME

# 📋 4. 상태 확인
docker ps -f name=$CONTAINER_NAME
