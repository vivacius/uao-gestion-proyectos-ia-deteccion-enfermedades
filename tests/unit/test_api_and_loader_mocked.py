"""Pruebas unitarias con mocks para cargador del modelo, manejo de errores en API y cliente de la interfaz."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import requests
import torch
from fastapi.testclient import TestClient

from api.main import app
from src.config import resolve_model_dir
from src.exceptions import (
    ImageValidationError,
    InferenceError,
    ModelLoadError,
    PlantDiseaseAppError,
)
from src.inference import predict_from_bytes
from src.model_loader import (
    ModelBundle,
    clear_model_cache,
    get_model_bundle,
    load_model_from_disk,
    verify_model_files,
)
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
    """Verifica que el cliente HTTP de la interfaz maneje caídas de conexión y timeouts."""
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
    """Verifica el manejo de respuestas HTTP no exitosas en el cliente de la interfaz."""
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
    """Verifica que el cliente HTTP de la interfaz procese respuestas exitosas de /health y /predict."""
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


@pytest.mark.unit
def test_load_model_from_disk_success_with_mocks(tmp_path: Path) -> None:
    """Verifica la carga local exitosa del procesador y modelo DINOv2 usando mocks sin pesos reales."""
    # Arrange
    (tmp_path / "config.json").write_text("{}", encoding="utf-8")
    (tmp_path / "preprocessor_config.json").write_text("{}", encoding="utf-8")
    (tmp_path / "model.safetensors").write_bytes(b"dummy-weights")

    mock_processor = MagicMock()
    mock_model = MagicMock()
    mock_model.config = SimpleNamespace(
        id2label={0: "Apple___healthy", 1: "Tomato___Late_blight"},
        label2id={"Apple___healthy": 0, "Tomato___Late_blight": 1},
        architectures=["Dinov2ForImageClassification"],
    )

    # Act
    with (
        patch("src.model_loader.AutoImageProcessor.from_pretrained", return_value=mock_processor) as p_proc,
        patch(
            "src.model_loader.AutoModelForImageClassification.from_pretrained",
            return_value=mock_model,
        ) as p_model,
    ):
        bundle = load_model_from_disk(tmp_path)

    # Assert
    p_proc.assert_called_once_with(str(tmp_path.resolve()), local_files_only=True)
    p_model.assert_called_once_with(str(tmp_path.resolve()), local_files_only=True)
    mock_model.to.assert_called_once_with(torch.device("cpu"))
    mock_model.eval.assert_called_once()
    assert bundle.architecture == "Dinov2ForImageClassification"
    assert bundle.id2label == {0: "Apple___healthy", 1: "Tomato___Late_blight"}
    assert bundle.label2id == {"Apple___healthy": 0, "Tomato___Late_blight": 1}


@pytest.mark.unit
def test_get_model_bundle_singleton_caching_and_force_reload(tmp_path: Path) -> None:
    """Verifica el patrón singleton de get_model_bundle, force_reload y cambio de directorio."""
    # Arrange
    clear_model_cache()
    dir_a = tmp_path / "a"
    dir_b = tmp_path / "b"
    bundle_a = MagicMock(spec=ModelBundle, model_dir=dir_a.resolve())
    bundle_b = MagicMock(spec=ModelBundle, model_dir=dir_b.resolve())

    try:
        # Act
        with patch("src.model_loader.load_model_from_disk", side_effect=[bundle_a, bundle_a, bundle_b]) as m:
            first = get_model_bundle(dir_a)
            second = get_model_bundle(dir_a)
            reloaded = get_model_bundle(dir_a, force_reload=True)
            switched = get_model_bundle(dir_b)

        # Assert
        assert first is bundle_a
        assert second is bundle_a
        assert reloaded is bundle_a
        assert switched is bundle_b
        assert m.call_count == 3
    finally:
        clear_model_cache()


@pytest.mark.unit
def test_predict_from_bytes_success_with_mocked_bundle(valid_jpeg_bytes: bytes) -> None:
    """Verifica el flujo completo de predict_from_bytes aislando el modelo con un ModelBundle simulado."""

    # Arrange
    def fake_processor(*, images, return_tensors):  # noqa: ANN001, ANN202
        assert return_tensors == "pt"
        return {"pixel_values": torch.zeros((1, 3, 224, 224), dtype=torch.float32)}

    fake_model = MagicMock()
    fake_model.return_value = SimpleNamespace(logits=torch.tensor([[0.2, 4.5, -1.0]]))

    bundle = ModelBundle(
        model=fake_model,
        processor=fake_processor,
        device=torch.device("cpu"),
        model_dir=Path("."),
        id2label={0: "Apple___Apple_scab", 1: "Tomato___Late_blight", 2: "Tomato___healthy"},
        label2id={"Apple___Apple_scab": 0, "Tomato___Late_blight": 1, "Tomato___healthy": 2},
        architecture="Dinov2ForImageClassification",
    )

    # Act
    result = predict_from_bytes(
        image_bytes=valid_jpeg_bytes,
        filename="hoja.jpg",
        content_type="image/jpeg",
        top_k=3,
        bundle=bundle,
    )

    # Assert
    fake_model.assert_called_once()
    assert result.predicted_category == "Tomato___Late_blight"
    assert result.class_id == 1
    assert len(result.top_predictions) == 3
    assert result.inference_time_ms >= 0.0


@pytest.mark.unit
def test_predict_from_bytes_wraps_unexpected_error_as_inference_error(valid_jpeg_bytes: bytes) -> None:
    """Verifica que fallos inesperados durante el forward se envuelvan en InferenceError."""

    # Arrange
    def fake_processor(*, images, return_tensors):  # noqa: ANN001, ANN202
        return {"pixel_values": torch.zeros((1, 3, 224, 224), dtype=torch.float32)}

    fake_model = MagicMock(side_effect=RuntimeError("Fallo de tensor en CPU"))
    bundle = ModelBundle(
        model=fake_model,
        processor=fake_processor,
        device=torch.device("cpu"),
        model_dir=Path("."),
        id2label={0: "Apple___healthy"},
        label2id={"Apple___healthy": 0},
        architecture="Dinov2ForImageClassification",
    )

    # Act / Assert
    with pytest.raises(InferenceError, match="Fallo de tensor en CPU"):
        predict_from_bytes(image_bytes=valid_jpeg_bytes, filename="hoja.jpg", bundle=bundle)


@pytest.mark.unit
def test_predict_from_bytes_propagates_image_validation_error(valid_jpeg_bytes: bytes) -> None:
    """Verifica que ImageValidationError se propague sin ser envuelta en InferenceError."""
    # Arrange
    bundle = MagicMock(spec=ModelBundle, processor=MagicMock(), device=torch.device("cpu"))

    # Act / Assert
    with patch("src.inference.preprocess_image", side_effect=ImageValidationError("Tensor inválido")):
        with pytest.raises(ImageValidationError, match="Tensor inválido"):
            predict_from_bytes(image_bytes=valid_jpeg_bytes, filename="hoja.jpg", bundle=bundle)


@pytest.mark.unit
def test_api_lifespan_preloads_model_and_handles_load_error_with_mocks() -> None:
    """Verifica el arranque lifespan de FastAPI tanto en carga exitosa como degradada usando mocks."""
    # Arrange & Act (caso exitoso)
    fake_bundle = SimpleNamespace(
        architecture="Dinov2ForImageClassification",
        device=torch.device("cpu"),
        id2label={0: "Apple___healthy"},
        model_dir=Path("."),
    )
    with patch("api.main.get_model_bundle", return_value=fake_bundle) as mock_ok:
        with TestClient(app) as client:
            resp_ok = client.get("/health")

    # Assert (caso exitoso)
    mock_ok.assert_called()
    assert resp_ok.status_code == 200
    assert resp_ok.json()["status"] == "ok"

    # Arrange & Act (caso degradado)
    with patch("api.main.get_model_bundle", side_effect=ModelLoadError("Sin pesos")):
        with TestClient(app) as client:
            resp_deg = client.get("/health")

    # Assert (caso degradado)
    assert resp_deg.status_code == 200
    assert resp_deg.json()["status"] == "degraded"
