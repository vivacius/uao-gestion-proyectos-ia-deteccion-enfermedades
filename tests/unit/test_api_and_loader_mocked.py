"""Pruebas unitarias con mocks para cargador del modelo, manejo de errores en API y cliente Streamlit."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests
from fastapi.testclient import TestClient

from api.main import app
from src.config import resolve_model_dir
from src.exceptions import InferenceError, ModelLoadError, PlantDiseaseAppError
from src.model_loader import clear_model_cache, load_model_from_disk, verify_model_files
from src.postprocessing import ClassificationResult, TopPredictionItem
from ui.api_client import fetch_api_health, request_image_prediction


@pytest.mark.unit
def test_resolve_model_dir_respects_env_var(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica que resolve_model_dir priorice la variable de entorno MODEL_DIR."""
    monkeypatch.setenv("MODEL_DIR", str(tmp_path))
    assert resolve_model_dir() == tmp_path.resolve()


@pytest.mark.unit
def test_verify_model_files_missing_directory(tmp_path: Path) -> None:
    """Verifica que un directorio inexistente lance ModelLoadError."""
    non_existent = tmp_path / "no_existe"
    with pytest.raises(ModelLoadError, match="no existe"):
        verify_model_files(non_existent)


@pytest.mark.unit
def test_verify_model_files_missing_required_artifacts(tmp_path: Path) -> None:
    """Verifica que la ausencia de archivos obligatorios del modelo lance ModelLoadError."""
    (tmp_path / "config.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ModelLoadError, match="Faltan archivos obligatorios"):
        verify_model_files(tmp_path)


@pytest.mark.unit
def test_verify_model_files_empty_artifact(tmp_path: Path) -> None:
    """Verifica que un archivo obligatorio de 0 bytes lance ModelLoadError."""
    (tmp_path / "config.json").write_text("{}", encoding="utf-8")
    (tmp_path / "preprocessor_config.json").write_text("{}", encoding="utf-8")
    (tmp_path / "model.safetensors").write_bytes(b"")

    with pytest.raises(ModelLoadError, match="están vacíos"):
        verify_model_files(tmp_path)


@pytest.mark.unit
def test_load_model_from_disk_wraps_transformers_exception(tmp_path: Path) -> None:
    """Verifica que cualquier error interno de Transformers se envuelva en ModelLoadError."""
    (tmp_path / "config.json").write_text("{}", encoding="utf-8")
    (tmp_path / "preprocessor_config.json").write_text("{}", encoding="utf-8")
    (tmp_path / "model.safetensors").write_bytes(b"dummy")

    with patch(
        "src.model_loader.AutoImageProcessor.from_pretrained",
        side_effect=RuntimeError("Archivo safetensors inválido"),
    ):
        with pytest.raises(ModelLoadError, match="Error al cargar el modelo local"):
            load_model_from_disk(tmp_path)


@pytest.mark.unit
def test_clear_model_cache_executes_cleanly() -> None:
    """Verifica que clear_model_cache reinicie la caché sin errores."""
    clear_model_cache()


@pytest.mark.unit
def test_api_health_when_model_fails_to_load() -> None:
    """Verifica que /health responda estado 'degraded' y model_available=False si el modelo falla."""
    client = TestClient(app)
    with patch(
        "api.main.get_model_bundle",
        side_effect=ModelLoadError("Simulación de modelo ausente"),
    ):
        response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["model_available"] is False
    assert "Simulación de modelo ausente" in payload["detail"]


@pytest.mark.unit
def test_api_predict_with_mocked_inference(valid_jpeg_bytes: bytes) -> None:
    """Verifica el contrato JSON de /predict utilizando un mock de inferencia."""
    fake_result = ClassificationResult(
        predicted_category="Tomato___Late_blight",
        class_id=30,
        plant="Tomate",
        plant_en="Tomato",
        disease_or_condition="Tizón tardío (Phytophthora infestans)",
        disease_or_condition_en="Late blight",
        is_healthy=False,
        health_status="Enferma",
        confidence=0.9512,
        confidence_percentage=95.12,
        top_predictions=[
            TopPredictionItem(
                rank=1,
                class_id=30,
                predicted_category="Tomato___Late_blight",
                plant="Tomate",
                plant_en="Tomato",
                disease_or_condition="Tizón tardío (Phytophthora infestans)",
                disease_or_condition_en="Late blight",
                is_healthy=False,
                health_status="Enferma",
                confidence=0.9512,
                confidence_percentage=95.12,
            ),
            TopPredictionItem(
                rank=2,
                class_id=29,
                predicted_category="Tomato___Early_blight",
                plant="Tomate",
                plant_en="Tomato",
                disease_or_condition="Tizón temprano (Alternaria)",
                disease_or_condition_en="Early blight",
                is_healthy=False,
                health_status="Enferma",
                confidence=0.031,
                confidence_percentage=3.1,
            ),
            TopPredictionItem(
                rank=3,
                class_id=37,
                predicted_category="Tomato___healthy",
                plant="Tomate",
                plant_en="Tomato",
                disease_or_condition="Sana (sin enfermedad aparente)",
                disease_or_condition_en="Healthy",
                is_healthy=True,
                health_status="Sana",
                confidence=0.0178,
                confidence_percentage=1.78,
            ),
        ],
        inference_time_ms=25.4,
    )

    client = TestClient(app)
    with patch("api.main.predict_from_bytes", return_value=fake_result):
        response = client.post(
            "/predict",
            files={"file": ("hoja_tomate.jpg", valid_jpeg_bytes, "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["predicted_category"] == "Tomato___Late_blight"
    assert data["plant"] == "Tomate"
    assert data["is_healthy"] is False
    assert data["health_status"] == "Enferma"
    assert data["confidence_percentage"] == 95.12
    assert len(data["top_predictions"]) == 3
    assert data["inference_time_ms"] == 25.4


@pytest.mark.unit
def test_api_predict_handles_internal_inference_error(valid_jpeg_bytes: bytes) -> None:
    """Verifica que un fallo inesperado en inferencia devuelva HTTP 500."""
    client = TestClient(app)
    with patch(
        "api.main.predict_from_bytes",
        side_effect=InferenceError("Fallo simulado de inferencia"),
    ):
        response = client.post(
            "/predict",
            files={"file": ("hoja.jpg", valid_jpeg_bytes, "image/jpeg")},
        )

    assert response.status_code == 500
    data = response.json()
    assert data["error_type"] == "InferenceError"
    assert "Fallo simulado de inferencia" in data["detail"]


@pytest.mark.unit
def test_api_predict_handles_model_load_error_with_503(valid_jpeg_bytes: bytes) -> None:
    """Verifica que ModelLoadError en /predict devuelva HTTP 503 Service Unavailable."""
    client = TestClient(app)
    with patch(
        "api.main.predict_from_bytes",
        side_effect=ModelLoadError("Modelo no disponible temporalmente"),
    ):
        response = client.post(
            "/predict",
            files={"file": ("hoja.jpg", valid_jpeg_bytes, "image/jpeg")},
        )

    assert response.status_code == 503
    data = response.json()
    assert data["error_type"] == "ModelLoadError"


@pytest.mark.unit
def test_api_predict_handles_generic_app_error_with_400(valid_jpeg_bytes: bytes) -> None:
    """Verifica que la excepción base PlantDiseaseAppError devuelva HTTP 400."""
    client = TestClient(app)
    with patch(
        "api.main.predict_from_bytes",
        side_effect=PlantDiseaseAppError("Error de aplicación genérico"),
    ):
        response = client.post(
            "/predict",
            files={"file": ("hoja.jpg", valid_jpeg_bytes, "image/jpeg")},
        )

    assert response.status_code == 400
    data = response.json()
    assert data["error_type"] == "PlantDiseaseAppError"


@pytest.mark.unit
def test_ui_api_client_handles_connection_and_timeout_errors(valid_jpeg_bytes: bytes) -> None:
    """Verifica que el cliente HTTP de Streamlit maneje caídas de conexión y timeouts."""
    with patch("ui.api_client.requests.get", side_effect=requests.ConnectionError()):
        health_res = fetch_api_health(base_url="http://127.0.0.1:9999")
    assert health_res.success is False
    assert health_res.status_code == 0

    with patch("ui.api_client.requests.get", side_effect=requests.Timeout()):
        health_timeout = fetch_api_health(base_url="http://127.0.0.1:9999")
    assert health_timeout.success is False
    assert "tiempo de espera" in (health_timeout.error_message or "")

    with patch("ui.api_client.requests.post", side_effect=requests.ConnectionError()):
        pred_res = request_image_prediction(
            image_bytes=valid_jpeg_bytes,
            filename="hoja.jpg",
            base_url="http://127.0.0.1:9999",
        )
    assert pred_res.success is False
    assert pred_res.status_code == 0

    with patch("ui.api_client.requests.post", side_effect=requests.Timeout()):
        pred_timeout = request_image_prediction(
            image_bytes=valid_jpeg_bytes,
            filename="hoja.jpg",
            base_url="http://127.0.0.1:9999",
        )
    assert pred_timeout.success is False
    assert "tiempo máximo de espera" in (pred_timeout.error_message or "")


@pytest.mark.unit
def test_ui_api_client_handles_degraded_and_error_responses(valid_jpeg_bytes: bytes) -> None:
    """Verifica el manejo de respuestas HTTP no exitosas en el cliente de Streamlit."""
    mock_degraded = MagicMock()
    mock_degraded.status_code = 200
    mock_degraded.json.return_value = {
        "status": "degraded",
        "model_available": False,
        "detail": "Faltan pesos",
    }
    with patch("ui.api_client.requests.get", return_value=mock_degraded):
        res_deg = fetch_api_health()
    assert res_deg.success is False
    assert res_deg.error_message == "Faltan pesos"

    mock_err = MagicMock()
    mock_err.status_code = 415
    mock_err.json.return_value = {"detail": "Formato no admitido"}
    with patch("ui.api_client.requests.post", return_value=mock_err):
        res_err = request_image_prediction(valid_jpeg_bytes, "archivo.gif")
    assert res_err.success is False
    assert res_err.status_code == 415
    assert res_err.error_message == "Formato no admitido"


@pytest.mark.unit
def test_ui_api_client_success_parsing(valid_jpeg_bytes: bytes) -> None:
    """Verifica que el cliente HTTP de Streamlit procese respuestas exitosas de /health y /predict."""
    mock_get_resp = MagicMock()
    mock_get_resp.status_code = 200
    mock_get_resp.json.return_value = {"status": "ok", "model_available": True, "num_classes": 38}

    with patch("ui.api_client.requests.get", return_value=mock_get_resp):
        health_res = fetch_api_health()
    assert health_res.success is True
    assert health_res.data is not None
    assert health_res.data["model_available"] is True

    mock_post_resp = MagicMock()
    mock_post_resp.status_code = 200
    mock_post_resp.json.return_value = {
        "predicted_category": "Apple___healthy",
        "confidence_percentage": 99.1,
    }

    with patch("ui.api_client.requests.post", return_value=mock_post_resp):
        pred_res = request_image_prediction(valid_jpeg_bytes, "apple.jpg")
    assert pred_res.success is True
    assert pred_res.data is not None
    assert pred_res.data["predicted_category"] == "Apple___healthy"
