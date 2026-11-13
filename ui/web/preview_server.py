"""Servidor local de previsualización y pruebas del Frontend AgroScan AI.

Permite probar la interfaz HTML/CSS/JS de forma aislada, incluyendo respuestas
simuladas (mock) para /health y /predict sin requerir la carga pesada del modelo.

Uso:
    python ui/web/preview_server.py [puerto]
"""

from __future__ import annotations

import json
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys

WEB_DIR = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000


class AgroScanPreviewHandler(SimpleHTTPRequestHandler):
    """Manejador HTTP que sirve los archivos estáticos y responde a mocks de la API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        """Maneja rutas estáticas y el endpoint de prueba /health."""
        if self.path in ("/health", "/health/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            mock_health = {
                "status": "ok",
                "model_available": True,
                "model_name": "rodynaemad/plant-disease-dinov2-small",
                "architecture": "DINOv2ForImageClassification",
                "device": "cpu",
                "num_classes": 38,
                "model_path": "model.safetensors",
                "detail": "Servidor de pruebas y previsualización local activo.",
            }
            self.wfile.write(json.dumps(mock_health).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        """Maneja el endpoint de prueba /predict con un diagnóstico simulado de ejemplo."""
        if self.path.startswith("/predict"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            mock_prediction = {
                "predicted_category": "Tomato___Late_blight",
                "class_id": 30,
                "plant": "Tomate",
                "plant_en": "Tomato",
                "disease_or_condition": "Tizón tardío",
                "disease_or_condition_en": "Late blight",
                "is_healthy": False,
                "health_status": "Enferma",
                "confidence": 0.8842,
                "confidence_percentage": 88.42,
                "is_uncertain": False,
                "inference_time_ms": 142.5,
                "top_predictions": [
                    {
                        "rank": 1,
                        "class_id": 30,
                        "predicted_category": "Tomato___Late_blight",
                        "plant": "Tomate",
                        "plant_en": "Tomato",
                        "disease_or_condition": "Tizón tardío",
                        "disease_or_condition_en": "Late blight",
                        "is_healthy": False,
                        "health_status": "Enferma",
                        "confidence": 0.8842,
                        "confidence_percentage": 88.42,
                    },
                    {
                        "rank": 2,
                        "class_id": 29,
                        "predicted_category": "Tomato___Early_blight",
                        "plant": "Tomate",
                        "plant_en": "Tomato",
                        "disease_or_condition": "Tizón temprano",
                        "disease_or_condition_en": "Early blight",
                        "is_healthy": False,
                        "health_status": "Enferma",
                        "confidence": 0.0815,
                        "confidence_percentage": 8.15,
                    },
                    {
                        "rank": 3,
                        "class_id": 37,
                        "predicted_category": "Tomato___healthy",
                        "plant": "Tomate",
                        "plant_en": "Tomato",
                        "disease_or_condition": "Sana",
                        "disease_or_condition_en": "Healthy",
                        "is_healthy": True,
                        "health_status": "Sana",
                        "confidence": 0.0210,
                        "confidence_percentage": 2.10,
                    },
                ],
                "disclaimer": (
                    "Herramienta orientativa de apoyo al cribado en campo. "
                    "No constituye prescripción fitosanitaria ni sustituye la inspección agronómica."
                ),
            }
            self.wfile.write(json.dumps(mock_prediction).encode("utf-8"))
            return

        self.send_error(404, "Endpoint no encontrado")

    def do_OPTIONS(self):
        """Maneja preflight CORS."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()


def run():
    server = HTTPServer(("127.0.0.1", PORT), AgroScanPreviewHandler)
    print(f"\n=======================================================")
    print(f" Servidor de Previsualización AgroScan AI")
    print(f" URL Local: http://127.0.0.1:{PORT}")
    print(f" Directorio Web: {WEB_DIR}")
    print(f"=======================================================\n")
    print("Presiona Ctrl + C para detener el servidor.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    run()
