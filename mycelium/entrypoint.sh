#!/bin/sh

set -e

# Create config directory if it doesn't exist
mkdir -p /usr/share/nginx/html/config

# Replace variables in config.js and place it in the correct location
envsubst < /usr/share/nginx/html/utils/config.template.js > /usr/share/nginx/html/config/config.js

# Replace environment variables in the Nginx config
envsubst '$BACKEND_HOST $BACKEND_PORT $FRONTEND_PORT $FRONTEND_HOST' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

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
