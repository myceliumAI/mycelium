FROM postgres:15-alpine

# Set build arguments with default values
ARG POSTGRES_USER
ARG POSTGRES_DB
ARG POSTGRES_PORT

# Set environment variables from build arguments
ENV POSTGRES_USER=${POSTGRES_USER} \
    POSTGRES_DB=${POSTGRES_DB}
    #POSTGRES_PASSWORD -> to be set at runtime

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD pg_isready -U ${POSTGRES_USER} || exit 1

# Expose port
EXPOSE ${POSTGRES_PORT} 