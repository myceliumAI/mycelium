#!/bin/bash

set -e  # Exit on error

# Print banner
echo " 🔧 Setting up environment variables..."

# Copy .env_example to .env
cp .env_example .env
echo " ✨ Created new .env file from template"

# Generate secrets
echo " 🔑 Generating secure secrets..."

# Function to generate and validate secrets
generate_secret() {
    local result
    case "$1" in
        "base64")
            result=$(openssl rand -base64 "$2" | tr -d '\n/' | cut -c1-"$2")
            ;;
        "hex")
            result=$(openssl rand -hex "$2")
            ;;
    esac
    echo "$result"
}

# Generate all required secrets
echo " 💡 Generating PostgreSQL password..."
PG_PASSWORD=$(generate_secret "base64" 32)

echo " 💡 Generating Keycloak admin password..."
KC_ADMIN_PASSWORD=$(generate_secret "base64" 32)

echo " 💡 Generating Keycloak client ID..."
KC_CLIENT_ID=$(generate_secret "base64" 12)


# Function to update env file safely
update_env_var() {
    local placeholder=$1
    local value=$2
    local escaped_value=$(echo "$value" | sed 's/[\/&]/\\&/g')
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS requires an empty string after -i
        sed -i '' "s|$placeholder|$escaped_value|g" .env
    else
        # Linux version
        sed -i "s|$placeholder|$escaped_value|g" .env
    fi
}

# Verify .env file was created and has content
if [ ! -s .env ]; then
    echo "❌ Error: .env file is empty or was not created properly"
    exit 1
fi

# Update all placeholders in the .env file
echo " 📝 Updating environment variables..."
update_env_var "__POSTGRES_PASSWORD__" "$PG_PASSWORD"
update_env_var "__KC_BOOTSTRAP_ADMIN_PASSWORD__" "$KC_ADMIN_PASSWORD"
update_env_var "__KC_CLIENT_ID__" "$KC_CLIENT_ID"

echo " ✅ Environment setup complete!"
echo " 📝 Your .env file has been created with secure random values"
echo " ⚠️  Please review the .env file and modify any other values as needed"

# Print important values
echo ""
echo " 🔐 Generated Secrets (save these somewhere secure):"
echo " ▶️ PostgreSQL Password: $PG_PASSWORD"
echo " ▶️ Keycloak Admin Password: $KC_ADMIN_PASSWORD"
echo " ▶️ Keycloak Client ID: $KC_CLIENT_ID"