#!/bin/bash

# Exit on error
set -e

# Configuration
KC_DEFAULT_HOST=keycloak
KC_DEFAULT_PORT=8080
KC_DEFAULT_HEALTH_PORT=9000

echo "🔐 Starting Keycloak bootstrap process..."
echo "📍 Using Keycloak at ${KC_DEFAULT_HOST}:${KC_DEFAULT_PORT}"

# Function to check health endpoint with timeout
check_health() {
    local endpoint=$1
    local description=$2
    local timeout=5
    
    echo "⏳ Checking Keycloak ${description}..."
    if curl -f --max-time ${timeout} "http://${KC_DEFAULT_HOST}:${KC_DEFAULT_HEALTH_PORT}${endpoint}" > /dev/null 2>&1; then
        echo "✅ ${description} check passed"
        return 0
    else
        echo "❌ ${description} check failed"
        echo "🔍 Attempted to connect to: http://${KC_DEFAULT_HOST}:${KC_DEFAULT_HEALTH_PORT}${endpoint}"
        return 1
    fi
}

# Check basic health
if ! check_health "/health" "basic health"; then
    echo "❌ Cannot connect to Keycloak. Is it running?"
    exit 1
fi

# Check readiness
if ! check_health "/health/ready" "readiness"; then
    echo "❌ Keycloak is not ready"
    exit 1
fi

# Check liveness
if ! check_health "/health/live" "liveness"; then
    echo "❌ Keycloak is not live"
    exit 1
fi

echo "✨ Keycloak is up and running at ${KC_DEFAULT_HOST}:${KC_DEFAULT_PORT}"

# Get access token for admin
echo "🔑 Getting admin token using username: ${KC_BOOTSTRAP_ADMIN_USERNAME}"
TOKEN_RESPONSE=$(curl -s -X POST "http://${KC_DEFAULT_HOST}:${KC_DEFAULT_PORT}/realms/master/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "username=${KC_BOOTSTRAP_ADMIN_USERNAME}" \
    --data-urlencode "password=${KC_BOOTSTRAP_ADMIN_PASSWORD}" \
    --data-urlencode "grant_type=password" \
    --data-urlencode "client_id=admin-cli")

# Debug the response
echo "🔍 Token response: ${TOKEN_RESPONSE}"

ADMIN_TOKEN=$(echo "${TOKEN_RESPONSE}" | jq -r '.access_token')

if [ -z "$ADMIN_TOKEN" ] || [ "$ADMIN_TOKEN" = "null" ]; then
    echo "❌ Failed to parse admin token from response"
    echo "🔍 Response: ${TOKEN_RESPONSE}"
    exit 1
fi

echo "✅ Successfully obtained admin token"


# Create realm with registration settings
echo "🔧 Creating realm: ${KC_REALM}"
curl -s -w "\n%{http_code}" -X POST "http://${KC_DEFAULT_HOST}:${KC_DEFAULT_PORT}/admin/realms" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"realm\": \"${KC_REALM}\",
        \"enabled\": true,
        \"registrationAllowed\": true,
        \"registrationEmailAsUsername\": true,
        \"verifyEmail\": false,
        \"loginWithEmailAllowed\": true,
        \"duplicateEmailsAllowed\": false,
        \"resetPasswordAllowed\": true,
        \"editUsernameAllowed\": false
    }"

# Create client with all needed settings
echo "🔧 Creating client: ${KC_CLIENT_ID}"
curl -s -w "\n%{http_code}" -X POST "http://${KC_DEFAULT_HOST}:${KC_DEFAULT_PORT}/admin/realms/${KC_REALM}/clients" \
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
        \"implicitFlowEnabled\": false,
        \"directAccessGrantsEnabled\": true,
        \"rootUrl\": \"http://${FRONTEND_HOST}:${FRONTEND_PORT}\",
        \"redirectUris\": [\"http://${FRONTEND_HOST}:${FRONTEND_PORT}/*\"],
        \"adminUrl\": \"http://${FRONTEND_HOST}:${FRONTEND_PORT}\",
        \"webOrigins\": [\"*\"]
    }"

# Only show success if we made it this far
echo "✅ Keycloak bootstrap completed successfully!"