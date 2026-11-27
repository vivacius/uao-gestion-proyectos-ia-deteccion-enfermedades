# Feature Specification: Expansión de Suite Unitaria a >= 350 Pruebas (M4)

**Feature Branch**: `test/m4-unit-tests-350`  
**Created**: 2026-11-26  
**Status**: Prospectiva (elaborada antes de escribir las pruebas)  
**Input**: Issue `#52` (`[M4-GOV]`) — Ampliación de la suite unitaria (`tests/unit/`) desde 180 hasta al menos 350 pruebas AAA reales, sin mocks triviales ni aserciones vacías.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cobertura exhaustiva de taxonomía, contratos y cliente HTTP (Priority: P1)

Como responsable de QA (`@vivacius`), quiero ampliar la suite unitaria a mínimo 350 pruebas AAA cubriendo las 38 categorías fitosanitarias reales, los esquemas Pydantic v2, las excepciones de dominio, el preprocesamiento de imágenes, el cliente HTTP desacoplado y los contratos M4, para blindar el sistema ante regresiones en menos de 15 segundos.

**Independent Test**: Ejecutar `uv run --no-sync pytest tests/unit -q --cov=src --cov=api` y confirmar `>= 350` pruebas aprobadas, `0` fallidas y cobertura `>= 85 %`.

**Acceptance Scenarios**:

1. **Given** la suite unitaria en `tests/unit/`, **When** se ejecuta `pytest tests/unit`, **Then** recopila y aprueba al menos 350 pruebas estructuradas bajo Arrange-Act-Assert (AAA).
2. **Given** `uv run --no-sync ruff check .` y `ruff format --check .`, **When** se valida la calidad estática, **Then** ambos comandos terminan con código `0`.

## Requirements *(mandatory)*

- **FR-001**: Todas las pruebas nuevas DEBEN seguir el patrón AAA y validar comportamiento real (cero pruebas vacías).
- **FR-002**: Ninguna prueba unitaria DEBE depender de red ni cargar `model.safetensors`.

## Success Criteria *(mandatory)*

- **SC-001**: Total de pruebas en `tests/unit/` $\ge 350$ con 100 % en verde.
- **SC-002**: Cobertura en `src/` y `api/` $\ge 85\%$ y Ruff sin observaciones.
