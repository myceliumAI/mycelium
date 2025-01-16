#!/bin/sh
set -e

# Store the original postgres entry point
POSTGRES_ENTRY_POINT="docker-entrypoint.sh postgres"

# Function to create user database
create_user_db() {
    until pg_isready -U "$POSTGRES_USER" -h localhost; do
        echo "🕐 Waiting for postgres to be ready..."
        sleep 1
    done

    echo "✨ Creating database with same name as user if it doesn't exist..."
    # Check if database exists
    if ! psql -U "$POSTGRES_USER" -lqt | cut -d \| -f 1 | grep -qw "$POSTGRES_USER"; then
        createdb -U "$POSTGRES_USER" "$POSTGRES_USER"
        echo "✅ Database $POSTGRES_USER created"
    else
        echo "📝 Database $POSTGRES_USER already exists"
    fi
}

# Start postgres in background
$POSTGRES_ENTRY_POINT &

# Wait for it to start and create database
create_user_db

# Wait for postgres to finish
wait $! 