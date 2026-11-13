"""Módulo de validación y preprocesamiento de imágenes."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import torch
from PIL import Image, UnidentifiedImageError

from src.config import (
    ALLOWED_EXTENSIONS,
    ALLOWED_MIME_TYPES,
    ALLOWED_PIL_FORMATS,
    DEVICE,
    MAX_IMAGE_SIZE_BYTES,
    MAX_IMAGE_SIZE_MB,
    MIN_IMAGE_DIMENSION,
)
from src.exceptions import (
    CorruptedImageError,
    EmptyImageError,
    ImageTooLargeError,
    ImageValidationError,
    InvalidImageFormatException,
    UnsupportedImageFormatError,
)

# Contratos numéricos y de normalización ImageNet para DINOv2 (HU-02: AC2.2 y AC2.3)
RESIZE_SHORTEST_EDGE: int = 256
CROP_SIZE: int = 224
EXPECTED_TENSOR_SHAPE: tuple[int, int, int, int] = (1, 3, 224, 224)
IMAGENET_MEAN: tuple[float, float, float] = (0.485, 0.456, 0.406)
IMAGENET_STD: tuple[float, float, float] = (0.229, 0.224, 0.225)


def validate_file_metadata(
    filename: str | None = None,
    content_type: str | None = None,
) -> None:
    """Valida la extensión del nombre de archivo y el tipo MIME declarados."""
    if filename is not None and filename.strip():
        ext = Path(filename.strip()).suffix.lower()
        if ext and ext not in ALLOWED_EXTENSIONS:
            allowed_str = ", ".join(sorted(ALLOWED_EXTENSIONS))
            raise UnsupportedImageFormatError(
                f"Extensión de archivo no permitida ('{ext}'). Formatos admitidos: {allowed_str}."
            )

    if content_type is not None and content_type.strip():
        normalized_mime = content_type.split(";")[0].strip().lower()
        if normalized_mime and normalized_mime not in ALLOWED_MIME_TYPES:
            raise UnsupportedImageFormatError(
                f"Tipo de contenido MIME no admitido ('{normalized_mime}'). "
                "Solo se aceptan imágenes JPG, JPEG o PNG."
            )


def validate_and_open_image(
    image_bytes: bytes,
    filename: str | None = None,
    content_type: str | None = None,
    max_size_bytes: int = MAX_IMAGE_SIZE_BYTES,
) -> Image.Image:
    """Valida los bytes de una imagen y devuelve un objeto ``PIL.Image.Image`` en modo RGB.

    Realiza las siguientes comprobaciones:
    1. Archivo no vacío.
    2. Tamaño máximo permitido.
    3. Extensión y MIME type válidos (si se proporcionan).
    4. Integridad estructural de la imagen y carga completa de píxeles.
    5. Formato real decodificado por Pillow (JPEG o PNG).
    6. Dimensiones mínimas válidas.
    7. Conversión a espacio de color RGB.
    """
    if not isinstance(image_bytes, (bytes, bytearray)) or len(image_bytes) == 0:
        raise EmptyImageError("El archivo enviado está vacío. Por favor, suba una imagen válida.")

    if len(image_bytes) > max_size_bytes:
        size_mb = len(image_bytes) / (1024 * 1024)
        raise ImageTooLargeError(
            f"La imagen supera el límite máximo permitido de {MAX_IMAGE_SIZE_MB} MB "
            f"(tamaño recibido: {size_mb:.2f} MB)."
        )

    validate_file_metadata(filename=filename, content_type=content_type)

    try:
        with Image.open(BytesIO(image_bytes)) as probe_img:
            detected_format = (probe_img.format or "").upper()
            probe_img.verify()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        raise CorruptedImageError(
            "El archivo no es una imagen válida o se encuentra dañado/corrupto."
        ) from exc

    if detected_format not in ALLOWED_PIL_FORMATS:
        raise UnsupportedImageFormatError(
            f"Formato de imagen no admitido ('{detected_format or 'desconocido'}'). "
            "Solo se permiten archivos JPG, JPEG o PNG."
        )

    try:
        image = Image.open(BytesIO(image_bytes))
        image.load()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        raise CorruptedImageError(
            "La imagen está truncada o corrupta y no pudo decodificarse completamente."
        ) from exc

    width, height = image.size
    if width < MIN_IMAGE_DIMENSION or height < MIN_IMAGE_DIMENSION:
        raise InvalidImageFormatException(
            f"Las dimensiones de la imagen ({width}x{height} px) son demasiado pequeñas. "
            f"El mínimo requerido es {MIN_IMAGE_DIMENSION}x{MIN_IMAGE_DIMENSION} px."
        )

    if image.mode != "RGB":
        image = image.convert("RGB")

    return image


def normalize_pil_to_tensor(
    image: Image.Image,
    device: torch.device | str = DEVICE,
) -> torch.Tensor:
    """Transforma una imagen PIL al tensor normalizado ``[1, 3, 224, 224]`` (``torch.float32``).

    Aplica determinísticamente el contrato numérico de DINOv2 (AC2.2 y AC2.3):
    1. Conversión a espacio de color RGB.
    2. Redimensionado bicúbico donde el lado más corto mide 256 px preservando relación de aspecto.
    3. Recorte central (``center_crop``) a 224x224 px.
    4. Reescalado al rango ``[0.0, 1.0]`` (factor ``1/255``).
    5. Normalización por canal con media ImageNet ``[0.485, 0.456, 0.406]`` y
       desviación estándar ``[0.229, 0.224, 0.225]``.
    """
    if not isinstance(image, Image.Image):
        raise InvalidImageFormatException(
            "Se requiere una instancia válida de PIL.Image.Image para el preprocesamiento."
        )

    if image.mode != "RGB":
        image = image.convert("RGB")

    width, height = image.size
    if width <= 0 or height <= 0:
        raise InvalidImageFormatException("La imagen tiene dimensiones inválidas.")

    if width < height:
        new_width = RESIZE_SHORTEST_EDGE
        new_height = int(round(height * (RESIZE_SHORTEST_EDGE / width)))
    else:
        new_height = RESIZE_SHORTEST_EDGE
        new_width = int(round(width * (RESIZE_SHORTEST_EDGE / height)))

    resized = image.resize((new_width, new_height), resample=Image.Resampling.BICUBIC)

    left = (new_width - CROP_SIZE) // 2
    top = (new_height - CROP_SIZE) // 2
    cropped = resized.crop((left, top, left + CROP_SIZE, top + CROP_SIZE))

    raw_bytes = cropped.tobytes()
    uint8_tensor = torch.frombuffer(bytearray(raw_bytes), dtype=torch.uint8)
    chw_tensor = uint8_tensor.view(CROP_SIZE, CROP_SIZE, 3).permute(2, 0, 1).to(torch.float32)
    rescaled = chw_tensor / 255.0

    mean = torch.tensor(IMAGENET_MEAN, dtype=torch.float32).view(3, 1, 1)
    std = torch.tensor(IMAGENET_STD, dtype=torch.float32).view(3, 1, 1)
    normalized = (rescaled - mean) / std

    target_device = torch.device(device)
    return normalized.unsqueeze(0).to(target_device)


def preprocess_image(
    image: Image.Image,
    processor: Any | None = None,
    device: torch.device | str = DEVICE,
) -> dict[str, torch.Tensor]:
    """Aplica las transformaciones oficiales definidas en ``preprocessor_config.json``.

    Transformaciones aplicadas por ``BitImageProcessor`` del modelo (o el pipeline
    determinista equivalente si ``processor`` es ``None``):
    - Conversión a RGB (garantizada previamente y en el procesador).
    - Redimensionado del lado más corto a 256 px (interpolación bicúbica, ``resample=3``).
    - Recorte central (``center_crop``) a 224x224 px.
    - Reescalado de píxeles con factor ``1/255`` (``0.00392156862745098``).
    - Normalización con media ``[0.485, 0.456, 0.406]`` y desviación ``[0.229, 0.224, 0.225]``.
    - Conversión a tensor PyTorch ``pixel_values`` con forma ``(1, 3, 224, 224)`` y ``torch.float32``.
    """
    if not isinstance(image, Image.Image):
        raise InvalidImageFormatException(
            "El objeto de entrada para preprocesamiento no es una imagen PIL válida."
        )

    if image.mode != "RGB":
        image = image.convert("RGB")

    target_device = torch.device(device)

    if processor is None:
        pixel_values = normalize_pil_to_tensor(image=image, device=target_device)
        return {"pixel_values": pixel_values}

    inputs = processor(images=image, return_tensors="pt")
    output: dict[str, torch.Tensor] = {}
    for key, tensor in inputs.items():
        cast_tensor = tensor.to(device=target_device, dtype=torch.float32)
        output[key] = cast_tensor

    if "pixel_values" not in output:
        raise ImageValidationError("El procesador de imágenes no generó la clave obligatoria 'pixel_values'.")

    if tuple(output["pixel_values"].shape) != EXPECTED_TENSOR_SHAPE:
        raise ImageValidationError(
            f"Forma de tensor inválida: se esperaba {EXPECTED_TENSOR_SHAPE}, "
            f"pero se obtuvo {tuple(output['pixel_values'].shape)}."
        )

    return output
