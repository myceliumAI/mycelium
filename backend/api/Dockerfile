# Step 1: Use Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables with default values
ARG API_PORT

ARG POSTGRES_PORT
ARG POSTGRES_HOST
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB


ENV API_PORT=${API_PORT} \
    POSTGRES_PORT=${POSTGRES_PORT} \
    POSTGRES_HOST=${POSTGRES_HOST} \
    POSTGRES_USER=${POSTGRES_USER} \
    POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
    POSTGRES_DB=${POSTGRES_DB}


# Step 2: Set the working directory
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry and configure it
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Step 5: Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Step 6: Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Step 7: Copy the application code
COPY . .

# Step 8: Install the project
RUN poetry install --no-interaction --no-ansi

# Modifications pour la sécurité et la configuration
# Step 9: Create necessary directories
RUN mkdir -p /app/app/database && \
    chown -R nobody:nogroup /app/app/database && \
    chmod 770 /app/app/database

# Step 10: Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${API_PORT}/health || exit 1

# Step 11: Switch to non-root user
USER nobody

# Step 12: Expose the FastAPI app port
EXPOSE ${API_PORT}

# Step 13: Command to run the FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $API_PORT"]