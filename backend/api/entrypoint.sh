#!/bin/bash
set -e

# Replace localhost with host.docker.internal for Docker host access
if [ "$POSTGRES_HOST" = "localhost" ]; then
    export POSTGRES_HOST="host.docker.internal"
    echo "💡 Replacing localhost with host.docker.internal for Docker host access"
fi

echo "💫 Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$API_PORT"