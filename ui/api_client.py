"""Cliente HTTP para que la interfaz Streamlit consuma el servicio FastAPI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from src.config import API_BASE_URL


@dataclass(frozen=True)
class ApiClientResponse:
    """Resultado encapsulado de una llamada a la API REST."""

    success: bool
    status_code: int
    data: dict[str, Any] | None = None
    error_message: str | None = None


def fetch_api_health(
    base_url: str = API_BASE_URL,
    timeout: float = 5.0,
) -> ApiClientResponse:
    """Consulta el endpoint ``GET /health`` del backend FastAPI."""
    url = f"{base_url.rstrip('/')}/health"
    try:
        response = requests.get(url, timeout=timeout)
        payload = response.json()
        if response.status_code == 200 and payload.get("model_available"):
            return ApiClientResponse(
                success=True,
                status_code=response.status_code,
                data=payload,
            )
        detail = payload.get("detail") or "El modelo no se encuentra disponible en el servidor."
        return ApiClientResponse(
            success=False,
            status_code=response.status_code,
            data=payload,
            error_message=detail,
        )
    except requests.ConnectionError:
        return ApiClientResponse(
            success=False,
            status_code=0,
            error_message=(
                f"No se pudo conectar con el servidor de inferencia en {base_url}. "
                "Asegúrese de que la API FastAPI esté en ejecución."
            ),
        )
    except requests.Timeout:
        return ApiClientResponse(
            success=False,
            status_code=0,
            error_message=(
                "El servidor de inferencia tardó demasiado en responder (tiempo de espera agotado)."
            ),
        )
    except Exception as exc:
        return ApiClientResponse(
            success=False,
            status_code=0,
            error_message=f"Error inesperado al verificar el estado del servidor: {exc}",
        )


def request_image_prediction(
    image_bytes: bytes,
    filename: str,
    content_type: str = "image/jpeg",
    base_url: str = API_BASE_URL,
    timeout: float = 30.0,
) -> ApiClientResponse:
    """Envía una imagen al endpoint ``POST /predict`` de FastAPI y retorna el resultado."""
    url = f"{base_url.rstrip('/')}/predict"
    files = {"file": (filename, image_bytes, content_type)}

    try:
        response = requests.post(url, files=files, timeout=timeout)
        try:
            payload = response.json()
        except ValueError:
            payload = {}

        if response.status_code == 200:
            return ApiClientResponse(
                success=True,
                status_code=200,
                data=payload,
            )

        error_detail = payload.get("detail")
        if isinstance(error_detail, list):
            error_detail = "; ".join(
                item.get("msg", str(item)) if isinstance(item, dict) else str(item)
                for item in error_detail
            )
        elif not error_detail:
            error_detail = f"El servidor devolvió un error (código HTTP {response.status_code})."

        return ApiClientResponse(
            success=False,
            status_code=response.status_code,
            data=payload,
            error_message=str(error_detail),
        )
    except requests.ConnectionError:
        return ApiClientResponse(
            success=False,
            status_code=0,
            error_message=(
                f"No fue posible comunicarse con la API en {base_url}. "
                "Verifique que el servicio FastAPI esté iniciado antes de analizar la imagen."
            ),
        )
    except requests.Timeout:
        return ApiClientResponse(
            success=False,
            status_code=0,
            error_message="La solicitud de clasificación superó el tiempo máximo de espera.",
        )
    except Exception as exc:
        return ApiClientResponse(
            success=False,
            status_code=0,
            error_message=f"Ocurrió un error al enviar la imagen al servicio de inferencia: {exc}",
        )
