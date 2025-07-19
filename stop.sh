#!/bin/bash

set -e

SERVICE_NAME="pet-happy-api"
COMPOSE_FILES="-f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.prod.yml"

echo "🛑 [STOP] Stopping $SERVICE_NAME (all environments)"

docker compose $COMPOSE_FILES down --remove-orphans

echo "✅ [DONE] All containers stopped and cleaned up."
