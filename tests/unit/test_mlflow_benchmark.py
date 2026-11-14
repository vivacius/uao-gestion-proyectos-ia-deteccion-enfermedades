"""Pruebas unitarias para el script de benchmark y trazabilidad en MLflow."""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from scripts.run_mlflow_benchmark import (
    Dinov2InferenceWrapper,
    build_fixed_evaluation_set,
    create_synthetic_benchmark_sample,
    get_git_commit_hash,
    parse_arguments,
)
from src.postprocessing import ClassificationResult, TopPredictionItem


@pytest.mark.unit
class TestMlflowBenchmarkComponents:
    """Verifica los módulos de benchmarking, generación de datos y envoltura de modelos."""

    def test_create_synthetic_benchmark_sample_generates_valid_image(self) -> None:
        """Arrange & Act: Generar muestra sintética con patrón necrótico."""
        img_bytes = create_synthetic_benchmark_sample(
            width=200, height=200, mode="RGB", image_format="JPEG", spot_type="necrotic"
        )

        # Assert
        assert isinstance(img_bytes, bytes)
        assert len(img_bytes) > 0
        img = Image.open(io.BytesIO(img_bytes))
        assert img.size == (200, 200)
        assert img.format == "JPEG"

    def test_build_fixed_evaluation_set_has_ten_samples(self) -> None:
        """Arrange & Act: Construir conjunto fijo de evaluación."""
        samples = build_fixed_evaluation_set()

        # Assert: 10 muestras con nombres únicos y bytes válidos
        assert len(samples) == 10
        names = [s[0] for s in samples]
        assert len(set(names)) == 10
        for name, data in samples:
            assert isinstance(name, str)
            assert isinstance(data, bytes)
            assert len(data) > 0

    def test_get_git_commit_hash_returns_string(self) -> None:
        """Arrange & Act: Obtener hash de Git."""
        commit_hash = get_git_commit_hash()

        # Assert
        assert isinstance(commit_hash, str)
        assert len(commit_hash) > 0

    def test_dinov2_inference_wrapper_predict_with_bytes(self) -> None:
        """Arrange: Configurar wrapper PyFunc con mock de predict_from_bytes."""
        wrapper = Dinov2InferenceWrapper()
        fake_top = TopPredictionItem(
            rank=1,
            class_id=37,
            predicted_category="Tomato___healthy",
            plant="Tomate",
            plant_en="Tomato",
            disease_or_condition="Sana (sin enfermedad aparente)",
            disease_or_condition_en="Healthy",
            is_healthy=True,
            health_status="Sana",
            confidence=0.95,
            confidence_percentage=95.0,
        )
        fake_result = ClassificationResult(
            predicted_category="Tomato___healthy",
            class_id=37,
            plant="Tomate",
            plant_en="Tomato",
            disease_or_condition="Sana (sin enfermedad aparente)",
            disease_or_condition_en="Healthy",
            is_healthy=True,
            health_status="Sana",
            confidence=0.95,
            confidence_percentage=95.0,
            top_predictions=[fake_top],
            inference_time_ms=12.5,
        )

        with patch("scripts.run_mlflow_benchmark.predict_from_bytes", return_value=fake_result):
            # Act
            predictions = wrapper.predict(
                context=MagicMock(),
                model_input=[b"fake_image_bytes"],
                params={"top_k": 3, "threshold": 0.60},
            )

        # Assert
        assert len(predictions) == 1
        assert predictions[0]["predicted_category"] == "Tomato___healthy"
        assert predictions[0]["is_uncertain"] is False
        assert predictions[0]["top_predictions"][0]["confidence"] == 0.95

    def test_dinov2_inference_wrapper_handles_file_path(self, tmp_path: Path) -> None:
        """Arrange: Crear archivo de imagen temporal y pasar ruta string."""
        sample_file = tmp_path / "sample.jpg"
        sample_file.write_bytes(b"dummy_image_data")

        wrapper = Dinov2InferenceWrapper()
        fake_result = ClassificationResult(
            predicted_category="Corn___healthy",
            class_id=14,
            plant="Maíz",
            plant_en="Corn",
            disease_or_condition="Sana (sin enfermedad aparente)",
            disease_or_condition_en="Healthy",
            is_healthy=True,
            health_status="Sana",
            confidence=0.35,
            confidence_percentage=35.0,
            top_predictions=[],
            inference_time_ms=10.0,
        )

        with patch("scripts.run_mlflow_benchmark.predict_from_bytes", return_value=fake_result):
            # Act
            predictions = wrapper.predict(
                context=MagicMock(),
                model_input=[str(sample_file)],
                params={"top_k": 3, "threshold": 0.60},
            )

        # Assert
        assert len(predictions) == 1
        assert predictions[0]["predicted_category"] == "Corn___healthy"
        assert predictions[0]["is_uncertain"] is True

    def test_parse_arguments_default_values(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Arrange: Simular argumentos de consola por defecto."""
        monkeypatch.setattr("sys.argv", ["run_mlflow_benchmark.py"])

        # Act
        args = parse_arguments()

        # Assert
        assert "sqlite:///" in args.tracking_uri
        assert args.no_register is False
