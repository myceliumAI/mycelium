# Load environment variables at the start of each target that needs them
define load_env
	$(eval include $(PWD)/.env)
	$(eval export)
endef

.PHONY: help check check-dev check-prod setup-env front-dev back-dev \
        build-front build-back run-front run-back \
        clean clean-front clean-back

help: ## Show this help message
	@echo '🔧 Setup & Utils:'
	@echo '  check-dev       - Check development dependencies'
	@echo '  check-prod      - Check production/deployment dependencies'
	@echo '  setup-env       - Create .env file from example'
	@echo '  clean           - Remove all Docker resources (images, containers, volumes) and .env file'
	@echo '  clean-front     - Remove frontend Docker resources'
	@echo '  clean-back      - Remove backend Docker resources and volumes'
	@echo ''
	@echo '🚀 Running Applications:'
	@echo '  launch          - Launch all services (frontend, backend) in production mode'
	@echo '  front           - Run frontend from Docker Hub image'
	@echo '  back            - Run backend services using Docker Compose'
	@echo '  front-dev       - Start the frontend locally in development mode'
	@echo '  back-dev        - Start the backend locally in development mode'
	@echo ''
	@echo '📦 Docker Operations:'
	@echo '  build-front     - Build frontend Docker image locally'
	@echo '  build-back      - Build backend Docker images locally'


# SETUP

check-dev: ## Check development dependencies
	@chmod +x ./scripts/check_deps.sh
	@./scripts/check_deps.sh dev

check-prod: ## Check production dependencies
	@chmod +x ./scripts/check_deps.sh
	@./scripts/check_deps.sh deploy

setup-env: ## Create .env file from example
	@chmod +x ./scripts/setup_env.sh
	@./scripts/setup_env.sh


# FRONTEND

front-dev: ## Launch the frontend application
	$(call load_env)
	@cd mycelium && \
	yarn install && \
	yarn cross-env VUE_CLI_SERVICE_CONFIG_PATH=./config/vue.config.js \
	yarn serve

build-front: ## Build frontend Docker image locally
	$(call load_env)
	@echo "💡 Building frontend image locally..."
	@docker build \
		--build-arg BACKEND_HOST=${BACKEND_HOST} \
		--build-arg BACKEND_PORT=${BACKEND_PORT} \
		--build-arg FRONTEND_HOST=${FRONTEND_HOST} \
		--build-arg FRONTEND_PORT=${FRONTEND_PORT} \
		--build-arg NGINX_LOG_LEVEL=${NGINX_LOG_LEVEL} \
		-t mycelium-frontend:latest ./mycelium
	@echo "✅ Frontend image built successfully"

front: build-front ## Run frontend from local image
	$(call load_env)
	@echo "💡 Starting frontend container from local image..."
	@docker run -d \
		--name mycelium-frontend \
		--env-file .env \
		mycelium-frontend:latest
	@echo "✅ Frontend container started on port ${FRONTEND_PORT}"


# BACKEND

back-dev: ## Launch the backend application in development mode
	$(call load_env)
	@echo "💡 Starting PostgreSQL and Keycloak with Docker Compose..."
	@chmod +x backend/scripts/keycloak_bootstrap.sh
	@cd backend && docker compose up -d db keycloak keycloak-bootstrap
	@echo "✅ Infrastructure services started"
	@echo "💡 Starting FastAPI backend in development mode..."
	@cd backend && \
	poetry install && \
	poetry run uvicorn app.main:app --port ${BACKEND_PORT} --host 0.0.0.0 --reload

build-back: ## Build backend Docker images locally
	$(call load_env)
	@echo "💡 Building backend images locally..."
	@cd backend && docker compose build
	@echo "✅ Backend images built successfully"

back: build-back ## Run backend services using Docker Compose
	$(call load_env)
	@echo "💡 Starting backend services with Docker Compose..."
	@chmod +x backend/scripts/keycloak_bootstrap.sh
	@cd backend && docker compose up -d
	@echo "✅ Backend services started"


launch: back front ## Launch all services in production mode



# CLEANUP

clean-front: ## Clean frontend Docker resources
	@echo "💡 Starting frontend cleanup..."
	-docker stop mycelium-frontend 2>/dev/null || true
	-docker rm mycelium-frontend 2>/dev/null || true
	-docker rmi mycelium-frontend:latest 2>/dev/null || true
	-docker rmi $$(docker images --filter "reference=*/mycelium-frontend" -q) 2>/dev/null || true
	@echo "✅ Frontend cleanup completed"
clean-back: ## Clean backend Docker resources and volumes
	@echo "💡 Starting backend cleanup..."
	@echo "🗑️  Stopping and removing services..."
	-docker ps -a --filter "name=keycloak-" -q | xargs -r docker stop
	-docker ps -a --filter "name=keycloak-" -q | xargs -r docker rm
	-docker ps -a --filter "name=db-" -q | xargs -r docker stop
	-docker ps -a --filter "name=db-" -q | xargs -r docker rm
	@echo "🗑️  Removing postgres volume..."
	-docker volume rm backend_postgres-data 2>/dev/null || true
	@echo "✅ Backend cleanup completed"

clean: clean-front clean-back ## Clean all Docker resources and configuration files
	@echo "\n🗑️  Removing .env file..."
	-rm -f .env
	@echo "\n✅ All cleanup completed successfully"

.PHONY: clean clean-front clean-back


