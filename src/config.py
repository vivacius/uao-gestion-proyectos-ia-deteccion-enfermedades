"""Configuración centralizada de la aplicación."""

from __future__ import annotations

import os
from pathlib import Path

# Directorio raíz del proyecto
BASE_DIR: Path = Path(__file__).resolve().parent.parent


def resolve_model_dir() -> Path:
    """Resuelve la ruta local donde se encuentran los archivos del modelo preentrenado.

    Prioridad:
    1. Variable de entorno ``MODEL_DIR`` (si está definida).
    2. Carpeta ``modelo_plantas/`` dentro de la raíz del proyecto.
    3. Raíz del proyecto si los artefactos del modelo están directamente allí.
    """
    env_model_dir = os.getenv("MODEL_DIR")
    if env_model_dir:
        return Path(env_model_dir).resolve()

    subdir_candidate = BASE_DIR / "modelo_plantas"
    if (subdir_candidate / "config.json").is_file() and (
        subdir_candidate / "model.safetensors"
    ).is_file():
        return subdir_candidate

    if (BASE_DIR / "config.json").is_file() and (
        BASE_DIR / "model.safetensors"
    ).is_file():
        return BASE_DIR

    return subdir_candidate


MODEL_DIR: Path = resolve_model_dir()

# Archivos obligatorios del modelo local de Hugging Face
REQUIRED_MODEL_FILES: tuple[str, ...] = (
    "config.json",
    "preprocessor_config.json",
    "model.safetensors",
)

# Dispositivo de ejecución (exclusivamente CPU según requerimiento)
DEVICE: str = "cpu"

# Parámetros de validación de imágenes
ALLOWED_EXTENSIONS: frozenset[str] = frozenset({".jpg", ".jpeg", ".png"})
ALLOWED_MIME_TYPES: frozenset[str] = frozenset(
    {"image/jpeg", "image/jpg", "image/png", "application/octet-stream"}
)
ALLOWED_PIL_FORMATS: frozenset[str] = frozenset({"JPEG", "JPG", "PNG"})

MAX_IMAGE_SIZE_MB: int = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
MAX_IMAGE_SIZE_BYTES: int = MAX_IMAGE_SIZE_MB * 1024 * 1024
MIN_IMAGE_DIMENSION: int = 16

# Parámetros de inferencia
DEFAULT_TOP_K: int = 3
NUM_EXPECTED_CLASSES: int = 38

# Configuración de red para API REST y cliente Streamlit
API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "8000"))
API_BASE_URL: str = os.getenv("API_BASE_URL", f"http://127.0.0.1:{API_PORT}")

# Aviso agronómico obligatorio
AGRONOMIC_DISCLAIMER: str = (
    "Las predicciones generadas por este sistema de inteligencia artificial son "
    "estrictamente orientativas y de apoyo preliminar; no sustituyen un diagnóstico "
    "ni una evaluación agronómica o fitopatológica profesional."
)
