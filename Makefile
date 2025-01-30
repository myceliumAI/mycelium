# Load environment variables at the start of each target that needs them
define load_env
	@if [ ! -f $(PWD)/.env ]; then \
		echo "⚠️  No .env file found! Please run 'make setup' first"; \
		exit 1; \
	fi
	$(eval include $(PWD)/.env)
	$(eval export)
endef

.PHONY: help check check-dev check-prod setup clean clean-front clean-back clean-db clean-api clean-keycloak launch launch-dev front back front-dev back-dev build-front build-back build-api build-keycloak build-db build api api-dev keycloak db test test-front test-back test-back-coverage lint lint-fix format lint-back lint-front lint-fix-back lint-fix-front format-back format-front format-fix format-fix-back format-fix-front

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
	@echo '  build           - Build all backend images locally'
	@echo ''
	@echo '🧪 Tests:'
	@echo '  test            - Run all tests'
	@echo '  test-front      - Run frontend tests'
	@echo '  test-back       - Run all backend tests (unittest + pytest)'
	@echo '  test-back-coverage - Generate and display test coverage report'
	@echo '  lint            - Run Ruff linter'
	@echo '  lint-back       - Check code quality and style for backend'
	@echo '  lint-front      - Check code quality and style for frontend'
	@echo '  lint-fix        - Run Ruff linter with auto-fix'
	@echo '  lint-fix-back   - Auto-fix linting issues for backend'
	@echo '  lint-fix-front  - Auto-fix linting issues for frontend'
	@echo '  format          - Run all formatters (ruff)'
	@echo '  format-back     - Format backend code'
	@echo '  format-front    - Format frontend code'
	@echo '  format-fix      - Auto-fix formatting issues for both backend and frontend'
	@echo '  format-fix-back - Auto-fix backend formatting issues'
	@echo '  format-fix-front - Auto-fix frontend formatting issues'


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
		--add-host=host.docker.internal:host-gateway \
		mycelium-frontend:latest
	@echo "✅ Frontend container started on port ${FRONTEND_PORT}"

front-dev: ## Launch the frontend application
	$(call load_env)
	@cd mycelium && \
	yarn install && \
	VITE_KC_HOST=${KC_HOST} \
	VITE_KC_PORT=${KC_PORT} \
	VITE_KC_REALM=${KC_REALM} \
	VITE_KC_CLIENT_ID=${KC_CLIENT_ID} \
	VITE_API_HOST=${API_HOST} \
	VITE_API_PORT=${API_PORT} \
	VITE_FRONTEND_PORT=${FRONTEND_PORT} \
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
		--add-host=host.docker.internal:host-gateway \
		mycelium-backend-api:latest
	@echo "✅ Backend API service started"


api-dev: ## Launch the backend API service in development mode
	$(call load_env)
	@cd backend/api && \
	poetry lock && \
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
		--add-host=host.docker.internal:host-gateway \
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
		--build-arg POSTGRES_SOCKET=${POSTGRES_SOCKET} \
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

build: build-api build-keycloak build-db build-front ## Build all images locally
	@echo "✅ All images built successfully"

# # # # # # 
#  TEST   #
# # # # # # 

test-front: ## Run frontend tests
	@echo "💡 Running frontend tests..."
	$(call load_env)
	@echo "⚠️  No frontend tests implemented yet"
	@exit 0

test-back: ## Run all backend tests
	@echo "💡 Running all backend tests..."
	$(call load_env)
	@cd backend/api && \
	poetry lock && \
	poetry install && \
	echo "Running unittest tests..." && \
	poetry run python -m unittest tests/tools_test.py -v && \
	echo "\nRunning pytest tests..." && \
	poetry run pytest tests/ -v
	@echo "✅ Backend tests completed"

test-back-coverage: ## Generate and display test coverage report
	@echo "💡 Generating test coverage report..."
	$(call load_env)
	@cd backend/api && \
	poetry lock && \
	poetry install && \
	poetry run pytest --cov=app --cov-report=term-missing
	@echo "✅ Coverage report generated"

test: test-front test-back test-back-coverage ## Run all tests and display coverage
	@echo "✅ All tests, linting and coverage report completed"


# # # # # # #
#  LINTING  #
# # # # # # #


# BACKEND

lint-back: ## Check code quality and style for backend
	@echo "💡 Running Ruff linter on backend..."
	@cd backend/api && \
	poetry lock && \
	poetry install && \
	poetry run ruff check .
	@echo "✅ Backend linting completed"

lint-fix-back: ## Auto-fix linting issues for backend
	@echo "💡 Fixing backend linting issues..."
	@cd backend/api && \
	poetry lock && \
	poetry install && \
	poetry run ruff check --fix .
	@echo "✅ Backend auto-fix completed"

# FRONTEND

lint-front: ## Check code quality and style for frontend
	@echo "💡 Running ESLint on frontend..."
	@cd mycelium && \
	yarn install && \
	yarn lint
	@echo "✅ Frontend linting completed"

lint-fix-front: ## Auto-fix linting issues for frontend
	@echo "💡 Fixing frontend linting issues..."
	@cd mycelium && \
	yarn install && \
	yarn lint --fix
	@echo "✅ Frontend auto-fix completed"

# ALLL

lint: lint-back lint-front ## Check code quality and style for both backend and frontend
	@echo "✅ All linting completed"

lint-fix: lint-fix-back lint-fix-front ## Auto-fix linting issues for both backend and frontend
	@echo "✅ All auto-fix completed"


# # # # # # # #
#  FORMATTING #
# # # # # # # #


# BACKEND

format-back: ## Format backend code
	@echo "💡 Formatting backend code..."
	@cd backend/api && \
	poetry lock && \
	poetry install && \
	poetry run ruff format . --check
	@echo "✅ Backend formatting completed"

format-fix-back: ## Auto-fix backend formatting issues
	@echo "💡 Formatting backend code..."
	@cd backend/api && \
	poetry lock && \
	poetry install && \
	poetry run ruff format .
	@echo "✅ Backend formatting completed"


# ALL

format: format-back ## Format code for backend
	@echo "✅ All formatting completed"

format-fix: format-fix-back ## Auto-fix formatting issues for backend
	@echo "✅ All formatting fixes completed"
