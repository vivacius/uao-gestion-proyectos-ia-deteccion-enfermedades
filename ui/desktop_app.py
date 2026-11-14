"""Interfaz gráfica de escritorio en Tkinter para identificación de enfermedades en plantas."""

from __future__ import annotations

import mimetypes
import sys
import threading
import tkinter as tk
from io import BytesIO
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

from PIL import Image, ImageOps, ImageTk

# Asegurar que la raíz del proyecto esté en sys.path al ejecutar directamente `python ui/desktop_app.py`
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import AGRONOMIC_DISCLAIMER, API_BASE_URL, MAX_IMAGE_SIZE_MB  # noqa: E402
from ui.api_client import ApiClientResponse, fetch_api_health, request_image_prediction  # noqa: E402

# Paleta de colores institucional / agrícola (alineada con la interfaz web)
COLOR_BG_MAIN = "#f4f7f5"
COLOR_CARD_BG = "#ffffff"
COLOR_HEADER_BG = "#1b4332"
COLOR_HEADER_SUB = "#d8f3dc"
COLOR_PRIMARY = "#2d6a4f"
COLOR_PRIMARY_ACTIVE = "#1b4332"
COLOR_TEXT_PRIMARY = "#1b262c"
COLOR_TEXT_MUTED = "#52616b"
COLOR_BORDER = "#d9e2dc"

COLOR_HEALTHY_BG = "#d8f3dc"
COLOR_HEALTHY_FG = "#1b4332"
COLOR_HEALTHY_BORDER = "#2d6a4f"

COLOR_DISEASED_BG = "#ffe5d9"
COLOR_DISEASED_FG = "#6a040f"
COLOR_DISEASED_BORDER = "#d90429"

COLOR_WARNING_BG = "#fff3cd"
COLOR_WARNING_FG = "#664d03"


def guess_mime_type(file_path: Path) -> str:
    """Determina el tipo MIME adecuado para la imagen seleccionada."""
    guessed, _ = mimetypes.guess_type(str(file_path))
    if guessed in {"image/jpeg", "image/png"}:
        return guessed
    ext = file_path.suffix.lower()
    if ext == ".png":
        return "image/png"
    return "image/jpeg"


class PlantDiseaseDesktopApp:
    """Aplicación de escritorio en Tkinter que consume el servicio FastAPI de inferencia."""

    def __init__(self, root: tk.Tk, initial_api_url: str = API_BASE_URL) -> None:
        self.root = root
        self.root.title("🌿 Sistema IA de Diagnóstico Fitosanitario en Hojas (DINOv2-small)")
        self.root.geometry("1280x820")
        self.root.minsize(1080, 720)
        self.root.configure(bg=COLOR_BG_MAIN)

        # Estado interno de la sesión
        self.api_url_var = tk.StringVar(value=initial_api_url)
        self.selected_file_path: Path | None = None
        self.selected_image_bytes: bytes = b""
        self.preview_photo: ImageTk.PhotoImage | None = None
        self.is_analyzing: bool = False
        self.last_prediction: dict[str, Any] | None = None

        self._configure_styles()
        self._build_layout()

        # Verificar estado de la API al iniciar
        self.root.after(150, self.check_api_health_async)

    def _configure_styles(self) -> None:
        """Configura los estilos visuales de ttk."""
        self.style = ttk.Style(self.root)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self.style.configure(
            "Primary.TButton",
            background=COLOR_PRIMARY,
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", COLOR_PRIMARY_ACTIVE), ("disabled", "#95b8a6")],
            foreground=[("disabled", "#e9ecef")],
        )

        self.style.configure(
            "Secondary.TButton",
            background="#e9f5ee",
            foreground=COLOR_HEADER_BG,
            font=("Segoe UI", 9, "bold"),
            padding=(10, 6),
        )
        self.style.map(
            "Secondary.TButton",
            background=[("active", "#ccebd9")],
        )

        self.style.configure(
            "Confidence.Horizontal.TProgressbar",
            troughcolor="#e9ecef",
            background=COLOR_PRIMARY,
            thickness=18,
        )

        self.style.configure(
            "Top3.Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=COLOR_TEXT_PRIMARY,
            rowheight=28,
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "Top3.Treeview.Heading",
            background="#e9f5ee",
            foreground=COLOR_HEADER_BG,
            font=("Segoe UI", 9, "bold"),
        )

    def _build_layout(self) -> None:
        """Construye la estructura visual completa de la ventana."""
        # 1. Encabezado superior
        header_frame = tk.Frame(self.root, bg=COLOR_HEADER_BG, padx=24, pady=14)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header_frame,
            text="🌿 Identificador de Enfermedades en Plantas con IA",
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_HEADER_BG,
            fg="#ffffff",
            anchor="w",
        )
        title_lbl.pack(fill=tk.X)

        subtitle_lbl = tk.Label(
            header_frame,
            text=(
                "Clasificación automatizada de hojas mediante visión por computador basada en el modelo "
                "DINOv2-small preentrenado sobre 38 categorías fitosanitarias (ejecución en CPU vía FastAPI)."
            ),
            font=("Segoe UI", 10),
            bg=COLOR_HEADER_BG,
            fg=COLOR_HEADER_SUB,
            anchor="w",
        )
        subtitle_lbl.pack(fill=tk.X, pady=(2, 0))

        # 2. Contenedor principal de 3 columnas (Sidebar | Carga de imagen | Resultados)
        body_frame = tk.Frame(self.root, bg=COLOR_BG_MAIN, padx=16, pady=14)
        body_frame.pack(fill=tk.BOTH, expand=True)

        body_frame.columnconfigure(0, weight=0, minsize=275)
        body_frame.columnconfigure(1, weight=4, minsize=340)
        body_frame.columnconfigure(2, weight=6, minsize=480)
        body_frame.rowconfigure(0, weight=1)

        self._build_sidebar(body_frame)
        self._build_upload_panel(body_frame)
        self._build_results_panel(body_frame)

    def _build_sidebar(self, parent: tk.Frame) -> None:
        """Construye el panel lateral izquierdo con el estado de FastAPI e instrucciones."""
        sidebar = tk.Frame(
            parent,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            padx=14,
            pady=14,
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(
            sidebar,
            text="⚙️ Estado del Servicio",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_HEADER_BG,
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            sidebar,
            text="URL del servidor FastAPI:",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            anchor="w",
        ).pack(fill=tk.X)

        url_entry = ttk.Entry(sidebar, textvariable=self.api_url_var, font=("Segoe UI", 9))
        url_entry.pack(fill=tk.X, pady=(4, 8))

        self.btn_check_health = ttk.Button(
            sidebar,
            text="🔄 Verificar conexión",
            style="Secondary.TButton",
            command=self.check_api_health_async,
        )
        self.btn_check_health.pack(fill=tk.X, pady=(0, 10))

        # Tarjeta de estado de conexión
        self.health_badge = tk.Label(
            sidebar,
            text="⏳ Verificando estado de la API...",
            font=("Segoe UI", 9, "bold"),
            bg="#e9ecef",
            fg=COLOR_TEXT_PRIMARY,
            padx=8,
            pady=6,
            wraplength=235,
            justify="left",
            anchor="w",
        )
        self.health_badge.pack(fill=tk.X, pady=(0, 6))

        self.health_details_lbl = tk.Label(
            sidebar,
            text="",
            font=("Segoe UI", 8),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            justify="left",
            anchor="w",
            wraplength=235,
        )
        self.health_details_lbl.pack(fill=tk.X, pady=(0, 10))

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, pady=8)

        tk.Label(
            sidebar,
            text="📋 Instrucciones de uso",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_HEADER_BG,
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 4))

        instructions_text = (
            "1. Seleccione una fotografía clara de una hoja individual (JPG, JPEG o PNG, "
            f"máx. {MAX_IMAGE_SIZE_MB} MB).\n\n"
            "2. Verifique la vista previa en el panel central.\n\n"
            "3. Presione «Analizar fotografía».\n\n"
            "4. Revise la planta identificada, la condición fitosanitaria, la confianza y el Top-3."
        )
        tk.Label(
            sidebar,
            text=instructions_text,
            font=("Segoe UI", 9),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            justify="left",
            anchor="w",
            wraplength=235,
        ).pack(fill=tk.X, pady=(0, 10))

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, pady=8)

        tk.Label(
            sidebar,
            text="🌱 Cultivos soportados (14)",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_HEADER_BG,
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 4))

        tk.Label(
            sidebar,
            text=(
                "Manzano, Arándano, Cerezo, Maíz, Vid (Uva), Naranjo, Duraznero, "
                "Pimiento morrón, Papa, Frambueso, Soja, Calabaza, Fresa y Tomate."
            ),
            font=("Segoe UI", 8),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            justify="left",
            anchor="w",
            wraplength=235,
        ).pack(fill=tk.X)

    def _build_upload_panel(self, parent: tk.Frame) -> None:
        """Construye el panel central para seleccionar y previsualizar la fotografía."""
        upload_card = tk.Frame(
            parent,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            padx=16,
            pady=14,
        )
        upload_card.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        upload_card.columnconfigure(0, weight=1)
        upload_card.rowconfigure(2, weight=1)

        tk.Label(
            upload_card,
            text="📤 1. Cargar fotografía de la hoja",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_HEADER_BG,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 10))

        btn_select = ttk.Button(
            upload_card,
            text="📂 Seleccionar imagen (JPG, JPEG, PNG)...",
            style="Secondary.TButton",
            command=self.select_image_file,
        )
        btn_select.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Contenedor de vista previa
        self.preview_container = tk.Frame(
            upload_card,
            bg="#f8faf9",
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        )
        self.preview_container.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.preview_container.columnconfigure(0, weight=1)
        self.preview_container.rowconfigure(0, weight=1)

        self.preview_label = tk.Label(
            self.preview_container,
            text=(
                "📷\n\nNinguna imagen seleccionada.\n\n"
                "Haga clic en «Seleccionar imagen» para cargar\n"
                "una fotografía en formato JPG, JPEG o PNG."
            ),
            font=("Segoe UI", 10),
            bg="#f8faf9",
            fg=COLOR_TEXT_MUTED,
            justify="center",
        )
        self.preview_label.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        self.file_info_label = tk.Label(
            upload_card,
            text="Archivo: ninguno",
            font=("Segoe UI", 8),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.file_info_label.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        self.btn_analyze = ttk.Button(
            upload_card,
            text="🔍 Analizar fotografía",
            style="Primary.TButton",
            command=self.analyze_image_async,
            state=tk.DISABLED,
        )
        self.btn_analyze.grid(row=4, column=0, sticky="ew")

    def _build_results_panel(self, parent: tk.Frame) -> None:
        """Construye el panel derecho donde se presentan los resultados del diagnóstico."""
        results_card = tk.Frame(
            parent,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            padx=18,
            pady=14,
        )
        results_card.grid(row=0, column=2, sticky="nsew")
        results_card.columnconfigure(0, weight=1)
        results_card.rowconfigure(5, weight=1)

        tk.Label(
            results_card,
            text="🔬 2. Resultado de la Clasificación",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_HEADER_BG,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Banner de estado fitosanitario (Sana / Enferma / Esperando)
        self.status_banner = tk.Label(
            results_card,
            text=(
                "ℹ️ Seleccione una fotografía y presione «Analizar fotografía» "
                "para obtener el diagnóstico orientativo."
            ),
            font=("Segoe UI", 10, "bold"),
            bg="#e9f5ee",
            fg=COLOR_HEADER_BG,
            padx=12,
            pady=10,
            anchor="w",
            justify="left",
            wraplength=520,
        )
        self.status_banner.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        # Tarjetas de métricas principales (Planta, Confianza, Tiempo)
        metrics_frame = tk.Frame(results_card, bg=COLOR_CARD_BG)
        metrics_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        for col_idx in range(3):
            metrics_frame.columnconfigure(col_idx, weight=1, uniform="metric")

        self.metric_plant_val, self.metric_plant_sub = self._create_metric_card(
            metrics_frame, col=0, title="🌱 Planta identificada", initial_val="—", initial_sub=""
        )
        self.metric_conf_val, self.metric_conf_sub = self._create_metric_card(
            metrics_frame, col=1, title="🎯 Confianza del modelo", initial_val="—", initial_sub=""
        )
        self.metric_time_val, self.metric_time_sub = self._create_metric_card(
            metrics_frame, col=2, title="⏱️ Tiempo de inferencia", initial_val="—", initial_sub="CPU"
        )

        # Detalle de enfermedad y barra de progreso
        detail_frame = tk.Frame(results_card, bg=COLOR_CARD_BG)
        detail_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        detail_frame.columnconfigure(0, weight=1)

        self.condition_lbl = tk.Label(
            detail_frame,
            text="🦠 Enfermedad o condición detectada: —",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_PRIMARY,
            anchor="w",
            justify="left",
            wraplength=540,
        )
        self.condition_lbl.grid(row=0, column=0, sticky="ew")

        self.tech_label_lbl = tk.Label(
            detail_frame,
            text="Etiqueta técnica del modelo: —",
            font=("Segoe UI", 8),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.tech_label_lbl.grid(row=1, column=0, sticky="ew", pady=(2, 6))

        self.confidence_bar = ttk.Progressbar(
            detail_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100.0,
            style="Confidence.Horizontal.TProgressbar",
        )
        self.confidence_bar.grid(row=2, column=0, sticky="ew")

        # Sección Top-3 (Gráfico de barras en Canvas + Tabla Treeview)
        top3_section = tk.Frame(results_card, bg=COLOR_CARD_BG)
        top3_section.grid(row=5, column=0, sticky="nsew", pady=(4, 10))
        top3_section.columnconfigure(0, weight=1)
        top3_section.rowconfigure(2, weight=1)

        tk.Label(
            top3_section,
            text="📊 Tres categorías más probables (Top-3)",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_HEADER_BG,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.top3_canvas = tk.Canvas(
            top3_section,
            height=115,
            bg="#f8faf9",
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        )
        self.top3_canvas.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.top3_canvas.bind("<Configure>", lambda _event: self._redraw_top3_bars())

        columns = ("rank", "plant", "condition", "status", "confidence")
        self.top3_tree = ttk.Treeview(
            top3_section,
            columns=columns,
            show="headings",
            height=3,
            style="Top3.Treeview",
        )
        self.top3_tree.heading("rank", text="Pos.")
        self.top3_tree.heading("plant", text="Planta")
        self.top3_tree.heading("condition", text="Enfermedad / Condición")
        self.top3_tree.heading("status", text="Estado")
        self.top3_tree.heading("confidence", text="Confianza (%)")

        self.top3_tree.column("rank", width=48, anchor="center", stretch=False)
        self.top3_tree.column("plant", width=115, anchor="w")
        self.top3_tree.column("condition", width=210, anchor="w")
        self.top3_tree.column("status", width=80, anchor="center", stretch=False)
        self.top3_tree.column("confidence", width=95, anchor="e", stretch=False)
        self.top3_tree.grid(row=2, column=0, sticky="nsew")

        # Aviso agronómico obligatorio
        self.disclaimer_lbl = tk.Label(
            results_card,
            text=f"📌 Aviso importante: {AGRONOMIC_DISCLAIMER}",
            font=("Segoe UI", 8),
            bg=COLOR_WARNING_BG,
            fg=COLOR_WARNING_FG,
            padx=10,
            pady=8,
            justify="left",
            anchor="w",
            wraplength=540,
        )
        self.disclaimer_lbl.grid(row=6, column=0, sticky="ew")

    def _create_metric_card(
        self,
        parent: tk.Frame,
        col: int,
        title: str,
        initial_val: str,
        initial_sub: str,
    ) -> tuple[tk.Label, tk.Label]:
        """Crea una tarjeta visual para mostrar una métrica clave."""
        padx = (0, 6) if col < 2 else (0, 0)
        card = tk.Frame(
            parent,
            bg="#f8faf9",
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            padx=10,
            pady=8,
        )
        card.grid(row=0, column=col, sticky="nsew", padx=padx)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            bg="#f8faf9",
            fg=COLOR_TEXT_MUTED,
            anchor="w",
        ).pack(fill=tk.X)

        val_lbl = tk.Label(
            card,
            text=initial_val,
            font=("Segoe UI", 12, "bold"),
            bg="#f8faf9",
            fg=COLOR_HEADER_BG,
            anchor="w",
        )
        val_lbl.pack(fill=tk.X, pady=(2, 0))

        sub_lbl = tk.Label(
            card,
            text=initial_sub,
            font=("Segoe UI", 8),
            bg="#f8faf9",
            fg=COLOR_TEXT_MUTED,
            anchor="w",
        )
        sub_lbl.pack(fill=tk.X)
        return val_lbl, sub_lbl

    # ------------------------------------------------------------------
    # Comunicación con FastAPI (hilos en segundo plano)
    # ------------------------------------------------------------------

    def check_api_health_async(self) -> None:
        """Consulta el endpoint GET /health sin bloquear el hilo principal de Tkinter."""
        base_url = self.api_url_var.get().strip() or API_BASE_URL
        self.health_badge.configure(
            text="⏳ Verificando conexión con FastAPI...",
            bg="#e9ecef",
            fg=COLOR_TEXT_PRIMARY,
        )
        self.btn_check_health.configure(state=tk.DISABLED)

        def _worker() -> None:
            response = fetch_api_health(base_url=base_url)
            self.root.after(0, lambda: self._on_health_response(response))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_health_response(self, response: ApiClientResponse) -> None:
        """Actualiza la barra lateral con el resultado del health check."""
        self.btn_check_health.configure(state=tk.NORMAL)
        if response.success and response.data:
            data = response.data
            self.health_badge.configure(
                text="✅ API en línea y modelo disponible",
                bg=COLOR_HEALTHY_BG,
                fg=COLOR_HEALTHY_FG,
            )
            details = (
                f"Modelo: {data.get('model_name')}\n"
                f"Arquitectura: {data.get('architecture')}\n"
                f"Dispositivo: {str(data.get('device', 'cpu')).upper()}\n"
                f"Categorías soportadas: {data.get('num_classes', 38)}"
            )
            self.health_details_lbl.configure(text=details)
        else:
            self.health_badge.configure(
                text="❌ Servicio de inferencia no disponible",
                bg=COLOR_DISEASED_BG,
                fg=COLOR_DISEASED_FG,
            )
            self.health_details_lbl.configure(
                text=response.error_message or "Verifique que FastAPI esté ejecutándose."
            )

    # ------------------------------------------------------------------
    # Selección de imagen y ejecución de inferencia
    # ------------------------------------------------------------------

    def select_image_file(self) -> None:
        """Abre el diálogo nativo para seleccionar una imagen JPG, JPEG o PNG."""
        file_path_str = filedialog.askopenfilename(
            parent=self.root,
            title="Seleccionar fotografía de hoja",
            filetypes=[
                ("Imágenes soportadas (*.jpg;*.jpeg;*.png)", "*.jpg *.jpeg *.png"),
                ("JPEG (*.jpg;*.jpeg)", "*.jpg *.jpeg"),
                ("PNG (*.png)", "*.png"),
                ("Todos los archivos (*.*)", "*.*"),
            ],
        )
        if not file_path_str:
            return

        self.load_image_from_path(Path(file_path_str))

    def load_image_from_path(self, file_path: Path) -> bool:
        """Lee los bytes de la imagen seleccionada y actualiza la vista previa."""
        try:
            image_bytes = file_path.read_bytes()
            with Image.open(BytesIO(image_bytes)) as pil_img:
                pil_img.load()
                width, height = pil_img.size
                preview_img = ImageOps.exif_transpose(pil_img).convert("RGB")
        except Exception as exc:
            messagebox.showerror(
                "Archivo de imagen inválido",
                f"No fue posible abrir la imagen seleccionada:\n{exc}",
                parent=self.root,
            )
            return False

        self.selected_file_path = file_path
        self.selected_image_bytes = image_bytes

        # Redimensionar proporcionalmente para la vista previa
        preview_img.thumbnail((340, 340), Image.Resampling.LANCZOS)
        self.preview_photo = ImageTk.PhotoImage(preview_img)
        self.preview_label.configure(image=self.preview_photo, text="")

        size_kb = len(image_bytes) / 1024.0
        self.file_info_label.configure(
            text=f"Archivo: {file_path.name} ({width}×{height} px, {size_kb:.1f} KB)"
        )
        self.btn_analyze.configure(state=tk.NORMAL)

        self.status_banner.configure(
            text=(
                f"📸 Fotografía «{file_path.name}» lista para ser clasificada. "
                "Presione «Analizar fotografía»."
            ),
            bg="#e9f5ee",
            fg=COLOR_HEADER_BG,
        )
        return True

    def analyze_image_async(self) -> None:
        """Envía la fotografía seleccionada al endpoint POST /predict en un hilo secundario."""
        if not self.selected_file_path or not self.selected_image_bytes or self.is_analyzing:
            return

        self.is_analyzing = True
        self.btn_analyze.configure(state=tk.DISABLED, text="⏳ Analizando en CPU...")
        self.status_banner.configure(
            text="⏳ Analizando la hoja en el servidor de inferencia (CPU)...",
            bg="#e9ecef",
            fg=COLOR_TEXT_PRIMARY,
        )

        image_bytes = self.selected_image_bytes
        filename = self.selected_file_path.name
        content_type = guess_mime_type(self.selected_file_path)
        base_url = self.api_url_var.get().strip() or API_BASE_URL

        def _worker() -> None:
            response = request_image_prediction(
                image_bytes=image_bytes,
                filename=filename,
                content_type=content_type,
                base_url=base_url,
            )
            self.root.after(0, lambda: self._on_prediction_response(response))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_prediction_response(self, response: ApiClientResponse) -> None:
        """Procesa la respuesta de FastAPI y actualiza el panel de resultados."""
        self.is_analyzing = False
        self.btn_analyze.configure(state=tk.NORMAL, text="🔍 Analizar fotografía")

        if not response.success or response.data is None:
            error_msg = response.error_message or "Error desconocido al consultar la API."
            self.status_banner.configure(
                text=f"❌ Error al procesar la solicitud: {error_msg}",
                bg=COLOR_DISEASED_BG,
                fg=COLOR_DISEASED_FG,
            )
            messagebox.showerror("Error en la clasificación", error_msg, parent=self.root)
            return

        self.render_prediction_results(response.data)

    def render_prediction_results(self, data: dict[str, Any]) -> None:
        """Pinta los datos de predicción en todos los widgets del panel de resultados."""
        self.last_prediction = data

        plant_name = str(data.get("plant", "No disponible"))
        plant_en = str(data.get("plant_en", ""))
        condition_name = str(data.get("disease_or_condition", "No disponible"))
        condition_en = str(data.get("disease_or_condition_en", ""))
        predicted_category = str(data.get("predicted_category", ""))
        is_healthy = data.get("is_healthy")
        health_status = str(data.get("health_status", "No determinado"))
        confidence_pct = float(data.get("confidence_percentage", 0.0))
        inference_time_ms = float(data.get("inference_time_ms", 0.0))
        disclaimer = str(data.get("disclaimer", AGRONOMIC_DISCLAIMER))

        if is_healthy is True:
            self.status_banner.configure(
                text=(
                    f"✅ Estado fitosanitario estimado: HOJA SANA ({health_status})\n"
                    "La hoja analizada coincide con una categoría saludable dentro del catálogo del modelo."
                ),
                bg=COLOR_HEALTHY_BG,
                fg=COLOR_HEALTHY_FG,
            )
        elif is_healthy is False:
            self.status_banner.configure(
                text=(
                    f"⚠️ Estado estimado: POSIBLE ENFERMEDAD O PLAGA ({health_status})\n"
                    "Se detectaron patrones visuales compatibles con una afección foliar."
                ),
                bg=COLOR_DISEASED_BG,
                fg=COLOR_DISEASED_FG,
            )
        else:
            self.status_banner.configure(
                text=f"Estado fitosanitario: {health_status}",
                bg="#e9ecef",
                fg=COLOR_TEXT_PRIMARY,
            )

        self.metric_plant_val.configure(text=plant_name)
        self.metric_plant_sub.configure(text=plant_en)

        self.metric_conf_val.configure(text=f"{confidence_pct:.2f} %")
        self.metric_conf_sub.configure(text=f"Estado: {health_status}")

        self.metric_time_val.configure(text=f"{inference_time_ms:.2f} ms")
        self.metric_time_sub.configure(text="Inferencia en CPU")

        self.condition_lbl.configure(
            text=f"🦠 Enfermedad o condición detectada: {condition_name} ({condition_en})"
        )
        self.tech_label_lbl.configure(text=f"Etiqueta técnica del modelo: {predicted_category}")
        self.confidence_bar["value"] = max(0.0, min(100.0, confidence_pct))

        # Poblar tabla Treeview del Top-3
        for item_id in self.top3_tree.get_children():
            self.top3_tree.delete(item_id)

        top_predictions = data.get("top_predictions", [])
        for item in top_predictions:
            pct = float(item.get("confidence_percentage", 0.0))
            self.top3_tree.insert(
                "",
                tk.END,
                values=(
                    f"#{item.get('rank')}",
                    item.get("plant", ""),
                    item.get("disease_or_condition", ""),
                    item.get("health_status", ""),
                    f"{pct:.2f} %",
                ),
            )

        self.disclaimer_lbl.configure(text=f"📌 Aviso importante: {disclaimer}")
        self._redraw_top3_bars()

    def _redraw_top3_bars(self) -> None:
        """Dibuja las barras horizontales comparativas del Top-3 en el Canvas."""
        self.top3_canvas.delete("all")
        width = max(self.top3_canvas.winfo_width(), 420)

        if not self.last_prediction or not self.last_prediction.get("top_predictions"):
            self.top3_canvas.create_text(
                width // 2,
                55,
                text="Las 3 predicciones más probables se graficarán aquí tras el análisis.",
                fill=COLOR_TEXT_MUTED,
                font=("Segoe UI", 9),
            )
            return

        top_predictions = self.last_prediction["top_predictions"][:3]
        row_height = 34
        bar_max_width = max(width - 270, 120)

        for idx, item in enumerate(top_predictions):
            y_top = 10 + idx * row_height
            rank = item.get("rank", idx + 1)
            plant = item.get("plant", "")
            cond = item.get("disease_or_condition", "")
            pct = float(item.get("confidence_percentage", 0.0))
            label_text = f"#{rank} {plant} — {cond}"
            if len(label_text) > 34:
                label_text = label_text[:31] + "..."

            self.top3_canvas.create_text(
                10,
                y_top + 11,
                text=label_text,
                anchor="w",
                fill=COLOR_TEXT_PRIMARY,
                font=("Segoe UI", 8, "bold"),
            )

            bar_x0 = 205
            bar_y0 = y_top + 3
            bar_y1 = y_top + 20

            # Fondo de la barra
            self.top3_canvas.create_rectangle(
                bar_x0,
                bar_y0,
                bar_x0 + bar_max_width,
                bar_y1,
                fill="#e9ecef",
                outline="",
            )

            # Barra proporcional al porcentaje
            fill_width = max(int((pct / 100.0) * bar_max_width), 3 if pct > 0 else 0)
            bar_color = COLOR_PRIMARY if idx == 0 else "#52b788"
            if fill_width > 0:
                self.top3_canvas.create_rectangle(
                    bar_x0,
                    bar_y0,
                    bar_x0 + fill_width,
                    bar_y1,
                    fill=bar_color,
                    outline="",
                )

            self.top3_canvas.create_text(
                bar_x0 + bar_max_width + 8,
                y_top + 11,
                text=f"{pct:.2f}%",
                anchor="w",
                fill=COLOR_HEADER_BG,
                font=("Segoe UI", 8, "bold"),
            )


def main() -> None:
    """Punto de entrada principal para ejecutar la interfaz gráfica de escritorio en Tkinter."""
    root = tk.Tk()
    PlantDiseaseDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
