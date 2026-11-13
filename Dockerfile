# Stage 1: obtain a pinned toolchain without leaving uv in the runtime image.
FROM ghcr.io/astral-sh/uv:0.6.14 AS uv

# Stage 2: resolve production dependencies from the lockfile in an isolated venv.
FROM python:3.13-slim AS builder

COPY --from=uv /uv /uvx /bin/

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-install-project --no-dev

# Stage 3: ship only the application, production venv, and local model artifacts.
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_DIR=/app/modelo_plantas \
    API_HOST=0.0.0.0 \
    API_PORT=8000 \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY src/ ./src/
COPY api/ ./api/
COPY config.json preprocessor_config.json model.safetensors ./modelo_plantas/

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
