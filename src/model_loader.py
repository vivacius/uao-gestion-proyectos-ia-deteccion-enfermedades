"""Módulo de carga y verificación del modelo local DINOv2-small en CPU."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any

import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification, PreTrainedModel

from src.config import DEVICE, MODEL_DIR, REQUIRED_MODEL_FILES
from src.exceptions import ModelLoadError


@dataclass(frozen=True)
class ModelBundle:
    """Contenedor inmutable con el modelo, el procesador de imágenes y sus metadatos."""

    model: PreTrainedModel
    processor: Any
    device: torch.device
    model_dir: Path
    id2label: dict[int, str]
    label2id: dict[str, int]
    architecture: str


_BUNDLE_LOCK = Lock()
_CACHED_BUNDLE: ModelBundle | None = None


def verify_model_files(model_dir: Path | str | None = None) -> Path:
    """Verifica que la carpeta local del modelo y todos sus archivos requeridos existan.

    Args:
        model_dir: Ruta al directorio del modelo. Si es ``None``, utiliza ``MODEL_DIR``.

    Returns:
        Objeto ``Path`` resuelto del directorio del modelo.

    Raises:
        ModelLoadError: Si el directorio no existe o falta algún archivo obligatorio.
    """
    target_dir = Path(model_dir).resolve() if model_dir is not None else MODEL_DIR.resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        raise ModelLoadError(
            f"El directorio del modelo no existe o no es válido: '{target_dir}'."
        )

    missing_files: list[str] = []
    empty_files: list[str] = []

    for filename in REQUIRED_MODEL_FILES:
        file_path = target_dir / filename
        if not file_path.is_file():
            missing_files.append(filename)
        elif file_path.stat().st_size == 0:
            empty_files.append(filename)

    if missing_files:
        raise ModelLoadError(
            f"Faltan archivos obligatorios del modelo en '{target_dir}': {', '.join(missing_files)}."
        )

    if empty_files:
        raise ModelLoadError(
            f"Los siguientes archivos del modelo están vacíos en '{target_dir}': {', '.join(empty_files)}."
        )

    return target_dir


def load_model_from_disk(model_dir: Path | str | None = None) -> ModelBundle:
    """Carga el procesador y el modelo preentrenado exclusivamente desde la ruta local en CPU.

    No realiza descargas desde internet (``local_files_only=True``) ni altera los pesos.
    """
    target_dir = verify_model_files(model_dir)
    device = torch.device(DEVICE)

    try:
        processor = AutoImageProcessor.from_pretrained(
            str(target_dir),
            local_files_only=True,
        )
        model = AutoModelForImageClassification.from_pretrained(
            str(target_dir),
            local_files_only=True,
        )
        model.to(device)
        model.eval()
    except Exception as exc:
        raise ModelLoadError(
            f"Error al cargar el modelo local desde '{target_dir}': {exc}"
        ) from exc

    raw_id2label = getattr(model.config, "id2label", {}) or {}
    id2label: dict[int, str] = {int(k): str(v) for k, v in raw_id2label.items()}

    raw_label2id = getattr(model.config, "label2id", {}) or {}
    label2id: dict[str, int] = {str(k): int(v) for k, v in raw_label2id.items()}

    architectures = getattr(model.config, "architectures", None) or [model.__class__.__name__]
    architecture = str(architectures[0])

    return ModelBundle(
        model=model,
        processor=processor,
        device=device,
        model_dir=target_dir,
        id2label=id2label,
        label2id=label2id,
        architecture=architecture,
    )


def get_model_bundle(
    model_dir: Path | str | None = None,
    *,
    force_reload: bool = False,
) -> ModelBundle:
    """Obtiene la instancia en caché del modelo o la carga si aún no está inicializada."""
    global _CACHED_BUNDLE
    with _BUNDLE_LOCK:
        if _CACHED_BUNDLE is None or force_reload or (
            model_dir is not None and Path(model_dir).resolve() != _CACHED_BUNDLE.model_dir
        ):
            _CACHED_BUNDLE = load_model_from_disk(model_dir)
        return _CACHED_BUNDLE


def clear_model_cache() -> None:
    """Limpia la instancia en caché del modelo (útil para pruebas automatizadas)."""
    global _CACHED_BUNDLE
    with _BUNDLE_LOCK:
        _CACHED_BUNDLE = None
