#!/bin/bash

# Function to wait for Keycloak to be ready
wait_for_keycloak() {
    echo "Waiting for Keycloak to start..."
    until curl -s --fail http://localhost:${KC_MANAGEMENT_PORT}/health/ready > /dev/null; do
        sleep 2
    done
    echo "Keycloak is ready"
}

# Remove status file if it exists from a previous run
rm -f "${BOOTSTRAP_STATUS_FILE}"

# Start Keycloak in background
/opt/keycloak/bin/kc.sh start &
KEYCLOAK_PID=$!

# Wait for Keycloak to be ready
wait_for_keycloak

# Run bootstrap script
echo "Running bootstrap script..."
/scripts/keycloak_bootstrap.sh
BOOTSTRAP_RESULT=$?

if [ $BOOTSTRAP_RESULT -eq 0 ]; then
    echo "Bootstrap completed successfully"
    # Create status file to indicate successful bootstrap
    touch "${BOOTSTRAP_STATUS_FILE}"
else
    echo "Bootstrap failed with exit code $BOOTSTRAP_RESULT"
    kill $KEYCLOAK_PID
    exit $BOOTSTRAP_RESULT
fi

# Wait for Keycloak process
wait $KEYCLOAK_PID 