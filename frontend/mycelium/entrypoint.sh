#!/bin/sh

# Replace environment variables in the Nginx config
envsubst '$BACKEND_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf


# Set log level based on environment variable, default to 'error'
LOG_LEVEL=${NGINX_LOG_LEVEL:-error}

# Start Nginx with configured logging
exec nginx -g "daemon off; error_log /dev/stdout ${LOG_LEVEL};"
