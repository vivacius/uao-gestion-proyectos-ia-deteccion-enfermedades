"""Pruebas unitarias del cliente HTTP, helpers de scripts y contratos de despliegue M4."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import requests
import yaml

from scripts.run_mlflow_benchmark import create_synthetic_benchmark_sample
from scripts.validate_e2e_and_benchmark import (
    build_synthetic_leaf_jpeg,
    build_unsupported_gif,
    percentile,
    summarize_latencies,
)
from ui.api_client import fetch_api_health, request_image_prediction

ROOT = Path(__file__).resolve().parent.parent.parent


# --- Cliente HTTP desacoplado (ui/api_client.py) ---


def test_fetch_api_health_returns_success_when_model_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifica respuesta exitosa de fetch_api_health cuando model_available=True."""
    # Arrange
    mock_resp = MagicMock(status_code=200)
    mock_resp.json.return_value = {"status": "ok", "model_available": True}
    monkeypatch.setattr("ui.api_client.requests.get", lambda url, timeout: mock_resp)

    # Act
    res = fetch_api_health(base_url="http://127.0.0.1:8000/")

    # Assert
    assert res.success is True
    assert res.status_code == 200
    assert res.data == {"status": "ok", "model_available": True}


def test_fetch_api_health_fails_when_model_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifica manejo de servicio degradado cuando model_available=False."""
    # Arrange
    mock_resp = MagicMock(status_code=503)
    mock_resp.json.return_value = {"status": "degraded", "model_available": False, "detail": "Sin modelo"}
    monkeypatch.setattr("ui.api_client.requests.get", lambda url, timeout: mock_resp)

    # Act
    res = fetch_api_health(base_url="http://127.0.0.1:8000")

    # Assert
    assert res.success is False
    assert res.status_code == 503
    assert "Sin modelo" in (res.error_message or "")


@pytest.mark.parametrize(
    ("exc", "expected_fragment"),
    [
        (requests.ConnectionError("refused"), "No se pudo conectar"),
        (requests.Timeout("timed out"), "tardó demasiado"),
        (RuntimeError("boom"), "Error inesperado"),
    ],
)
def test_fetch_api_health_handles_network_exceptions(
    monkeypatch: pytest.MonkeyPatch,
    exc: Exception,
    expected_fragment: str,
) -> None:
    """Verifica captura controlada de ConnectionError, Timeout y errores genéricos."""

    # Arrange
    def _raise(*_args: object, **_kwargs: object) -> None:
        raise exc

    monkeypatch.setattr("ui.api_client.requests.get", _raise)

    # Act
    res = fetch_api_health(base_url="http://127.0.0.1:8000")

    # Assert
    assert res.success is False
    assert res.status_code == 0
    assert expected_fragment in (res.error_message or "")


def test_request_image_prediction_returns_payload_on_200(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifica envío multipart y retorno exitoso ante HTTP 200."""
    # Arrange
    mock_resp = MagicMock(status_code=200)
    mock_resp.json.return_value = {"predicted_category": "Tomato___healthy"}
    monkeypatch.setattr("ui.api_client.requests.post", lambda url, files, timeout: mock_resp)

    # Act
    res = request_image_prediction(b"jpeg-bytes", "leaf.jpg", base_url="http://localhost:8000/")

    # Assert
    assert res.success is True
    assert res.status_code == 200
    assert res.data == {"predicted_category": "Tomato___healthy"}


@pytest.mark.parametrize(
    ("status_code", "payload", "expected_text"),
    [
        (400, {"detail": "Imagen corrupta"}, "Imagen corrupta"),
        (415, {"detail": "Formato no soportado"}, "Formato no soportado"),
        (422, {"detail": [{"msg": "field required"}]}, "field required"),
        (500, {}, "código HTTP 500"),
    ],
)
def test_request_image_prediction_formats_http_errors(
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
    payload: dict[str, object],
    expected_text: str,
) -> None:
    """Verifica extracción de mensajes de error para respuestas HTTP 4xx/5xx."""
    # Arrange
    mock_resp = MagicMock(status_code=status_code)
    mock_resp.json.return_value = payload
    monkeypatch.setattr("ui.api_client.requests.post", lambda url, files, timeout: mock_resp)

    # Act
    res = request_image_prediction(b"bytes", "leaf.jpg")

    # Assert
    assert res.success is False
    assert res.status_code == status_code
    assert expected_text in (res.error_message or "")


def test_request_image_prediction_handles_non_json_error_body(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifica resiliencia cuando el servidor devuelve un cuerpo no JSON."""
    # Arrange
    mock_resp = MagicMock(status_code=502)
    mock_resp.json.side_effect = ValueError("not json")
    monkeypatch.setattr("ui.api_client.requests.post", lambda url, files, timeout: mock_resp)

    # Act
    res = request_image_prediction(b"bytes", "leaf.jpg")

    # Assert
    assert res.success is False
    assert res.status_code == 502
    assert "502" in (res.error_message or "")


@pytest.mark.parametrize(
    ("exc", "expected_fragment"),
    [
        (requests.ConnectionError("refused"), "No fue posible comunicarse"),
        (requests.Timeout("timeout"), "superó el tiempo máximo"),
        (OSError("socket closed"), "Ocurrió un error al enviar"),
    ],
)
def test_request_image_prediction_handles_transport_exceptions(
    monkeypatch: pytest.MonkeyPatch,
    exc: Exception,
    expected_fragment: str,
) -> None:
    """Verifica manejo seguro de fallos de red en POST /predict."""

    # Arrange
    def _raise(*_args: object, **_kwargs: object) -> None:
        raise exc

    monkeypatch.setattr("ui.api_client.requests.post", _raise)

    # Act
    res = request_image_prediction(b"bytes", "leaf.jpg")

    # Assert
    assert res.success is False
    assert res.status_code == 0
    assert expected_fragment in (res.error_message or "")


# --- Helpers de scripts (MLflow y E2E benchmarks) ---


@pytest.mark.parametrize(
    ("mode", "fmt", "spot_type"),
    [
        ("RGB", "JPEG", "none"),
        ("RGB", "JPEG", "brown"),
        ("RGB", "PNG", "yellow"),
        ("RGBA", "PNG", "brown"),
        ("L", "JPEG", "none"),
    ],
)
def test_create_synthetic_benchmark_sample_generates_non_empty_bytes(
    mode: str,
    fmt: str,
    spot_type: str,
) -> None:
    """Verifica generación determinista de muestras sintéticas para MLflow."""
    # Arrange / Act
    data = create_synthetic_benchmark_sample(224, 224, mode=mode, image_format=fmt, spot_type=spot_type)

    # Assert
    assert isinstance(data, bytes)
    assert len(data) > 100


def test_validate_e2e_synthetic_builders() -> None:
    """Verifica generadores de JPEG válido y GIF de rechazo en script E2E."""
    # Arrange / Act
    jpg = build_synthetic_leaf_jpeg()
    gif = build_unsupported_gif()

    # Assert
    assert jpg[:2] == b"\xff\xd8"
    assert gif[:3] == b"GIF"


@pytest.mark.parametrize(
    ("values", "pct", "expected"),
    [
        ([10.0, 20.0, 30.0, 40.0], 0.0, 10.0),
        ([10.0, 20.0, 30.0, 40.0], 50.0, 25.0),
        ([10.0, 20.0, 30.0, 40.0], 100.0, 40.0),
        ([42.5], 95.0, 42.5),
    ],
)
def test_percentile_computes_linear_interpolation(
    values: list[float],
    pct: float,
    expected: float,
) -> None:
    """Verifica cálculo exacto de percentiles lineales."""
    # Arrange / Act
    result = percentile(values, pct)

    # Assert
    assert result == pytest.approx(expected)


def test_summarize_latencies_computes_metrics_and_throughput() -> None:
    """Verifica resumen estadístico de latencias y throughput."""
    # Arrange
    samples = [50.0, 60.0, 70.0, 80.0]

    # Act
    summary = summarize_latencies(samples, wall_seconds=2.0)

    # Assert
    assert summary["n"] == 4.0
    assert summary["min_ms"] == 50.0
    assert summary["max_ms"] == 80.0
    assert summary["mean_ms"] == 65.0
    assert summary["throughput_rps"] == 2.0


# --- Contratos estáticos M4 (CI/CD, seguridad y gobernanza) ---


def test_gitlab_ci_defines_four_stages_and_coverage_gate() -> None:
    """Verifica las 4 etapas y el umbral de cobertura >= 85 % en .gitlab-ci.yml."""
    # Arrange
    content = (ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")
    parsed = yaml.safe_load(content)

    # Assert
    assert parsed["stages"] == ["quality", "test", "build", "deploy"]
    assert "--cov-fail-under=85" in content


def test_gitlab_ci_deploys_and_tags_latest_only_on_default_branch() -> None:
    """Verifica que solo main ($CI_DEFAULT_BRANCH) despliega y publica :latest."""
    # Arrange
    content = (ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")
    parsed = yaml.safe_load(content)
    deploy_job = parsed["deploy_vps"]
    build_script = "\n".join(parsed["build_docker"]["script"])
    deploy_script = "\n".join(deploy_job["script"])

    # Assert
    assert deploy_job["resource_group"] == "production"
    assert deploy_job["environment"]["name"] == "production"
    assert "IMAGE_TAG=${CI_COMMIT_SHA}" in deploy_script
    assert deploy_job["rules"] == [
        {"if": "$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH && $DEPLOY_HOST", "when": "on_success"},
        {"when": "never"},
    ]
    assert 'if [ "$CI_COMMIT_BRANCH" = "$CI_DEFAULT_BRANCH" ]; then' in build_script
    assert 'docker push "$CI_REGISTRY_IMAGE:latest"' in build_script


def test_github_mirror_workflow_forbids_force_push_and_url_tokens() -> None:
    """Verifica que mirror-to-gitlab.yml no usa --force ni incrusta tokens en la URL."""
    # Arrange
    content = (ROOT / ".github" / "workflows" / "mirror-to-gitlab.yml").read_text(encoding="utf-8")

    # Assert
    assert "--force" not in content
    assert "oauth2:${GITLAB_TOKEN}" not in content


def test_prod_compose_does_not_expose_api_port_8000_publicly() -> None:
    """Verifica que docker-compose.prod.yml no publica el puerto 8000 al host."""
    # Arrange
    content = (ROOT / "deploy" / "docker-compose.prod.yml").read_text(encoding="utf-8")
    parsed = yaml.safe_load(content)
    api_service = parsed["services"]["api"]

    # Assert
    assert "ports" not in api_service


def test_m4_governance_and_model_card_artifacts_exist() -> None:
    """Verifica presencia de artefactos clave de gobernanza y Model Card."""
    # Arrange / Act / Assert
    assert (ROOT / "docs" / "model-card.md").is_file()
    assert (ROOT / "docs" / "academic-compliance-matrix.md").is_file()
    assert (ROOT / "Makefile").is_file()
    assert (ROOT / "pyproject.toml").is_file()
