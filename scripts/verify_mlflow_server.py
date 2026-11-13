"""Script de verificación local del servidor MLflow y del Model Registry en el puerto 5050."""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def is_port_open(host: str, port: int) -> bool:
    """Verifica si un puerto TCP está respondiendo conexiones."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def verify_server() -> None:
    """Inicia el servidor MLflow temporalmente en el puerto 5050, verifica UI y API, y lo detiene."""
    server_cmd = [
        sys.executable,
        "-m",
        "mlflow",
        "server",
        "--backend-store-uri",
        "sqlite:///mlflow_tracking.db",
        "--default-artifact-root",
        "./mlflow_data/benchmark_runs",
        "--host",
        "127.0.0.1",
        "--port",
        "5050",
    ]

    print("Iniciando servidor MLflow en http://127.0.0.1:5050...")
    log_file = PROJECT_ROOT / "mlflow_server_test.log"
    log_fp = open(log_file, "w", encoding="utf-8")

    proc = subprocess.Popen(
        server_cmd,
        cwd=str(PROJECT_ROOT),
        stdout=log_fp,
        stderr=log_fp,
    )

    try:
        # Esperar a que el servidor abra el puerto 5050 (hasta 25 segundos)
        start_wait = time.time()
        server_ready = False
        while time.time() - start_wait < 25.0:
            if is_port_open("127.0.0.1", 5050):
                server_ready = True
                break
            time.sleep(0.5)

        if not server_ready:
            print("ERROR: El servidor MLflow no abrió el puerto 5050 en el tiempo esperado.", flush=True)
            log_fp.flush()
            if log_file.is_file():
                print(
                    "LOG DEL SERVIDOR:\n" + log_file.read_text(encoding="utf-8", errors="replace"), flush=True
                )
            sys.exit(1)

        print("Servidor MLflow respondiendo en el puerto 5050.")

        # 1. Probar UI HTTP GET
        with urllib.request.urlopen("http://127.0.0.1:5050/", timeout=10) as response:
            ui_status = response.status
            ui_content_sample = response.read(200).decode("utf-8", errors="replace")
            print(f"[OK] UI HTTP Status: {ui_status}")
            assert ui_status == 200, f"Status esperado 200, obtenido {ui_status}"
            assert "html" in ui_content_sample.lower()

        # 2. Probar API de Experimento
        exp_url = (
            "http://127.0.0.1:5050/api/2.0/mlflow/experiments/get-by-name"
            "?experiment_name=dinov2-plant-disease-screening"
        )
        with urllib.request.urlopen(exp_url, timeout=10) as response:
            exp_data = json.loads(response.read().decode("utf-8"))
            exp_id = exp_data["experiment"]["experiment_id"]
            exp_name = exp_data["experiment"]["name"]
            print(f"[OK] Experimento encontrado: '{exp_name}' (ID: {exp_id})")
            assert exp_name == "dinov2-plant-disease-screening"

        # 3. Probar API de Model Registry
        model_url = (
            "http://127.0.0.1:5050/api/2.0/mlflow/registered-models/get?name=dinov2-plant-disease-classifier"
        )
        with urllib.request.urlopen(model_url, timeout=10) as response:
            model_data = json.loads(response.read().decode("utf-8"))
            reg_model = model_data["registered_model"]
            model_name = reg_model["name"]
            latest_versions = reg_model.get("latest_versions", [])
            print(f"[OK] Modelo Registrado: '{model_name}' (Versiones: {len(latest_versions)})")
            assert model_name == "dinov2-plant-disease-classifier"
            assert len(latest_versions) >= 1
            print(f"[OK] Versión Activa en Registry: {latest_versions[0]['version']}")

        # 4. Probar API de Runs (confirmar 3 runs registrados)
        runs_url = "http://127.0.0.1:5050/api/2.0/mlflow/runs/search"
        search_payload = json.dumps({"experiment_ids": [exp_id]}).encode("utf-8")
        req = urllib.request.Request(
            runs_url,
            data=search_payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            runs_data = json.loads(response.read().decode("utf-8"))
            runs_list = runs_data.get("runs", [])
            print(f"[OK] Cantidad de Runs en el Experimento: {len(runs_list)}")
            assert len(runs_list) >= 3, f"Se esperaban al menos 3 runs, se encontraron {len(runs_list)}"
            for r in runs_list:
                tags_raw = r["data"].get("tags", [])
                tags_dict = (
                    {t["key"]: t["value"] for t in tags_raw} if isinstance(tags_raw, list) else tags_raw
                )
                metrics_raw = r["data"].get("metrics", [])
                metrics_dict = (
                    {m["key"]: m["value"] for m in metrics_raw}
                    if isinstance(metrics_raw, list)
                    else metrics_raw
                )
                r_name = tags_dict.get("mlflow.runName", "unnamed")
                latency = metrics_dict.get("latency_mean_ms", "N/A")
                uncertainty = metrics_dict.get("uncertainty_rate", "N/A")
                print(
                    f"     - Run: {r_name:<30} | Latencia media: {latency} ms | Incertidumbre: {uncertainty}"
                )

        print("\n*** TODAS LAS VERIFICACIONES DEL SERVIDOR MLFLOW Y REGISTRY PASARON CON ÉXITO ***\n")

    finally:
        print("Deteniendo servidor MLflow temporal...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        log_fp.close()
        if log_file.is_file():
            try:
                log_file.unlink()
            except Exception:
                pass
        print("Servidor MLflow detenido.")


if __name__ == "__main__":
    verify_server()
