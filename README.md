---
license: cc-by-sa-4.0
library_name: transformers
pipeline_tag: image-classification
base_model: facebook/dinov2-small
datasets:
- mohanty/PlantVillage
tags:
- agriculture
- plant-disease
- computer-vision
- dinov2
- image-classification
metrics:
- accuracy
- f1
model-index:
- name: plant-disease-dinov2-small
  results:
  - task:
      type: image-classification
      name: Plant disease classification (38 classes)
    dataset:
      name: PlantVillage (colour), leaf-level held-out split
      type: mohanty/PlantVillage
    metrics:
    - type: accuracy
      value: 0.9886
      name: Accuracy (unseen leaves)
    - type: f1
      value: 0.9849
      name: Macro F1 (unseen leaves)
---

# Plant Disease Classifier (DINOv2-small + linear head)

Identifies **38 crop–condition classes** (26 diseases and 12 healthy classes across 14 crops)
from a photo of a single leaf. Built as the open disease-scanning model for
[BloomTech](https://github.com/itsRou/bloomtech-smart-agriculture), my AI + IoT smart-agriculture
graduation project.

**Try it:** [Plant Disease Scanner Space](https://huggingface.co/spaces/rodynaemad/plant-disease-scanner)

| Metric (held-out test set, 10,862 photos) | Value |
|---|---|
| Accuracy on **leaves never seen in training** | **98.9%** |
| Macro F1 on leaves never seen in training | **98.5%** |
| Accuracy with a naive photo-level random split (for comparison) | 99.1% |

## Why "leaves never seen in training" matters

PlantVillage contains several photos of the **same physical leaf**. If photos are split
randomly, near-duplicates of a test leaf end up in training, which inflates test accuracy.
The dataset authors' `leaf-map.json` links 40,490 photos to 7,524 physical leaves. I split the
data so that **every photo of a given leaf lands on only one side** (stratified, leaf-grouped
80/20 split), and asserted that no leaf crosses the split. For this model the inflation from a
naive split is small (99.1% vs 98.9%), but the leaf-level number is the one to trust. The
remaining 13,815 photos have no leaf mapping and are split photo by photo.

## Usage

```python
from transformers import pipeline

classifier = pipeline("image-classification", model="rodynaemad/plant-disease-dinov2-small")
print(classifier("leaf.jpg", top_k=3))
# [{'label': 'Tomato___Late_blight', 'score': 0.999}, ...]
```

### In the browser (ONNX)

`onnx/model_with_features.onnx` (88 MB, fp32) and `onnx/model_with_features_quantized.onnx`
(24 MB, int8) take `pixel_values` (1×3×224×224, ImageNet-normalized) and return `logits` and
the 768-d `features` used for the out-of-distribution check. The fp32 export matches PyTorch
exactly. The int8 copy, which powers the [Space](https://huggingface.co/spaces/rodynaemad/plant-disease-scanner),
scores **98.7% accuracy (98.1% macro F1)** on the full leaf-level test set. Example with
[onnxruntime-web](https://onnxruntime.ai/docs/tutorials/web/) in the Space's `index.html`.

## How it was trained

- **Backbone:** [`facebook/dinov2-small`](https://huggingface.co/facebook/dinov2-small),
  frozen. Features are the concatenation of the CLS token and the mean patch token (768
  dimensions), exactly what `Dinov2ForImageClassification` feeds its classifier.
- **Head:** multinomial logistic regression on standardized features, with the standardization
  folded into the final linear layer. The regularization strength (C = 0.1) was chosen on a
  leaf-grouped validation split carved out of the training set; validation accuracy was 98.4–98.6%
  across C ∈ {0.1, 0.3, 1, 3}.
- **Data:** all 54,305 colour images of [PlantVillage](https://huggingface.co/datasets/mohanty/PlantVillage)
  (43,443 train / 10,862 test).
- **Check:** the exported Transformers model reproduces the trained classifier's predictions on
  100% of 200 sampled test images.

## Per-class F1 on unseen leaves

27 of 38 classes reach F1 ≥ 0.99. Weakest classes first:

| Crop | Condition | F1 |
|---|---|---|
| Corn (maize) | Cercospora leaf spot Gray leaf spot | 0.900 |
| Potato | healthy | 0.915 |
| Tomato | Early blight | 0.924 |
| Corn (maize) | Northern Leaf Blight | 0.949 |
| Tomato | Target Spot | 0.958 |
| Tomato | Late blight | 0.966 |
| Tomato | Bacterial spot | 0.967 |
| Tomato | Spider mites Two-spotted spider mite | 0.972 |
| Potato | Late blight | 0.972 |
| Tomato | Leaf Mold | 0.974 |
| Tomato | Septoria leaf spot | 0.984 |
| Tomato | healthy | 0.991 |
| Tomato | Tomato Yellow Leaf Curl Virus | 0.991 |
| Apple | Apple scab | 0.992 |
| Grape | Black rot | 0.994 |
| Grape | Esca (Black Measles) | 0.995 |
| Corn (maize) | Common rust | 0.996 |
| Pepper, bell | Bacterial spot | 0.997 |
| Potato | Early blight | 0.998 |
| Strawberry | Leaf scorch | 0.998 |
| Corn (maize) | healthy | 0.998 |
| Squash | Powdery mildew | 0.999 |
| Peach | Bacterial spot | 0.999 |
| Soybean | healthy | 1.000 |
| Apple | Black rot | 1.000 |
| Apple | Cedar apple rust | 1.000 |
| Apple | healthy | 1.000 |
| Blueberry | healthy | 1.000 |
| Cherry (including sour) | Powdery mildew | 1.000 |
| Cherry (including sour) | healthy | 1.000 |
| Grape | Leaf blight (Isariopsis Leaf Spot) | 1.000 |
| Grape | healthy | 1.000 |
| Orange | Haunglongbing (Citrus greening) | 1.000 |
| Peach | healthy | 1.000 |
| Pepper, bell | healthy | 1.000 |
| Raspberry | healthy | 1.000 |
| Strawberry | healthy | 1.000 |
| Tomato | Tomato mosaic virus | 1.000 |

The main confusion is between the two corn leaf-blight diseases (gray leaf spot vs. northern
leaf blight), which look alike. Potato healthy has only 152 photos in the whole dataset.

## Limitations

- **Lab photos only.** PlantVillage images show a single detached leaf on a plain background.
  Accuracy on field photos with clutter, multiple leaves, shadows or different cameras will be
  substantially lower. Do not read 98.9% as field performance.
- **Closed set.** The classifier always picks one of its 38 classes, even for images that are
  not leaves. The [Space](https://huggingface.co/spaces/rodynaemad/plant-disease-scanner) adds
  an out-of-distribution check (cosine similarity to per-class training centroids, calibrated so
  99% of real test leaves pass) that rejects solid colours, random noise and photos of people.
- **Not a diagnosis.** Use it as a screening aid and confirm with an agronomist or extension
  service before treating crops.

## License and attribution

Trained on PlantVillage (Hughes & Salathé, 2015; Mohanty, Hughes & Salathé, 2016), released
under CC BY-SA. This model is shared under **CC BY-SA 4.0**; the DINOv2 backbone is Apache 2.0.

## Author

[Rodayna Emad Mohamed](https://huggingface.co/rodynaemad), Research and Teaching Assistant,
College of Computer Science and AI, Pharos University in Alexandria ·
[GitHub](https://github.com/itsRou)

---

# 🌿 Aplicación de IA para Identificación de Enfermedades en Plantas (DINOv2-small)

Aplicación modular de Inteligencia Artificial para la **clasificación automatizada de enfermedades foliares en cultivos agrícolas** a partir de fotografías de hojas. Desarrollada como trabajo académico para la asignatura **Gestión de Proyectos de Inteligencia Artificial (UAO)**, aplicando buenas prácticas de ingeniería de software, arquitectura desacoplada **Model-as-a-Service (MaaS)** con **FastAPI**, interfaz gráfica en **Streamlit**, gestión reproducible de dependencias con **`uv`** y ejecución íntegra en **CPU** mediante **PyTorch** y **Hugging Face Transformers**.

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
│   └── main.py                      # Endpoints GET /health y POST /predict y manejadores de errores
├── ui/                              # Capa de presentación web (Streamlit)
│   ├── api_client.py                # Cliente HTTP desacoplado que consume la API REST (sin duplicar el modelo)
│   └── app.py                       # Interfaz gráfica en español para usuarios finales
├── tests/                           # Suite de pruebas automatizadas con pytest
│   ├── conftest.py                  # Generadores de imágenes sintéticas (JPG, PNG, RGBA, grises, corruptas, GIF)
│   ├── unit/                        # Pruebas unitarias rápidas (etiquetas, preprocesamiento, mocks de API/UI)
│   └── integration/                 # Pruebas de integración contra el modelo DINOv2-small real en CPU
├── Dockerfile                       # Imagen reproducible para CPU basada en Python 3.13 y uv
├── docker-compose.yml               # Orquestación de contenedores (FastAPI + Streamlit)
├── pyproject.toml                   # Definición del proyecto, dependencias y configuración de pytest/uv/ruff
├── uv.lock                          # Archivo de bloqueo exacto de dependencias
├── .gitignore                       # Exclusión de entornos virtuales, cachés y artefactos temporales
└── README.md                        # Documentación académica y ficha técnica del modelo
```

### Flujo de comunicación
1. El usuario carga una fotografía en la interfaz web **Streamlit** (`ui/app.py`).
2. **Streamlit** envía la imagen mediante una petición `POST /predict` (`multipart/form-data`) al backend **FastAPI** (`api/main.py`) usando `ui/api_client.py`, **evitando cargar una segunda copia del modelo en memoria**.
3. **FastAPI** delega en `src/inference.py`, que valida la imagen (`src/preprocessing.py`), aplica las transformaciones exactas de `preprocessor_config.json`, ejecuta el pase hacia adelante (`forward`) sobre **CPU** con `torch.no_grad()` y formatea el Top-3 (`src/postprocessing.py`).
4. La respuesta JSON estructurada regresa a **Streamlit**, donde se presentan indicadores visuales, barras de progreso y un gráfico comparativo de las tres categorías más probables.

---

## 🧠 3. Modelo Base Seleccionado

- **Nombre del modelo:** `rodynaemad/plant-disease-dinov2-small`
- **Enlace oficial en Hugging Face:** [https://huggingface.co/rodynaemad/plant-disease-dinov2-small](https://huggingface.co/rodynaemad/plant-disease-dinov2-small)
- **Autora del modelo preentrenado:** Rodayna Emad Mohamed (*Pharos University in Alexandria*).
- **Arquitectura:** `Dinov2ForImageClassification` basada en el backbone [`facebook/dinov2-small`](https://huggingface.co/facebook/dinov2-small) (congelado, extracción de características de 768 dimensiones combinando el token `CLS` y el promedio de parches) junto con un cabezal de clasificación lineal entrenado sobre las 54,305 imágenes en color del conjunto de datos **PlantVillage**.
- **Nota sobre las métricas reportadas por la autora:** En la documentación oficial del modelo (*Model Card*), la autora reporta una exactitud (*accuracy*) de **98.86%** y un **Macro F1 de 98.49%** sobre una partición de prueba de hojas no vistas durante el entrenamiento (*leaf-level held-out split* de 10,862 imágenes de PlantVillage). **Estas cifras corresponden exclusivamente al entrenamiento y evaluación publicados por la autora original del modelo y no se presentan como métricas de entrenamiento propio de este proyecto**, dado que en este trabajo utilizamos el modelo preentrenado tal como fue distribuido, sin modificar sus pesos (`model.safetensors`).

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
- **Python:** **Python 3.13** (verificado y probado con `CPython 3.13.7`; compatible también con Python 3.12).
- **Gestor de paquetes y entornos:** [`uv`](https://docs.astral.sh/uv/).
- **Librerías principales:** `torch` (compilación CPU), `transformers`, `safetensors`, `pillow`, `fastapi`, `uvicorn`, `streamlit`, `requests`, `pytest`, `ruff`.

---

## 🚀 6. Instalación y Ejecución Local en Windows (con `uv`)

### Paso 1: Ubicarse en el directorio del proyecto
Abra una terminal **PowerShell** en la carpeta raíz del repositorio:
```powershell
cd uao-gestion-proyectos-ia-deteccion-enfermedades
```

### Paso 2: Sincronizar el entorno virtual y dependencias con `uv`
```powershell
uv sync --python 3.13
```
Este comando creará automáticamente el entorno `.venv` e instalará todas las dependencias exactas definidas en `uv.lock` (incluyendo PyTorch para CPU).

### Paso 3: Iniciar la API REST (FastAPI)
En una primera ventana de PowerShell, ejecute:
```powershell
uv run uvicorn api.main:app --host 127.0.0.1 --port 8000
```
La API quedará disponible en `http://127.0.0.1:8000`.

### Paso 4: Iniciar la Interfaz Gráfica (Streamlit)
En una **segunda ventana de PowerShell** (manteniendo la API activa), ejecute:
```powershell
uv run streamlit run ui/app.py --server.port 8501
```
La aplicación web se abrirá en su navegador en `http://localhost:8501`.

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

## 🐳 8. Ejecución con Docker (CPU)

El proyecto incluye un `Dockerfile` optimizado para CPU (usando `python:3.13-slim`, `uv` y `uv.lock`) y un archivo `docker-compose.yml` que levanta de forma coordinada el contenedor de **FastAPI** y el contenedor de **Streamlit**.

### Gestión de los pesos del modelo (`model.safetensors`)
Los pesos del modelo (`model.safetensors`, ~88 MB) están gestionados mediante **Git LFS** (`.gitattributes`) y excluidos de commits accidentales en `.gitignore`. Dentro de Docker se disponibilizan copiando los artefactos locales en `/app/modelo_plantas/` o montándolos como volumen de solo lectura.

### Opción A: Iniciar todo el sistema con Docker Compose
```powershell
docker compose up --build
```
- **API REST (FastAPI):** `http://localhost:8000` (Swagger en `http://localhost:8000/docs`)
- **Interfaz Web (Streamlit):** `http://localhost:8501`

### Opción B: Construir y ejecutar contenedores manualmente
```powershell
# 1. Construir la imagen Docker
docker build -t plant-disease-app:latest .

# 2. Ejecutar la API FastAPI
docker run -d --name plant-disease-api -p 8000:8000 plant-disease-app:latest

# 3. Ejecutar la interfaz Streamlit conectada a la API
docker run -d --name plant-disease-ui -p 8501:8501 `
  -e API_BASE_URL="http://host.docker.internal:8000" `
  plant-disease-app:latest `
  uv run streamlit run ui/app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
```

---

## 🧪 9. Pruebas Automatizadas (`pytest`) y Calidad (`ruff`)

La suite de pruebas está dividida en **pruebas unitarias** (`tests/unit/`, que validan lógica de negocio, etiquetas, preprocesamiento y manejadores de errores con mocks) y **pruebas de integración** (`tests/integration/`, que cargan el modelo DINOv2-small real en CPU y ejecutan inferencias extremo a extremo a través de FastAPI).

```powershell
# Ejecutar toda la suite de pruebas (unitarias + integración)
uv run pytest -v

# Ejecutar únicamente las pruebas unitarias (rápidas, con mocks)
uv run pytest -v -m unit

# Ejecutar únicamente las pruebas de integración con el modelo real en CPU
uv run pytest -v -m integration

# Verificar estilo de código PEP 8 con Ruff
uv run ruff check src/ api/ ui/ tests/
```

---

## ⚠️ 10. Limitaciones del Modelo

1. **Fotografías en condiciones de laboratorio:** El modelo fue entrenado con el dataset *PlantVillage*, cuyas imágenes muestran una única hoja separada de la planta sobre un fondo neutro y uniforme. Su precisión puede disminuir significativamente ante fotografías tomadas en campo abierto con múltiples hojas superpuestas, tierra, sombras complejas o fondos ruidosos.
2. **Conjunto cerrado de 38 clases:** Al tratarse de un clasificador multiclase estándar con salida *Softmax*, el modelo siempre asignará probabilidades dentro de sus 38 categorías conocidas, incluso si el usuario sube la imagen de una especie vegetal no incluida en los 14 cultivos soportados o un objeto ajeno a una hoja.
3. **Alcance no diagnóstico:** Ciertos síntomas visuales (clorosis, necrosis marginal, manchas foliares) pueden deberse a deficiencias nutricionales, estrés hídrico o fitotoxicidad química y no necesariamente a un agente patógeno infeccioso. Toda decisión de manejo agronómico debe ser validada por un ingeniero agrónomo.

---

## 📜 11. Licencia y Atribución

- **Modelo preentrenado (`rodynaemad/plant-disease-dinov2-small`):** Creado por **Rodayna Emad Mohamed** (*College of Computer Science and AI, Pharos University in Alexandria*), distribuido bajo licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.
- **Backbone (`facebook/dinov2-small`):** Desarrollado por Meta AI Research, distribuido bajo licencia **Apache 2.0**.
- **Dataset base (*PlantVillage*):** Publicado por Hughes & Salathé (2015) y Mohanty, Hughes & Salathé (2016) bajo licencia **CC BY-SA**.
- **Código de esta aplicación:** Distribuido con fines académicos bajo licencia **CC BY-SA 4.0**, manteniendo la atribución correspondiente a los autores originales del modelo y del conjunto de datos.

---
