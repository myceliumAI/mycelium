#!/bin/bash

# Exit on error
set -e

echo "🔐 Starting Keycloak bootstrap process..."

# First check the basic health endpoint
echo "⏳ Checking Keycloak basic health..."
until curl -f "http://keycloak:9000/health" > /dev/null 2>&1; do
    echo "⏳ Waiting for Keycloak to start..."
    sleep 5
done

# Then check the ready status
echo "⏳ Checking Keycloak readiness..."
until curl -f "http://keycloak:9000/health/ready" > /dev/null 2>&1; do
    echo "⏳ Waiting for Keycloak to be ready..."
    sleep 5
done

# Finally check the live status
echo "⏳ Checking Keycloak liveness..."
until curl -f "http://keycloak:9000/health/live" > /dev/null 2>&1; do
    echo "⏳ Waiting for Keycloak to be live..."
    sleep 5
done

# Get access token for admin
echo "🔑 Getting admin token..."
ADMIN_TOKEN=$(curl -s -X POST "http://keycloak:8080/realms/master/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${KC_BOOTSTRAP_ADMIN_USERNAME}" \
    -d "password=${KC_BOOTSTRAP_ADMIN_PASSWORD}" \
    -d "grant_type=password" \
    -d "client_id=admin-cli" \
    | jq -r '.access_token')

if [ -z "$ADMIN_TOKEN" ]; then
    echo "❌ Failed to get admin token"
    exit 1
fi

# Create realm
echo "🌍 Creating realm: ${KC_REALM}"
curl -s -X POST "http://keycloak:8080/admin/realms" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"realm\": \"${KC_REALM}\",
        \"enabled\": true,
        \"displayName\": \"Mycelium Realm\",
        \"displayNameHtml\": \"<div class='kc-logo-text'>Mycelium</div>\"
    }"

# Create client
echo "🔧 Creating client: ${KC_CLIENT_ID}"
curl -s -X POST "http://keycloak:8080/admin/realms/${KC_REALM}/clients" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"clientId\": \"${KC_CLIENT_ID}\",
        \"name\": \"mycelium\",
        \"description\": \"Mycelium - Your Secure Data Management Hub\",
        \"enabled\": true,
        \"protocol\": \"openid-connect\",
        \"publicClient\": true,
        \"standardFlowEnabled\": true,
        \"directAccessGrantsEnabled\": false,
        \"serviceAccountsEnabled\": false,
        \"authorizationServicesEnabled\": false,
        \"rootUrl\": \"http://${FRONTEND_HOST}:${FRONTEND_PORT}\",
        \"baseUrl\": \"/\",
        \"adminUrl\": \"http://${FRONTEND_HOST}:${FRONTEND_PORT}\",
        \"redirectUris\": [
            \"http://${FRONTEND_HOST}:${FRONTEND_PORT}/*\"
        ],
        \"webOrigins\": [
            \"http://${FRONTEND_HOST}:${FRONTEND_PORT}\"
        ],
        \"postLogoutRedirectUris\": [
            \"http://${FRONTEND_HOST}:${FRONTEND_PORT}/login\"
        ]
    }"

echo "✅ Keycloak bootstrap completed successfully!"