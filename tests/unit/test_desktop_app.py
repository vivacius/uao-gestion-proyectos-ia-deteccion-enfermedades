"""Pruebas unitarias para la interfaz gráfica de escritorio en Tkinter (ui/desktop_app.py)."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from unittest.mock import patch

import pytest

from ui.api_client import ApiClientResponse
from ui.desktop_app import (
    COLOR_DISEASED_BG,
    COLOR_HEALTHY_BG,
    PlantDiseaseDesktopApp,
    guess_mime_type,
)


@pytest.fixture
def tk_root() -> tk.Tk:
    """Crea una instancia oculta de Tk para pruebas de widgets."""
    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError as exc:
        pytest.skip(f"Entorno Tcl/Tk no disponible: {exc}")
    yield root
    root.destroy()


@pytest.mark.unit
def test_guess_mime_type() -> None:
    """Verifica que guess_mime_type devuelva el MIME esperado para JPG y PNG."""
    assert guess_mime_type(Path("hoja.jpg")) == "image/jpeg"
    assert guess_mime_type(Path("hoja.jpeg")) == "image/jpeg"
    assert guess_mime_type(Path("hoja.png")) == "image/png"


@pytest.mark.unit
def test_desktop_app_health_response_online(tk_root: tk.Tk) -> None:
    """Verifica que el estado de la API se actualice a en línea cuando /health responde OK."""
    with patch.object(PlantDiseaseDesktopApp, "check_api_health_async"):
        app = PlantDiseaseDesktopApp(tk_root, initial_api_url="http://127.0.0.1:8000")

    health_resp = ApiClientResponse(
        success=True,
        status_code=200,
        data={
            "model_name": "rodynaemad/plant-disease-dinov2-small",
            "architecture": "Dinov2ForImageClassification",
            "device": "cpu",
            "num_classes": 38,
        },
    )
    app._on_health_response(health_resp)

    assert "API en línea" in app.health_badge.cget("text")
    assert app.health_badge.cget("bg") == COLOR_HEALTHY_BG
    assert "Dinov2ForImageClassification" in app.health_details_lbl.cget("text")


@pytest.mark.unit
def test_desktop_app_load_image_and_render_results(
    tk_root: tk.Tk,
    tmp_path: Path,
    valid_jpeg_bytes: bytes,
) -> None:
    """Verifica la carga de una imagen en disco y el renderizado del resultado Top-3."""
    img_file = tmp_path / "tomate_prueba.jpg"
    img_file.write_bytes(valid_jpeg_bytes)

    with patch.object(PlantDiseaseDesktopApp, "check_api_health_async"):
        app = PlantDiseaseDesktopApp(tk_root)

    loaded = app.load_image_from_path(img_file)
    assert loaded is True
    assert app.selected_file_path == img_file
    assert str(app.btn_analyze.cget("state")) == "normal"

    sample_prediction = {
        "predicted_category": "Tomato___Late_blight",
        "class_id": 30,
        "plant": "Tomate",
        "plant_en": "Tomato",
        "disease_or_condition": "Tizón tardío (Phytophthora infestans)",
        "disease_or_condition_en": "Late blight",
        "is_healthy": False,
        "health_status": "Enferma",
        "confidence": 0.965,
        "confidence_percentage": 96.5,
        "inference_time_ms": 48.2,
        "disclaimer": "Aviso de prueba.",
        "top_predictions": [
            {
                "rank": 1,
                "class_id": 30,
                "predicted_category": "Tomato___Late_blight",
                "plant": "Tomate",
                "disease_or_condition": "Tizón tardío (Phytophthora infestans)",
                "health_status": "Enferma",
                "confidence_percentage": 96.5,
            },
            {
                "rank": 2,
                "class_id": 29,
                "predicted_category": "Tomato___Early_blight",
                "plant": "Tomate",
                "disease_or_condition": "Tizón temprano (Alternaria)",
                "health_status": "Enferma",
                "confidence_percentage": 2.5,
            },
            {
                "rank": 3,
                "class_id": 37,
                "predicted_category": "Tomato___healthy",
                "plant": "Tomate",
                "disease_or_condition": "Sana (sin enfermedad aparente)",
                "health_status": "Sana",
                "confidence_percentage": 1.0,
            },
        ],
    }

    app.render_prediction_results(sample_prediction)

    assert app.status_banner.cget("bg") == COLOR_DISEASED_BG
    assert app.metric_plant_val.cget("text") == "Tomate"
    assert app.metric_conf_val.cget("text") == "96.50 %"
    assert len(app.top3_tree.get_children()) == 3
