"""Pruebas unitarias exhaustivas para el catálogo de 38 etiquetas, limpieza y postprocesamiento."""

from __future__ import annotations

import json

import pytest
import torch

from src.config import AGRONOMIC_DISCLAIMER, MODEL_DIR, NUM_EXPECTED_CLASSES
from src.labels import clean_identifier, parse_category_label
from src.postprocessing import process_logits

ALL_38_LABELS: list[tuple[int, str]] = [
    (0, "Apple___Apple_scab"),
    (1, "Apple___Black_rot"),
    (2, "Apple___Cedar_apple_rust"),
    (3, "Apple___healthy"),
    (4, "Blueberry___healthy"),
    (5, "Cherry_(including_sour)___Powdery_mildew"),
    (6, "Cherry_(including_sour)___healthy"),
    (7, "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot"),
    (8, "Corn_(maize)___Common_rust_"),
    (9, "Corn_(maize)___Northern_Leaf_Blight"),
    (10, "Corn_(maize)___healthy"),
    (11, "Grape___Black_rot"),
    (12, "Grape___Esca_(Black_Measles)"),
    (13, "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)"),
    (14, "Grape___healthy"),
    (15, "Orange___Haunglongbing_(Citrus_greening)"),
    (16, "Peach___Bacterial_spot"),
    (17, "Peach___healthy"),
    (18, "Pepper,_bell___Bacterial_spot"),
    (19, "Pepper,_bell___healthy"),
    (20, "Potato___Early_blight"),
    (21, "Potato___Late_blight"),
    (22, "Potato___healthy"),
    (23, "Raspberry___healthy"),
    (24, "Soybean___healthy"),
    (25, "Squash___Powdery_mildew"),
    (26, "Strawberry___Leaf_scorch"),
    (27, "Strawberry___healthy"),
    (28, "Tomato___Bacterial_spot"),
    (29, "Tomato___Early_blight"),
    (30, "Tomato___Late_blight"),
    (31, "Tomato___Leaf_Mold"),
    (32, "Tomato___Septoria_leaf_spot"),
    (33, "Tomato___Spider_mites Two-spotted_spider_mite"),
    (34, "Tomato___Target_Spot"),
    (35, "Tomato___Tomato_Yellow_Leaf_Curl_Virus"),
    (36, "Tomato___Tomato_mosaic_virus"),
    (37, "Tomato___healthy"),
]


@pytest.mark.unit
@pytest.mark.parametrize("class_id,raw_label", ALL_38_LABELS)
def test_individual_category_label_parsing_and_translation(
    class_id: int,
    raw_label: str,
) -> None:
    """Verifica individualmente cada una de las 38 clases del modelo en inglés y español."""
    assert 0 <= class_id < 38
    meta = parse_category_label(raw_label)

    assert meta.raw_label == raw_label
    assert meta.plant_en != ""
    assert meta.plant_es != ""
    assert meta.condition_en != ""
    assert meta.condition_es != ""

    if raw_label.endswith("___healthy"):
        assert meta.is_healthy is True
        assert meta.health_status == "Sana"
        assert meta.condition_en == "Healthy"
    else:
        assert meta.is_healthy is False
        assert meta.health_status == "Enferma"


@pytest.mark.unit
@pytest.mark.parametrize("class_id,raw_label", ALL_38_LABELS)
def test_process_logits_identifies_each_of_38_classes_as_top1(
    class_id: int,
    raw_label: str,
) -> None:
    """Verifica que process_logits seleccione cada una de las 38 clases cuando tiene el logit máximo."""
    id2label = dict(ALL_38_LABELS)
    logits = torch.zeros((1, 38), dtype=torch.float32)
    logits[0, class_id] = 10.0

    result = process_logits(
        logits=logits,
        id2label=id2label,
        inference_time_ms=12.34,
        top_k=3,
    )

    assert result.class_id == class_id
    assert result.predicted_category == raw_label
    assert result.top_predictions[0].class_id == class_id
    assert result.top_predictions[0].rank == 1
    assert result.confidence > 0.99


@pytest.mark.unit
@pytest.mark.parametrize(
    "raw_input,expected",
    [
        ("Apple___scab", "Apple scab"),
        ("  Corn__Common_rust_  ", "Corn Common rust"),
        ("SingleWord", "SingleWord"),
        ("Multiple___Underscores___Here", "Multiple Underscores Here"),
    ],
)
def test_clean_identifier_variants(raw_input: str, expected: str) -> None:
    """Verifica la normalización de espacios y guiones bajos en clean_identifier."""
    assert clean_identifier(raw_input) == expected


@pytest.mark.unit
def test_parse_healthy_category_label() -> None:
    """Verifica que una etiqueta sana identifique planta, estado 'Sana' e is_healthy=True."""
    meta = parse_category_label("Tomato___healthy")
    assert meta.raw_label == "Tomato___healthy"
    assert meta.plant_en == "Tomato"
    assert meta.plant_es == "Tomate"
    assert meta.is_healthy is True
    assert meta.health_status == "Sana"
    assert "Sana" in meta.condition_es


@pytest.mark.unit
def test_parse_diseased_category_label() -> None:
    """Verifica que una etiqueta de enfermedad identifique planta, enfermedad e is_healthy=False."""
    meta = parse_category_label("Apple___Apple_scab")
    assert meta.raw_label == "Apple___Apple_scab"
    assert meta.plant_en == "Apple"
    assert meta.plant_es == "Manzano"
    assert meta.is_healthy is False
    assert meta.health_status == "Enferma"
    assert "Sarna" in meta.condition_es


@pytest.mark.unit
def test_parse_unknown_or_empty_label() -> None:
    """Verifica el comportamiento resiliente ante etiquetas sin separador o vacías."""
    empty_meta = parse_category_label("   ")
    assert empty_meta.is_healthy is None
    assert empty_meta.health_status == "No determinado"

    unstructured_meta = parse_category_label("CustomPlantLabel")
    assert unstructured_meta.plant_en == "CustomPlantLabel"
    assert unstructured_meta.is_healthy is None
    assert unstructured_meta.health_status == "No determinado"


@pytest.mark.unit
def test_all_38_config_labels_coherence() -> None:
    """Comprueba que las 38 etiquetas de config.json sean coherentes y tengan traducción en español."""
    config_path = MODEL_DIR / "config.json"
    assert config_path.is_file(), f"No se encontró config.json en {config_path}"

    config_data = json.loads(config_path.read_text(encoding="utf-8"))
    id2label: dict[str, str] = config_data["id2label"]
    label2id: dict[str, int] = config_data["label2id"]

    assert len(id2label) == NUM_EXPECTED_CLASSES == 38
    assert len(label2id) == NUM_EXPECTED_CLASSES == 38

    healthy_count = 0
    diseased_count = 0

    for str_id, raw_label in id2label.items():
        idx = int(str_id)
        assert label2id[raw_label] == idx
        assert "___" in raw_label

        meta = parse_category_label(raw_label)
        assert meta.plant_es != ""
        assert meta.condition_es != ""
        assert meta.is_healthy in (True, False)
        if meta.is_healthy:
            healthy_count += 1
            assert meta.health_status == "Sana"
        else:
            diseased_count += 1
            assert meta.health_status == "Enferma"

    # Según la documentación oficial del modelo: 12 clases sanas y 26 enfermedades = 38 clases
    assert healthy_count == 12
    assert diseased_count == 26


@pytest.mark.unit
def test_process_logits_top3_and_1d_tensor_support() -> None:
    """Verifica el cálculo de softmax tanto para tensores 1D como 2D y ordenamiento Top-3."""
    dummy_id2label = {
        0: "Apple___Apple_scab",
        1: "Apple___Black_rot",
        2: "Apple___healthy",
        3: "Tomato___Late_blight",
    }
    logits_1d = torch.tensor([0.5, 1.2, 4.8, 2.1], dtype=torch.float32)

    result = process_logits(
        logits=logits_1d,
        id2label=dummy_id2label,
        inference_time_ms=14.567,
        top_k=3,
    )

    assert result.predicted_category == "Apple___healthy"
    assert result.class_id == 2
    assert result.plant == "Manzano"
    assert result.is_healthy is True
    assert result.health_status == "Sana"
    assert result.inference_time_ms == 14.57
    assert result.disclaimer == AGRONOMIC_DISCLAIMER
    assert len(result.top_predictions) == 3
    assert [item.class_id for item in result.top_predictions] == [2, 3, 1]


@pytest.mark.unit
def test_process_logits_invalid_tensor_shape_raises() -> None:
    """Verifica que un tensor de logits con dimensiones inválidas lance ValueError."""
    bad_logits = torch.zeros((1, 2, 4))
    with pytest.raises(ValueError, match="1D o 2D"):
        process_logits(logits=bad_logits, id2label={0: "Apple___healthy"}, inference_time_ms=1.0)
