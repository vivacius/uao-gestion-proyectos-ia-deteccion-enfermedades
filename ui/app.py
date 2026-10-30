"""Interfaz gráfica web en Streamlit para identificación de enfermedades en plantas."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.config import AGRONOMIC_DISCLAIMER, API_BASE_URL, MAX_IMAGE_SIZE_MB
from ui.api_client import fetch_api_health, request_image_prediction


def configure_page() -> None:
    """Configura los metadatos principales y estilos visuales de la página."""
    st.set_page_config(
        page_title="Sistema IA de Diagnóstico Fitosanitario en Hojas",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .main-header {
            background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
            color: #ffffff;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.25rem;
        }
        .main-header h1 {
            color: #ffffff !important;
            margin-bottom: 0.35rem;
            font-size: 2rem;
        }
        .main-header p {
            color: #d8f3dc;
            margin-bottom: 0;
            font-size: 1.05rem;
        }
        .status-card-healthy {
            background-color: #d8f3dc;
            border-left: 6px solid #2d6a4f;
            color: #1b4332;
            padding: 1rem 1.25rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .status-card-diseased {
            background-color: #ffe5d9;
            border-left: 6px solid #d90429;
            color: #6a040f;
            padding: 1rem 1.25rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    """Renderiza la barra lateral con el estado de la API e instrucciones de uso."""
    with st.sidebar:
        st.header("⚙️ Estado del Servicio")
        api_url = st.text_input(
            "URL del servidor FastAPI",
            value=API_BASE_URL,
            help="Dirección donde se ejecuta el servicio REST de inferencia.",
        )

        health = fetch_api_health(base_url=api_url)
        if health.success and health.data:
            st.success("API en línea y modelo disponible")
            st.caption(
                f"**Modelo:** `{health.data.get('model_name')}`\n\n"
                f"**Arquitectura:** `{health.data.get('architecture')}`\n\n"
                f"**Dispositivo:** `{str(health.data.get('device', 'cpu')).upper()}`\n\n"
                f"**Categorías soportadas:** `{health.data.get('num_classes', 38)}`"
            )
        else:
            st.error("Servicio de inferencia no disponible")
            if health.error_message:
                st.caption(health.error_message)

        st.divider()
        st.subheader("📋 Instrucciones de uso")
        st.markdown(
            "1. **Suba una fotografía** clara de una hoja individual en formato **JPG, JPEG o PNG**.\n"
            "2. **Verifique la vista previa** de la imagen cargada.\n"
            "3. Presione el botón **«Analizar fotografía»**.\n"
            "4. Revise la **planta identificada**, la **condición fitosanitaria**, el **nivel de confianza** "
            "y el gráfico con las **3 predicciones más probables**."
        )

        st.divider()
        st.subheader("🌱 Cultivos soportados (14)")
        st.caption(
            "Manzano, Arándano, Cerezo, Maíz, Vid (Uva), Naranjo, Duraznero, "
            "Pimiento morrón, Papa, Frambueso, Soja, Calabaza, Fresa y Tomate."
        )

    return api_url


def render_prediction_results(data: dict) -> None:
    """Muestra en pantalla el resultado detallado de la clasificación devuelta por FastAPI."""
    plant_name = data.get("plant", "No disponible")
    plant_en = data.get("plant_en", "")
    condition_name = data.get("disease_or_condition", "No disponible")
    condition_en = data.get("disease_or_condition_en", "")
    predicted_category = data.get("predicted_category", "")
    is_healthy = data.get("is_healthy")
    health_status = data.get("health_status", "No determinado")
    confidence_pct = float(data.get("confidence_percentage", 0.0))
    confidence_ratio = min(max(float(data.get("confidence", 0.0)), 0.0), 1.0)
    inference_time_ms = float(data.get("inference_time_ms", 0.0))
    top_predictions = data.get("top_predictions", [])
    disclaimer = data.get("disclaimer", AGRONOMIC_DISCLAIMER)

    st.subheader("🔬 Resultado de la Clasificación")

    if is_healthy is True:
        st.markdown(
            f"""
            <div class="status-card-healthy">
                <strong>✅ Estado fitosanitario estimado: HOJA SANA ({health_status})</strong><br>
                La hoja analizada coincide con una categoría saludable dentro del catálogo del modelo.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif is_healthy is False:
        st.markdown(
            f"""
            <div class="status-card-diseased">
                <strong>⚠️ Estado estimado: POSIBLE ENFERMEDAD O PLAGA ({health_status})</strong><br>
                Se detectaron patrones visuales compatibles con una afección foliar.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info(f"Estado fitosanitario: **{health_status}**")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="🌱 Planta identificada", value=plant_name, delta=plant_en or None, delta_color="off")
    with col_m2:
        st.metric(label="🎯 Confianza del modelo", value=f"{confidence_pct:.2f} %")
    with col_m3:
        st.metric(label="⏱️ Tiempo de inferencia", value=f"{inference_time_ms:.2f} ms")

    st.markdown(f"**🦠 Enfermedad o condición detectada:** {condition_name} *({condition_en})*")
    st.caption(f"Etiqueta técnica del modelo: `{predicted_category}`")

    st.markdown("**Nivel de confianza de la predicción principal:**")
    st.progress(confidence_ratio, text=f"{confidence_pct:.2f}% de probabilidad estimada")

    st.divider()
    st.subheader("📊 Tres categorías más probables (Top-3)")

    if top_predictions:
        chart_rows = []
        table_rows = []
        for item in top_predictions:
            label_display = f"#{item['rank']} {item['plant']} — {item['disease_or_condition']}"
            pct = float(item["confidence_percentage"])
            chart_rows.append(
                {
                    "Categoría": label_display,
                    "Confianza (%)": pct,
                }
            )
            table_rows.append(
                {
                    "Posición": f"#{item['rank']}",
                    "Planta": item["plant"],
                    "Enfermedad / Condición": item["disease_or_condition"],
                    "Estado": item["health_status"],
                    "Etiqueta del modelo": item["predicted_category"],
                    "Confianza (%)": f"{pct:.2f} %",
                }
            )

        df_chart = pd.DataFrame(chart_rows).set_index("Categoría")
        st.bar_chart(df_chart, horizontal=True, color="#2d6a4f")

        st.dataframe(
            pd.DataFrame(table_rows),
            use_container_width=True,
            hide_index=True,
        )

    st.warning(f"📌 **Aviso importante:** {disclaimer}")


def main() -> None:
    """Función principal de ejecución de la interfaz Streamlit."""
    configure_page()

    st.markdown(
        """
        <div class="main-header">
            <h1>🌿 Identificador de Enfermedades en Plantas con IA</h1>
            <p>
                Clasificación automatizada de hojas mediante visión por computador basada en el modelo
                <strong>DINOv2-small</strong> preentrenado sobre 38 categorías fitosanitarias.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("ℹ️ ¿Cómo funciona este sistema?", expanded=False):
        st.markdown(
            "Esta aplicación permite identificar posibles enfermedades vegetales a partir de la fotografía "
            "de una hoja. Al enviar una imagen, la interfaz web se comunica con un servicio "
            "**API REST (FastAPI)** que preprocesa la fotografía siguiendo la configuración oficial del "
            "modelo `rodynaemad/plant-disease-dinov2-small` y ejecuta la inferencia en **CPU** "
            "mediante **PyTorch**.\n\n"
            f"- **Formatos admitidos:** JPG, JPEG y PNG (tamaño máximo: {MAX_IMAGE_SIZE_MB} MB).\n"
            "- **Resultados entregados:** Planta identificada, enfermedad o condición probable, "
            "indicador de hoja sana o enferma, porcentaje de confianza, gráfico comparativo de las "
            "3 categorías más probables y tiempo empleado en la inferencia."
        )

    api_url = render_sidebar()

    col_left, col_right = st.columns([1, 1.35], gap="large")

    with col_left:
        st.subheader("📤 1. Cargar fotografía de la hoja")
        uploaded_file = st.file_uploader(
            "Seleccione una imagen en formato JPG, JPEG o PNG",
            type=["jpg", "jpeg", "png"],
            help=f"Suba una fotografía nítida de una hoja individual (máximo {MAX_IMAGE_SIZE_MB} MB).",
        )

        if uploaded_file is not None:
            image_bytes = uploaded_file.getvalue()
            st.markdown("**Vista previa de la fotografía cargada:**")
            st.image(
                image_bytes,
                caption=f"Archivo: {uploaded_file.name} ({len(image_bytes) / 1024:.1f} KB)",
                use_container_width=True,
            )

            analyze_clicked = st.button(
                "🔍 Analizar fotografía",
                type="primary",
                use_container_width=True,
            )
        else:
            image_bytes = b""
            analyze_clicked = False
            st.info(
                "Por favor, cargue una imagen en formato JPG, JPEG o PNG para visualizar "
                "su vista previa y habilitar el análisis."
            )

    with col_right:
        if uploaded_file is not None and analyze_clicked:
            with st.spinner("Analizando la hoja en el servidor de inferencia (CPU)..."):
                response = request_image_prediction(
                    image_bytes=image_bytes,
                    filename=uploaded_file.name,
                    content_type=uploaded_file.type or "image/jpeg",
                    base_url=api_url,
                )

            if response.success and response.data is not None:
                st.session_state["last_prediction"] = response.data
                st.session_state["last_filename"] = uploaded_file.name
                st.session_state["last_error"] = None
            else:
                st.session_state["last_prediction"] = None
                st.session_state["last_error"] = response.error_message

        if uploaded_file is None:
            st.subheader("📊 2. Panel de Resultados")
            st.caption(
                "Aquí se mostrarán el diagnóstico orientativo, el porcentaje de confianza y "
                "las 3 categorías más probables una vez que seleccione y analice una imagen."
            )
            st.info(f"💡 **Nota agronómica:** {AGRONOMIC_DISCLAIMER}")
        elif st.session_state.get("last_error"):
            st.subheader("❌ Error al procesar la solicitud")
            st.error(st.session_state["last_error"])
        elif (
            st.session_state.get("last_prediction") is not None
            and st.session_state.get("last_filename") == uploaded_file.name
        ):
            render_prediction_results(st.session_state["last_prediction"])
        else:
            st.subheader("📊 2. Panel de Resultados")
            st.info(
                "Fotografía lista para ser clasificada. Presione el botón **«Analizar fotografía»** "
                "para obtener la predicción del modelo."
            )


if __name__ == "__main__":
    main()
