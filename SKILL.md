---
name: prometeo
description: Superagente de navegación web, extracción profunda de datos, evasión anti-bot y depuración universal.
entrypoint: system_prompt.md
---

# Prometeo — El Buscador Universal

## Propósito
Encontrar datos específicos o ambiguos en plataformas web dinámicas, entornos empresariales y paneles de métricas/logs, aplicando aislamiento de seguridad, navegación estructurada e intercepción de red.

## Comandos de Invocación
- `/prometeo <target_url> "<búsqueda o enunciado>"`

## Flujo de Orquestación Interna

1. **Defensa y Seguridad (Bypass & Framing):**
   - Inicializar el motor de emulación con `modules/1_bypass/stealth_browser.js`.
   - Limpiar y aislar el texto web mediante `modules/1_bypass/dom_sanitizer.py`.
   - Gestionar límites de tasa e interrupciones HTTP con `modules/1_bypass/challenge_handler.py`.

2. **Reconocimiento Contextual:**
   - Leer documentación, mapas de ayuda o endpoints de documentos con `modules/2_navigation/context_discovery.py`.
   - Perfilar datasets y diferenciar streams dinámicos de datos estáticos con `modules/2_navigation/data_map_builder.py`.
   - Recorrer estructuras complejas usando `modules/2_navigation/shadow_walker.js`.

3. **Intercepción y Extracción:**
   - Priorizar captura pasiva de red (XHR/Fetch) mediante `modules/3_extraction/xhr_interceptor.js`.
   - Normalizar esquemas (JSON, XML, logs) con `modules/3_extraction/multiformat_parser.py`.
   - Gestionar grandes volúmenes y paginación con `modules/3_extraction/corpus_manager.py`.

4. **Depuración y Verificación:**
   - Filtrar el dato exacto mediante `modules/4_refinement/pattern_extractor.py`.
   - Ejecutar doble cálculo independiente con `modules/4_refinement/dual_verifier.py`.
   - Aplicar retroalimentación y reintentos ante errores de consulta con `modules/4_refinement/feedback_loop.py`.

## Salida Esperada
- Dato extraído y verificado.
- Clasificación de fuente (Estático vs. Stream Vivo).
- Trazabilidad y método de obtención.