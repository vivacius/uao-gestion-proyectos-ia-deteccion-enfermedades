"""Excepciones personalizadas de dominio para la aplicación."""

from __future__ import annotations


class PlantDiseaseAppError(Exception):
    """Excepción base de la aplicación."""


class ModelLoadError(PlantDiseaseAppError):
    """Error al cargar o verificar el modelo local desde disco."""


class ImageValidationError(PlantDiseaseAppError):
    """Excepción base para errores de validación o preprocesamiento de imágenes."""

    status_code: int = 400

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code


class EmptyImageError(ImageValidationError):
    """El archivo de imagen está vacío (0 bytes)."""

    status_code = 400


class ImageTooLargeError(ImageValidationError):
    """El archivo de imagen supera el tamaño máximo permitido."""

    status_code = 413


class UnsupportedImageFormatError(ImageValidationError):
    """El formato del archivo no corresponde a JPG, JPEG o PNG."""

    status_code = 415


class CorruptedImageError(ImageValidationError):
    """El archivo de imagen está dañado, truncado o no puede decodificarse."""

    status_code = 400


class InferenceError(PlantDiseaseAppError):
    """Error durante la ejecución de la inferencia del modelo."""
