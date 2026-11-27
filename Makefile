# Makefile académico M1–M4 — Detección Fitosanitaria con DINOv2-small
# Compatible con GNU Make en Linux y Windows 11 (sin sintaxis exclusiva de bash).
# Requisitos base: GNU Make, uv (Python 3.13) y Docker Desktop/Engine para targets docker-*.

.DEFAULT_GOAL := help

UV             ?= uv
DOCKER         ?= docker
DOCKER_COMPOSE ?= $(DOCKER) compose
API_HOST       ?= 127.0.0.1
API_PORT       ?= 8000
MLFLOW_HOST    ?= 127.0.0.1
MLFLOW_PORT    ?= 5050
IMAGE_NAME     ?= plant-disease-classifier
IMAGE_TAG      ?= 1.0.0

.PHONY: help sync lint format-check test-unit test-integration test coverage \
        build api mlflow docker-build docker-up docker-down docker-ps health ci

help: ## Muestra los targets disponibles y sus requisitos
	@echo "Targets disponibles (Grupo 2 - UAO | M1-M4):"
	@echo "  make sync             Sincroniza entorno determinista (.venv) con uv sync --frozen"
	@echo "  make lint             Ejecuta analisis estatico PEP 8 con Ruff"
	@echo "  make format-check     Verifica formateo con Ruff (--check)"
	@echo "  make test-unit        Ejecuta pruebas unitarias rapidas (con mocks)"
	@echo "  make test-integration Ejecuta pruebas de integracion (requiere model.safetensors)"
	@echo "  make test             Ejecuta test-unit + test-integration"
	@echo "  make coverage         Ejecuta unitarias con reporte de cobertura (src/ y api/)"
	@echo "  make build            Construye paquetes Wheel y sdist en dist/ (uv build)"
	@echo "  make api              Inicia servidor FastAPI en http://$(API_HOST):$(API_PORT) (requiere pesos)"
	@echo "  make mlflow           Inicia MLflow UI local en http://$(MLFLOW_HOST):$(MLFLOW_PORT)"
	@echo "  make docker-build     Construye imagen Docker CPU (requiere Docker daemon y pesos)"
	@echo "  make docker-up        Levanta api + web Nginx con Docker Compose"
	@echo "  make docker-down      Detiene los contenedores de Docker Compose"
	@echo "  make docker-ps        Lista el estado de los contenedores de Docker Compose"
	@echo "  make health           Consulta GET /health en http://$(API_HOST):$(API_PORT)/health"
	@echo "  make ci               Ejecuta el Quality Gate completo (lint + format-check + coverage)"

sync: ## Instala dependencias deterministas desde uv.lock (sin pip ni requirements.txt)
	$(UV) sync --frozen

lint: ## Verifica reglas de estilo y errores estaticos con Ruff
	$(UV) run ruff check .

format-check: ## Verifica formato de codigo con Ruff sin modificar archivos
	$(UV) run ruff format --check .

test-unit: ## Ejecuta pruebas unitarias aisladas (sin pesos reales)
	$(UV) run pytest tests/unit -v

test-integration: ## Ejecuta pruebas de integracion con DINOv2 real en CPU
	$(UV) run pytest tests/integration -v

test: test-unit test-integration ## Ejecuta la suite completa de pruebas (unitarias e integracion)

coverage: ## Ejecuta pruebas unitarias con cobertura combinada en src/ y api/
	$(UV) run pytest tests/unit -v --cov=src --cov=api --cov-report=term-missing

build: ## Empaqueta distribucion Wheel y sdist mediante uv build
	$(UV) build

api: ## Inicia API FastAPI y frontend estatico en http://127.0.0.1:8000
	$(UV) run uvicorn api.main:app --host $(API_HOST) --port $(API_PORT)

mlflow: ## Inicia servidor local de MLflow UI sobre mlflow_tracking.db (puerto 5050)
	$(UV) run mlflow server --backend-store-uri sqlite:///mlflow_tracking.db --default-artifact-root ./mlflow_data/benchmark_runs --host $(MLFLOW_HOST) --port $(MLFLOW_PORT)

docker-build: ## Construye imagen Docker CPU multi-etapa (requiere Docker daemon activo)
	$(DOCKER) build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-up: ## Inicia servicios api y web (Nginx) en segundo plano
	$(DOCKER_COMPOSE) up -d --build

docker-down: ## Detiene servicios de Docker Compose sin eliminar volumenes locales
	$(DOCKER_COMPOSE) down

docker-ps: ## Muestra el estado actual de los servicios Docker Compose
	$(DOCKER_COMPOSE) ps

health: ## Verifica disponibilidad del endpoint GET /health
	$(UV) run python -c "import urllib.request; print(urllib.request.urlopen('http://$(API_HOST):$(API_PORT)/health', timeout=5).read().decode())"

ci: lint format-check coverage ## Replica localmente el Quality Gate CI (M3)
