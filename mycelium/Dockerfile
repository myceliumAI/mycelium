FROM nginx:alpine

# Set environment variables with default values
ARG API_HOST
ARG API_PORT
ARG KC_HOST
ARG KC_PORT
ARG KC_REALM
ARG KC_CLIENT_ID
ARG FRONTEND_HOST
ARG FRONTEND_PORT
ARG NGINX_LOG_LEVEL

ENV API_HOST=${API_HOST} \
    API_PORT=${API_PORT} \
    KC_HOST=${KC_HOST} \
    KC_PORT=${KC_PORT} \
    KC_REALM=${KC_REALM} \
    KC_CLIENT_ID=${KC_CLIENT_ID} \
    FRONTEND_HOST=${FRONTEND_HOST} \
    FRONTEND_PORT=${FRONTEND_PORT} \
    NGINX_LOG_LEVEL=${NGINX_LOG_LEVEL}

# Install node, yarn and curl
RUN apk add --no-cache nodejs npm yarn curl

WORKDIR /app

# Copy files and build frontend
COPY package*.json ./
RUN yarn install
COPY . .
RUN yarn build

# Setup nginx and ensure template is in the correct location
COPY config/nginx.conf /etc/nginx/nginx.conf.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    mkdir -p /usr/share/nginx/html/utils && \
    mv /app/dist/* /usr/share/nginx/html/ && \
    rm -rf /app

# Create required directories and set permissions
RUN mkdir -p /var/cache/nginx /var/run /var/log/nginx && \
    chmod -R 777 /var/cache/nginx /var/run /var/log/nginx /etc/nginx /usr/share/nginx/html && \
    # Remove user directive from nginx.conf as we'll run nginx as non-root
    sed -i '/user/d' /etc/nginx/nginx.conf.template

# Add script tag for config.js in index.html
RUN sed -i 's/<head>/<head><script src="\/config\/config.js"><\/script>/' /usr/share/nginx/html/index.html

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Switch to non-root user
USER appuser

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${FRONTEND_PORT} || exit 1

EXPOSE ${FRONTEND_PORT}

ENTRYPOINT ["/entrypoint.sh"]