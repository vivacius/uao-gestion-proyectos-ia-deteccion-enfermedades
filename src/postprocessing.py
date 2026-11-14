"""Módulo de procesamiento e interpretación de resultados de inferencia."""

from __future__ import annotations

from dataclasses import dataclass

import torch

from src.config import AGRONOMIC_DISCLAIMER, DEFAULT_TOP_K
from src.labels import parse_category_label


@dataclass(frozen=True)
class TopPredictionItem:
    """Representa una predicción individual dentro del ranking Top-K."""

    rank: int
    class_id: int
    predicted_category: str
    plant: str
    plant_en: str
    disease_or_condition: str
    disease_or_condition_en: str
    is_healthy: bool | None
    health_status: str
    confidence: float
    confidence_percentage: float


@dataclass(frozen=True)
class ClassificationResult:
    """Resultado completo de la clasificación de una hoja."""

    predicted_category: str
    class_id: int
    plant: str
    plant_en: str
    disease_or_condition: str
    disease_or_condition_en: str
    is_healthy: bool | None
    health_status: str
    confidence: float
    confidence_percentage: float
    top_predictions: list[TopPredictionItem]
    inference_time_ms: float
    disclaimer: str = AGRONOMIC_DISCLAIMER


def process_logits(
    logits: torch.Tensor,
    id2label: dict[int, str],
    inference_time_ms: float,
    top_k: int = DEFAULT_TOP_K,
) -> ClassificationResult:
    """Convierte los logits de salida del modelo en un ``ClassificationResult`` estructurado.

    Calcula las probabilidades mediante ``softmax``, ordena las ``top_k`` categorías
    más probables y traduce/estructura cada etiqueta.
    """
    if logits.ndim == 2:
        logits_1d = logits[0]
    elif logits.ndim == 1:
        logits_1d = logits
    else:
        raise ValueError(
            f"Se esperaba un tensor de logits 1D o 2D, pero se recibió forma {tuple(logits.shape)}."
        )

    num_classes = int(logits_1d.shape[-1])
    effective_k = max(1, min(top_k, num_classes))

    probabilities = torch.nn.functional.softmax(logits_1d.float(), dim=-1)
    top_probs, top_indices = torch.topk(probabilities, k=effective_k)

    top_predictions: list[TopPredictionItem] = []
    for rank_idx in range(effective_k):
        class_id = int(top_indices[rank_idx].item())
        prob = float(top_probs[rank_idx].item())
        raw_label = id2label.get(class_id, f"Class_{class_id}")
        metadata = parse_category_label(raw_label)

        top_predictions.append(
            TopPredictionItem(
                rank=rank_idx + 1,
                class_id=class_id,
                predicted_category=metadata.raw_label,
                plant=metadata.plant_es,
                plant_en=metadata.plant_en,
                disease_or_condition=metadata.condition_es,
                disease_or_condition_en=metadata.condition_en,
                is_healthy=metadata.is_healthy,
                health_status=metadata.health_status,
                confidence=round(prob, 6),
                confidence_percentage=round(prob * 100.0, 2),
            )
        )

    best = top_predictions[0]
    return ClassificationResult(
        predicted_category=best.predicted_category,
        class_id=best.class_id,
        plant=best.plant,
        plant_en=best.plant_en,
        disease_or_condition=best.disease_or_condition,
        disease_or_condition_en=best.disease_or_condition_en,
        is_healthy=best.is_healthy,
        health_status=best.health_status,
        confidence=best.confidence,
        confidence_percentage=best.confidence_percentage,
        top_predictions=top_predictions,
        inference_time_ms=round(float(inference_time_ms), 2),
        disclaimer=AGRONOMIC_DISCLAIMER,
    )
