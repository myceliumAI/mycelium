#!/bin/sh

set -e

# Create config directory if it doesn't exist
mkdir -p /usr/share/nginx/html/config

# Generate the runtime config directly
cat > /usr/share/nginx/html/config/config.js << EOF
window.__RUNTIME_CONFIG__ = {
    KC_PORT: "${KC_PORT}",
    KC_REALM: "${KC_REALM}",
    KC_CLIENT_ID: "${KC_CLIENT_ID}",
    BACKEND_HOST: "${BACKEND_HOST}",
};
EOF

# Replace environment variables in the Nginx config
envsubst '$BACKEND_HOST $API_PORT $FRONTEND_PORT $FRONTEND_HOST' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Verify the config.js file exists and has content
if [ ! -s /usr/share/nginx/html/config/config.js ]; then
    echo "❌ Error: config.js is empty or not created"
    exit 1
fi

# Verify nginx configuration
nginx -t

# Log the substitution process
echo "✅ Runtime configuration generated"
echo "✅ Nginx configuration updated"
echo "🌐 Frontend URL (inside container): http://localhost:${FRONTEND_PORT}"

# Start Nginx with configured logging
exec nginx -g "daemon off;"
