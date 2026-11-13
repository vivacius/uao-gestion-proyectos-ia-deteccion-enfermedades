"""Pruebas unitarias para los recursos estáticos, servidor de previsualización y montaje en FastAPI."""

from __future__ import annotations

import io
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from api.main import app
from ui.web.preview_server import AgroScanPreviewHandler

WEB_DIR = Path(__file__).resolve().parent.parent.parent / "ui" / "web"
STATIC_DIR = WEB_DIR / "static"


@pytest.mark.unit
class TestWebAssetsIntegrity:
    """Verifica la existencia e integridad de los archivos estáticos de la interfaz."""

    def test_web_directory_contains_expected_files(self) -> None:
        """Arrange & Act: Verificar presencia de archivos clave en static y ui/web."""
        expected_static_files = ["index.html", "styles.css", "app.js"]
        for filename in expected_static_files:
            file_path = STATIC_DIR / filename
            assert file_path.exists(), f"El archivo estático '{filename}' no existe en {STATIC_DIR}."
            assert file_path.stat().st_size > 0, f"El archivo '{filename}' está vacío."

        expected_tool_files = ["preview_server.py", "README.md", "__init__.py"]
        for filename in expected_tool_files:
            file_path = WEB_DIR / filename
            assert file_path.exists(), f"El archivo '{filename}' no existe en {WEB_DIR}."

    def test_index_html_contains_required_elements(self) -> None:
        """Arrange: Cargar contenido de index.html."""
        html_content = (STATIC_DIR / "index.html").read_text(encoding="utf-8")

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
        js_content = (STATIC_DIR / "app.js").read_text(encoding="utf-8")

        # Act & Assert: Verificar rutas, contratos y resolución dinámica same-origin
        assert "/predict" in js_content, "app.js debe consumir la ruta /predict."
        assert "/health" in js_content, "app.js debe consumir la ruta /health."
        assert "is_uncertain" in js_content, "app.js debe evaluar el flag de incertidumbre del backend."
        assert "window.location.origin" in js_content, "app.js debe priorizar same-origin."
        assert "localStorage" in js_content, "app.js debe permitir configuración dinámica por usuario."


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


@pytest.mark.unit
class TestFastAPIStaticMount:
    """Pruebas con TestClient para verificar el montaje de estáticos en FastAPI."""

    @pytest.fixture(scope="class")
    @classmethod
    def client(cls):
        """Fixture que proporciona un TestClient instanciado sobre la aplicación FastAPI con mocks."""
        fake_bundle = MagicMock(
            architecture="DINOv2ForImageClassification",
            device="cpu",
            id2label={0: "Apple___healthy"},
            model_dir=Path("."),
        )
        with patch("api.main.get_model_bundle", return_value=fake_bundle):
            with TestClient(app) as test_client:
                yield test_client

    def test_root_serves_index_html(self, client: TestClient) -> None:
        """GET / debe retornar 200 y el HTML con AgroScan AI."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "AgroScan AI" in response.text

    def test_serves_css_asset(self, client: TestClient) -> None:
        """GET /styles.css debe retornar 200 y content-type text/css."""
        response = client.get("/styles.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_serves_js_asset(self, client: TestClient) -> None:
        """GET /app.js debe retornar 200 y script javascript."""
        response = client.get("/app.js")
        assert response.status_code == 200
        assert any(
            t in response.headers.get("content-type", "")
            for t in ["javascript", "text/javascript", "application/javascript"]
        )

    def test_health_endpoint_not_shadowed(self, client: TestClient) -> None:
        """GET /health debe responder JSON 200 de la API y no ser eclipsado por el mount estático."""
        fake_bundle = MagicMock(
            architecture="DINOv2ForImageClassification",
            device="cpu",
            id2label={0: "Apple___healthy"},
            model_dir=Path("."),
        )
        with patch("api.main.get_model_bundle", return_value=fake_bundle):
            response = client.get("/health")
            assert response.status_code == 200
            assert response.headers.get("content-type", "").startswith("application/json")
            assert response.json()["status"] == "ok"

    def test_docs_endpoint_not_shadowed(self, client: TestClient) -> None:
        """GET /docs debe responder 200 con la documentación Swagger UI."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_nonexistent_route_returns_404(self, client: TestClient) -> None:
        """GET /ruta_inexistente_xyz_404 debe responder 404 Not Found."""
        response = client.get("/ruta_inexistente_xyz_404")
        assert response.status_code == 404

    def test_python_source_files_not_exposed(self, client: TestClient) -> None:
        """Verifica que preview_server.py y __init__.py no sean accesibles vía HTTP."""
        resp_preview = client.get("/preview_server.py")
        assert resp_preview.status_code == 404, "preview_server.py no debe ser accesible vía HTTP"

        resp_init = client.get("/__init__.py")
        assert resp_init.status_code == 404, "__init__.py no debe ser accesible vía HTTP"
