#!/bin/bash

# Check if Keycloak is running
if ! curl -s -f "http://localhost:${KC_MANAGEMENT_PORT}/health" > /dev/null; then
    echo "Keycloak health check failed"
    exit 1
fi

# Check if bootstrap has completed
if [ ! -f "${BOOTSTRAP_STATUS_FILE}" ]; then
    echo "Bootstrap has not completed yet"
    exit 1
fi

exit 0 