"""Pruebas unitarias para el endpoint GET /model-info y el esquema ModelInfoResponse."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.routing import APIRoute

from api.main import app, model_info
from api.schemas import ModelInfoResponse
from src.exceptions import ModelLoadError


@pytest.fixture
def mock_model_bundle():
    """Genera un doble de prueba para ModelBundle sin tocar disco ni cargar pesos reales."""
    bundle = MagicMock()
    bundle.architecture = "Dinov2ForImageClassification"
    bundle.device = "cpu"
    bundle.id2label = {i: f"Clase_{i}" for i in range(38)}
    bundle.model_dir = Path("/app/modelo_plantas")
    return bundle


@pytest.mark.unit
def test_model_info_route_registration_in_app() -> None:
    """Verifica que la ruta GET /model-info esté registrada correctamente en la app FastAPI."""
    target_route = next(
        (route for route in app.routes if isinstance(route, APIRoute) and route.path == "/model-info"),
        None,
    )
    assert target_route is not None, "La ruta /model-info no está registrada en FastAPI."
    assert "GET" in target_route.methods
    assert target_route.response_model is ModelInfoResponse
    assert target_route.summary == "Consultar metadatos e información técnica del modelo"
    assert "Información del Modelo" in target_route.tags


@pytest.mark.unit
def test_get_model_info_success_http_200(mock_model_bundle) -> None:
    """Verifica que model_info retorne metadatos completos y modelo disponible cuando está cargado."""
    # Arrange
    with patch("api.main.get_model_bundle", return_value=mock_model_bundle):
        # Act
        response = model_info()

    # Assert
    assert isinstance(response, ModelInfoResponse)
    assert response.model_name == "rodynaemad/plant-disease-dinov2-small"
    assert response.architecture == "Dinov2ForImageClassification"
    assert response.device == "cpu"
    assert response.num_classes == 38
    assert response.model_available is True
    assert response.model_path == str(Path("/app/modelo_plantas"))


@pytest.mark.unit
def test_get_model_info_structure_and_types(mock_model_bundle) -> None:
    """Verifica que los tipos y campos obligatorios del contrato JSON se cumplan estrictamente."""
    # Arrange
    with patch("api.main.get_model_bundle", return_value=mock_model_bundle):
        # Act
        response = model_info()
        data = response.model_dump()

    # Assert
    assert isinstance(data["model_name"], str)
    assert isinstance(data["architecture"], str)
    assert isinstance(data["device"], str)
    assert isinstance(data["num_classes"], int)
    assert isinstance(data["model_available"], bool)
    assert isinstance(data["model_path"], str)

    # Validar serialización JSON pura
    json_str = response.model_dump_json()
    assert '"model_available":true' in json_str or '"model_available": true' in json_str


@pytest.mark.unit
def test_get_model_info_reutiliza_modelo_sin_recarga_adicional(mock_model_bundle) -> None:
    """Verifica que múltiples llamadas a model_info reutilicen la instancia existente."""
    # Arrange
    with patch("api.main.get_model_bundle", return_value=mock_model_bundle) as mock_get:
        # Act
        resp1 = model_info()
        resp2 = model_info()

    # Assert
    assert resp1.model_available is True
    assert resp2.model_available is True
    assert mock_get.call_count == 2


@pytest.mark.unit
def test_get_model_info_handles_model_unavailable_controlled() -> None:
    """Verifica que model_info maneje controladamente la ausencia del modelo sin fallar."""
    # Arrange
    with patch(
        "api.main.get_model_bundle",
        side_effect=ModelLoadError("Pesos de safetensors ausentes"),
    ):
        # Act
        response = model_info()

    # Assert
    assert isinstance(response, ModelInfoResponse)
    assert response.model_available is False
    assert response.architecture is None
    assert response.num_classes == 0
    assert response.model_path is None
    assert response.model_name == "rodynaemad/plant-disease-dinov2-small"
    assert response.device == "cpu"
