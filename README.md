# Prometeo Skill

Skill para agentes: **scrapper y buscador de datos**.

Prometeo navega plataformas web dinámicas, salta protecciones anti-bot, intercepta tráfico de red (XHR/Fetch) y extrae el dato que buscas, verificado y con trazabilidad de la fuente.

## Qué hace

1. **Bypass** — navegador stealth, sanitizado del DOM y manejo de challenges/rate-limits.
2. **Navigación** — descubre contexto, perfila datasets y recorre estructuras complejas (shadow DOM).
3. **Extracción** — captura pasiva de red, parseo multi-formato (JSON, XML, logs) y gestión de corpus/paginación.
4. **Verificación** — extracción por patrones, doble cálculo independiente y loop de feedback.

## Uso

```
/prometeo <target_url> "<búsqueda o enunciado>"
```

## Estructura

```
├── SKILL.md            # Instrucciones de la skill
├── system_prompt.md    # Entrypoint del superagente
├── modules/
│   ├── 1_bypass/       # Stealth browser, DOM sanitizer, challenge handler
│   ├── 2_navigation/   # Context discovery, data map, shadow walker
│   ├── 3_extraction/   # XHR interceptor, parser, corpus manager
│   └── 4_refinement/   # Pattern extractor, dual verifier, feedback loop
└── storage/            # Cachés de vocabulario y log de queries
```
