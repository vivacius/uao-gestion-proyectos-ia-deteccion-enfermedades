"""Catálogo de las 38 etiquetas de PlantVillage y utilidades de traducción/formateo."""

from __future__ import annotations

from dataclasses import dataclass

# Traducción de los 14 cultivos del dataset PlantVillage al español
PLANT_TRANSLATIONS_ES: dict[str, str] = {
    "Apple": "Manzano",
    "Blueberry": "Arándano",
    "Cherry (including sour)": "Cerezo (incluyendo guindo)",
    "Cherry_(including_sour)": "Cerezo (incluyendo guindo)",
    "Corn (maize)": "Maíz",
    "Corn_(maize)": "Maíz",
    "Grape": "Vid (Uva)",
    "Orange": "Naranjo (Cítrico)",
    "Peach": "Duraznero (Melocotonero)",
    "Pepper, bell": "Pimiento morrón",
    "Pepper,_bell": "Pimiento morrón",
    "Potato": "Papa (Patata)",
    "Raspberry": "Frambueso",
    "Soybean": "Soja (Soya)",
    "Squash": "Calabaza (Zapallo)",
    "Strawberry": "Fresa (Frutilla)",
    "Tomato": "Tomate",
}

# Traducción de las enfermedades y condiciones de PlantVillage al español
CONDITION_TRANSLATIONS_ES: dict[str, str] = {
    "healthy": "Sana (sin enfermedad aparente)",
    "Apple_scab": "Sarna del manzano (Venturia inaequalis)",
    "Apple scab": "Sarna del manzano (Venturia inaequalis)",
    "Black_rot": "Podredumbre negra",
    "Black rot": "Podredumbre negra",
    "Cedar_apple_rust": "Roya del manzano y el cedro",
    "Cedar apple rust": "Roya del manzano y el cedro",
    "Powdery_mildew": "Oídio (Cenicilla polvorienta)",
    "Powdery mildew": "Oídio (Cenicilla polvorienta)",
    "Cercospora_leaf_spot Gray_leaf_spot": "Mancha gris de la hoja (Cercospora)",
    "Cercospora leaf spot Gray leaf spot": "Mancha gris de la hoja (Cercospora)",
    "Common_rust_": "Roya común del maíz",
    "Common_rust": "Roya común del maíz",
    "Common rust": "Roya común del maíz",
    "Northern_Leaf_Blight": "Tizón norteño de la hoja del maíz",
    "Northern Leaf Blight": "Tizón norteño de la hoja del maíz",
    "Esca_(Black_Measles)": "Yesca de la vid (Sarampión negro / Esca)",
    "Esca (Black Measles)": "Yesca de la vid (Sarampión negro / Esca)",
    "Leaf_blight_(Isariopsis_Leaf_Spot)": "Tizón de la hoja (Mancha foliar por Isariopsis)",
    "Leaf blight (Isariopsis Leaf Spot)": "Tizón de la hoja (Mancha foliar por Isariopsis)",
    "Haunglongbing_(Citrus_greening)": "Huanglongbing (HLB / Enverdecimiento de los cítricos)",
    "Haunglongbing (Citrus greening)": "Huanglongbing (HLB / Enverdecimiento de los cítricos)",
    "Bacterial_spot": "Mancha bacteriana",
    "Bacterial spot": "Mancha bacteriana",
    "Early_blight": "Tizón temprano (Alternaria)",
    "Early blight": "Tizón temprano (Alternaria)",
    "Late_blight": "Tizón tardío (Phytophthora infestans)",
    "Late blight": "Tizón tardío (Phytophthora infestans)",
    "Leaf_scorch": "Quemadura foliar de la fresa",
    "Leaf scorch": "Quemadura foliar de la fresa",
    "Leaf_Mold": "Moho de la hoja del tomate (Passalora fulva)",
    "Leaf Mold": "Moho de la hoja del tomate (Passalora fulva)",
    "Septoria_leaf_spot": "Mancha foliar por Septoria",
    "Septoria leaf spot": "Mancha foliar por Septoria",
    "Spider_mites Two-spotted_spider_mite": "Ácaro de dos manchas (Arañuela roja)",
    "Spider mites Two-spotted spider mite": "Ácaro de dos manchas (Arañuela roja)",
    "Target_Spot": "Mancha anillada (Corynespora cassiicola)",
    "Target Spot": "Mancha anillada (Corynespora cassiicola)",
    "Tomato_Yellow_Leaf_Curl_Virus": "Virus del rizado amarillo de la hoja del tomate (TYLCV)",
    "Tomato Yellow Leaf Curl Virus": "Virus del rizado amarillo de la hoja del tomate (TYLCV)",
    "Tomato_mosaic_virus": "Virus del mosaico del tomate (ToMV)",
    "Tomato mosaic virus": "Virus del mosaico del tomate (ToMV)",
}


@dataclass(frozen=True)
class CategoryMetadata:
    """Información estructurada de una categoría del modelo."""

    raw_label: str
    plant_en: str
    plant_es: str
    condition_en: str
    condition_es: str
    is_healthy: bool | None
    health_status: str


def clean_identifier(text: str) -> str:
    """Limpia guiones bajos repetidos y espacios sobrantes."""
    cleaned = text.replace("_", " ").strip()
    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")
    return cleaned


def parse_category_label(raw_label: str) -> CategoryMetadata:
    """Descompone una etiqueta del modelo (ej. ``Tomato___Late_blight``) en sus metadatos.

    Soporta tanto el separador estándar ``___`` de PlantVillage como etiquetas genéricas.
    """
    if not raw_label or not raw_label.strip():
        return CategoryMetadata(
            raw_label="",
            plant_en="Unknown",
            plant_es="Desconocida",
            condition_en="Unknown",
            condition_es="Desconocida",
            is_healthy=None,
            health_status="No determinado",
        )

    label = raw_label.strip()
    if "___" in label:
        raw_plant, raw_condition = label.split("___", maxsplit=1)
    else:
        raw_plant = label
        raw_condition = "unknown"

    plant_en = clean_identifier(raw_plant)
    condition_en = clean_identifier(raw_condition)

    plant_es = (
        PLANT_TRANSLATIONS_ES.get(raw_plant)
        or PLANT_TRANSLATIONS_ES.get(plant_en)
        or plant_en
    )

    if raw_condition == "unknown":
        condition_es = "Condición no especificada"
        is_healthy: bool | None = None
        health_status = "No determinado"
    else:
        condition_es = (
            CONDITION_TRANSLATIONS_ES.get(raw_condition)
            or CONDITION_TRANSLATIONS_ES.get(condition_en)
            or condition_en
        )
        is_healthy = condition_en.lower() == "healthy"
        health_status = "Sana" if is_healthy else "Enferma"

    return CategoryMetadata(
        raw_label=label,
        plant_en=plant_en,
        plant_es=plant_es,
        condition_en="Healthy" if condition_en.lower() == "healthy" else condition_en,
        condition_es=condition_es,
        is_healthy=is_healthy,
        health_status=health_status,
    )
