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
REALM_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "http://keycloak:8080/admin/realms" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"realm\": \"${KC_REALM}\",
        \"enabled\": true,
        \"displayName\": \"Mycelium Realm\",
        \"displayNameHtml\": \"<div class='kc-logo-text'>Mycelium</div>\"
    }")

HTTP_CODE=$(echo "$REALM_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$REALM_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" != "201" ] && [ "$HTTP_CODE" != "409" ]; then
    echo "❌ Failed to create realm: $RESPONSE_BODY"
    exit 1
fi

if [ "$HTTP_CODE" = "409" ]; then
    echo "⚠️ Realm already exists, continuing..."
fi

# Create client
echo "🔧 Creating client: ${KC_CLIENT_ID}"
CLIENT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "http://keycloak:8080/admin/realms/${KC_REALM}/clients" \
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
        \"attributes\": {
            \"post.logout.redirect.uris\": \"http://${FRONTEND_HOST}:${FRONTEND_PORT}/login\"
        }
    }")

HTTP_CODE=$(echo "$CLIENT_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$CLIENT_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" != "201" ] && [ "$HTTP_CODE" != "409" ]; then
    echo "❌ Failed to create client: $RESPONSE_BODY"
    exit 1
fi

if [ "$HTTP_CODE" = "409" ]; then
    echo "⚠️ Client already exists, continuing..."
fi

echo "✅ Keycloak bootstrap completed successfully!"