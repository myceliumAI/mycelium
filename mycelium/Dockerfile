FROM nginx:alpine

# Set environment variables with default values
ARG BACKEND_HOST
ARG BACKEND_PORT

ARG KC_REALM
ARG KC_PORT
ARG KC_CLIENT_ID

ARG FRONTEND_HOST
ARG FRONTEND_PORT
ARG NGINX_LOG_LEVEL

ENV BACKEND_HOST=${BACKEND_HOST} \
    BACKEND_PORT=${BACKEND_PORT} \
    KC_URL=http://${BACKEND_HOST}:${KC_PORT} \
    KC_REALM=${KC_REALM} \
    KC_CLIENT_ID=${KC_CLIENT_ID} \
    FRONTEND_HOST=${FRONTEND_HOST} \
    FRONTEND_PORT=${FRONTEND_PORT} \
    VUE_CLI_SERVICE_CONFIG_PATH=./config/vue.config.js \
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

# Add script tag for config.js in index.html
RUN sed -i 's/<head>/<head><script src="\/config\/config.js"><\/script>/' /usr/share/nginx/html/index.html

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${FRONTEND_PORT} || exit 1

EXPOSE ${FRONTEND_PORT}

ENTRYPOINT ["/entrypoint.sh"]

# Create a simpler runtime config injection
RUN echo "window.__RUNTIME_CONFIG__ = {};" > /usr/share/nginx/html/config/config.js
