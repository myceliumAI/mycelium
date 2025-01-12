FROM quay.io/keycloak/keycloak:26.0.7

# Set build arguments with default values
ARG KC_PORT
ARG KC_MANAGEMENT_PORT
ARG KC_REALM
ARG KC_BOOTSTRAP_ADMIN_USERNAME
ARG KC_BOOTSTRAP_ADMIN_PASSWORD
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_PORT

# Set environment variables from build arguments
ENV KC_PORT=${KC_PORT} \
    KC_MANAGEMENT_PORT=${KC_MANAGEMENT_PORT} \
    KC_REALM=${KC_REALM} \
    KC_BOOTSTRAP_ADMIN_USERNAME=${KC_BOOTSTRAP_ADMIN_USERNAME} \
    KC_BOOTSTRAP_ADMIN_PASSWORD=${KC_BOOTSTRAP_ADMIN_PASSWORD} \
    KC_DB=postgres \
    KC_DB_USERNAME=${POSTGRES_USER} \
    KC_DB_PASSWORD=${POSTGRES_PASSWORD} \
    KC_DB_URL=jdbc:postgresql://db:${POSTGRES_PORT}/${POSTGRES_DB} \
    KC_HTTP_ENABLED=true \
    KC_HTTPS_REQUIRED=none \
    KC_HOSTNAME_STRICT=false \
    KC_PROXY=edge \
    KC_HEALTH_ENABLED=true \
    KC_METRICS_ENABLED=true \
    KC_HTTP_RELATIVE_PATH=/ \
    KC_HOSTNAME_STRICT_HTTPS=false \
    BOOTSTRAP_STATUS_FILE=/tmp/bootstrap_completed

# Install required packages
RUN microdnf update -y && \
    microdnf install -y curl jq bash && \
    microdnf clean all

# Copy scripts
COPY scripts/keycloak_bootstrap.sh /scripts/
COPY scripts/entrypoint.sh /scripts/
COPY scripts/healthcheck.sh /scripts/
RUN chmod +x /scripts/*.sh

# Expose ports
EXPOSE ${KC_PORT} ${KC_MANAGEMENT_PORT}

# Add healthcheck
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD /scripts/healthcheck.sh

# Use custom entrypoint
ENTRYPOINT ["/scripts/entrypoint.sh"]