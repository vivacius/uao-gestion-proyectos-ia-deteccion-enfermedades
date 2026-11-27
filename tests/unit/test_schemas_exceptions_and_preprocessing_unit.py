"""Pruebas unitarias de esquemas Pydantic v2, excepciones, configuración y preprocesamiento."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image
from pydantic import ValidationError

from api.schemas import (
    ErrorResponse,
    HealthResponse,
    ModelInfoResponse,
    PredictionResponse,
    TopPredictionSchema,
)
from src.config import (
    AGRONOMIC_DISCLAIMER,
    ALLOWED_EXTENSIONS,
    ALLOWED_PIL_FORMATS,
    DEFAULT_TOP_K,
    DEVICE,
    MAX_IMAGE_SIZE_BYTES,
    MIN_IMAGE_DIMENSION,
    NUM_EXPECTED_CLASSES,
    resolve_model_dir,
)
from src.exceptions import (
    CorruptedImageError,
    EmptyImageError,
    ImageTooLargeError,
    ImageValidationError,
    InferenceError,
    InvalidImageFormatException,
    ModelLoadError,
    PlantDiseaseAppError,
)
from src.preprocessing import validate_and_open_image, validate_file_metadata


def _make_image_bytes(
    fmt: str = "JPEG",
    mode: str = "RGB",
    size: tuple[int, int] = (64, 64),
) -> bytes:
    """Genera bytes de imagen en memoria para pruebas unitarias."""
    color: int | tuple[int, ...] = 128 if mode == "L" else (128, 255) if mode == "LA" else (40, 120, 50)
    img = Image.new(mode, size, color=color)
    buf = BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def _valid_top_item(rank: int = 1) -> TopPredictionSchema:
    """Construye un TopPredictionSchema válido para reutilizar en pruebas."""
    return TopPredictionSchema(
        rank=rank,
        class_id=0,
        predicted_category="Apple___Apple_scab",
        plant="Manzano",
        plant_en="Apple",
        disease_or_condition="Sarna del manzano",
        disease_or_condition_en="Apple scab",
        is_healthy=False,
        health_status="Enferma",
        confidence=0.85,
        confidence_percentage=85.0,
    )


# --- Esquemas Pydantic v2 ---


def test_health_response_defaults_and_ok_status() -> None:
    """Verifica valores por defecto y campos obligatorios de HealthResponse."""
    # Arrange / Act
    resp = HealthResponse(status="ok", model_available=True)

    # Assert
    assert resp.status == "ok"
    assert resp.model_available is True
    assert resp.device == "cpu"


def test_model_info_response_defaults() -> None:
    """Verifica valores por defecto de ModelInfoResponse."""
    # Arrange / Act
    resp = ModelInfoResponse(model_available=True)

    # Assert
    assert resp.num_classes == 38
    assert resp.architecture == "Dinov2ForImageClassification"


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("rank", 0),
        ("class_id", -1),
        ("confidence", -0.01),
        ("confidence", 1.01),
        ("confidence_percentage", -1.0),
        ("confidence_percentage", 100.5),
    ],
)
def test_top_prediction_schema_rejects_out_of_range_values(field: str, bad_value: float | int) -> None:
    """Verifica que TopPredictionSchema rechaza valores fuera de rango contractual."""
    # Arrange
    payload = _valid_top_item().model_dump()
    payload[field] = bad_value

    # Act / Assert
    with pytest.raises(ValidationError):
        TopPredictionSchema(**payload)


def test_prediction_response_roundtrip_serialization() -> None:
    """Verifica serialización JSON de PredictionResponse con Top-3."""
    # Arrange
    items = [_valid_top_item(1), _valid_top_item(2), _valid_top_item(3)]
    resp = PredictionResponse(
        predicted_category="Apple___Apple_scab",
        class_id=0,
        plant="Manzano",
        plant_en="Apple",
        disease_or_condition="Sarna del manzano",
        disease_or_condition_en="Apple scab",
        is_healthy=False,
        health_status="Enferma",
        confidence=0.85,
        confidence_percentage=85.0,
        top_predictions=items,
        inference_time_ms=65.4,
        disclaimer=AGRONOMIC_DISCLAIMER,
    )

    # Act
    dumped = resp.model_dump()

    # Assert
    assert dumped["confidence"] == 0.85
    assert len(dumped["top_predictions"]) == 3
    assert dumped["disclaimer"] == AGRONOMIC_DISCLAIMER


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("class_id", -1),
        ("confidence", -0.01),
        ("confidence", 1.01),
        ("confidence_percentage", -0.5),
        ("confidence_percentage", 100.1),
        ("inference_time_ms", -1.0),
        ("top_predictions", []),
        ("top_predictions", [_valid_top_item(1)] * 4),
    ],
)
def test_prediction_response_rejects_invalid_constraints(field: str, bad_value: object) -> None:
    """Verifica restricciones Pydantic de PredictionResponse en campos numéricos y Top-K."""
    # Arrange
    payload: dict[str, object] = {
        "predicted_category": "Apple___Apple_scab",
        "class_id": 0,
        "plant": "Manzano",
        "plant_en": "Apple",
        "disease_or_condition": "Sarna del manzano",
        "disease_or_condition_en": "Apple scab",
        "is_healthy": False,
        "health_status": "Enferma",
        "confidence": 0.85,
        "confidence_percentage": 85.0,
        "top_predictions": [_valid_top_item(1)],
        "inference_time_ms": 10.0,
        "disclaimer": AGRONOMIC_DISCLAIMER,
    }
    payload[field] = bad_value

    # Act / Assert
    with pytest.raises(ValidationError):
        PredictionResponse(**payload)  # type: ignore[arg-type]


def test_error_response_model_dump() -> None:
    """Verifica serialización de ErrorResponse."""
    # Arrange / Act
    err = ErrorResponse(detail="Archivo vacío", error_type="EmptyImageError")

    # Assert
    assert err.model_dump() == {"detail": "Archivo vacío", "error_type": "EmptyImageError"}


# --- Excepciones de dominio y configuración ---


@pytest.mark.parametrize(
    ("exc_cls", "expected_parent", "expected_status"),
    [
        (ImageValidationError, PlantDiseaseAppError, 400),
        (InvalidImageFormatException, ImageValidationError, 400),
        (EmptyImageError, InvalidImageFormatException, 400),
        (CorruptedImageError, InvalidImageFormatException, 400),
        (ImageTooLargeError, ImageValidationError, 413),
    ],
)
def test_validation_exception_hierarchy_and_status_codes(
    exc_cls: type[ImageValidationError],
    expected_parent: type[Exception],
    expected_status: int,
) -> None:
    """Verifica herencia y código HTTP contractual de cada excepción de validación."""
    # Arrange / Act
    err = exc_cls("error de prueba")

    # Assert
    assert isinstance(err, expected_parent)
    assert err.status_code == expected_status


def test_image_validation_error_allows_custom_status_code() -> None:
    """Verifica sobreescritura explícita de status_code en ImageValidationError."""
    # Arrange / Act
    err = ImageValidationError("mensaje", status_code=422)

    # Assert
    assert err.status_code == 422


def test_model_and_inference_exceptions_inherit_from_base() -> None:
    """Verifica que ModelLoadError e InferenceError heredan de PlantDiseaseAppError."""
    # Arrange / Act
    load_err = ModelLoadError("falta archivo")
    inf_err = InferenceError("fallo inferencia")

    # Assert
    assert isinstance(load_err, PlantDiseaseAppError)
    assert isinstance(inf_err, PlantDiseaseAppError)


def test_config_constants_match_contract() -> None:
    """Verifica invariantes de configuración en src/config.py."""
    # Arrange / Act / Assert
    assert DEVICE == "cpu"
    assert DEFAULT_TOP_K == 3
    assert NUM_EXPECTED_CLASSES == 38
    assert ALLOWED_EXTENSIONS == frozenset({".jpg", ".jpeg", ".png"})
    assert ALLOWED_PIL_FORMATS == frozenset({"JPEG", "JPG", "PNG"})
    assert MIN_IMAGE_DIMENSION == 16
    assert "orientativas" in AGRONOMIC_DISCLAIMER


def test_resolve_model_dir_respects_env_var(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Verifica prioridad de la variable de entorno MODEL_DIR."""
    # Arrange
    custom_dir = tmp_path / "custom_model"
    monkeypatch.setenv("MODEL_DIR", str(custom_dir))

    # Act
    resolved = resolve_model_dir()

    # Assert
    assert resolved == custom_dir.resolve()


# --- Preprocesamiento: casos borde de metadatos y decodificación ---


@pytest.mark.parametrize(
    ("filename", "content_type"),
    [
        ("HOJA.JPG", "IMAGE/JPEG"),
        ("captura.JPEG", "image/jpeg; charset=binary"),
        ("muestra.PNG", "image/png"),
        ("archivo_sin_extension", "application/octet-stream"),
        (None, None),
    ],
)
def test_validate_file_metadata_accepts_valid_inputs(
    filename: str | None,
    content_type: str | None,
) -> None:
    """Verifica aceptación de extensiones en mayúsculas y MIME con parámetros."""
    # Arrange / Act / Assert
    validate_file_metadata(filename=filename, content_type=content_type)


@pytest.mark.parametrize(
    ("filename", "content_type"),
    [
        ("imagen.webp", "image/jpeg"),
        ("animacion.gif", "image/gif"),
        ("documento.pdf", "application/pdf"),
        ("hoja.bmp", None),
        ("hoja.jpg", "text/plain"),
        ("hoja.png", "image/svg+xml"),
    ],
)
def test_validate_file_metadata_rejects_unsupported_formats(
    filename: str,
    content_type: str | None,
) -> None:
    """Verifica rechazo HTTP 415 ante extensiones o MIME no soportados."""
    # Arrange / Act / Assert
    with pytest.raises(ImageValidationError) as exc_info:
        validate_file_metadata(filename=filename, content_type=content_type)
    assert exc_info.value.status_code == 415


@pytest.mark.parametrize(
    ("fmt", "mode", "size"),
    [
        ("JPEG", "RGB", (16, 16)),
        ("JPEG", "L", (64, 64)),
        ("PNG", "RGBA", (48, 48)),
        ("PNG", "LA", (32, 32)),
        ("PNG", "P", (64, 64)),
        ("PNG", "RGB", (512, 384)),
    ],
)
def test_validate_and_open_image_converts_modes_to_rgb(
    fmt: str,
    mode: str,
    size: tuple[int, int],
) -> None:
    """Verifica conversión uniforme a modo RGB en formatos y modos soportados."""
    # Arrange
    raw = _make_image_bytes(fmt=fmt, mode=mode, size=size)

    # Act
    opened = validate_and_open_image(raw, filename=f"leaf.{fmt.lower()}")

    # Assert
    assert opened.mode == "RGB"
    assert opened.size == size


def test_validate_and_open_image_rejects_empty_bytes() -> None:
    """Verifica EmptyImageError ante archivo vacío de 0 bytes."""
    # Arrange / Act / Assert
    with pytest.raises(EmptyImageError):
        validate_and_open_image(b"", filename="empty.jpg")


def test_validate_and_open_image_rejects_oversized_payload() -> None:
    """Verifica ImageTooLargeError cuando se supera el tamaño máximo."""
    # Arrange
    oversized = b"\xff\xd8\xff" + b"0" * 100

    # Act / Assert
    with pytest.raises(ImageTooLargeError):
        validate_and_open_image(oversized, filename="big.jpg", max_size_bytes=50)


def test_validate_and_open_image_rejects_corrupted_bytes() -> None:
    """Verifica CorruptedImageError ante bytes aleatorios no decodificables."""
    # Arrange
    bad_bytes = b"not-a-valid-jpeg-or-png-payload"

    # Act / Assert
    with pytest.raises(CorruptedImageError):
        validate_and_open_image(bad_bytes, filename="corrupt.jpg")


def test_validate_and_open_image_rejects_too_small_dimensions() -> None:
    """Verifica rechazo cuando la imagen es menor a MIN_IMAGE_DIMENSION."""
    # Arrange
    tiny = _make_image_bytes(fmt="PNG", mode="RGB", size=(15, 15))

    # Act / Assert
    with pytest.raises(InvalidImageFormatException):
        validate_and_open_image(tiny, filename="tiny.png")


def test_max_image_size_bytes_is_positive_multiple_of_mb() -> None:
    """Verifica consistencia del límite de tamaño en bytes."""
    # Arrange / Act / Assert
    assert MAX_IMAGE_SIZE_BYTES >= 1024 * 1024
    assert MAX_IMAGE_SIZE_BYTES % (1024 * 1024) == 0
