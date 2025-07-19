#!/bin/bash

set -e

SERVICE_NAME="pet-happy-api"
COMPOSE_FILES="-f docker-compose.base.yml -f docker-compose.prod.yml"

echo "🚀 [START: PROD] Starting $SERVICE_NAME in production mode"

docker compose $COMPOSE_FILES --env-file .env up -d --build --force-recreate

echo "📦 [STATUS] Container status:"
docker compose $COMPOSE_FILES ps
