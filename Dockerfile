# Imagen base oficial de Python 3.13 ligera para ejecución en CPU
FROM python:3.13-slim

# Copiar el binario oficial de uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Variables de entorno para ejecución determinista y sin buffering en CPU
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    MODEL_DIR=/app/modelo_plantas \
    API_HOST=0.0.0.0 \
    API_PORT=8000 \
    API_BASE_URL=http://127.0.0.1:8000

WORKDIR /app

# 1. Instalar dependencias de Python de forma reproducible usando uv.lock
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-install-project --no-dev

# 2. Copiar el código fuente de la aplicación y archivos del proyecto
COPY src/ ./src/
COPY api/ ./api/
COPY ui/ ./ui/
COPY tests/ ./tests/
COPY README.md ./

# 3. Copiar los artefactos locales del modelo a /app/modelo_plantas
COPY config.json preprocessor_config.json model.safetensors ./modelo_plantas/

# Exponer puertos de FastAPI (8000) y Streamlit (8501)
EXPOSE 8000 8501

# Comando por defecto: inicia la API FastAPI en el puerto 8000
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
