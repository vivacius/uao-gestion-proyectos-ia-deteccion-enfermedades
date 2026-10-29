"""Esquemas Pydantic para las respuestas de la API REST."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Esquema de respuesta del endpoint ``GET /health``."""

    status: str = Field(..., description="Estado general del servicio ('ok' o 'degraded').")
    model_available: bool = Field(..., description="Indica si el modelo local está cargado y disponible.")
    model_name: str = Field(
        default="rodynaemad/plant-disease-dinov2-small",
        description="Identificador del modelo base preentrenado.",
    )
    architecture: str | None = Field(
        default=None,
        description="Arquitectura interna de la red neuronal.",
    )
    device: str = Field(default="cpu", description="Dispositivo de cómputo activo.")
    num_classes: int = Field(default=0, description="Cantidad de clases soportadas por el modelo.")
    model_path: str | None = Field(default=None, description="Ruta local desde donde se cargó el modelo.")
    detail: str | None = Field(default=None, description="Detalle adicional o mensaje de error si aplica.")


class TopPredictionSchema(BaseModel):
    """Esquema para cada una de las categorías más probables (Top-3)."""

    rank: int = Field(..., ge=1, description="Posición en el ranking de probabilidad (1 a 3).")
    class_id: int = Field(..., ge=0, description="Índice numérico de la clase en el modelo.")
    predicted_category: str = Field(
        ...,
        description="Etiqueta original del modelo (ej. 'Tomato___Late_blight').",
    )
    plant: str = Field(..., description="Nombre de la planta en español.")
    plant_en: str = Field(..., description="Nombre de la planta en inglés.")
    disease_or_condition: str = Field(..., description="Enfermedad o condición detectada en español.")
    disease_or_condition_en: str = Field(..., description="Enfermedad o condición detectada en inglés.")
    is_healthy: bool | None = Field(
        default=None,
        description="True si la hoja se clasificó como sana, False si presenta enfermedad.",
    )
    health_status: str = Field(
        ...,
        description="Estado fitosanitario ('Sana', 'Enferma' o 'No determinado').",
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Probabilidad estimada en rango [0, 1].")
    confidence_percentage: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Porcentaje de confianza en rango [0, 100].",
    )


class PredictionResponse(BaseModel):
    """Esquema de respuesta del endpoint ``POST /predict``."""

    predicted_category: str = Field(
        ...,
        description="Nombre de la categoría predicha con mayor probabilidad.",
    )
    class_id: int = Field(..., ge=0, description="Identificador numérico de la categoría predicha.")
    plant: str = Field(..., description="Planta identificada (en español).")
    plant_en: str = Field(..., description="Planta identificada (en inglés).")
    disease_or_condition: str = Field(..., description="Enfermedad o condición detectada (en español).")
    disease_or_condition_en: str = Field(..., description="Enfermedad o condición detectada (en inglés).")
    is_healthy: bool | None = Field(
        default=None,
        description="Indica si la hoja fue clasificada como sana (True) o enferma (False).",
    )
    health_status: str = Field(..., description="Estado de la hoja: 'Sana' o 'Enferma'.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Puntuación de confianza del modelo [0, 1].")
    confidence_percentage: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Porcentaje de confianza del modelo [0, 100].",
    )
    top_predictions: list[TopPredictionSchema] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="Lista con las tres categorías más probables ordenadas de mayor a menor confianza.",
    )
    inference_time_ms: float = Field(
        ...,
        ge=0.0,
        description="Tiempo empleado en la inferencia en milisegundos.",
    )
    disclaimer: str = Field(
        ...,
        description="Aviso sobre el carácter orientativo de las predicciones.",
    )


class ErrorResponse(BaseModel):
    """Esquema estándar de error devuelto por la API."""

    detail: str = Field(..., description="Descripción clara del error ocurrido.")
    error_type: str = Field(..., description="Tipo o categoría del error.")
