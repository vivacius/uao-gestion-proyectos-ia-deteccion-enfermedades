"""Fixtures compartidos para las pruebas unitarias y de integración."""

from __future__ import annotations

from io import BytesIO

import pytest
from PIL import Image, ImageDraw


def create_leaf_like_image(
    width: int = 300,
    height: int = 300,
    mode: str = "RGB",
    image_format: str = "JPEG",
) -> bytes:
    """Genera una imagen sintética válida en memoria simulando una hoja sobre fondo neutro."""
    bg_color = (220, 220, 220) if mode == "RGB" else (220, 220, 220, 255) if mode == "RGBA" else 200
    img = Image.new(mode, (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    if mode in ("RGB", "RGBA"):
        leaf_color = (45, 130, 55) if mode == "RGB" else (45, 130, 55, 255)
        spot_color = (120, 75, 30) if mode == "RGB" else (120, 75, 30, 255)
    else:
        leaf_color = 90
        spot_color = 50

    draw.ellipse(
        (int(width * 0.15), int(height * 0.1), int(width * 0.85), int(height * 0.9)),
        fill=leaf_color,
    )
    draw.ellipse(
        (int(width * 0.4), int(height * 0.35), int(width * 0.55), int(height * 0.5)),
        fill=spot_color,
    )

    buffer = BytesIO()
    img.save(buffer, format=image_format)
    return buffer.getvalue()


@pytest.fixture
def valid_jpeg_bytes() -> bytes:
    """Devuelve bytes de una imagen JPEG RGB válida de 300x300 px."""
    return create_leaf_like_image(width=300, height=300, mode="RGB", image_format="JPEG")


@pytest.fixture
def valid_png_bytes() -> bytes:
    """Devuelve bytes de una imagen PNG RGB válida de 280x280 px."""
    return create_leaf_like_image(width=280, height=280, mode="RGB", image_format="PNG")


@pytest.fixture
def valid_rgba_png_bytes() -> bytes:
    """Devuelve bytes de una imagen PNG con canal alfa (RGBA) para probar conversión a RGB."""
    return create_leaf_like_image(width=260, height=260, mode="RGBA", image_format="PNG")


@pytest.fixture
def valid_grayscale_jpeg_bytes() -> bytes:
    """Devuelve bytes de una imagen JPEG en escala de grises (modo L) para probar conversión a RGB."""
    return create_leaf_like_image(width=260, height=260, mode="L", image_format="JPEG")


@pytest.fixture
def unsupported_gif_bytes() -> bytes:
    """Devuelve bytes de una imagen GIF (formato no permitido)."""
    return create_leaf_like_image(width=100, height=100, mode="RGB", image_format="GIF")


@pytest.fixture
def unsupported_bmp_bytes() -> bytes:
    """Devuelve bytes de una imagen BMP (formato no permitido)."""
    return create_leaf_like_image(width=100, height=100, mode="RGB", image_format="BMP")


@pytest.fixture
def corrupted_image_bytes() -> bytes:
    """Devuelve una secuencia de bytes arbitrarios que no conforman una imagen válida."""
    return b"\xff\xd8\xff\xe0\x00\x10JFIF_CORRUPTED_DATA_NOT_AN_IMAGE_1234567890"
