FROM postgres:17.2-alpine

# Set build arguments with default values
ARG POSTGRES_USER
ARG POSTGRES_DB
ARG POSTGRES_PORT

# Set environment variables from build arguments
ENV POSTGRES_USER=${POSTGRES_USER} \
    POSTGRES_DB=${POSTGRES_DB} \
    POSTGRES_PORT=${POSTGRES_PORT}  
    #POSTGRES_PASSWORD -> to be set at runtime

# Expose port
EXPOSE ${POSTGRES_PORT}

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

CMD ["docker-entrypoint.sh", "postgres"]
