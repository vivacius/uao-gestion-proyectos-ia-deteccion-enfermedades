"""Pruebas de contrato para el empaquetado Wheel y la contenerización de HU-08."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[2]


def test_pyproject_exposes_buildable_packages_and_web_assets() -> None:
    """Verifica que uv build incluya src, api, ui y los activos estáticos del frontend."""
    # Arrange
    pyproject_path = ROOT / "pyproject.toml"

    # Act
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    build_system = data["build-system"]
    setuptools_config = data["tool"]["setuptools"]

    # Assert
    assert build_system["build-backend"] == "setuptools.build_meta"
    assert any(requirement.startswith("setuptools>=") for requirement in build_system["requires"])
    assert {"src", "api", "ui", "ui.web"} <= set(setuptools_config["packages"])
    assert "static/*" in setuptools_config["package-data"]["ui.web"]


def test_dockerfile_is_multistage_and_includes_runtime_assets() -> None:
    """Verifica la imagen CPU multi-etapa, el usuario no root y los activos necesarios."""
    # Arrange
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")

    # Act & Assert
    assert " AS builder" in dockerfile
    assert " AS runtime" in dockerfile
    assert "COPY --from=builder /opt/venv /opt/venv" in dockerfile
    assert "COPY --chown=appuser:appuser ui/web/static ./ui/web/static" in dockerfile
    assert "model.safetensors" in dockerfile
    assert "USER appuser" in dockerfile
    assert "HEALTHCHECK" in dockerfile
    assert 'CMD ["uvicorn", "api.main:app"' in dockerfile
    assert "streamlit" not in dockerfile.lower()


def test_compose_orchestrates_api_and_web_with_health_gate() -> None:
    """Verifica que Compose levante API y frontend web en red interna compartida."""
    # Arrange
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    nginx = (ROOT / "deploy" / "nginx.conf").read_text(encoding="utf-8")

    # Act & Assert
    assert "api:" in compose
    assert "web:" in compose
    assert '"8000:8000"' in compose
    assert '"8080:80"' in compose
    assert "nginx:1.27-alpine" in compose
    assert "condition: service_healthy" in compose
    assert "streamlit" not in compose.lower()
    assert "proxy_pass http://api:8000;" in nginx
    assert "try_files $uri $uri/ /index.html;" in nginx
