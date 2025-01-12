# Load environment variables at the start of each target that needs them
define load_env
	$(eval include $(PWD)/.env)
	$(eval export)
endef

.PHONY: help check check-dev check-prod setup clean clean-front clean-back clean-db clean-api clean-keycloak launch launch-dev front back front-dev back-dev build-front build-back build-api build-keycloak build-db build-all api api-dev keycloak db

help: ## Show this help message
	@echo '🔧 Setup & Utils:'
	@echo '  check           - Check all services'
	@echo '  check-dev       - Check development dependencies'
	@echo '  check-prod      - Check production/deployment dependencies'
	@echo '  setup           - Create .env file from example'
	@echo '  clean           - Clean all Docker resources and configuration files'
	@echo '  clean-front     - Clean frontend Docker resources'
	@echo '  clean-back      - Clean backend Docker resources and volumes'
	@echo '  clean-db        - Clean backend DB Docker resources and volumes'
	@echo '  clean-api       - Clean backend API Docker resources'
	@echo '  clean-keycloak  - Clean backend Keycloak Docker resources'
	@echo ''
	@echo '🚀 Running Applications:'
	@echo '  launch          - Launch all services in production mode'
	@echo '  launch-dev      - Launch all services in development mode'
	@echo '  front           - Run frontend from local image'
	@echo '  back            - Run backend services using Docker Compose'
	@echo '  front-dev       - Launch the frontend application'
	@echo '  back-dev        - Launch the backend in development mode (API local, other services in Docker)'
	@echo '  api             - Run backend API service'
	@echo '  api-dev         - Launch the backend API service in development mode'
	@echo '  keycloak        - Run backend Keycloak service'
	@echo '  db              - Run backend DB service'
	@echo ''
	@echo '📦 Docker Operations:'
	@echo '  build-front     - Build frontend Docker image locally'
	@echo '  build-back      - Build backend Docker images locally'
	@echo '  build-api       - Build backend API Docker image locally'
	@echo '  build-keycloak  - Build backend Keycloak Docker image locally'
	@echo '  build-db        - Build backend DB Docker image locally'
	@echo '  build-all       - Build all backend images locally'


# # # # # # 
#  SETUP  #
# # # # # # 

# CHECK

check: check-dev check-prod ## Check all services

check-dev: ## Check development dependencies
	@chmod +x ./scripts/check_deps.sh
	@./scripts/check_deps.sh dev

check-prod: ## Check production dependencies
	@chmod +x ./scripts/check_deps.sh
	@./scripts/check_deps.sh deploy

# SETUP

setup: ## Create .env file from example
	@chmod +x ./scripts/setup_env.sh
	@./scripts/setup_env.sh

# # # # # # 
#  CLEAN  #
# # # # # # 

# FRONTEND

clean-front: ## Clean frontend Docker resources
	@echo "💡 Starting frontend cleanup..."
	-docker stop $$(docker ps -a -q --filter "name=mycelium-frontend") 2>/dev/null || true
	-docker rm $$(docker ps -a -q --filter "name=mycelium-frontend") 2>/dev/null || true
	-docker rmi $$(docker images --filter "reference=mycelium-frontend*" -q) 2>/dev/null || true
	@echo "✅ Frontend cleanup completed"

# BACKEND

clean-db: ## Clean backend DB Docker resources and volumes
	@echo "💡 Starting DB cleanup..."
	-docker stop $$(docker ps -a -q --filter "name=mycelium-backend-db") 2>/dev/null || true
	-docker rm $$(docker ps -a -q --filter "name=mycelium-backend-db") 2>/dev/null || true
	-docker rmi $$(docker images --filter "reference=mycelium-backend-db*" -q) 2>/dev/null || true
	-docker volume rm $$(docker volume ls -q -f name=mycelium-backend_db) 2>/dev/null || true
	@echo "✅ DB cleanup completed"

clean-api: ## Clean backend API Docker resources
	@echo "💡 Starting API cleanup..."
	-docker stop $$(docker ps -a -q --filter "name=mycelium-backend-api") 2>/dev/null || true
	-docker rm $$(docker ps -a -q --filter "name=mycelium-backend-api") 2>/dev/null || true
	-docker rmi $$(docker images --filter "reference=mycelium-backend-api*" -q) 2>/dev/null || true
	@echo "✅ API cleanup completed"

clean-keycloak: ## Clean backend Keycloak Docker resources
	@echo "💡 Starting Keycloak cleanup..."
	-docker stop $$(docker ps -a -q --filter "name=mycelium-backend-keycloak") 2>/dev/null || true
	-docker rm $$(docker ps -a -q --filter "name=mycelium-backend-keycloak") 2>/dev/null || true
	-docker rmi $$(docker images --filter "reference=mycelium-backend-keycloak*" -q) 2>/dev/null || true
	@echo "✅ Keycloak cleanup completed"


clean-back: clean-db clean-api clean-keycloak ## Clean backend Docker resources and volumes

# ALL

clean: clean-front clean-back ## Clean all Docker resources and configuration files
	@echo "\n🗑️  Removing .env file..."
	-rm -f .env
	@echo "\n✅ All cleanup completed successfully"

# # # # # # 
#  RUN    #
# # # # # # 

# FRONTEND

front: build-front ## Run frontend from local image
	$(call load_env)
	@echo "💡 Starting frontend container from local image..."
	-docker stop mycelium-frontend 2>/dev/null || true
	-docker rm mycelium-frontend 2>/dev/null || true
	@docker run -p ${FRONTEND_PORT}:${FRONTEND_PORT} -d \
		--name mycelium-frontend \
		--env-file .env \
		mycelium-frontend:latest
	@echo "✅ Frontend container started on port ${FRONTEND_PORT}"

front-dev: ## Launch the frontend application
	$(call load_env)
	@cd mycelium && \
	yarn install && \
	yarn cross-env \
		VUE_CLI_SERVICE_CONFIG_PATH=./config/vue.config.js \
		VUE_APP_KC_HOST=${KC_HOST} \
		VUE_APP_KC_PORT=${KC_PORT} \
		VUE_APP_KC_REALM=${KC_REALM} \
		VUE_APP_KC_CLIENT_ID=${KC_CLIENT_ID} \
		VUE_APP_API_HOST=${API_HOST} \
		VUE_APP_API_PORT=${API_PORT} \
		yarn serve

# BACKEND


api: build-api ## Run backend API service
	$(call load_env)
	@echo "💡 Starting backend API service from local image..."
	-docker stop mycelium-backend-api 2>/dev/null || true
	-docker rm mycelium-backend-api 2>/dev/null || true
	@docker run -p ${API_PORT}:${API_PORT} -d \
		--name mycelium-backend-api \
		--env-file .env \
		mycelium-backend-api:latest
	@echo "✅ Backend API service started"


api-dev: ## Launch the backend API service in development mode
	$(call load_env)
	@cd backend/api && \
	poetry lock --no-update && \
	poetry install && \
	poetry run uvicorn app.main:app --port ${API_PORT} --host 0.0.0.0 --reload


keycloak: build-keycloak ## Run backend Keycloak service
	$(call load_env)
	@echo "💡 Starting backend Keycloak service from local image..."
	-docker stop mycelium-backend-keycloak 2>/dev/null || true
	-docker rm mycelium-backend-keycloak 2>/dev/null || true
	@docker run -p ${KC_PORT}:8080 -d \
		--name mycelium-backend-keycloak \
		--env KC_DB_PASSWORD=${POSTGRES_PASSWORD} \
		--env-file .env \
		mycelium-backend-keycloak:latest
	@echo "✅ Backend Keycloak service started"


db: build-db ## Run backend DB service
	$(call load_env)
	@echo "💡 Starting backend DB service from local image..."
	-docker stop mycelium-backend-db 2>/dev/null || true
	-docker rm mycelium-backend-db 2>/dev/null || true
	@docker run -p ${POSTGRES_PORT}:${POSTGRES_PORT} -d \
		--name mycelium-backend-db \
		--env-file .env \
		mycelium-backend-db:latest
	@echo "✅ Backend DB service started"

back: build-back ## Run backend services using Docker Compose
	$(call load_env)
	@echo "💡 Starting all backend services with Docker Compose..."
	@cd backend && docker compose --env-file ../.env -p mycelium-backend up -d
	@echo "✅ All backend services started successfully"

back-dev: build-back ## Launch the backend in development mode (API local, other services in Docker)
	$(call load_env)
	@echo "💡 Starting DB and Keycloak services with Docker Compose..."
	@cd backend && docker compose --env-file ../.env -p mycelium-backend up -d db keycloak
	@echo "💡 Starting API in development mode..."
	@$(MAKE) api-dev
	@echo "✅ Backend development environment started successfully"

# ALL

launch: back front ## Launch all services in production mode

launch-dev: back-dev front-dev ## Launch all services in development mode

# # # # # # 
#  BUILD  #
# # # # # # 

# FRONTEND

build-front: ## Build frontend Docker image locally
	$(call load_env)
	@echo "💡 Building frontend image locally..."
	@docker build \
		--build-arg API_HOST=${API_HOST} \
		--build-arg API_PORT=${API_PORT} \
		--build-arg KC_PORT=${KC_PORT} \
		--build-arg KC_REALM=${KC_REALM} \
		--build-arg KC_CLIENT_ID=${KC_CLIENT_ID} \
		--build-arg FRONTEND_HOST=${FRONTEND_HOST} \
		--build-arg FRONTEND_PORT=${FRONTEND_PORT} \
		--build-arg NGINX_LOG_LEVEL=${NGINX_LOG_LEVEL} \
		-t mycelium-frontend:latest ./mycelium
	@echo "✅ Frontend image built successfully"

# BACKEND

build-back: ## Build backend Docker images locally
	$(call load_env)
	@echo "💡 Building backend images locally..."
	@cd backend && docker compose -p mycelium-backend build
	@echo "✅ Backend images built successfully"

build-api: ## Build backend API Docker image locally
	$(call load_env)
	@echo "💡 Building backend API image locally..."
	@cd backend/api && docker build \
		--build-arg API_PORT=${API_PORT} \
		--build-arg POSTGRES_PORT=${POSTGRES_PORT} \
		--build-arg POSTGRES_HOST=${POSTGRES_HOST} \
		--build-arg POSTGRES_USER=${POSTGRES_USER} \
		--build-arg POSTGRES_DB=${POSTGRES_DB} \
		-t mycelium-backend-api:latest .
	@echo "✅ Backend API image built successfully"

build-keycloak: ## Build backend Keycloak Docker image locally
	$(call load_env)
	@echo "💡 Building backend Keycloak image locally..."
	@cd backend/keycloak && docker build \
		--build-arg KC_PORT=${KC_PORT} \
		--build-arg KC_MANAGEMENT_PORT=${KC_MANAGEMENT_PORT} \
		--build-arg KC_REALM=${KC_REALM} \
		--build-arg KC_BOOTSTRAP_ADMIN_USERNAME=${KC_BOOTSTRAP_ADMIN_USERNAME} \
		--build-arg POSTGRES_USER=${POSTGRES_USER} \
		--build-arg POSTGRES_DB=${POSTGRES_DB} \
		--build-arg POSTGRES_PORT=${POSTGRES_PORT} \
		--build-arg POSTGRES_HOST=${POSTGRES_HOST} \
		--build-arg FRONTEND_HOST=${FRONTEND_HOST} \
		--build-arg FRONTEND_PORT=${FRONTEND_PORT} \
		-t mycelium-backend-keycloak:latest .
	@echo "✅ Backend Keycloak image built successfully"

build-db: ## Build backend DB Docker image locally
	$(call load_env)
	@echo "💡 Building backend DB image locally..."
	@cd backend/database && docker build \
		--build-arg POSTGRES_USER=${POSTGRES_USER} \
		--build-arg POSTGRES_DB=${POSTGRES_DB} \
		--build-arg POSTGRES_PORT=${POSTGRES_PORT} \
		-t mycelium-backend-db:latest .
	@echo "✅ Backend DB image built successfully"

# ALL

build-all: build-api build-keycloak build-db ## Build all backend images locally
	@echo "✅ All backend images built successfully"
