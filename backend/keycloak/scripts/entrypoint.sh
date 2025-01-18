#!/bin/bash


# Build database URL
if [ -n "$POSTGRES_SOCKET" ] && [ "$POSTGRES_SOCKET" != "" ]; then
    echo "🔌 Using Unix socket connection for database"
    KC_DB_URL="jdbc:postgresql://localhost/${POSTGRES_DB}?socketFactory=org.newsclub.net.unix.AFUNIXSocketFactory&socketFactoryArg=${POSTGRES_SOCKET}"

else
    echo "🌐 Using TCP connection for database"
    # Handle localhost case for POSTGRES_HOST
    if [ "${POSTGRES_HOST}" = "localhost" ]; then
        export POSTGRES_HOST="host.docker.internal"
        echo "💡 POSTGRES_HOST was localhost, using host.docker.internal instead"
    fi
    KC_DB_URL="jdbc:postgresql://${POSTGRES_HOST}:${POSTGRES_PORT:-5432}/${POSTGRES_DB}"
fi
export KC_DB_URL

# Function to wait for Keycloak to be ready
wait_for_keycloak() {
    echo "⏳ Waiting for Keycloak to start..."
    # Double quote variable to prevent globbing and word splitting
    until curl -s --fail "http://localhost:${KC_MANAGEMENT_PORT}/health" > /dev/null; do
        sleep 2
    done
    echo "✅ Keycloak is ready"
}

# Remove status file if it exists from a previous run
rm -f "${BOOTSTRAP_STATUS_FILE}"

# Start Keycloak in background
/opt/keycloak/bin/kc.sh start &
KEYCLOAK_PID=$!

# Wait for Keycloak to be ready
wait_for_keycloak

# Run bootstrap script
echo "🔧 Running bootstrap script..."
/scripts/keycloak_bootstrap.sh
BOOTSTRAP_RESULT=$?

if [ $BOOTSTRAP_RESULT -eq 0 ]; then
    echo "✅ Bootstrap completed successfully"
    # Create status file to indicate successful bootstrap
    touch "${BOOTSTRAP_STATUS_FILE}"
else
    echo "❌ Bootstrap failed with exit code $BOOTSTRAP_RESULT"
    kill $KEYCLOAK_PID
    exit $BOOTSTRAP_RESULT
fi

tail --pid=$KEYCLOAK_PID -f /dev/null 