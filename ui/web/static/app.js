/**
 * ============================================================================
 * AgroScan AI — Controlador del Frontend (Vanilla JavaScript)
 * Universidad Autónoma de Occidente · Maestría en IA y Ciencia de Datos
 * ============================================================================
 */

(function () {
  'use strict';

  // --- Configuración y Estado Global ---
  // Prioriza el mismo origen (window.location.origin) para despliegues unificados y uso local,
  // permitiendo sobrescribir dinámicamente el endpoint mediante el panel de configuración (localStorage).
  function getInitialApiUrl() {
    const saved = localStorage.getItem('agroscan_api_url');
    if (saved) return saved;

    return window.location.origin.startsWith('http')
      ? window.location.origin
      : 'http://127.0.0.1:8000';
  }

  const DEFAULT_API_URL = getInitialApiUrl();
  let currentApiUrl = DEFAULT_API_URL;
  let selectedFile = null;

  // --- Elementos del DOM ---
  const elements = {
    // Header & Settings
    apiStatusBadge: document.getElementById('api-status-badge'),
    apiStatusText: document.getElementById('api-status-text'),
    toggleSettingsBtn: document.getElementById('toggle-settings-btn'),
    settingsPanel: document.getElementById('settings-panel'),
    apiUrlInput: document.getElementById('api-url-input'),
    saveApiUrlBtn: document.getElementById('save-api-url-btn'),

    // Carga de Imagen
    dropzone: document.getElementById('dropzone'),
    imageInput: document.getElementById('image-input'),
    dropzonePrompt: document.getElementById('dropzone-prompt'),
    previewContainer: document.getElementById('preview-container'),
    imagePreview: document.getElementById('image-preview'),
    removeImageBtn: document.getElementById('remove-image-btn'),
    predictBtn: document.getElementById('predict-btn'),
    btnText: document.getElementById('btn-text'),
    loadingIndicator: document.getElementById('loading-indicator'),
    loadingMsg: document.getElementById('loading-msg'),

    // Resultados
    emptyState: document.getElementById('empty-state'),
    resultsContent: document.getElementById('results-content'),
    uncertaintyBanner: document.getElementById('uncertainty-banner'),
    uncertaintyText: document.getElementById('uncertainty-text'),
    healthStatusBadge: document.getElementById('health-status-badge'),
    inferenceTimeLabel: document.getElementById('inference-time-label'),
    plantName: document.getElementById('plant-name'),
    diseaseName: document.getElementById('disease-name'),
    confidencePercentage: document.getElementById('confidence-percentage'),
    confidenceBar: document.getElementById('confidence-bar'),
    top3List: document.getElementById('top3-list'),
    disclaimerText: document.getElementById('disclaimer-text'),
    errorBanner: document.getElementById('error-banner'),
    errorTitle: document.getElementById('error-title'),
    errorDesc: document.getElementById('error-desc'),
  };

  // --- Inicialización ---
  function init() {
    elements.apiUrlInput.value = currentApiUrl;
    setupEventListeners();
    checkApiHealth();
  }

  // --- Configuración de Eventos ---
  function setupEventListeners() {
    // Toggle Ajustes
    elements.toggleSettingsBtn.addEventListener('click', () => {
      elements.settingsPanel.classList.toggle('hidden');
    });

    // Guardar / Probar URL API
    elements.saveApiUrlBtn.addEventListener('click', () => {
      let url = elements.apiUrlInput.value.trim();
      if (!url) url = DEFAULT_API_URL;
      // Remover barra final
      url = url.replace(/\/+$/, '');
      currentApiUrl = url;
      localStorage.setItem('agroscan_api_url', url);
      checkApiHealth();
    });

    // Carga mediante input file / cámara
    elements.imageInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelection(e.target.files[0]);
      }
    });

    // Drag & Drop
    ['dragenter', 'dragover'].forEach((eventName) => {
      elements.dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        elements.dropzone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach((eventName) => {
      elements.dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        elements.dropzone.classList.remove('dragover');
      });
    });

    elements.dropzone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      if (dt.files && dt.files[0]) {
        handleFileSelection(dt.files[0]);
      }
    });

    // Botón remover imagen
    elements.removeImageBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      clearSelectedImage();
    });

    // Botón Diagnosticar
    elements.predictBtn.addEventListener('click', () => {
      if (selectedFile) {
        performInference(selectedFile);
      }
    });
  }

  // --- Verificación de Salud de la API (/health) ---
  async function checkApiHealth() {
    updateApiStatus('checking', 'Conectando con API...');
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 4000);

      const response = await fetch(`${currentApiUrl}/health`, {
        method: 'GET',
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (response.ok) {
        const data = await response.json();
        if (data.status === 'ok' && data.model_available) {
          updateApiStatus('online', `API en línea (${data.device.toUpperCase()})`);
        } else {
          updateApiStatus('offline', 'Modelo degradado');
        }
      } else {
        updateApiStatus('offline', `HTTP ${response.status}`);
      }
    } catch (err) {
      updateApiStatus('offline', 'API fuera de línea');
    }
  }

  function updateApiStatus(state, message) {
    elements.apiStatusBadge.className = 'badge';
    elements.apiStatusText.textContent = message;

    if (state === 'online') {
      elements.apiStatusBadge.classList.add('badge-online');
    } else if (state === 'offline') {
      elements.apiStatusBadge.classList.add('badge-offline');
    } else {
      elements.apiStatusBadge.classList.add('badge-checking');
    }
  }

  // --- Manejo y Validación de Archivo ---
  function handleFileSelection(file) {
    hideError();

    // Validar tipo de archivo
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!validTypes.includes(file.type.toLowerCase())) {
      showError('Formato no permitido', 'Por favor selecciona una imagen válida en formato JPG, JPEG o PNG.');
      return;
    }

    // Validar tamaño (máximo 10 MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      showError('Archivo demasiado grande', 'La imagen supera los 10 MB máximos permitidos.');
      return;
    }

    selectedFile = file;

    // Mostrar previsualización
    const reader = new FileReader();
    reader.onload = (e) => {
      elements.imagePreview.src = e.target.result;
      elements.dropzonePrompt.classList.add('hidden');
      elements.previewContainer.classList.remove('hidden');
      elements.predictBtn.disabled = false;
    };
    reader.readAsDataURL(file);
  }

  function clearSelectedImage() {
    selectedFile = null;
    elements.imageInput.value = '';
    elements.imagePreview.src = '';
    elements.previewContainer.classList.add('hidden');
    elements.dropzonePrompt.classList.remove('hidden');
    elements.predictBtn.disabled = true;
    hideError();
  }

  // --- Inferencia con el Backend (POST /predict) ---
  async function performInference(file) {
    setLoading(true);
    hideError();
    hideResults();

    const formData = new FormData();
    formData.append('file', file, file.name);

    try {
      const response = await fetch(`${currentApiUrl}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errMessage = `Error HTTP ${response.status}`;
        try {
          const errData = await response.json();
          errMessage = errData.detail || errData.message || errMessage;
        } catch (_) {}
        throw new Error(errMessage);
      }

      const result = await response.json();
      renderResults(result);
    } catch (err) {
      showError('Error durante el diagnóstico', err.message || 'No fue posible conectar con el servidor.');
    } finally {
      setLoading(false);
    }
  }

  // --- Renderizado de Resultados ---
  function renderResults(data) {
    elements.emptyState.classList.add('hidden');
    elements.resultsContent.classList.remove('hidden');

    // 1. Diagnóstico Principal
    elements.plantName.textContent = data.plant || 'Especie no identificada';
    elements.diseaseName.textContent = data.disease_or_condition || data.predicted_category;

    // Estado fitosanitario (Sana vs Enferma)
    const isHealthy = data.is_healthy === true || data.health_status === 'Sana';
    elements.healthStatusBadge.textContent = isHealthy ? 'Planta Sana' : 'Patología Detectada';
    elements.healthStatusBadge.className = 'badge ' + (isHealthy ? 'badge-healthy' : 'badge-sick');

    // Tiempo de Inferencia
    const timeMs = data.inference_time_ms ? `${data.inference_time_ms} ms` : '< 300 ms';
    elements.inferenceTimeLabel.textContent = `Inferencia CPU: ${timeMs}`;

    // Confianza Principal
    const confPct = typeof data.confidence_percentage === 'number'
      ? data.confidence_percentage
      : (data.confidence * 100);
    const confFixed = confPct.toFixed(1);
    elements.confidencePercentage.textContent = `${confFixed}%`;
    elements.confidenceBar.style.width = `${Math.min(100, Math.max(0, confPct))}%`;

    // 2. Alerta de Incertidumbre (Umbral tau = 0.60 / 60%)
    const isUncertain = data.is_uncertain === true || confPct < 60.0;
    if (isUncertain) {
      elements.uncertaintyBanner.classList.remove('hidden');
      if (data.warning_message) {
        elements.uncertaintyText.textContent = data.warning_message;
      }
    } else {
      elements.uncertaintyBanner.classList.add('hidden');
    }

    // 3. Top-3 Diagnósticos Más Probables
    elements.top3List.innerHTML = '';
    const topPredictions = data.top_predictions || [];

    topPredictions.forEach((item) => {
      const itemPct = typeof item.confidence_percentage === 'number'
        ? item.confidence_percentage
        : (item.confidence * 100);
      const itemTitle = `${item.plant} — ${item.disease_or_condition}`;

      const itemEl = document.createElement('div');
      itemEl.className = 'top3-item';
      itemEl.innerHTML = `
        <div class="top3-row">
          <span class="top3-label">${escapeHtml(itemTitle)}</span>
          <span class="top3-percent">${itemPct.toFixed(1)}%</span>
        </div>
        <div class="top3-bar-bg">
          <div class="top3-bar-fill" style="width: ${Math.min(100, Math.max(0, itemPct))}%;"></div>
        </div>
      `;
      elements.top3List.appendChild(itemEl);
    });

    // 4. Descargo de Responsabilidad Agronómica
    if (data.disclaimer) {
      elements.disclaimerText.innerHTML = `<strong>Aviso Agronómico:</strong> ${escapeHtml(data.disclaimer)}`;
    }
  }

  // --- Estados de UI y Utilidades ---
  function setLoading(isLoading) {
    if (isLoading) {
      elements.loadingIndicator.classList.remove('hidden');
      elements.predictBtn.disabled = true;
      elements.btnText.textContent = 'Analizando con DINOv2...';
    } else {
      elements.loadingIndicator.classList.add('hidden');
      elements.predictBtn.disabled = !selectedFile;
      elements.btnText.textContent = 'Diagnosticar Hoja';
    }
  }

  function hideResults() {
    elements.resultsContent.classList.add('hidden');
    elements.emptyState.classList.remove('hidden');
  }

  function showError(title, message) {
    elements.errorTitle.textContent = title;
    elements.errorDesc.textContent = message;
    elements.errorBanner.classList.remove('hidden');
  }

  function hideError() {
    elements.errorBanner.classList.add('hidden');
  }

  function escapeHtml(text) {
    if (!text) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Arrancar aplicación
  document.addEventListener('DOMContentLoaded', init);
})();
