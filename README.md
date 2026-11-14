# 🌿 Sistema de Clasificación de Enfermedades en Plantas (DINOv2-small)

**Universidad Autónoma de Occidente (UAO) — Maestría en Inteligencia Artificial y Ciencia de Datos**  
*Asignatura: Gestión de Proyectos en IA y Ciencia de Datos · Grupo 2 · Periodo 2026-2*

![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=uv&logoColor=white)
![Ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64?logo=ruff&logoColor=black)
![pytest](https://img.shields.io/badge/pytest-158%20unit%20%7C%206%20integration-0A9EDC?logo=pytest&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend%20CPU-009688?logo=fastapi&logoColor=white)
[![Quality Gate CI (M3)](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/Code%20MIT%20%7C%20Weights%20CC%20BY--SA%204.0-lightgrey)

---

Aplicación modular de Inteligencia Artificial para la **clasificación asistida de posibles enfermedades foliares en cultivos agrícolas** a partir de fotografías de hojas. Desarrollada para la asignatura **Gestión de Proyectos en IA y Ciencia de Datos (UAO)** bajo arquitectura desacoplada **Model-as-a-Service (MaaS)** con **FastAPI**, gestión reproducible de dependencias con **`uv`** (Python 3.13) y ejecución íntegra en **CPU** mediante **PyTorch**, **SafeTensors** y **Hugging Face Transformers**.

> **Decisión arquitectónica M3 (D-01):** Por decisión confirmada del equipo, la interfaz gráfica para la entrega del Módulo 3 **NO utiliza Streamlit**; el frontend web independiente consume la API FastAPI exclusivamente vía HTTP sin cargar pesos del modelo.

---

## 📌 1. Descripción del Proyecto y Problema que Resuelve

### Problema que resuelve
Las enfermedades fitosanitarias provocan pérdidas significativas en el rendimiento y la calidad de los cultivos agrícolas. La identificación temprana de patologías foliares suele requerir inspección visual especializada en campo o análisis de laboratorio, recursos que no siempre están disponibles de forma inmediata para pequeños y medianos productores o estudiantes de ciencias agrarias.

### Solución propuesta
Este sistema proporciona una herramienta de apoyo preliminar que analiza fotografías digitales de hojas individuales (`JPG`, `JPEG` o `PNG`) y estima en milisegundos:
1. **La especie vegetal (planta)** a la que pertenece la hoja (entre 14 cultivos).
2. **La enfermedad o condición fitosanitaria probable** (entre 38 categorías: 26 patologías/plagas y 12 estados saludables).
3. **El estado general de la hoja** (`Sana` o `Enferma`).
4. **El porcentaje de confianza** del modelo junto con el **ranking de las 3 categorías más probables (Top-3)** y el **tiempo de inferencia en CPU**.

> **⚠️ Aviso Agronómico Importante:** Las predicciones generadas por esta aplicación son estrictamente **orientativas** y de cribado preliminar; **no sustituyen** una evaluación ni un diagnóstico agronómico o fitopatológico profesional.

---

## 🏗️ 2. Arquitectura del Sistema

El proyecto implementa una arquitectura modular y desacoplada en capas para garantizar mantenibilidad, testabilidad y separación de responsabilidades:

```text
.
├── config.json                      # Arquitectura DINOv2 y mapeo de las 38 etiquetas (id2label / label2id)
├── preprocessor_config.json         # Parámetros oficiales de BitImageProcessor
├── model.safetensors                # Pesos preentrenados en formato SafeTensors (~88 MB, Git LFS)
├── src/                             # Núcleo de negocio e inferencia
│   ├── config.py                    # Configuración centralizada, rutas, límites y constantes
│   ├── exceptions.py                # Jerarquía de excepciones de dominio con códigos HTTP asociados
│   ├── labels.py                    # Catálogo, limpieza y traducción al español de las 38 categorías
│   ├── model_loader.py              # Verificación de archivos y carga local en CPU (singleton thread-safe)
│   ├── preprocessing.py             # Validación de archivos/formatos, conversión RGB y tensores PyTorch
│   ├── postprocessing.py            # Cálculo de Softmax, ordenamiento Top-3 y estructuración de salidas
│   └── inference.py                 # Orquestador del flujo de inferencia y medición de latencia (ms)
├── api/                             # Capa de servicio REST (Model-as-a-Service con FastAPI)
│   ├── schemas.py                   # Modelos de datos y validación con Pydantic v2
│   └── main.py                      # Endpoints GET /health, GET /model-info y POST /predict
├── ui/                              # Capa de presentación (escritorio Tkinter y frontend web)
│   ├── api_client.py                # Cliente HTTP desacoplado que consume la API REST (sin duplicar el modelo)
│   ├── desktop_app.py               # Interfaz gráfica nativa de escritorio en español (Tkinter — operativa M3)
│   └── web/                         # Frontend HTML/CSS/JS y servidor de previsualización con mocks
├── deploy/
│   └── nginx.conf                   # Proxy same-origin del frontend web para Docker Compose
├── docs/                            # Documentación técnica, diagramas Archify y guías de reproducción
│   ├── architecture/                # Diagramas C4/componentes (.html, .svg, .json)
│   ├── getting-started.md           # Guía de arranque reproducible en Windows con uv y Spec Kit
│   ├── model-card.md                # Ficha técnica oficial del modelo (Mitchell et al., 2019)
│   └── qa-e2e-benchmarks.md         # Reporte empírico de validación E2E y benchmarks en CPU
├── specs/                           # Especificaciones SDD (Spec Kit) por unidad de trabajo
├── tests/                           # Suite de pruebas automatizadas con pytest
│   ├── conftest.py                  # Generadores de imágenes sintéticas (JPG, PNG, RGBA, grises, corruptas, GIF)
│   ├── unit/                        # Pruebas unitarias rápidas aisladas con mocks (sin pesos reales)
│   └── integration/                 # Pruebas de integración contra el modelo DINOv2-small real en CPU
├── AGENTS.md                        # Gobernanza, matriz de responsabilidades y reglas para agentes IA
├── pyproject.toml                   # Definición del proyecto, dependencias y configuración de pytest/uv/ruff
├── uv.lock                          # Archivo de bloqueo exacto de dependencias
└── README.md                        # Documentación principal del proyecto y ficha técnica
```

> Consulta el diagrama visual de arquitectura en [`docs/architecture/system-architecture.svg`](docs/architecture/system-architecture.svg) (o la vista interactiva [`docs/architecture/system-architecture.html`](docs/architecture/system-architecture.html)).

### Flujo de comunicación
1. El usuario carga una fotografía foliar en la **interfaz de escritorio en Tkinter (`ui/desktop_app.py`)** (o en la nueva interfaz web independiente sin Streamlit en curso bajo HU-06), que se comunica vía HTTP con el backend.
2. El cliente (`ui/api_client.py`) envía la imagen mediante `POST /predict` (`multipart/form-data`) al backend **FastAPI** (`api/main.py`), **sin cargar pesos ni importar PyTorch/Transformers en la capa de presentación**.
3. **FastAPI** delega en `src/inference.py`, que valida la imagen (`src/preprocessing.py`), aplica las transformaciones exactas de `preprocessor_config.json`, ejecuta el pase hacia adelante (`forward`) sobre **CPU** con `torch.no_grad()` y formatea el Top-3 (`src/postprocessing.py`).
4. La respuesta JSON estructurada regresa al frontend, mostrando la predicción, probabilidades Top-3, advertencia por baja confianza ($\tau = 0.60$) y descargo agronómico.

---

## 🧠 3. Modelo Base Seleccionado

- **Nombre del modelo:** `rodynaemad/plant-disease-dinov2-small`
- **Enlace oficial en Hugging Face:** [https://huggingface.co/rodynaemad/plant-disease-dinov2-small](https://huggingface.co/rodynaemad/plant-disease-dinov2-small)
- **Autora del modelo preentrenado:** Rodayna Emad Mohamed (*Pharos University in Alexandria*).
- **Arquitectura:** `Dinov2ForImageClassification` basada en el backbone [`facebook/dinov2-small`](https://huggingface.co/facebook/dinov2-small) (congelado, extracción de características de 768 dimensiones combinando el token `CLS` y el promedio de parches) junto con un cabezal de clasificación lineal entrenado sobre las 54,305 imágenes en color del conjunto de datos **PlantVillage**.
- **Nota sobre las métricas reportadas por la autora:** En la documentación oficial del modelo (*Model Card*), la autora reporta una exactitud (*accuracy*) de **98.86%** y un **Macro F1 de 98.49%** sobre una partición de prueba de hojas no vistas durante el entrenamiento (*leaf-level held-out split* de 10,862 imágenes de PlantVillage). **Estas cifras corresponden exclusivamente al entrenamiento y evaluación publicados por la autora original del modelo y no se presentan como métricas de entrenamiento propio de este proyecto**, dado que en este trabajo utilizamos el modelo preentrenado tal como fue distribuido, sin modificar sus pesos (`model.safetensors`).
- **Model Card oficial del proyecto:** Consulta la ficha técnica completa, análisis de sesgos, consideraciones éticas y métricas computacionales reales en CPU en [`docs/model-card.md`](docs/model-card.md) (elaborada bajo el estándar de Mitchell et al., 2019).

### Preprocesamiento oficial aplicado (`preprocessor_config.json`)
El módulo `src/preprocessing.py` utiliza `AutoImageProcessor.from_pretrained(..., local_files_only=True)` (`BitImageProcessor`) respetando fielmente los parámetros originales del modelo:
- **Conversión de color:** `RGB` (`do_convert_rgb: true`).
- **Redimensionamiento:** Lado más corto a `256 px` mediante interpolación bicúbica (`resample: 3`).
- **Recorte central (`center_crop`):** `224 × 224 px`.
- **Reescalado:** Factor `1/255` (`0.00392156862745098`).
- **Normalización (ImageNet):** Media `[0.485, 0.456, 0.406]` y desviación estándar `[0.229, 0.224, 0.225]`.
- **Salida:** Tensor de PyTorch `pixel_values` de dimensión `(1, 3, 224, 224)` en `float32` sobre `CPU`.

---

## 🍃 4. Descripción de las 38 Categorías del Modelo

El modelo clasifica fotografías foliares en **38 categorías** distribuidas en **14 cultivos** (**12 categorías de hojas sanas** y **26 categorías de enfermedades o plagas**):

| ID | Etiqueta del Modelo (`id2label`) | Planta (ES) | Enfermedad / Condición (ES) | Estado |
|---:|---|---|---|---|
| 0 | `Apple___Apple_scab` | Manzano | Sarna del manzano (*Venturia inaequalis*) | Enferma |
| 1 | `Apple___Black_rot` | Manzano | Podredumbre negra | Enferma |
| 2 | `Apple___Cedar_apple_rust` | Manzano | Roya del manzano y el cedro | Enferma |
| 3 | `Apple___healthy` | Manzano | Sana (sin enfermedad aparente) | Sana |
| 4 | `Blueberry___healthy` | Arándano | Sana (sin enfermedad aparente) | Sana |
| 5 | `Cherry_(including_sour)___Powdery_mildew` | Cerezo (incluyendo guindo) | Oídio (Cenicilla polvorienta) | Enferma |
| 6 | `Cherry_(including_sour)___healthy` | Cerezo (incluyendo guindo) | Sana (sin enfermedad aparente) | Sana |
| 7 | `Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot` | Maíz | Mancha gris de la hoja (*Cercospora*) | Enferma |
| 8 | `Corn_(maize)___Common_rust_` | Maíz | Roya común del maíz | Enferma |
| 9 | `Corn_(maize)___Northern_Leaf_Blight` | Maíz | Tizón norteño de la hoja del maíz | Enferma |
| 10 | `Corn_(maize)___healthy` | Maíz | Sana (sin enfermedad aparente) | Sana |
| 11 | `Grape___Black_rot` | Vid (Uva) | Podredumbre negra | Enferma |
| 12 | `Grape___Esca_(Black_Measles)` | Vid (Uva) | Yesca de la vid (Sarampión negro / Esca) | Enferma |
| 13 | `Grape___Leaf_blight_(Isariopsis_Leaf_Spot)` | Vid (Uva) | Tizón de la hoja (Mancha foliar por *Isariopsis*) | Enferma |
| 14 | `Grape___healthy` | Vid (Uva) | Sana (sin enfermedad aparente) | Sana |
| 15 | `Orange___Haunglongbing_(Citrus_greening)` | Naranjo (Cítrico) | Huanglongbing (HLB / Enverdecimiento de los cítricos) | Enferma |
| 16 | `Peach___Bacterial_spot` | Duraznero (Melocotonero) | Mancha bacteriana | Enferma |
| 17 | `Peach___healthy` | Duraznero (Melocotonero) | Sana (sin enfermedad aparente) | Sana |
| 18 | `Pepper,_bell___Bacterial_spot` | Pimiento morrón | Mancha bacteriana | Enferma |
| 19 | `Pepper,_bell___healthy` | Pimiento morrón | Sana (sin enfermedad aparente) | Sana |
| 20 | `Potato___Early_blight` | Papa (Patata) | Tizón temprano (*Alternaria*) | Enferma |
| 21 | `Potato___Late_blight` | Papa (Patata) | Tizón tardío (*Phytophthora infestans*) | Enferma |
| 22 | `Potato___healthy` | Papa (Patata) | Sana (sin enfermedad aparente) | Sana |
| 23 | `Raspberry___healthy` | Frambueso | Sana (sin enfermedad aparente) | Sana |
| 24 | `Soybean___healthy` | Soja (Soya) | Sana (sin enfermedad aparente) | Sana |
| 25 | `Squash___Powdery_mildew` | Calabaza (Zapallo) | Oídio (Cenicilla polvorienta) | Enferma |
| 26 | `Strawberry___Leaf_scorch` | Fresa (Frutilla) | Quemadura foliar de la fresa | Enferma |
| 27 | `Strawberry___healthy` | Fresa (Frutilla) | Sana (sin enfermedad aparente) | Sana |
| 28 | `Tomato___Bacterial_spot` | Tomate | Mancha bacteriana | Enferma |
| 29 | `Tomato___Early_blight` | Tomate | Tizón temprano (*Alternaria*) | Enferma |
| 30 | `Tomato___Late_blight` | Tomate | Tizón tardío (*Phytophthora infestans*) | Enferma |
| 31 | `Tomato___Leaf_Mold` | Tomate | Moho de la hoja del tomate (*Passalora fulva*) | Enferma |
| 32 | `Tomato___Septoria_leaf_spot` | Tomate | Mancha foliar por *Septoria* | Enferma |
| 33 | `Tomato___Spider_mites Two-spotted_spider_mite` | Tomate | Ácaro de dos manchas (Arañuela roja) | Enferma |
| 34 | `Tomato___Target_Spot` | Tomate | Mancha anillada (*Corynespora cassiicola*) | Enferma |
| 35 | `Tomato___Tomato_Yellow_Leaf_Curl_Virus` | Tomate | Virus del rizado amarillo de la hoja del tomate (TYLCV) | Enferma |
| 36 | `Tomato___Tomato_mosaic_virus` | Tomate | Virus del mosaico del tomate (ToMV) | Enferma |
| 37 | `Tomato___healthy` | Tomate | Sana (sin enfermedad aparente) | Sana |

---

## 💻 5. Requisitos Técnicos

- **Sistema Operativo:** Windows 10/11, Linux o macOS (64 bits).
- **Hardware:** Procesador estándar **CPU** (no requiere GPU ni librerías CUDA). Mínimo recomendado: 4 GB de RAM.
- **Python:** **Python 3.13** (verificado en `CPython 3.13.18`).
- **Gestor de paquetes y entornos:** [`uv`](https://docs.astral.sh/uv/) (prohibido usar `pip` o `requirements.txt`).
- **Librerías principales:** `torch` (CPU), `transformers`, `safetensors`, `pillow`, `fastapi`, `uvicorn`, `pydantic`, `pytest`, `ruff`.

---

## 🚀 6. Instalación y Ejecución Local (con `uv`)

### Paso 1: Ubicarse en el directorio del proyecto
Abra una terminal **PowerShell** en la carpeta raíz del repositorio:
```powershell
cd uao-gestion-proyectos-ia-deteccion-enfermedades
```

### Paso 2: Sincronizar el entorno virtual determinista con `uv`
```powershell
uv sync --frozen
```
Este comando crea `.venv` e instala exactamente las dependencias fijadas en `uv.lock` (incluyendo PyTorch CPU).

### Paso 3: Verificar pesos locales del modelo
Asegúrese de contar localmente con `config.json`, `preprocessor_config.json` y `model.safetensors` (~88 MB, Git LFS) en la raíz del proyecto o en `modelo_plantas/` (o definiendo la variable de entorno `MODEL_DIR`). La aplicación carga el modelo con `local_files_only=True` sin conexión a internet.

### Paso 4: Iniciar la API REST (FastAPI)
```powershell
uv run uvicorn api.main:app --host 127.0.0.1 --port 8000
```
La API quedará disponible en `http://127.0.0.1:8000` (Swagger UI en `http://127.0.0.1:8000/docs`).

### Paso 5: Iniciar la Interfaz Gráfica Operativa (Tkinter)
En una **segunda ventana de PowerShell** (manteniendo la API FastAPI activa), inicie la interfaz gráfica de escritorio en Tkinter:
```powershell
uv run python ui/desktop_app.py
```

> **Nota M3 (D-01):** La interfaz Streamlit fue retirada de la entrega M3. Como interfaz operativa inmediata se dispone de la aplicación de escritorio **Tkinter (`ui/desktop_app.py`)**, mientras la interfaz web desacoplada en HTML/CSS/JS avanza bajo **HU-06 (Issue #9)**. Ambas consumen la API FastAPI exclusivamente vía HTTP.

---

## 📡 7. Uso de la API REST mediante Swagger Docs

Con el servidor FastAPI en ejecución, acceda a la documentación interactiva OpenAPI (Swagger UI) en:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoint `GET /health`
Verifica el estado del servicio y si el modelo local se cargó correctamente en CPU.

**Ejemplo de respuesta (`200 OK`):**
```json
{
  "status": "ok",
  "model_available": true,
  "model_name": "rodynaemad/plant-disease-dinov2-small",
  "architecture": "Dinov2ForImageClassification",
  "device": "cpu",
  "num_classes": 38,
  "model_path": "/app/modelo_plantas",
  "detail": "Servicio operativo y modelo cargado correctamente en CPU."
}
```

### Endpoint `GET /model-info`
Retorna los metadatos técnicos del modelo DINOv2-small cargado en CPU y su ruta local de pesos (`ModelInfoResponse`).

**Ejemplo de respuesta (`200 OK`):**
```json
{
  "model_name": "rodynaemad/plant-disease-dinov2-small",
  "architecture": "Dinov2ForImageClassification",
  "device": "cpu",
  "num_classes": 38,
  "model_available": true,
  "model_path": "C:/.../modelo_plantas"
}
```

### Endpoint `POST /predict`
Recibe un archivo de imagen (`file`, formatos `JPG`, `JPEG` o `PNG`, hasta `10 MB`) y retorna la predicción principal, el Top-3 y el tiempo de inferencia.

**Cómo probarlo desde Swagger UI:**
1. En `http://127.0.0.1:8000/docs`, despliegue **`POST /predict`**.
2. Haga clic en **«Try it out»**.
3. En el campo **`file`**, seleccione una fotografía de hoja en formato `.jpg`, `.jpeg` o `.png`.
4. Presione **«Execute»**.

**Ejemplo de respuesta (`200 OK`):**
```json
{
  "predicted_category": "Tomato___Late_blight",
  "class_id": 30,
  "plant": "Tomate",
  "plant_en": "Tomato",
  "disease_or_condition": "Tizón tardío (Phytophthora infestans)",
  "disease_or_condition_en": "Late blight",
  "is_healthy": false,
  "health_status": "Enferma",
  "confidence": 0.984512,
  "confidence_percentage": 98.45,
  "top_predictions": [
    {
      "rank": 1,
      "class_id": 30,
      "predicted_category": "Tomato___Late_blight",
      "plant": "Tomate",
      "plant_en": "Tomato",
      "disease_or_condition": "Tizón tardío (Phytophthora infestans)",
      "disease_or_condition_en": "Late blight",
      "is_healthy": false,
      "health_status": "Enferma",
      "confidence": 0.984512,
      "confidence_percentage": 98.45
    },
    {
      "rank": 2,
      "class_id": 29,
      "predicted_category": "Tomato___Early_blight",
      "plant": "Tomate",
      "plant_en": "Tomato",
      "disease_or_condition": "Tizón temprano (Alternaria)",
      "disease_or_condition_en": "Early blight",
      "is_healthy": false,
      "health_status": "Enferma",
      "confidence": 0.010234,
      "confidence_percentage": 1.02
    },
    {
      "rank": 3,
      "class_id": 34,
      "predicted_category": "Tomato___Target_Spot",
      "plant": "Tomate",
      "plant_en": "Tomato",
      "disease_or_condition": "Mancha anillada (Corynespora cassiicola)",
      "disease_or_condition_en": "Target Spot",
      "is_healthy": false,
      "health_status": "Enferma",
      "confidence": 0.003112,
      "confidence_percentage": 0.31
    }
  ],
  "inference_time_ms": 62.45,
  "disclaimer": "Las predicciones generadas por este sistema de inteligencia artificial son estrictamente orientativas y de apoyo preliminar; no sustituyen un diagnóstico ni una evaluación agronómica o fitopatológica profesional."
}
```

---

## 🐳 8. Empaquetado Wheel y Contenerización Docker (HU-08)

Implementado conforme a los criterios **AC8.1–AC8.3** y a la decisión **D-01** (sin Streamlit).

### 8.1 Paquete Wheel y sdist

```bash
uv build
```

Genera en `dist/`:

- `plant_disease_classifier-1.0.0-py3-none-any.whl`
- `plant_disease_classifier-1.0.0.tar.gz`

El wheel incluye los paquetes `src/`, `api/`, `ui/` y los activos estáticos de `ui/web/static/`.

### 8.2 Imagen Docker CPU multi-etapa

```bash
docker build -t plant-disease-classifier:1.0.0 .
docker run --rm -p 8000:8000 plant-disease-classifier:1.0.0
curl http://localhost:8000/health
```

La imagen final no incluye `uv` ni dependencias de desarrollo, ejecuta como usuario no root e incorpora el modelo local y el frontend web servido por FastAPI en `/`. La documentación OpenAPI queda disponible en `http://localhost:8000/docs`.

### 8.3 Orquestación con Docker Compose

```bash
docker compose up --build -d
curl http://localhost:8000/health
# Interfaz web: http://localhost:8080
# Swagger UI:   http://localhost:8080/docs
docker compose down
```

Compose levanta dos servicios en la red interna compartida:

- `api`: FastAPI + DINOv2 en CPU, publicado en `8000`.
- `web`: Nginx con el frontend estático y proxy same-origin hacia `api:8000`, publicado en `8080`.

El servicio `api` cuenta con *healthcheck* y el servicio `web` espera a que esté saludable antes de arrancar.

### 8.4 Requisitos

- Archivos locales `model.safetensors`, `config.json` y `preprocessor_config.json` presentes en la raíz.
- Docker Desktop o Docker Engine con el daemon activo.
- No se requiere Streamlit ni ninguna interfaz adicional.

---

## 🧪 9. Pruebas Automatizadas (`pytest`) y Calidad (`ruff`)

La suite de pruebas está dividida en:
- **Pruebas unitarias (`tests/unit/`):** Ejecución rápida y aislada mediante *mocks* (sin leer `model.safetensors`).
- **Pruebas de integración (`tests/integration/`):** Cargan el modelo DINOv2-small real en CPU y validan el flujo extremo a extremo contra FastAPI.

```powershell
# Ejecutar pruebas unitarias aisladas con reporte de cobertura
uv run pytest tests/unit -v --cov=src --cov=api --cov-report=term-missing

# Ejecutar pruebas de integración contra el modelo real en CPU
uv run pytest tests/integration -v

# Verificar estilo de código PEP 8 (lint y formato) con Ruff
uv run ruff check .
uv run ruff format --check .
```

---

## ⚠️ 10. Limitaciones del Modelo

1. **Fotografías en condiciones de laboratorio:** El modelo fue entrenado con el dataset *PlantVillage*, cuyas imágenes muestran una única hoja separada de la planta sobre un fondo neutro y uniforme. Su precisión puede disminuir significativamente ante fotografías tomadas en campo abierto con múltiples hojas superpuestas, tierra, sombras complejas o fondos ruidosos.
2. **Conjunto cerrado de 38 clases:** Al tratarse de un clasificador multiclase estándar con salida *Softmax*, el modelo siempre asignará probabilidades dentro de sus 38 categorías conocidas, incluso si el usuario sube la imagen de una especie vegetal no incluida en los 14 cultivos soportados o un objeto ajeno a una hoja.
3. **Alcance no diagnóstico:** Ciertos síntomas visuales (clorosis, necrosis marginal, manchas foliares) pueden deberse a deficiencias nutricionales, estrés hídrico o fitotoxicidad química y no necesariamente a un agente patógeno infeccioso. Toda decisión de manejo agronómico debe ser validada por un ingeniero agrónomo.

---

## 📜 11. Licencia y Atribución

- **Código fuente de la aplicación:** El código original del Grupo 2 (`src/`, `api/`, frontend y `tests/`) se distribuye bajo licencia **MIT**. Consulte [`LICENSE`](LICENSE).
- **Pesos del modelo (`rodynaemad/plant-disease-dinov2-small`, `model.safetensors`):** Creado por **Rodayna Emad Mohamed** (*College of Computer Science and AI, Pharos University in Alexandria*), distribuido bajo **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.
- **Backbone (`facebook/dinov2-small`):** Desarrollado por Meta AI Research, distribuido bajo licencia **Apache 2.0**.
- **Dataset de entrenamiento (*PlantVillage*):** Publicado por Hughes & Salathé (2015) y Mohanty, Hughes & Salathé (2016). La distribución `mohanty/PlantVillage` en Hugging Face declara licencia **CC BY-SA 3.0**; esa licencia aplica al conjunto de datos y no se sustituye por la licencia de los pesos ajustados.
- **Pesos ajustados del modelo:** La Model Card de `rodynaemad/plant-disease-dinov2-small` declara **CC BY-SA 4.0**. Esta licencia aplica exclusivamente a los pesos distribuidos por la autora y no relicencia el dataset de origen.
- **Alcance de la licencia MIT:** La licencia MIT se limita al código fuente original del Grupo 2 y no se extiende a los pesos, la arquitectura base ni los datos de terceros, que conservan sus licencias y atribuciones obligatorias.

---

## 🤝 12. Gobernanza, Equipo y Trazabilidad

| Integrante | Rol Principal | Historias Asignadas |
| :--- | :--- | :--- |
| **Santiago Correa Campaña** (`@vivacius`) | DevOps, Calidad y Pruebas | HU-01 (#4), HU-07 (#10) |
| **José Isaac Silva Calderón** (`@josesilvacalderon111`) | Ingestión, Preprocesamiento y Empaquetado | HU-02 (#5), HU-08 (#11) |
| **Jhonatan Andrés Tapia Córdoba** (`@JhonatanTC99`) | ML/Backend, API FastAPI y Code Reviewer | HU-03 (#6), HU-05 (#8) |
| **John Restrepo Aparicio** (`@JohnRestrepo-coder`) | Postprocesamiento, Taxonomía y Frontend | HU-04 (#7), HU-06 (#9) |

- **Gobernanza y Reglas de Agentes:** [`AGENTS.md`](AGENTS.md)
- **Guía de Reproducción (Windows + `uv` + Spec Kit):** [`docs/getting-started.md`](docs/getting-started.md)
- **Especificaciones SDD (Spec Kit):** [`specs/001-m3-sdd-setup/`](specs/001-m3-sdd-setup/)
- **Tablero Kanban (GitHub Projects):** [GitHub Projects #1](https://github.com/users/vivacius/projects/1)
- **Tickets de Historias (Issues):** [Issues #4 a #11](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues)

