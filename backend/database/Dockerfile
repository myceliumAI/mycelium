FROM postgres:17.2-alpine

# Set build arguments with default values
ARG POSTGRES_USER
ARG POSTGRES_DB
ARG POSTGRES_PORT

# Set environment variables from build arguments
ENV POSTGRES_USER=${POSTGRES_USER} \
    POSTGRES_DB=${POSTGRES_DB}
    #POSTGRES_PASSWORD -> to be set at runtime

# Create non-root user and set permissions
RUN adduser -D nonroot && \
    mkdir -p /var/lib/postgresql/data && \
    chown -R nonroot:nonroot /var/lib/postgresql/data && \
    chown -R nonroot:nonroot /var/run/postgresql

# Copy and setup entrypoint script
COPY --chown=nonroot:nonroot entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Switch to non-root user
USER nonroot

# Set custom entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# Expose port
EXPOSE ${POSTGRES_PORT}