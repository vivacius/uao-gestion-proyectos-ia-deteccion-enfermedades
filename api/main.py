"""Punto de entrada de la API REST con FastAPI para inferencia de enfermedades en plantas."""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import asdict
from typing import AsyncIterator

from fastapi import FastAPI, File, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.schemas import ErrorResponse, HealthResponse, PredictionResponse
from src.config import DEFAULT_TOP_K, DEVICE
from src.exceptions import (
    ImageValidationError,
    InferenceError,
    ModelLoadError,
    PlantDiseaseAppError,
)
from src.inference import predict_from_bytes
from src.model_loader import get_model_bundle


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Precarga el modelo en memoria al iniciar el servidor FastAPI."""
    try:
        get_model_bundle()
    except ModelLoadError:
        # Si el modelo no está disponible en el arranque, /health informará el estado degradado
        pass
    yield


app = FastAPI(
    title="API de Identificación de Enfermedades en Plantas (DINOv2-small)",
    description=(
        "Servicio de inferencia (Model-as-a-Service) para clasificar posibles "
        "enfermedades vegetales a partir de fotografías de hojas utilizando el modelo "
        "preentrenado `rodynaemad/plant-disease-dinov2-small` sobre PyTorch en CPU."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ImageValidationError)
async def image_validation_exception_handler(
    _request: Request,
    exc: ImageValidationError,
) -> JSONResponse:
    """Convierte errores de validación de imagen en respuestas HTTP estructuradas."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": str(exc),
            "error_type": exc.__class__.__name__,
        },
    )


@app.exception_handler(ModelLoadError)
async def model_load_exception_handler(
    _request: Request,
    exc: ModelLoadError,
) -> JSONResponse:
    """Convierte errores de carga del modelo en HTTP 503 Service Unavailable."""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": str(exc),
            "error_type": exc.__class__.__name__,
        },
    )


@app.exception_handler(InferenceError)
async def inference_exception_handler(
    _request: Request,
    exc: InferenceError,
) -> JSONResponse:
    """Convierte errores internos de inferencia en HTTP 500 Internal Server Error."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "error_type": exc.__class__.__name__,
        },
    )


@app.exception_handler(PlantDiseaseAppError)
async def generic_app_exception_handler(
    _request: Request,
    exc: PlantDiseaseAppError,
) -> JSONResponse:
    """Manejador de respaldo para cualquier otra excepción de dominio."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "error_type": exc.__class__.__name__,
        },
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Verificar el estado de la API y disponibilidad del modelo",
    tags=["Salud del Servicio"],
)
def health_check() -> HealthResponse:
    """Informa si la aplicación está activa y si el modelo DINOv2-small está cargado en CPU."""
    try:
        bundle = get_model_bundle()
        return HealthResponse(
            status="ok",
            model_available=True,
            model_name="rodynaemad/plant-disease-dinov2-small",
            architecture=bundle.architecture,
            device=str(bundle.device),
            num_classes=len(bundle.id2label),
            model_path=str(bundle.model_dir),
            detail="Servicio operativo y modelo cargado correctamente en CPU.",
        )
    except ModelLoadError as exc:
        return HealthResponse(
            status="degraded",
            model_available=False,
            model_name="rodynaemad/plant-disease-dinov2-small",
            architecture=None,
            device=DEVICE,
            num_classes=0,
            model_path=None,
            detail=str(exc),
        )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Imagen vacía, corrupta o inválida"},
        413: {"model": ErrorResponse, "description": "Imagen supera el tamaño máximo permitido"},
        415: {"model": ErrorResponse, "description": "Formato de archivo no permitido"},
        500: {"model": ErrorResponse, "description": "Error interno durante la inferencia"},
        503: {"model": ErrorResponse, "description": "Modelo no disponible"},
    },
    summary="Clasificar una fotografía de hoja para identificar posibles enfermedades",
    tags=["Inferencia"],
)
async def predict_endpoint(
    file: UploadFile = File(
        ...,
        description="Archivo de imagen de una hoja en formato JPG, JPEG o PNG.",
    ),
) -> PredictionResponse:
    """Recibe una fotografía de hoja vegetal y devuelve la predicción principal y el Top-3."""
    image_bytes = await file.read()

    result = predict_from_bytes(
        image_bytes=image_bytes,
        filename=file.filename,
        content_type=file.content_type,
        top_k=DEFAULT_TOP_K,
    )

    return PredictionResponse(**asdict(result))
