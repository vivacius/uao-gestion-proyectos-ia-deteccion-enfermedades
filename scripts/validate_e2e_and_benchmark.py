"""Script reproducible de validación integral E2E y benchmarks en CPU (Issue #30 / SPEC-008).

Mide por separado:
1. Validación funcional E2E de rutas FastAPI (/, /health, /model-info, /docs, /predict y errores HTTP).
2. Latencia pura de inferencia en CPU (predict_from_bytes).
3. Latencia HTTP E2E de POST /predict (secuencial y concurrente) contra uvicorn real.
4. Consumo real de memoria RAM (RSS) y CPU bajo Python 3.13.
"""

from __future__ import annotations

import json
import math
import os
import platform
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
from typing import Any

import httpx
from PIL import Image, ImageDraw

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.inference import predict_from_bytes  # noqa: E402
from src.model_loader import get_model_bundle  # noqa: E402


def build_synthetic_leaf_jpeg(width: int = 300, height: int = 300) -> bytes:
    """Genera una imagen JPEG sintética en memoria simulando una hoja sobre fondo neutro."""
    img = Image.new("RGB", (width, height), color=(225, 225, 225))
    draw = ImageDraw.Draw(img)
    draw.ellipse((45, 30, 255, 270), fill=(48, 132, 58))
    draw.ellipse((120, 105, 165, 150), fill=(125, 78, 32))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=92)
    return buf.getvalue()


def build_unsupported_gif() -> bytes:
    """Genera una imagen GIF válida para comprobar rechazo controlado HTTP 415."""
    img = Image.new("RGB", (100, 100), color=(200, 200, 200))
    buf = BytesIO()
    img.save(buf, format="GIF")
    return buf.getvalue()


def percentile(values: list[float], pct: float) -> float:
    """Calcula un percentil lineal sobre una lista no vacía de valores en milisegundos."""
    ordered = sorted(values)
    idx = (len(ordered) - 1) * (pct / 100.0)
    low = math.floor(idx)
    high = math.ceil(idx)
    if low == high:
        return ordered[int(idx)]
    weight = idx - low
    return ordered[low] * (1.0 - weight) + ordered[high] * weight


def summarize_latencies(latencies_ms: list[float], wall_seconds: float) -> dict[str, float]:
    """Calcula estadísticas de latencia (ms) y throughput (req/s)."""
    return {
        "n": float(len(latencies_ms)),
        "min_ms": round(min(latencies_ms), 2),
        "mean_ms": round(statistics.mean(latencies_ms), 2),
        "p50_ms": round(percentile(latencies_ms, 50.0), 2),
        "p95_ms": round(percentile(latencies_ms, 95.0), 2),
        "max_ms": round(max(latencies_ms), 2),
        "throughput_rps": round(len(latencies_ms) / wall_seconds, 2) if wall_seconds > 0 else 0.0,
    }


def get_process_memory_mb(pid: int) -> float | None:
    """Consulta la memoria RSS (Working Set) de un proceso en MB."""
    if os.name == "nt":
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"(Get-Process -Id {pid}).WorkingSet64 / 1MB",
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0 and res.stdout.strip():
            try:
                return round(float(res.stdout.strip().replace(",", ".")), 2)
            except ValueError:
                return None
    return None


def wait_for_server(base_url: str, timeout_s: float = 45.0) -> None:
    """Espera hasta que GET /health responda HTTP 200 con el modelo cargado."""
    deadline = time.perf_counter() + timeout_s
    while time.perf_counter() < deadline:
        try:
            resp = httpx.get(f"{base_url}/health", timeout=2.0)
            if resp.status_code == 200 and resp.json().get("model_available") is True:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.5)
    raise TimeoutError(f"El servidor FastAPI no respondió listo en {timeout_s} s.")


def run_benchmark() -> dict[str, Any]:
    """Ejecuta validación E2E y benchmarks de CPU y HTTP."""
    jpeg_bytes = build_synthetic_leaf_jpeg()
    gif_bytes = build_unsupported_gif()
    corrupted_bytes = b"\xff\xd8\xff\xe0\x00\x10CORRUPTED_NOT_AN_IMAGE"

    # 1. Benchmark de inferencia pura en CPU
    bundle = get_model_bundle()
    for _ in range(3):
        predict_from_bytes(jpeg_bytes, filename="warmup.jpg", content_type="image/jpeg", bundle=bundle)

    cpu_latencies: list[float] = []
    t0_cpu = time.perf_counter()
    for i in range(20):
        t_start = time.perf_counter()
        result = predict_from_bytes(
            jpeg_bytes,
            filename=f"leaf_{i}.jpg",
            content_type="image/jpeg",
            bundle=bundle,
        )
        cpu_latencies.append((time.perf_counter() - t_start) * 1000.0)
    wall_cpu = time.perf_counter() - t0_cpu
    cpu_stats = summarize_latencies(cpu_latencies, wall_cpu)
    local_rss_mb = get_process_memory_mb(os.getpid())

    # 2. Validación E2E HTTP y benchmark contra uvicorn real
    port = 8011
    base_url = f"http://127.0.0.1:{port}"
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        wait_for_server(base_url)
        server_rss_mb = get_process_memory_mb(proc.pid)

        with httpx.Client(base_url=base_url, timeout=15.0) as client:
            r_root = client.get("/")
            r_health = client.get("/health")
            r_info = client.get("/model-info")
            r_docs = client.get("/docs")
            r_ok = client.post("/predict", files={"file": ("hoja.jpg", jpeg_bytes, "image/jpeg")})
            r_corrupt = client.post("/predict", files={"file": ("mala.jpg", corrupted_bytes, "image/jpeg")})
            r_gif = client.post("/predict", files={"file": ("hoja.gif", gif_bytes, "image/gif")})

            e2e_checks = {
                "GET_/": {
                    "status": r_root.status_code,
                    "is_html": "text/html" in r_root.headers.get("content-type", ""),
                },
                "GET_/health": {"status": r_health.status_code, "payload": r_health.json()},
                "GET_/model-info": {"status": r_info.status_code, "payload": r_info.json()},
                "GET_/docs": {"status": r_docs.status_code},
                "POST_/predict_valid": {
                    "status": r_ok.status_code,
                    "top_k_count": len(r_ok.json().get("top_predictions", [])),
                    "has_disclaimer": bool(r_ok.json().get("disclaimer")),
                    "predicted_category": r_ok.json().get("predicted_category"),
                    "confidence_percentage": r_ok.json().get("confidence_percentage"),
                },
                "POST_/predict_corrupted": {"status": r_corrupt.status_code, "detail": r_corrupt.json()},
                "POST_/predict_unsupported_gif": {"status": r_gif.status_code, "detail": r_gif.json()},
            }

            # Warmup HTTP
            for _ in range(3):
                client.post("/predict", files={"file": ("warmup.jpg", jpeg_bytes, "image/jpeg")})

            # Secuencial (N=20)
            seq_latencies: list[float] = []
            t0_seq = time.perf_counter()
            for i in range(20):
                ts = time.perf_counter()
                resp = client.post("/predict", files={"file": (f"seq_{i}.jpg", jpeg_bytes, "image/jpeg")})
                assert resp.status_code == 200
                seq_latencies.append((time.perf_counter() - ts) * 1000.0)
            wall_seq = time.perf_counter() - t0_seq
            http_seq_stats = summarize_latencies(seq_latencies, wall_seq)

        # Concurrente (N=20, 4 workers)
        def send_one(idx: int) -> float:
            ts = time.perf_counter()
            resp = httpx.post(
                f"{base_url}/predict",
                files={"file": (f"conc_{idx}.jpg", jpeg_bytes, "image/jpeg")},
                timeout=15.0,
            )
            assert resp.status_code == 200
            return (time.perf_counter() - ts) * 1000.0

        conc_latencies: list[float] = []
        t0_conc = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(send_one, i) for i in range(20)]
            for fut in as_completed(futures):
                conc_latencies.append(fut.result())
        wall_conc = time.perf_counter() - t0_conc
        http_conc_stats = summarize_latencies(conc_latencies, wall_conc)
        server_rss_after_mb = get_process_memory_mb(proc.pid)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    return {
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
            "architecture": bundle.architecture,
            "num_classes": len(bundle.id2label),
            "sample_prediction": result.predicted_category,
            "local_rss_mb": local_rss_mb,
            "server_rss_before_load_test_mb": server_rss_mb,
            "server_rss_after_load_test_mb": server_rss_after_mb,
        },
        "e2e_checks": e2e_checks,
        "cpu_pure_inference_ms": cpu_stats,
        "http_sequential_ms": http_seq_stats,
        "http_concurrent_4workers_ms": http_conc_stats,
    }


if __name__ == "__main__":
    report = run_benchmark()
    print(json.dumps(report, indent=2, ensure_ascii=False))
