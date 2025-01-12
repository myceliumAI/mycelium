#!/bin/bash

# Exit on error
set -e

# Enable error trace
set -o pipefail

# Function to handle errors
error_handler() {
    local line_no=$1
    local error_code=$2
    local last_command="${BASH_COMMAND}"
    echo "❌ Error occurred in script at line ${line_no}"
    echo "❌ Exit code: ${error_code}"
    echo "❌ Failed command: ${last_command}"
}

# Set up the error trap
trap 'error_handler ${LINENO} $?' ERR

# Configuration
KC_HOST_LOCAL=localhost
KC_PORT_LOCAL=8080

echo "📍 Using Keycloak at ${KC_HOST_LOCAL}:${KC_PORT_LOCAL}"

# Get access token for admin
echo "🔑 Getting admin token using username: ${KC_BOOTSTRAP_ADMIN_USERNAME}"
TOKEN_RESPONSE=$(curl -s -X POST "http://${KC_HOST_LOCAL}:${KC_PORT_LOCAL}/realms/master/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "username=${KC_BOOTSTRAP_ADMIN_USERNAME}" \
    --data-urlencode "password=${KC_BOOTSTRAP_ADMIN_PASSWORD}" \
    --data-urlencode "grant_type=password" \
    --data-urlencode "client_id=admin-cli" || echo "CURL_ERROR:$?")

# Check if curl failed
if [[ $TOKEN_RESPONSE == CURL_ERROR:* ]]; then
    echo "❌ Failed to connect to Keycloak server"
    echo "❌ Curl error code: ${TOKEN_RESPONSE#CURL_ERROR:}"
    exit 1
fi

# Debug the response
echo "🔍 Token response: ${TOKEN_RESPONSE}"

ADMIN_TOKEN=$(echo "${TOKEN_RESPONSE}" | jq -r '.access_token')

if [ -z "$ADMIN_TOKEN" ] || [ "$ADMIN_TOKEN" = "null" ]; then
    echo "❌ Failed to parse admin token from response"
    echo "❌ Error details from response: $(echo "${TOKEN_RESPONSE}" | jq -r '.error_description // .error // "No error details available"')"
    exit 1
fi

echo "✅ Successfully obtained admin token"


# Create realm with registration settings
echo "🔧 Creating realm: ${KC_REALM}"
curl -s -w "\n%{http_code}" -X POST "http://${KC_HOST_LOCAL}:${KC_PORT_LOCAL}/admin/realms" \
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
curl -s -w "\n%{http_code}" -X POST "http://${KC_HOST_LOCAL}:${KC_PORT_LOCAL}/admin/realms/${KC_REALM}/clients" \
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

# Check if Google credentials are available
if [ -n "${KC_GOOGLE_CLIENT_ID}" ] && [ -n "${KC_GOOGLE_CLIENT_SECRET}" ] && \
   [ "${KC_GOOGLE_CLIENT_ID}" != "null" ] && [ "${KC_GOOGLE_CLIENT_SECRET}" != "null" ]; then
    echo "🔧 Creating Google Identity Provider"
    curl -s -w "\n%{http_code}" -X POST "http://${KC_HOST_LOCAL}:${KC_PORT_LOCAL}/admin/realms/${KC_REALM}/identity-provider/instances" \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"alias\": \"google\",
            \"displayName\": \"Google\",
            \"providerId\": \"google\",
            \"enabled\": true,
            \"updateProfileFirstLoginMode\": \"on\",
            \"trustEmail\": true,
            \"storeToken\": false,
            \"addReadTokenRoleOnCreate\": false,
            \"authenticateByDefault\": false,
            \"linkOnly\": false,
            \"firstBrokerLoginFlowAlias\": \"first broker login\",
            \"config\": {
                \"clientId\": \"${KC_GOOGLE_CLIENT_ID}\",
                \"clientSecret\": \"${KC_GOOGLE_CLIENT_SECRET}\",
                \"useUserInfoProvider\": true
            }
        }"
    echo "✅ Google Identity Provider configured successfully"
else
    echo "ℹ️ Skipping Google Identity Provider setup - credentials not provided"
fi

# Only show success if we made it this far
echo "✅ Keycloak bootstrap completed successfully!"