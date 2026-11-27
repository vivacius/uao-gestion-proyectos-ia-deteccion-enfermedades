"""Pruebas unitarias exhaustivas de taxonomía PlantVillage (38 clases) y postprocesamiento."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch

from src.config import AGRONOMIC_DISCLAIMER
from src.labels import (
    CONDITION_TRANSLATIONS_ES,
    PLANT_TRANSLATIONS_ES,
    clean_identifier,
    parse_category_label,
)
from src.postprocessing import process_logits

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.json"
ID2LABEL: dict[int, str] = {
    int(k): v for k, v in json.loads(CONFIG_PATH.read_text(encoding="utf-8"))["id2label"].items()
}
ALL_CLASSES: list[tuple[int, str]] = sorted(ID2LABEL.items())


@pytest.mark.parametrize(("class_id", "raw_label"), ALL_CLASSES)
def test_parse_category_label_all_38_classes(class_id: int, raw_label: str) -> None:
    """Verifica traducción al español y estado fitosanitario para las 38 clases reales."""
    # Arrange
    expected_healthy = raw_label.endswith("___healthy")
    expected_status = "Sana" if expected_healthy else "Enferma"

    # Act
    meta = parse_category_label(raw_label)

    # Assert
    assert 0 <= class_id < 38
    assert meta.raw_label == raw_label
    assert meta.plant_es and meta.plant_es != ""
    assert meta.condition_es and meta.condition_es != ""
    assert meta.is_healthy is expected_healthy
    assert meta.health_status == expected_status


@pytest.mark.parametrize(("class_id", "raw_label"), ALL_CLASSES)
def test_process_logits_ranks_each_of_38_classes_first(class_id: int, raw_label: str) -> None:
    """Verifica que process_logits posiciona en rank 1 a cada una de las 38 clases."""
    # Arrange
    logits = torch.full((1, 38), -5.0, dtype=torch.float32)
    logits[0, class_id] = 6.0

    # Act
    result = process_logits(logits=logits, id2label=ID2LABEL, inference_time_ms=12.5, top_k=3)

    # Assert
    assert result.class_id == class_id
    assert result.predicted_category == raw_label
    assert result.top_predictions[0].rank == 1
    assert len(result.top_predictions) == 3
    assert 0.99 <= result.confidence <= 1.0
    assert result.disclaimer == AGRONOMIC_DISCLAIMER


@pytest.mark.parametrize(
    ("raw_text", "expected"),
    [
        ("Tomato_Late_blight", "Tomato Late blight"),
        ("Apple___Black_rot", "Apple Black rot"),
        ("  Corn__Common__rust_  ", "Corn Common rust"),
        ("SingleWord", "SingleWord"),
        ("Multiple___Spaces___Here", "Multiple Spaces Here"),
    ],
)
def test_clean_identifier_normalizes_underscores_and_spaces(raw_text: str, expected: str) -> None:
    """Verifica la limpieza de guiones bajos y espacios repetidos."""
    # Arrange / Act
    cleaned = clean_identifier(raw_text)

    # Assert
    assert cleaned == expected


@pytest.mark.parametrize(
    ("raw_label", "expected_plant", "expected_status"),
    [
        ("", "Desconocida", "No determinado"),
        ("   ", "Desconocida", "No determinado"),
        ("NoSeparatorLabel", "NoSeparatorLabel", "No determinado"),
        ("CustomPlant___unknown", "CustomPlant", "No determinado"),
        ("CustomPlant___Nueva_Enfermedad", "CustomPlant", "Enferma"),
    ],
)
def test_parse_category_label_edge_cases(
    raw_label: str,
    expected_plant: str,
    expected_status: str,
) -> None:
    """Verifica el comportamiento de parse_category_label ante entradas atípicas."""
    # Arrange / Act
    meta = parse_category_label(raw_label)

    # Assert
    assert meta.plant_es == expected_plant
    assert meta.health_status == expected_status


def test_process_logits_accepts_1d_tensor() -> None:
    """Verifica que process_logits soporta tensores 1D sin dimensión de batch."""
    # Arrange
    logits = torch.zeros(38, dtype=torch.float32)
    logits[15] = 4.5

    # Act
    result = process_logits(logits=logits, id2label=ID2LABEL, inference_time_ms=8.0, top_k=3)

    # Assert
    assert result.class_id == 15
    assert result.top_predictions[0].class_id == 15


def test_process_logits_rejects_3d_tensor() -> None:
    """Verifica que process_logits rechaza tensores de rango inválido (3D)."""
    # Arrange
    logits = torch.zeros((1, 1, 38), dtype=torch.float32)

    # Act / Assert
    with pytest.raises(ValueError, match="1D o 2D"):
        process_logits(logits=logits, id2label=ID2LABEL, inference_time_ms=5.0)


def test_process_logits_clamps_top_k_minimum_to_one() -> None:
    """Verifica que top_k <= 0 se acota a al menos 1 predicción."""
    # Arrange
    logits = torch.zeros((1, 38), dtype=torch.float32)

    # Act
    result = process_logits(logits=logits, id2label=ID2LABEL, inference_time_ms=4.0, top_k=0)

    # Assert
    assert len(result.top_predictions) == 1


def test_process_logits_clamps_top_k_maximum_to_num_classes() -> None:
    """Verifica que top_k mayor al número de clases se acota a num_classes."""
    # Arrange
    logits = torch.zeros((1, 5), dtype=torch.float32)
    small_map = {i: f"Tomato___Class_{i}" for i in range(5)}

    # Act
    result = process_logits(logits=logits, id2label=small_map, inference_time_ms=4.0, top_k=99)

    # Assert
    assert len(result.top_predictions) == 5


def test_process_logits_fallback_when_label_missing_from_id2label() -> None:
    """Verifica etiqueta de respaldo Class_<id> si falta la clave en id2label."""
    # Arrange
    logits = torch.tensor([[10.0, 0.0]], dtype=torch.float32)

    # Act
    result = process_logits(logits=logits, id2label={}, inference_time_ms=3.0, top_k=2)

    # Assert
    assert result.predicted_category == "Class_0"
    assert result.health_status == "No determinado"


@pytest.mark.parametrize(("plant_key", "expected_es"), list(PLANT_TRANSLATIONS_ES.items())[:10])
def test_plant_translations_dictionary_entries_are_non_empty(
    plant_key: str,
    expected_es: str,
) -> None:
    """Verifica entradas de traducción de cultivos al español."""
    # Arrange / Act
    meta = parse_category_label(f"{plant_key}___healthy")

    # Assert
    assert meta.plant_es == expected_es
    assert meta.is_healthy is True


@pytest.mark.parametrize(("cond_key", "expected_es"), list(CONDITION_TRANSLATIONS_ES.items())[:6])
def test_condition_translations_dictionary_entries_map_correctly(
    cond_key: str,
    expected_es: str,
) -> None:
    """Verifica entradas de traducción de enfermedades en español."""
    # Arrange / Act
    meta = parse_category_label(f"Tomato___{cond_key}")

    # Assert
    assert meta.condition_es == expected_es
