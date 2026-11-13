"""Pruebas unitarias para los recursos estáticos y el servidor de pruebas del Frontend Web."""

from __future__ import annotations

import io
import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ui.web.preview_server import AgroScanPreviewHandler

WEB_DIR = Path(__file__).resolve().parent.parent.parent / "ui" / "web"


@pytest.mark.unit
class TestWebAssetsIntegrity:
    """Verifica la existencia e integridad de los archivos estáticos de la interfaz."""

    def test_web_directory_contains_expected_files(self) -> None:
        """Arrange & Act: Verificar presencia de archivos clave."""
        expected_files = ["index.html", "styles.css", "app.js", "preview_server.py", "README.md"]

        # Assert
        for filename in expected_files:
            file_path = WEB_DIR / filename
            assert file_path.exists(), f"El archivo esperado '{filename}' no existe en {WEB_DIR}."
            assert file_path.stat().st_size > 0, f"El archivo '{filename}' está vacío."

    def test_index_html_contains_required_elements(self) -> None:
        """Arrange: Cargar contenido de index.html."""
        html_content = (WEB_DIR / "index.html").read_text(encoding="utf-8")

        # Act & Assert: Verificar elementos requeridos por la especificación
        required_selectors = [
            'id="dropzone"',
            'id="image-input"',
            'id="predict-btn"',
            'id="uncertainty-banner"',
            'id="top3-list"',
            'id="health-status-badge"',
            'capture="environment"',
        ]
        for selector in required_selectors:
            assert selector in html_content, f"index.html debe contener el elemento '{selector}'."

    def test_app_js_contains_endpoint_contracts(self) -> None:
        """Arrange: Cargar contenido de app.js."""
        js_content = (WEB_DIR / "app.js").read_text(encoding="utf-8")

        # Act & Assert: Verificar rutas y contratos con la API
        assert "/predict" in js_content, "app.js debe consumir la ruta /predict."
        assert "/health" in js_content, "app.js debe consumir la ruta /health."
        assert "is_uncertain" in js_content, "app.js debe evaluar el flag de incertidumbre del backend."
        assert "agroscanai.online" in js_content, "app.js debe soportar resolución de dominio en producción."


@pytest.mark.unit
class TestPreviewServerHandler:
    """Pruebas unitarias para la lógica del servidor de previsualización local."""

    def _create_mock_handler(self, path: str, method: str = "GET") -> AgroScanPreviewHandler:
        """Crea una instancia de AgroScanPreviewHandler con streams simulados."""
        handler = AgroScanPreviewHandler.__new__(AgroScanPreviewHandler)
        handler.path = path
        handler.command = method
        handler.rfile = io.BytesIO()
        handler.wfile = io.BytesIO()
        handler.requestline = f"{method} {path} HTTP/1.1"
        handler.client_address = ("127.0.0.1", 12345)
        handler.close_connection = True
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.send_error = MagicMock()
        return handler

    def test_do_get_health_endpoint(self) -> None:
        """Arrange: Crear handler para GET /health."""
        handler = self._create_mock_handler(path="/health", method="GET")

        # Act
        handler.do_GET()

        # Assert
        handler.send_response.assert_called_once_with(200)
        output = handler.wfile.getvalue().decode("utf-8")
        data = json.loads(output)
        assert data["status"] == "ok"
        assert data["model_available"] is True
        assert "dinov2" in data["model_name"]

    def test_do_post_predict_endpoint(self) -> None:
        """Arrange: Crear handler para POST /predict."""
        handler = self._create_mock_handler(path="/predict", method="POST")

        # Act
        handler.do_POST()

        # Assert
        handler.send_response.assert_called_once_with(200)
        output = handler.wfile.getvalue().decode("utf-8")
        data = json.loads(output)
        assert data["plant"] == "Tomate"
        assert len(data["top_predictions"]) == 3
        assert data["confidence_percentage"] > 0
        assert data["is_uncertain"] is False

    def test_do_post_unknown_endpoint_returns_404(self) -> None:
        """Arrange: Crear handler para ruta POST inexistente."""
        handler = self._create_mock_handler(path="/unknown-route", method="POST")

        # Act
        handler.do_POST()

        # Assert
        handler.send_error.assert_called_once_with(404, "Endpoint no encontrado")
