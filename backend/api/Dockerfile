# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables with default values
ARG API_PORT

ARG POSTGRES_PORT
ARG POSTGRES_HOST
ARG POSTGRES_USER
ARG POSTGRES_DB


ENV API_PORT=${API_PORT} \
    POSTGRES_PORT=${POSTGRES_PORT} \
    POSTGRES_HOST=${POSTGRES_HOST} \
    POSTGRES_USER=${POSTGRES_USER} \
    POSTGRES_DB=${POSTGRES_DB}
    #POSTGRES_PASSWORD -> to be set at runtime


# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends\
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and configure it
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root --without dev

# Copy the application code
COPY . .

# Copy and set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create necessary directories
RUN mkdir -p /app/app/database && \
    chown -R nobody:nogroup /app/app/database && \
    chmod 770 /app/app/database

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${API_PORT}/health || exit 1

# Switch to non-root user
USER nobody

# Expose the FastAPI app port
EXPOSE ${API_PORT}

# Command to run the FastAPI app
ENTRYPOINT ["/entrypoint.sh"]