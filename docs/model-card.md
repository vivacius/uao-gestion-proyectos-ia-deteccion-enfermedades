# Model Card: Clasificador Fitosanitario DINOv2-small para Detección de Enfermedades en Plantas

**Universidad:** Universidad Autónoma de Occidente (UAO)  
**Programa:** Maestría en Inteligencia Artificial y Ciencia de Datos  
**Asignatura:** Gestión de Proyectos en IA y Ciencia de Datos (Periodo 2026-2)  
**Grupo:** 2  
**Autor de la Model Card:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Fecha de Publicación:** 13 de noviembre de 2026  
**Versión del Artefacto:** 1.0.0 (Módulo 3)  
**Estándar de Documentación:** Estructura canónica de *Model Cards for Model Reporting* (Mitchell et al., 2019)  
**Especificación Trazable:** [`specs/009-m3-model-card/spec.md`](../specs/009-m3-model-card/spec.md) · **Issue:** [#29](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/29)

---

## 1. Detalles del Modelo (Model Details)

### 1.1. Información General y Ficha Técnica (AC-MC-01)
El modelo clasificador fitosanitario es una red neuronal de visión computacional basada en arquitectura *Vision Transformer* (ViT) adaptada para la tarea de clasificación multiclase de patologías foliares y estados de salud vegetal sobre imágenes de hojas individuales.

| Parámetro / Atributo | Especificación Técnica |
| :--- | :--- |
| **Identificador del Modelo Adaptado** | `rodynaemad/plant-disease-dinov2-small` |
| **Arquitectura de Red** | `Dinov2ForImageClassification` (`facebook/dinov2-small` como *backbone* auto-supervisado) |
| **Desarrollador / Adaptador** | Rodayna Emad Mohamed (Pharos University in Alexandria) |
| **Formato de Serialización** | `SafeTensors` (`model.safetensors`, integridad criptográfica verificada sin ejecución arbitraria de código) |
| **Tamaño en Disco del Artefacto** | ~`88 MB` (gestionado mediante Git LFS) |
| **Tipo de Inferencia** | Inferencia local determinista ejecutada **100% en CPU** (sin aceleración CUDA ni dependencias GPU) |
| **Frameworks de Ejecución** | PyTorch 2.5+, Hugging Face Transformers 4.46+, FastAPI 0.115+, Python 3.13 con gestor `uv` |
| **Patrón Arquitectónico** | *Model-as-a-Service* (MaaS) desacoplado mediante API REST asíncrona |

### 1.2. Contrato Tensorial de Entrada y Preprocesamiento
El núcleo de inferencia implementa una tubería de preprocesamiento estricta basada en la especificación oficial de `BitImageProcessor` (`preprocessor_config.json`):

1. **Lectura y Decodificación:** Admite archivos binarios de imágenes en formatos estándar `JPEG`, `JPG` y `PNG`.
2. **Normalización del Espacio de Color:** Conversión obligatoria a espacio tricromático `RGB` (descartando canales alfa en PNGs transparentes o duplicando canales en imágenes en escala de grises).
3. **Remuestreo Espacial:** Escalado bidimensional a resolución $224 \times 224\text{ píxeles}$ mediante interpolación bicúbica (`resample=PIL.Image.Resampling.BICUBIC`).
4. **Contrato Tensorial:** Tensor flotante de forma exacta $[1, 3, 224, 224]$ (`dtype=torch.float32`), con normalización basada en estadísticas globales de ImageNet:
   $$\mu = [0.485, 0.456, 0.406], \quad \sigma = [0.229, 0.224, 0.225]$$

### 1.3. Catálogo Taxonómico de Salida (38 Categorías)
El cabezal de clasificación proyecta logits sobre un espacio discreto de **38 clases botánicas** distribuidas a lo largo de **14 especies de cultivo agrícola** (catalogadas y traducidas en `src/labels.py`):

* **14 Cultivos Soportados:** Manzano (*Apple*), Arándano (*Blueberry*), Cerezo (*Cherry*), Maíz (*Corn*), Vid/Uva (*Grape*), Naranjo/Cítrico (*Orange*), Duraznero (*Peach*), Pimiento morrón (*Pepper, bell*), Papa (*Potato*), Frambueso (*Raspberry*), Soja (*Soybean*), Calabaza/Zapallo (*Squash*), Fresa (*Strawberry*) y Tomate (*Tomato*).
* **Distribución de Condiciones:**
  * **12 Estados Saludables:** Hojas asintomáticas sin evidencia visible de infección o infestación.
  * **26 Estados Patológicos:** Infecciones fúngicas (ej. roya, oídio, sarna, tizón tardío por *Phytophthora infestans*, tizón temprano por *Alternaria*), bacterianas (ej. mancha bacteriana por *Xanthomonas*), virales (ej. virus del mosaico, virus del rizado amarillo del tomate) y plagas foliares (ej. ácaro de dos manchas / arañuela roja).

---

## 2. Uso Previsto y Alcance (Intended Use) (AC-MC-02)

### 2.1. Propósito Primario y Ámbito de Aplicación
El sistema está diseñado **exclusivamente como una herramienta de apoyo preliminar y cribado fitosanitario rápido en campo**. Su objetivo es proporcionar a técnicos agrícolas, extensionistas rurales, pequeños y medianos productores y estudiantes de agronomía una primera aproximación visual que oriente la inspección presencial y priorice la atención técnica de lotes de cultivo.

### 2.2. Usuarios Objetivo
* **Técnicos agrícolas y extensionistas:** Para filtrado rápido de síntomas en recorridos agronómicos de rutina.
* **Pequeños y medianos agricultores:** Como mecanismo de orientación temprana para consultar oportunamente al especialista.
* **Comunidad académica y formativa:** En entornos universitarios y de laboratorio docente como demostrador de modelos de visión artificial aplicados al sector agropecuario.

### 2.3. Casos de Uso No Previstos y Prohibiciones Explícitas (Out-of-Scope & Misuse)

> [!CAUTION]
> **PROHIBICIÓN ESTRICTA DE DIAGNÓSTICO DEFINITIVO Y PRESCRIPCIÓN AUTOMÁTICA:**
> 1. **Prohibición de Diagnóstico Concluyente:** El modelo **NO** es un dispositivo de diagnóstico fitopatológico oficial. Sus predicciones no sustituyen el análisis microbiológico de laboratorio, las pruebas moleculares (PCR/ELISA) ni el dictamen presencial de un Ingeniero Agrónomo o fitopatólogo colegiado.
> 2. **Prohibición de Prescripción Química Automatizada:** Queda **terminantemente prohibido** integrar este modelo en sistemas automatizados de fumigación, dosificación de pesticidas, fungicidas o fertilizantes químicos, o actuadores robóticos que ejecuten tratamientos directos sin validación humana previa. El uso indebido puede provocar fitotoxicidad en el cultivo, inducción de resistencias biológicas, contaminación de cuencas hídricas o severas pérdidas económicas.
> 3. **Prohibición en Decisiones Destructivas:** No debe usarse para ordenar la erradicación masiva, quema o arranque de cultivos sin verificación pericial independiente.
> 4. **Prohibición en Regímenes Fuera de Dominio:** No está previsto para su uso en especies vegetales no contempladas en las 14 clases oficiales, patologías de tallo, raíz o fruto, ni en seres humanos o animales.

---

## 3. Factores de Evaluación (Evaluation Factors)

El comportamiento y la confiabilidad del modelo están condicionados por factores físicos, botánicos y ambientales que deben considerarse en la captura fotográfica:

1. **Iluminación Ambiental:** Variaciones extremas de luz solar directa (reflejos especulares en la cutícula foliar) o sombras pronunciadas distorsionan la textura y el color de las manchas cloróticas o necróticas.
2. **Encuadre y Geometría de Captura:** El modelo asume una **única hoja desplegada y centrada** en el encuadre. Ángulos oblicuos severos, enrollamiento foliar o tomas lejanas de la planta completa degradan sustancialmente la discriminación de características.
3. **Complejidad del Fondo:** La presencia de malezas, suelo desnudo irregular, manos del operario u hojas adyacentes en el fondo introduce ruido visual capaz de activar activaciones espurias en el mecanismo de auto-atención del Transformer.
4. **Estado Fenológico del Cultivo:** Síntomas en etapas tempranas de infección (micro-puntuaciones incipientes) pueden confundirse con carencias nutricionales (ej. deficiencia de magnesio o nitrógeno) o estrés abiótico (sequía o daño mecánico).

---

## 4. Métricas Empíricas Reales y Honestidad Científica (Metrics) (AC-MC-03)

### 4.1. Declaración de Honestidad Metodológica (Sin Invención de Datos)

> [!IMPORTANT]
> **POLÍTICA DE RIGOR Y NO INVENCIÓN DE MÉTRICAS DIAGNÓSTICAS:**
> En estricto cumplimiento de la política de integridad académica de la UAO y las directrices del proyecto:
> * Los 3 runs registrados en MLflow Tracking (`Baseline`, `Strict`, `Exploratory`) y los scripts de validación del repositorio se ejecutaron sobre un **banco de prueba de 10 imágenes sintéticas deterministas generadas proceduralmente** (con patrones de degradación de píxeles, manchas simuladas y ruido controlado), diseñadas específicamente para medir latencia, serialización y estabilidad del servicio.
> * Dado que las imágenes sintéticas **carecen de ground truth botánico real (etiquetas verdaderas de laboratorio)**, **NO ES POSIBLE calcular matemáticamente ni se reporta métrica alguna de Accuracy, Balanced Accuracy, Precision, Recall ni Macro F1 agronómico**.
> * Está **expresamente prohibido inventar métricas sintéticas ficticias** que simulen desempeño clínico. Cualquier cifra de precisión que no provenga de un conjunto de test etiquetado real sería científicamente fraudulenta.
> * Las únicas métricas reportadas y garantizadas corresponden al **rendimiento computacional y latencias de inferencia reales medidas empíricamente en el hardware del proyecto**, registradas en `docs/qa-e2e-benchmarks.md` y en la base local de MLflow (`mlflow.db`).

### 4.2. Umbral de Incertidumbre y Descargo Operativo
El sistema incorpora un filtro matemático de incertidumbre basado en la confianza de la clase más probable ($P_{\max}$):
* **Umbral Nominal:** $\tau = 0.60$ (con variantes experimentales evaluadas en MLflow de $\tau = 0.80$ y $\tau = 0.40$).
* **Comportamiento:** Si $P_{\max} < \tau$, el sistema marca la bandera booleana `is_uncertain=True`, activa una advertencia visual destacada en la interfaz y emite el motivo contractual: *"La confianza de la predicción está por debajo del umbral recomendado (0.60). Se recomienda consultar con un agrónomo."*
* **Descargo Obligatorio:** En todas las respuestas de la API (`POST /predict`) se adjunta el descargo institucional: *"Las predicciones son orientativas y no sustituyen el diagnóstico agronómico profesional."*

---

## 5. Datos de Evaluación (Evaluation Data)

1. **Conjunto de Evaluación Local en CPU:** 10 muestras sintéticas deterministas parametrizadas en `scripts/run_mlflow_benchmark.py` y `tests/conftest.py` (formatos JPEG, PNG, dimensiones de 200 a 400 px, modos RGB y escala de grises con simulación de necrosis y manchas).
2. **Propósito de los Datos de Evaluación:** Medición de latencia de cómputo en CPU pura, latencias de transporte de red HTTP, prueba de carga concurrente, serialización de contratos Pydantic v2 y validación de la suite de 176 pruebas unitarias y 6 pruebas integradas con Pytest.

---

## 6. Datos de Entrenamiento (Training Data)

1. **Dataset Fuente:** Dataset público de referencia **PlantVillage** (Hughes & Salathé, 2015; Mohanty, Hughes & Salathé, 2016).
2. **Volumen del Corpus:** Aproximadamente 54,306 fotografías en alta resolución de hojas individuales recortadas.
3. **Distribución:** 38 clases botánicas correspondientes a 14 especies vegetales de interés comercial y alimentario.
4. **Condición de Adquisición:** Imágenes recolectadas y fotografiadas bajo **condiciones experimentales de laboratorio estrictamente controladas**, utilizando fondos neutros uniformes (fondos negros, grises o blancos) e iluminación artificial estandarizada.
5. **Sesgo Crítico del Dataset de Entrenamiento:** Las hojas del dataset PlantVillage fueron fotografiadas desprendidas de la planta sobre mesas de trabajo, lo que induce un sesgo de fondo significativo frente a imágenes tomadas directamente en parcelas agrícolas con follaje vivo, ramas, insectos y suelo.

---

## 7. Análisis Cuantitativos y Benchmarks en CPU (Quantitative Analyses)

Las siguientes mediciones fueron obtenidas empíricamente en el entorno real de desarrollo del proyecto (`develop`, commit `734fbdf`), documentadas en el reporte oficial [`docs/qa-e2e-benchmarks.md`](./qa-e2e-benchmarks.md):

* **Entorno Medido:** Windows 11, Procesador Intel Core de 12 CPUs lógicas, Python 3.13.18, `uv sync --frozen`, PyTorch 2.5.1 en modo CPU puro.
* **Consumo de Memoria RAM (RSS con modelo cargado):** **`459.64 MB`** (cumpliendo con solvencia la meta contractual $< 1.8\text{ GB}$).

### 7.1. Benchmarks de Latencia y Rendimiento en CPU

Protocolo estandarizado: 3 corridas de calentamiento seguidas de $N=20$ mediciones sobre muestra JPEG ($300 \times 300\text{ px}$):

| Escenario Medido | Muestras ($N$) | Latencia Mínima | Latencia Media | Latencia p50 | **Latencia p95** | Latencia Máxima | Throughput | Meta Contractual | Estado |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Inferencia Pura en CPU (`predict_from_bytes`)** | 20 | 49.33 ms | **66.10 ms** | 66.19 ms | **77.33 ms** | 89.29 ms | 15.13 req/s | $< 300\text{ ms}$ | ✅ Cumplida |
| **HTTP E2E Secuencial (`POST /predict`)** | 20 | 60.64 ms | 70.01 ms | 69.21 ms | **81.39 ms** | 84.95 ms | 14.28 req/s | $\text{p95} < 450\text{ ms}$ | ✅ Cumplida |
| **HTTP E2E Concurrente (`4 workers` en paralelo)** | 20 | 76.42 ms | 264.86 ms | 285.59 ms | **314.60 ms** | 317.25 ms | 14.11 req/s | $\text{p95} < 450\text{ ms}$ | ✅ Cumplida |

### 7.2. Trazabilidad en MLflow Tracking (`SPEC-007`)
Se formalizaron 3 runs reproducibles en el servidor local de MLflow Tracking:
* **Run 1 — `dinov2-baseline`:** Configuración nominal $\tau=0.60$, `top_k=3`. Inferencia CPU determinista registrada con artefactos JSON y CSV.
* **Run 2 — `dinov2-strict`:** Configuración conservadora $\tau=0.80$, diseñada para reducir falsos positivos en entornos de riesgo fitosanitario.
* **Run 3 — `dinov2-exploratory`:** Configuración exploratoria $\tau=0.40$, orientada a maximizar sensibilidad en tamizajes rápidos.
* **Model Registry:** Registro formal del artefacto empaquetado bajo el nombre **`dinov2-plant-disease-classifier` (Versión 1)**.

---

## 8. Consideraciones Éticas, Sesgos y Mitigación (Ethical Considerations)

### 8.1. Análisis Detallado de Factores de Sesgo

```
┌────────────────────────────────────────────────────────────────────────┐
│                      MATRIZ DE SESGOS DEL MODELO                       │
├─────────────────────────┬──────────────────────────────────────────────┤
│ 1. Iluminación          │ Sensibilidad a sobreexposición y sombras.    │
│ 2. Ángulo y Encuadre    │ Diseñado para hoja aislada; falla en racimo. │
│ 3. Síntomas Cruzados    │ Solapamiento visual entre hongos y bacterias.│
│ 4. Brecha Laboratorio   │ Fondo neutro en training vs. maleza en campo.│
└─────────────────────────┴──────────────────────────────────────────────┘
```

1. **Sesgo por Iluminación y Variabilidad Lumínica:** La reflectancia foliar bajo sol cenital puede ocultar lesiones necróticas iniciales o crear falsas clorosis por saturación lumínica.
2. **Sesgo de Ángulo, Encuadre y Oclusión:** El modelo pierde precisión si la hoja está doblada, comida parcialmente por insectos en sus márgenes o tapada por ramas.
3. **Síntomas Visuales Cruzados (Confusión Inter-Clase):** Diversos fitopatógenos producen manifestaciones visuales fenotípicamente convergentes (ej. halo amarillo alrededor de manchas marrones típico tanto de *Septoria* como de *Alternaria*). El modelo no realiza tinción celular ni microscopía, por lo que su capacidad discriminativa se limita a patrones de coloración y textura macroscópica.
4. **Brecha de Dominio Laboratorio vs. Campo (*Out-of-Distribution Shift*):** Es el riesgo más crítico. Al haber sido entrenado con PlantVillage (fondo de mesa de laboratorio), cuando el modelo procesa imágenes de hojas sujetas en la planta con tierra o maleza al fondo, las activaciones de los parches del Vision Transformer pueden dispersarse, reduciendo la confianza efectiva.

### 8.2. Impacto Socioeconómico y Agronómico
* **Riesgo de Falsos Negativos:** Una enfermedad grave (ej. Tizón tardío de la papa) clasificada erróneamente como "Sana" puede demorar la intervención técnica, provocando pérdidas masivas de cosecha para un pequeño agricultor campesino.
* **Riesgo de Falsos Positivos:** Una hoja sana con manchas de lodo o deficiencia mineral clasificada como enfermedad fúngica puede inducir al agricultor a realizar gastos innecesarios en fungicidas tóxicos.
* **Mitigación Operativa:** El umbral de corte $\tau=0.60$ y el despliegue del Top-3 de alternativas con sus respectivas probabilidades garantizan que el operador reciba un abanico de posibilidades y no una falsa certeza absoluta.

---

## 9. Trazabilidad Legal, Licenciamiento y Atribuciones (AC-MC-04)

El proyecto respeta de manera estricta la cadena de derechos de autor y licencias de código abierto, conforme a lo establecido en el archivo oficial [`LICENSE`](../LICENSE):

```
┌───────────────────────────────────────────────────────────────────────┐
│                   CADENA DE LICENCIAMIENTO DEL SISTEMA                │
├───────────────────────────────┬───────────────────┬───────────────────┤
│ Componente                    │ Autor / Origen    │ Licencia Oficial  │
├───────────────────────────────┼───────────────────┼───────────────────┤
│ Código fuente original        │ Grupo 2 (UAO)     │ MIT License       │
│ Pesos adaptados SafeTensors   │ Rodayna Emad M.   │ CC BY-SA 4.0      │
│ Arquitectura DINOv2-small     │ Meta AI Research  │ Apache 2.0        │
│ Dataset de origen PlantVillage│ Hughes & Salathé  │ CC BY-SA 3.0      │
└───────────────────────────────┴───────────────────┴───────────────────┘
```

1. **Código Fuente del Proyecto (`MIT License`):** Cubre todo el código original desarrollado por el equipo (Santiago Correa, José Silva, Jhonatan Tapia y John Restrepo) en `src/`, `api/`, `ui/`, `tests/` y documentación.
2. **Pesos Adaptados (`CC BY-SA 4.0`):** Los pesos `rodynaemad/plant-disease-dinov2-small` (`model.safetensors`) distribuidos por Rodayna Emad Mohamed (Pharos University in Alexandria) conservan la licencia *Creative Commons Attribution-ShareAlike 4.0 International*.
3. **Arquitectura Base (`Apache 2.0`):** El modelo fundacional `facebook/dinov2-small` fue creado por Meta AI Research y está licenciado bajo *Apache License, Version 2.0*.
4. **Dataset de Entrenamiento (`CC BY-SA 3.0`):** El corpus `mohanty/PlantVillage` está protegido bajo *Creative Commons Attribution-ShareAlike 3.0 Unported*.
5. **Gobernanza de Datos y Privacidad:** El sistema procesa las imágenes foliares en memoria volátil tipo stream; **no almacena, persiste ni transfiere imágenes ni metadatos personales o de geolocalización** a servidores de terceros, blindando la privacidad del usuario y del predio agrícola.

---

## 10. Advertencias y Recomendaciones Operativas (Caveats & Recommendations)

Para maximizar la utilidad del sistema y minimizar los riesgos de error en campo, se recomienda seguir el siguiente protocolo operativo:

1. **Protocolo de Captura en Campo:**
   * Limpiar suavemente la superficie de la hoja si presenta lodo o polvo excesivo.
   * Colocar la hoja sobre una superficie de color liso o neutro (o interponer la mano limpia con guante neutro si está adherida a la planta) para evitar fondos con follaje desordenado.
   * Evitar el uso de flash directo; preferir sombra suave natural en días soleados.
   * Asegurar que el área afectada ocupe al menos el 50% del encuadre de la fotografía.
2. **Interpretación del Top-3:**
   * No considerar únicamente la primera predicción si la confianza es intermedia ($0.60 \le P < 0.85$). El ranking Top-3 proporciona diagnósticos diferenciales valiosos para el especialista agronómico.
3. **Actuación ante Incertidumbre:**
   * Cuando la aplicación indique `is_uncertain=True` ($P < 0.60$), **descartar la predicción automática** y remitir inmediatamente una muestra física del tejido vegetal al laboratorio fitopatológico de referencia regional.

---

*Documento técnico auditado para el cierre y sustentación del Módulo 3 — Grupo 2 UAO.*
