"""Pruebas de integración ejecutadas contra el modelo DINOv2-small real en CPU y la API FastAPI."""

from __future__ import annotations

import pytest
import torch
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app
from src.config import NUM_EXPECTED_CLASSES
from src.inference import predict_from_bytes
from src.model_loader import get_model_bundle
from src.preprocessing import preprocess_image, validate_and_open_image


@pytest.fixture(scope="module")
def real_model_bundle():
    """Carga el modelo real desde la carpeta local una sola vez para las pruebas de integración."""
    return get_model_bundle(force_reload=True)


@pytest.fixture(scope="module")
def api_client() -> TestClient:
    """Cliente de pruebas integrado con FastAPI y el modelo real."""
    return TestClient(app)


@pytest.mark.integration
def test_real_model_loads_locally_on_cpu(real_model_bundle) -> None:
    """Verifica que el modelo real se cargue desde la ruta local en CPU con sus 38 clases."""
    assert real_model_bundle.device == torch.device("cpu")
    assert real_model_bundle.architecture == "Dinov2ForImageClassification"
    assert len(real_model_bundle.id2label) == NUM_EXPECTED_CLASSES == 38
    assert len(real_model_bundle.label2id) == NUM_EXPECTED_CLASSES == 38

    first_param = next(real_model_bundle.model.parameters())
    assert first_param.device.type == "cpu"
    assert not real_model_bundle.model.training


@pytest.mark.integration
def test_real_preprocessor_matches_preprocessor_config(
    real_model_bundle,
    valid_jpeg_bytes: bytes,
) -> None:
    """Verifica que el procesador real aplique resize (256), center_crop (224x224) y normalización."""
    processor = real_model_bundle.processor
    assert processor.do_resize is True
    assert processor.size == {"shortest_edge": 256}
    assert processor.do_center_crop is True
    assert processor.crop_size == {"height": 224, "width": 224}
    assert processor.do_normalize is True
    assert list(processor.image_mean) == [0.485, 0.456, 0.406]
    assert list(processor.image_std) == [0.229, 0.224, 0.225]

    pil_img: Image.Image = validate_and_open_image(valid_jpeg_bytes, filename="leaf.jpg")
    tensors = preprocess_image(pil_img, processor=processor, device=real_model_bundle.device)

    assert "pixel_values" in tensors
    pixel_values = tensors["pixel_values"]
    assert pixel_values.shape == (1, 3, 224, 224)
    assert pixel_values.dtype == torch.float32
    assert pixel_values.device.type == "cpu"


@pytest.mark.integration
def test_real_inference_pipeline_from_bytes(
    real_model_bundle,
    valid_jpeg_bytes: bytes,
) -> None:
    """Ejecuta una inferencia real completa sobre CPU y verifica coherencia de probabilidades y etiquetas."""
    result = predict_from_bytes(
        image_bytes=valid_jpeg_bytes,
        filename="leaf.jpg",
        content_type="image/jpeg",
        top_k=3,
        bundle=real_model_bundle,
    )

    assert result.predicted_category in real_model_bundle.label2id
    assert 0 <= result.class_id < 38
    assert result.plant != ""
    assert result.disease_or_condition != ""
    assert result.health_status in ("Sana", "Enferma")
    assert isinstance(result.is_healthy, bool)
    assert 0.0 < result.confidence <= 1.0
    assert 0.0 < result.confidence_percentage <= 100.0
    assert result.inference_time_ms > 0.0
    assert len(result.top_predictions) == 3

    # Las probabilidades del Top-3 deben estar en orden no creciente y sumar <= 1.0
    probs = [item.confidence for item in result.top_predictions]
    assert probs[0] >= probs[1] >= probs[2]
    assert sum(probs) <= 1.0001


@pytest.mark.integration
def test_api_health_endpoint_real_model(api_client: TestClient) -> None:
    """Comprueba que GET /health responda HTTP 200 con el modelo real disponible en CPU."""
    response = api_client.get("/health")
    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["model_available"] is True
    assert payload["device"] == "cpu"
    assert payload["num_classes"] == 38
    assert payload["architecture"] == "Dinov2ForImageClassification"


@pytest.mark.integration
def test_api_predict_endpoint_real_jpeg_and_png(
    api_client: TestClient,
    valid_jpeg_bytes: bytes,
    valid_png_bytes: bytes,
) -> None:
    """Comprueba POST /predict con imágenes JPG y PNG reales contra el modelo en CPU."""
    for filename, mime, content in [
        ("hoja_prueba.jpg", "image/jpeg", valid_jpeg_bytes),
        ("hoja_prueba.png", "image/png", valid_png_bytes),
    ]:
        response = api_client.post(
            "/predict",
            files={"file": (filename, content, mime)},
        )
        assert response.status_code == 200
        data = response.json()

        required_keys = {
            "predicted_category",
            "class_id",
            "plant",
            "plant_en",
            "disease_or_condition",
            "disease_or_condition_en",
            "is_healthy",
            "health_status",
            "confidence",
            "confidence_percentage",
            "top_predictions",
            "inference_time_ms",
            "disclaimer",
        }
        assert required_keys.issubset(data.keys())
        assert len(data["top_predictions"]) == 3
        assert data["inference_time_ms"] > 0.0
        assert data["health_status"] in ("Sana", "Enferma")


@pytest.mark.integration
def test_api_predict_rejects_invalid_inputs(
    api_client: TestClient,
    corrupted_image_bytes: bytes,
    unsupported_gif_bytes: bytes,
) -> None:
    """Verifica que POST /predict rechace imágenes vacías, corruptas y formatos no soportados."""
    # 1. Archivo vacío
    resp_empty = api_client.post(
        "/predict",
        files={"file": ("vacia.jpg", b"", "image/jpeg")},
    )
    assert resp_empty.status_code == 400
    assert resp_empty.json()["error_type"] == "EmptyImageError"

    # 2. Archivo corrupto
    resp_corrupt = api_client.post(
        "/predict",
        files={"file": ("corrupta.jpg", corrupted_image_bytes, "image/jpeg")},
    )
    assert resp_corrupt.status_code == 400
    assert resp_corrupt.json()["error_type"] == "CorruptedImageError"

    # 3. Formato no permitido (GIF)
    resp_gif = api_client.post(
        "/predict",
        files={"file": ("animacion.gif", unsupported_gif_bytes, "image/gif")},
    )
    assert resp_gif.status_code == 415
    assert resp_gif.json()["error_type"] == "UnsupportedImageFormatError"
