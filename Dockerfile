# syntax=docker/dockerfile:1.7

# Etapa 1: binario oficial de uv fijado para resolver dependencias reproducibles.
FROM ghcr.io/astral-sh/uv:0.13.1 AS uv

# Etapa 2: construir el entorno virtual de producción desde uv.lock.
FROM python:3.13-slim AS builder

COPY --from=uv /uv /uvx /bin/

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-install-project --no-dev

# Etapa 3: imagen final mínima, sin uv ni dependencias de desarrollo.
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    MODEL_DIR=/app/modelo_plantas \
    API_HOST=0.0.0.0 \
    API_PORT=8000

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser api/ ./api/
COPY --chown=appuser:appuser ui/web/static ./ui/web/static
COPY --chown=appuser:appuser config.json preprocessor_config.json model.safetensors ./modelo_plantas/

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
