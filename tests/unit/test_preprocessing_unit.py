"""Pruebas unitarias para la validación y el preprocesamiento de imágenes."""

from __future__ import annotations

from io import BytesIO
from unittest.mock import MagicMock

import pytest
import torch
from PIL import Image

from src.exceptions import (
    CorruptedImageError,
    EmptyImageError,
    ImageTooLargeError,
    ImageValidationError,
    UnsupportedImageFormatError,
)
from src.preprocessing import preprocess_image, validate_and_open_image, validate_file_metadata


@pytest.mark.unit
def test_validate_and_open_valid_jpeg_and_png(
    valid_jpeg_bytes: bytes,
    valid_png_bytes: bytes,
) -> None:
    """Verifica que imágenes JPG y PNG válidas se abran correctamente en modo RGB."""
    img_jpg = validate_and_open_image(valid_jpeg_bytes, filename="hoja.jpg", content_type="image/jpeg")
    assert img_jpg.mode == "RGB"
    assert img_jpg.size == (300, 300)

    img_png = validate_and_open_image(valid_png_bytes, filename="hoja.png", content_type="image/png")
    assert img_png.mode == "RGB"
    assert img_png.size == (280, 280)


@pytest.mark.unit
def test_converts_rgba_and_grayscale_to_rgb(
    valid_rgba_png_bytes: bytes,
    valid_grayscale_jpeg_bytes: bytes,
) -> None:
    """Verifica que imágenes RGBA o en escala de grises se conviertan automáticamente a RGB."""
    rgba_converted = validate_and_open_image(valid_rgba_png_bytes, filename="hoja_alpha.png")
    assert rgba_converted.mode == "RGB"

    gray_converted = validate_and_open_image(valid_grayscale_jpeg_bytes, filename="hoja_gris.jpeg")
    assert gray_converted.mode == "RGB"


@pytest.mark.unit
@pytest.mark.parametrize(
    "valid_filename,valid_mime",
    [
        ("leaf.jpg", "image/jpeg"),
        ("leaf.JPG", "image/jpeg"),
        ("leaf.jpeg", "image/jpg"),
        ("leaf.JPEG", "image/jpeg; charset=binary"),
        ("leaf.png", "image/png"),
        ("leaf.PNG", "application/octet-stream"),
    ],
)
def test_validate_file_metadata_accepts_allowed_formats(
    valid_filename: str,
    valid_mime: str,
) -> None:
    """Verifica que todas las combinaciones válidas de extensión y MIME sean aceptadas."""
    validate_file_metadata(filename=valid_filename, content_type=valid_mime)


@pytest.mark.unit
@pytest.mark.parametrize(
    "bad_filename",
    [
        "imagen.gif",
        "imagen.bmp",
        "imagen.webp",
        "imagen.tiff",
        "imagen.tif",
        "imagen.svg",
        "imagen.ico",
        "documento.pdf",
        "datos.txt",
        "archivo.zip",
        "video.mp4",
        "modelo.safetensors",
    ],
)
def test_validate_file_metadata_rejects_disallowed_extensions(bad_filename: str) -> None:
    """Verifica que cualquier extensión distinta de .jpg, .jpeg o .png sea rechazada con código 415."""
    with pytest.raises(UnsupportedImageFormatError) as exc_info:
        validate_file_metadata(filename=bad_filename, content_type="image/jpeg")
    assert exc_info.value.status_code == 415


@pytest.mark.unit
@pytest.mark.parametrize(
    "bad_mime",
    [
        "image/gif",
        "image/bmp",
        "image/webp",
        "image/tiff",
        "image/svg+xml",
        "application/pdf",
        "text/plain",
        "text/html",
        "application/json",
        "video/mp4",
    ],
)
def test_validate_file_metadata_rejects_disallowed_mime_types(bad_mime: str) -> None:
    """Verifica que cualquier MIME type no admitido sea rechazado con código 415."""
    with pytest.raises(UnsupportedImageFormatError) as exc_info:
        validate_file_metadata(filename="hoja.jpg", content_type=bad_mime)
    assert exc_info.value.status_code == 415


@pytest.mark.unit
def test_rejects_empty_image_bytes() -> None:
    """Verifica que bytes vacíos lancen EmptyImageError (HTTP 400)."""
    with pytest.raises(EmptyImageError) as exc_info:
        validate_and_open_image(b"", filename="vacia.jpg")
    assert exc_info.value.status_code == 400


@pytest.mark.unit
def test_rejects_oversized_image(valid_jpeg_bytes: bytes) -> None:
    """Verifica que archivos mayores al límite lancen ImageTooLargeError (HTTP 413)."""
    with pytest.raises(ImageTooLargeError) as exc_info:
        validate_and_open_image(valid_jpeg_bytes, filename="grande.jpg", max_size_bytes=100)
    assert exc_info.value.status_code == 413


@pytest.mark.unit
def test_rejects_unsupported_pil_formats_even_with_spoofed_extension(
    unsupported_gif_bytes: bytes,
    unsupported_bmp_bytes: bytes,
) -> None:
    """Verifica que una imagen GIF o BMP renombrada como .jpg sea rechazada por su formato real."""
    with pytest.raises(UnsupportedImageFormatError):
        validate_and_open_image(unsupported_gif_bytes, filename="falsa.jpg", content_type="image/jpeg")

    with pytest.raises(UnsupportedImageFormatError):
        validate_and_open_image(unsupported_bmp_bytes, filename="falsa.png", content_type="image/png")


@pytest.mark.unit
def test_rejects_corrupted_image_bytes(corrupted_image_bytes: bytes) -> None:
    """Verifica que bytes corruptos lancen CorruptedImageError (HTTP 400)."""
    with pytest.raises(CorruptedImageError) as exc_info:
        validate_and_open_image(corrupted_image_bytes, filename="corrupta.jpg")
    assert exc_info.value.status_code == 400


@pytest.mark.unit
@pytest.mark.parametrize("w,h", [(1, 1), (8, 8), (15, 200), (200, 15)])
def test_rejects_tiny_dimensions(w: int, h: int) -> None:
    """Verifica que una imagen menor al tamaño mínimo (16x16 px) sea rechazada."""
    tiny_img = Image.new("RGB", (w, h), color=(0, 255, 0))
    buf = BytesIO()
    tiny_img.save(buf, format="PNG")

    with pytest.raises(ImageValidationError, match="demasiado pequeñas"):
        validate_and_open_image(buf.getvalue(), filename="minima.png")


@pytest.mark.unit
def test_preprocess_image_calls_processor_and_moves_to_cpu() -> None:
    """Verifica que preprocess_image convierta a RGB, invoque al procesador y devuelva tensores en CPU."""
    mock_processor = MagicMock(
        return_value={"pixel_values": torch.zeros((1, 3, 224, 224), dtype=torch.float32)}
    )
    rgba_img = Image.new("RGBA", (300, 300), color=(10, 120, 30, 255))

    tensors = preprocess_image(image=rgba_img, processor=mock_processor, device="cpu")

    assert "pixel_values" in tensors
    assert tensors["pixel_values"].shape == (1, 3, 224, 224)
    assert tensors["pixel_values"].device.type == "cpu"

    called_img = mock_processor.call_args.kwargs["images"]
    assert called_img.mode == "RGB"
    assert mock_processor.call_args.kwargs["return_tensors"] == "pt"
