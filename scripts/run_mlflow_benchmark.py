"""Script reproducible de experimentación, evaluación y registro en MLflow para DINOv2-small en CPU.

Unidad de Trabajo: M3-IMP-MLF-01
Cumplimiento de Anuncio 007:
- Servidor / Tracking UI activo en http://127.0.0.1:5050 (o SQLite local).
- Tres configuraciones experimentales comparables y genuinamente distintas (Baseline tau=0.60,
  Strict tau=0.80, Exploratory tau=0.40).
- Métricas computacionales reales medidas en CPU (latencia media, p50, p95, throughput, incertidumbre).
- Artefactos estructurados (CSV, JSON, reporte de benchmark).
- Tags y parámetros de trazabilidad completa.
- Registro del modelo en Model Registry (versión 1) trazable al servicio de FastAPI.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import logging
import os
import platform
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

# Garantizar que la raíz del proyecto esté en sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Desactivar avisos ruidosos de MLflow
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

import mlflow  # noqa: E402
from mlflow.models.signature import infer_signature  # noqa: E402
from mlflow.tracking import MlflowClient  # noqa: E402

from src.config import BASE_DIR, MODEL_DIR, REQUIRED_MODEL_FILES  # noqa: E402
from src.inference import predict_from_bytes  # noqa: E402
from src.model_loader import get_model_bundle  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mlflow_benchmark")

EXPERIMENT_NAME = "dinov2-plant-disease-screening"
REGISTERED_MODEL_NAME = "dinov2-plant-disease-classifier"


def get_git_commit_hash() -> str:
    """Obtiene el hash del commit actual de Git para trazabilidad."""
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(BASE_DIR),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return output.strip()
    except Exception:
        return "unknown-commit"


def create_synthetic_benchmark_sample(
    width: int,
    height: int,
    mode: str = "RGB",
    image_format: str = "JPEG",
    spot_type: str = "none",
) -> bytes:
    """Genera bytes de una imagen foliar sintética determinista para benchmarking."""
    bg_color = (220, 220, 220) if mode == "RGB" else (220, 220, 220, 255) if mode == "RGBA" else 200
    img = Image.new(mode, (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    if mode in ("RGB", "RGBA"):
        leaf_color = (45, 130, 55) if mode == "RGB" else (45, 130, 55, 255)
        spot_color = (120, 75, 30) if mode == "RGB" else (120, 75, 30, 255)
        yellow_color = (190, 180, 40) if mode == "RGB" else (190, 180, 40, 255)
    else:
        leaf_color = 90
        spot_color = 50
        yellow_color = 120

    # Silueta de la hoja
    draw.ellipse(
        (int(width * 0.12), int(height * 0.08), int(width * 0.88), int(height * 0.92)),
        fill=leaf_color,
    )

    if spot_type == "necrotic":
        draw.ellipse(
            (int(width * 0.35), int(height * 0.30), int(width * 0.55), int(height * 0.50)),
            fill=spot_color,
        )
    elif spot_type == "chlorotic":
        draw.ellipse(
            (int(width * 0.25), int(height * 0.25), int(width * 0.65), int(height * 0.65)),
            fill=yellow_color,
        )
        draw.ellipse(
            (int(width * 0.40), int(height * 0.40), int(width * 0.50), int(height * 0.50)),
            fill=spot_color,
        )
    elif spot_type == "multi_spot":
        for ox, oy in [
            (0.25, 0.25),
            (0.55, 0.35),
            (0.40, 0.60),
            (0.65, 0.65),
            (0.30, 0.70),
        ]:
            draw.ellipse(
                (
                    int(width * ox),
                    int(height * oy),
                    int(width * (ox + 0.12)),
                    int(height * (oy + 0.12)),
                ),
                fill=spot_color,
            )

    buffer = io.BytesIO()
    img.save(buffer, format=image_format)
    return buffer.getvalue()


def build_fixed_evaluation_set() -> list[tuple[str, bytes]]:
    """Construye el conjunto fijo e inmutable de evaluación (10 muestras representativas).

    Nota de integridad técnica:
    Los ejemplos son sintéticos reproducibles. No poseen etiquetas de ground-truth verificadas,
    por lo que se registra explícitamente `is_labeled = False` y se omiten métricas de calidad
    (Accuracy/F1) para no inventar datos.
    """
    samples: list[tuple[str, bytes]] = [
        (
            "sample_01_healthy_standard_300x300.jpg",
            create_synthetic_benchmark_sample(300, 300, "RGB", "JPEG", "none"),
        ),
        (
            "sample_02_necrotic_spot_300x300.jpg",
            create_synthetic_benchmark_sample(300, 300, "RGB", "JPEG", "necrotic"),
        ),
        (
            "sample_03_chlorotic_halo_280x280.png",
            create_synthetic_benchmark_sample(280, 280, "RGB", "PNG", "chlorotic"),
        ),
        (
            "sample_04_multi_spot_rust_320x320.jpg",
            create_synthetic_benchmark_sample(320, 320, "RGB", "JPEG", "multi_spot"),
        ),
        (
            "sample_05_healthy_hires_400x400.jpg",
            create_synthetic_benchmark_sample(400, 400, "RGB", "JPEG", "none"),
        ),
        (
            "sample_06_rgba_alpha_spot_260x260.png",
            create_synthetic_benchmark_sample(260, 260, "RGBA", "PNG", "necrotic"),
        ),
        (
            "sample_07_grayscale_leaf_300x300.jpg",
            create_synthetic_benchmark_sample(300, 300, "L", "JPEG", "multi_spot"),
        ),
        (
            "sample_08_compact_healthy_224x224.png",
            create_synthetic_benchmark_sample(224, 224, "RGB", "PNG", "none"),
        ),
        (
            "sample_09_large_chlorotic_450x450.jpg",
            create_synthetic_benchmark_sample(450, 450, "RGB", "JPEG", "chlorotic"),
        ),
        (
            "sample_10_dense_rust_350x350.jpg",
            create_synthetic_benchmark_sample(350, 350, "RGB", "JPEG", "multi_spot"),
        ),
    ]
    return samples


class Dinov2InferenceWrapper(mlflow.pyfunc.PythonModel):
    """Envoltorio PyFunc para servir el modelo DINOv2-small registrado en MLflow."""

    def load_context(self, context: mlflow.pyfunc.PythonModelContext) -> None:
        """Carga el modelo determinista desde la carpeta local verificada."""
        get_model_bundle()

    def predict(
        self,
        context: Any,
        model_input: list[Any],
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Ejecuta inferencia sobre una lista o payload de bytes de imágenes."""
        results: list[dict[str, Any]] = []
        top_k = params.get("top_k", 3) if params else 3
        threshold = params.get("threshold", 0.60) if params else 0.60

        # Si el input es un DataFrame de pandas o lista de bytes / paths
        if hasattr(model_input, "iloc"):
            items = model_input.iloc[:, 0].tolist()
        elif isinstance(model_input, (list, tuple)):
            items = list(model_input)
        else:
            items = [model_input]

        for item in items:
            if isinstance(item, str):
                # Puede ser ruta de archivo o bytes codificados
                file_path = Path(item)
                if file_path.is_file():
                    img_bytes = file_path.read_bytes()
                else:
                    raise ValueError(f"Ruta de imagen inválida: '{item}'.")
            elif isinstance(item, (bytes, bytearray)):
                img_bytes = bytes(item)
            else:
                raise TypeError(f"Tipo de entrada no compatible para inferencia: {type(item)}.")

            prediction = predict_from_bytes(img_bytes, top_k=top_k)
            res_dict = asdict(prediction)
            is_uncertain = prediction.confidence < threshold
            res_dict["confidence_threshold"] = threshold
            res_dict["is_uncertain"] = is_uncertain
            res_dict["uncertainty_reason"] = (
                f"Confianza {prediction.confidence:.2%} inferior al umbral mínimo ({threshold:.2%})."
                if is_uncertain
                else None
            )
            results.append(res_dict)

        return results


def run_single_evaluation(
    run_name: str,
    run_description: str,
    confidence_threshold: float,
    top_k: int,
    eval_samples: list[tuple[str, bytes]],
    git_commit: str,
    output_dir: Path,
    register_model: bool = False,
) -> dict[str, Any]:
    """Ejecuta un run experimental completo en MLflow y retorna su resumen."""
    run_output_dir = output_dir / run_name
    run_output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Iniciando Run: '%s' (tau=%.2f, top_k=%d)...", run_name, confidence_threshold, top_k)

    with mlflow.start_run(run_name=run_name, description=run_description) as active_run:
        run_id = active_run.info.run_id

        # 1. Registro de Parámetros
        mlflow.log_params(
            {
                "model_name": "rodynaemad/plant-disease-dinov2-small",
                "architecture": "Dinov2ForImageClassification",
                "inference_device": "cpu",
                "confidence_threshold": confidence_threshold,
                "top_k": top_k,
                "input_resolution": "224x224",
                "crop_size": 224,
                "shortest_edge_resize": 256,
                "interpolation": "bicubic",
                "normalization_mean": "[0.485, 0.456, 0.406]",
                "normalization_std": "[0.229, 0.224, 0.225]",
                "num_classes": 38,
                "is_labeled": False,
                "eval_samples_count": len(eval_samples),
                "evaluation_mode": "offline-benchmark-cpu",
            }
        )

        # 2. Registro de Tags Trazables
        mlflow.set_tags(
            {
                "version": "1.0.0",
                "environment": "local-cpu",
                "license": "MIT",
                "git_commit": git_commit,
                "unit": "M3-IMP-MLF-01",
                "author": "Grupo 2",
                "reviewer": "Jhonatan Tapia",
                "task": "plant-disease-classification",
                "framework": "PyTorch",
                "transformers_version": "4.46.x",
            }
        )

        # 3. Inferencia real con medición de latencia por muestra
        latencies_ms: list[float] = []
        predictions_records: list[dict[str, Any]] = []
        confidences: list[float] = []
        uncertain_count = 0

        # Calentamiento inicial (1 muestra descartada) para evitar sesgos de carga inicial
        _ = predict_from_bytes(eval_samples[0][1], top_k=top_k)

        for filename, img_bytes in eval_samples:
            start_ns = time.perf_counter_ns()
            pred = predict_from_bytes(
                img_bytes,
                top_k=top_k,
            )
            elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
            latencies_ms.append(elapsed_ms)

            top1_prob = pred.confidence
            confidences.append(top1_prob)

            is_uncertain = top1_prob < confidence_threshold
            if is_uncertain:
                uncertain_count += 1

            uncertainty_reason = (
                f"Confianza {top1_prob:.2%} inferior al umbral mínimo ({confidence_threshold:.2%})."
                if is_uncertain
                else "N/A"
            )

            predicted_name_es = f"{pred.plant} — {pred.disease_or_condition}"
            top_candidates_str = "; ".join(
                f"{item.plant}-{item.disease_or_condition} ({item.confidence_percentage:.1f}%)"
                for item in pred.top_predictions
            )

            predictions_records.append(
                {
                    "image_name": filename,
                    "predicted_category": pred.predicted_category,
                    "predicted_name_es": predicted_name_es,
                    "top1_probability": round(top1_prob, 4),
                    "confidence_threshold": confidence_threshold,
                    "is_uncertain": is_uncertain,
                    "uncertainty_reason": uncertainty_reason,
                    "latency_ms": round(elapsed_ms, 2),
                    "top_candidates": top_candidates_str,
                }
            )

        # 4. Cálculo de Métricas Reales
        sorted_latencies = sorted(latencies_ms)
        n = len(sorted_latencies)
        latency_mean = sum(latencies_ms) / n
        latency_p50 = sorted_latencies[int(n * 0.50)]
        latency_p95 = sorted_latencies[min(int(n * 0.95), n - 1)]
        latency_min = sorted_latencies[0]
        latency_max = sorted_latencies[-1]
        throughput = (n / (sum(latencies_ms) / 1000.0)) if sum(latencies_ms) > 0 else 0.0
        uncertainty_rate = uncertain_count / n
        mean_top1_conf = sum(confidences) / n

        metrics = {
            "latency_mean_ms": round(latency_mean, 2),
            "latency_p50_ms": round(latency_p50, 2),
            "latency_p95_ms": round(latency_p95, 2),
            "latency_min_ms": round(latency_min, 2),
            "latency_max_ms": round(latency_max, 2),
            "throughput_img_per_sec": round(throughput, 2),
            "uncertainty_rate": round(uncertainty_rate, 4),
            "mean_top1_confidence": round(mean_top1_conf, 4),
            "evaluated_samples": n,
        }
        mlflow.log_metrics(metrics)

        # 5. Generación de Artefactos Estructurados
        # CSV de predicciones
        csv_path = run_output_dir / "predictions_summary.csv"
        with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(predictions_records[0].keys()))
            writer.writeheader()
            writer.writerows(predictions_records)
        mlflow.log_artifact(str(csv_path), artifact_path="evaluation_reports")

        # JSON detallado de predicciones
        json_path = run_output_dir / "predictions.json"
        with open(json_path, mode="w", encoding="utf-8") as f:
            json.dump(
                {
                    "run_name": run_name,
                    "run_id": run_id,
                    "parameters": {"threshold": confidence_threshold, "top_k": top_k},
                    "metrics": metrics,
                    "predictions": predictions_records,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
        mlflow.log_artifact(str(json_path), artifact_path="evaluation_reports")

        # Reporte del Hardware y Entorno
        report_path = run_output_dir / "benchmark_report.json"
        with open(report_path, mode="w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "hardware": {
                        "platform": platform.platform(),
                        "processor": platform.processor(),
                        "python_version": sys.version,
                        "device": "CPU",
                    },
                    "git": {"commit": git_commit},
                    "model": {
                        "name": "rodynaemad/plant-disease-dinov2-small",
                        "safetensors_path": str(MODEL_DIR / "model.safetensors"),
                        "required_files": list(REQUIRED_MODEL_FILES),
                    },
                    "summary": metrics,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
        mlflow.log_artifact(str(report_path), artifact_path="system_metadata")

        # 6. Registro del Modelo en Model Registry (solo en el Run de referencia / Baseline)
        registered_version: str | None = None
        if register_model:
            logger.info("Registrando modelo en Model Registry: '%s'...", REGISTERED_MODEL_NAME)
            sample_input = [str(BASE_DIR / "tests" / "fixtures" / "dummy.jpg")]
            signature = infer_signature(sample_input, [{"predicted_category": "str", "confidence": 0.99}])

            model_info = mlflow.pyfunc.log_model(
                artifact_path="model",
                python_model=Dinov2InferenceWrapper(),
                registered_model_name=REGISTERED_MODEL_NAME,
                signature=signature,
            )
            logger.info("Modelo registrado exitosamente: %s", model_info.model_uri)

            # Obtener la versión registrada usando el cliente de MLflow
            client = MlflowClient()
            try:
                latest_versions = client.get_latest_versions(REGISTERED_MODEL_NAME)
                if latest_versions:
                    registered_version = str(latest_versions[0].version)
                    client.set_model_version_tag(
                        name=REGISTERED_MODEL_NAME,
                        version=registered_version,
                        key="stage_candidate",
                        value="m3_sustentacion",
                    )
                    client.update_model_version(
                        name=REGISTERED_MODEL_NAME,
                        version=registered_version,
                        description=(
                            "Modelo DINOv2-small optimizado para inferencia en CPU de patologías vegetales. "
                            "Versión trazable al servicio FastAPI (puerto 8000) y sustentación M3."
                        ),
                    )
            except Exception as reg_err:
                logger.warning("No se pudo actualizar etiquetas del registro: %s", reg_err)

        logger.info(
            "Run '%s' completado: Latencia Media=%.2f ms, P95=%.2f ms, Throughput=%.2f, Incert=%.1f%%.",
            run_name,
            latency_mean,
            latency_p95,
            throughput,
            uncertainty_rate * 100,
        )

        return {
            "run_name": run_name,
            "run_id": run_id,
            "threshold": confidence_threshold,
            "top_k": top_k,
            "metrics": metrics,
            "registered_version": registered_version,
        }


def execute_all_runs(
    tracking_uri: str,
    output_dir: Path | None = None,
    register_model: bool = True,
) -> list[dict[str, Any]]:
    """Configura el experimento y ejecuta los 3 runs comparables y diferenciados."""
    mlflow.set_tracking_uri(tracking_uri)
    logger.info("Conectado a MLflow Tracking URI: %s", tracking_uri)

    mlflow.set_experiment(EXPERIMENT_NAME)

    git_commit = get_git_commit_hash()
    eval_samples = build_fixed_evaluation_set()
    logger.info("Conjunto fijo de evaluación cargado (%d muestras).", len(eval_samples))

    if output_dir is None:
        output_dir = BASE_DIR / "mlflow_data" / "benchmark_runs"
    output_dir.mkdir(parents=True, exist_ok=True)

    configs = [
        {
            "run_name": "dinov2-baseline-tau0.60",
            "run_description": (
                "Configuración estándar de referencia con umbral tau=0.60 y top-3 predicciones. "
                "Coincide con los contratos de HU-04 y el servicio productivo de FastAPI."
            ),
            "confidence_threshold": 0.60,
            "top_k": 3,
            "register_model": register_model,
        },
        {
            "run_name": "dinov2-strict-tau0.80",
            "run_description": (
                "Configuración estricta de alta certeza agronómica (tau=0.80, top-3). "
                "Reduce falsos positivos a costa de incrementar la tasa de incertidumbre."
            ),
            "confidence_threshold": 0.80,
            "top_k": 3,
            "register_model": False,
        },
        {
            "run_name": "dinov2-permissive-tau0.40",
            "run_description": (
                "Configuración permisiva de campo para cribado preliminar (tau=0.40, top-5). "
                "Reduce la tasa de abstención de respuesta y amplía las hipótesis diagnósticas."
            ),
            "confidence_threshold": 0.40,
            "top_k": 5,
            "register_model": False,
        },
    ]

    summaries: list[dict[str, Any]] = []
    for cfg in configs:
        summary = run_single_evaluation(
            run_name=cfg["run_name"],
            run_description=cfg["run_description"],
            confidence_threshold=cfg["confidence_threshold"],
            top_k=cfg["top_k"],
            eval_samples=eval_samples,
            git_commit=git_commit,
            output_dir=output_dir,
            register_model=cfg["register_model"],
        )
        summaries.append(summary)

    logger.info("Evaluación de los 3 runs de MLflow completada con éxito.")
    return summaries


def parse_arguments() -> argparse.Namespace:
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Ejecutar benchmark de inferencia DINOv2 y registrar 3 runs en MLflow Tracking."
    )
    parser.add_argument(
        "--tracking-uri",
        type=str,
        default=os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow_tracking.db"),
        help="URI del servidor de tracking de MLflow (defecto: sqlite:///mlflow_tracking.db).",
    )
    parser.add_argument(
        "--no-register",
        action="store_true",
        help="Omitir el registro del modelo en el Model Registry de MLflow.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    summaries = execute_all_runs(
        tracking_uri=args.tracking_uri,
        register_model=not args.no_register,
    )
    print("\n" + "=" * 60)
    print("RESUMEN DE EJECUCIONES EN MLFLOW TRACKING:")
    print("=" * 60)
    for s in summaries:
        m = s["metrics"]
        print(
            f"Run: {s['run_name']:<30} | Latencia: {m['latency_mean_ms']:>6.2f} ms | "
            f"P95: {m['latency_p95_ms']:>6.2f} ms | Throughput: {m['throughput_img_per_sec']:>5.2f} img/s | "
            f"Incertidumbre: {m['uncertainty_rate'] * 100:>5.1f}%"
        )
        if s.get("registered_version"):
            print(f"  └── Model Registry: {REGISTERED_MODEL_NAME} (Versión {s['registered_version']})")
    print("=" * 60 + "\n")
