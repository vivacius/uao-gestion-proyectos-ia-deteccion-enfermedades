"""Módulo de inferencia en CPU que integra validación, preprocesamiento, modelo y postprocesamiento."""

from __future__ import annotations

import time

import torch

from src.config import DEFAULT_TOP_K
from src.exceptions import ImageValidationError, InferenceError, ModelLoadError
from src.model_loader import ModelBundle, get_model_bundle
from src.postprocessing import ClassificationResult, process_logits
from src.preprocessing import preprocess_image, validate_and_open_image


def predict_from_bytes(
    image_bytes: bytes,
    filename: str | None = None,
    content_type: str | None = None,
    top_k: int = DEFAULT_TOP_K,
    bundle: ModelBundle | None = None,
) -> ClassificationResult:
    """Ejecuta el flujo completo de inferencia a partir de los bytes de una imagen.

    Args:
        image_bytes: Contenido binario del archivo de imagen.
        filename: Nombre original del archivo (opcional, para validar extensión).
        content_type: Tipo MIME del archivo (opcional, para validar formato).
        top_k: Cantidad de categorías más probables a retornar (por defecto 3).
        bundle: Instancia del modelo ya cargada (si no se especifica, usa el singleton).

    Returns:
        ``ClassificationResult`` con la predicción principal, top-k y tiempo de inferencia.
    """
    pil_image = validate_and_open_image(
        image_bytes=image_bytes,
        filename=filename,
        content_type=content_type,
    )

    active_bundle = bundle if bundle is not None else get_model_bundle()

    try:
        start_time = time.perf_counter()
        tensor_inputs = preprocess_image(
            image=pil_image,
            processor=active_bundle.processor,
            device=active_bundle.device,
        )
        with torch.no_grad():
            outputs = active_bundle.model(**tensor_inputs)
            logits = outputs.logits
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    except (ImageValidationError, ModelLoadError):
        raise
    except Exception as exc:
        raise InferenceError(
            f"Ocurrió un error interno durante la inferencia del modelo: {exc}"
        ) from exc

    return process_logits(
        logits=logits,
        id2label=active_bundle.id2label,
        inference_time_ms=elapsed_ms,
        top_k=top_k,
    )
