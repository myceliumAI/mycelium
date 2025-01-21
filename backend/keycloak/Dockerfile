FROM registry.access.redhat.com/ubi9:9.5 AS ubi-micro-build
RUN mkdir -p /mnt/rootfs
RUN dnf install --installroot /mnt/rootfs curl jq --releasever 9 --setopt install_weak_deps=false --nodocs -y && \
    dnf clean all && \
    dnf --installroot /mnt/rootfs clean all && \
    rpm --root /mnt/rootfs -e --nodeps setup

FROM quay.io/keycloak/keycloak:26.1.0
COPY --from=ubi-micro-build /mnt/rootfs /

# Set build arguments with default values
ARG KC_PORT
ARG KC_MANAGEMENT_PORT
ARG KC_REALM
ARG KC_BOOTSTRAP_ADMIN_USERNAME
ARG POSTGRES_USER
ARG POSTGRES_DB
ARG POSTGRES_PORT
ARG POSTGRES_HOST
ARG FRONTEND_HOST
ARG FRONTEND_PORT

# Set environment variables from build arguments
ENV KC_PORT=${KC_PORT} \
    KC_MANAGEMENT_PORT=${KC_MANAGEMENT_PORT} \
    KC_REALM=${KC_REALM} \
    KC_BOOTSTRAP_ADMIN_USERNAME=${KC_BOOTSTRAP_ADMIN_USERNAME} \
    KC_DB=postgres \
    KC_DB_USERNAME=${POSTGRES_USER} \
    KC_HTTP_ENABLED=true \
    KC_HTTPS_REQUIRED=none \
    KC_HOSTNAME_STRICT=false \
    KC_HEALTH_ENABLED=true \
    KC_METRICS_ENABLED=true \
    KC_HTTP_RELATIVE_PATH=/ \
    BOOTSTRAP_STATUS_FILE=/tmp/bootstrap_completed \
    POSTGRES_DB=${POSTGRES_DB} \
    POSTGRES_PORT=${POSTGRES_PORT} \
    POSTGRES_HOST=${POSTGRES_HOST} \
    FRONTEND_HOST=${FRONTEND_HOST} \
    FRONTEND_PORT=${FRONTEND_PORT}
    #KC_BOOTSTRAP_ADMIN_PASSWORD -> to be set at runtime
    #KC_DB_PASSWORD -> to be set at runtime
    #KC_CLIENT_ID -> to be set at runtime
    #KC_GOOGLE_CLIENT_ID -> to be set at runtime
    #KC_GOOGLE_CLIENT_SECRET -> to be set at runtime


# Copy scripts
USER root
COPY --chown=keycloak:keycloak scripts/keycloak_bootstrap.sh /scripts/
COPY --chown=keycloak:keycloak scripts/entrypoint.sh /scripts/
COPY --chown=keycloak:keycloak scripts/healthcheck.sh /scripts/
RUN chmod 500 /scripts/*.sh
USER keycloak

# Expose ports
EXPOSE ${KC_PORT} ${KC_MANAGEMENT_PORT}

# Add healthcheck
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD /scripts/healthcheck.sh

# Use custom entrypoint
ENTRYPOINT ["/scripts/entrypoint.sh"]
