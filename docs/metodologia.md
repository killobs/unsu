# Metodología / Methodology

*English version below.*

## Español

### 1. Qué entra al registro

Un sistema entra a `datos/sistemas/` solo si hay al menos una fuente pública citable con fecha de captura. No hay excepciones: sin evidencia no hay ficha, por más plausible que parezca la existencia del sistema.

### 2. Nivel de confianza de la detección

Cada sistema declara uno de estos tres niveles, visible en la interfaz con la misma prioridad que cualquier otro campo — nunca como nota al pie:

- **confirmado_fuente_oficial**: aparece en un documento oficial nombrado (catálogo PCM, portal de la entidad, norma, resolución).
- **inferido_contratacion**: se detectó por coincidencia de términos en una contratación pública (ver §3), sin confirmación oficial adicional. Va acompañado del proceso de contratación exacto como evidencia.
- **reportado_prensa**: solo aparece en cobertura periodística, sin documento oficial ni contratación identificable.

### 3. Criterio de detección por contrataciones (resultado de la Fase 0)

La API de búsqueda del Portal de Contrataciones Abiertas del OECE hace coincidencia difusa por palabra suelta, no por frase exacta — un término de dos o más palabras puede traer miles de resultados irrelevantes (ver `docs/fase-0-detectabilidad.md`). El criterio operativo:

1. Buscar cada término de la lista de detección contra `/api/v1/search`, por año.
2. Descartar todo resultado cuyo título+descripción no contenga la frase exacta del término (filtro de frase exacta del lado del cliente).
3. Lo que sobrevive entra como **candidato**, con `nivel_confianza: inferido_contratacion` — nunca se promueve solo a "confirmado" sin revisión humana o fuente oficial adicional.
4. La ausencia de un sistema en este barrido no prueba que no exista: puede haber sido desarrollado internamente, sin contratación externa nombrada.

Lista de términos vigente (ver también `docs/fase-0-detectabilidad.md` para el resultado empírico de cada uno): inteligencia artificial, aprendizaje automático, machine learning, reconocimiento facial, biometría, analítica predictiva, procesamiento de lenguaje natural, chatbot, asistente virtual, visión computacional, modelo predictivo, algoritmo de scoring, deep learning, IA generativa, voicebot. Se excluye "redes neuronales" en solitario — en la Fase 0 dio 0% de precisión incluso con filtro de frase exacta.

### 4. Clasificación de riesgo (propia, no oficial)

**Esta clasificación es una elaboración propia del proyecto, no la clasificación oficial del reglamento peruano** (que a la fecha de esta versión no publica un listado propio por sistema). Se etiqueta como tal en cada ficha, con este criterio, inspirado en la estructura de cuatro niveles del EU AI Act pero aplicado con lectura propia a cada caso:

- **Riesgo alto**: el sistema toma o asiste una decisión que afecta directamente un derecho fundamental o un proceso con consecuencias legales para la persona (ejemplos: evaluación de expedientes electorales, proyección de resoluciones judiciales, verificación biométrica para identidad, diagnóstico médico).
- **Riesgo limitado**: interactúa directamente con la ciudadanía pero no decide sobre derechos (ejemplos: chatbots de atención, asistentes virtuales informativos).
- **Riesgo mínimo**: uso interno, soporte administrativo, sin interacción directa con el público ni decisión sobre derechos (ejemplos: monitoreo de servidores, herramientas de productividad interna).
- **Pendiente de clasificar**: información insuficiente en la fuente para asignar un nivel.

Mapeo a EU AI Act y NIST AI RMF: se registra como referencia comparada, no como equivalencia jurídica — el marco peruano y el europeo no son intercambiables.

### 5–6. Esquema de las fichas de sistema y entidad

La especificación completa de campos ya no vive aquí — se publicó como estándar abierto, versionado e
independiente en [`docs/esquema/`](esquema/README.md), pensado para que otra jurisdicción pueda adoptarlo sin
depender del código de este repositorio. Esta sección de metodología se queda con los *criterios de llenado*
(qué significa cada valor, cuándo usar cada estado); `docs/esquema/` se queda con la *forma* (qué campos existen,
de qué tipo, en qué orden).

---

## English

### 1. What enters the registry

A system enters `datos/sistemas/` only if there is at least one citable public source with a capture date. No exceptions.

### 2. Detection confidence level

- **confirmado_fuente_oficial** (confirmed by official source): named in an official document.
- **inferido_contratacion** (inferred from procurement): detected via term match in public procurement data, uncorroborated.
- **reportado_prensa** (press-reported): only in news coverage.

### 3. Procurement-based detection criterion (Phase 0 result)

The OECE open-contracting search API does fuzzy single-word matching, not exact-phrase matching — see `docs/fase-0-detectabilidad.md` for the empirical measurement (up to 82% false positives on naive term search). Operating rule: search by term, filter client-side for the exact phrase in title+description, and treat every survivor as a **candidate** (`inferido_contratacion`), never an automatic confirmed entry. Absence from this sweep does not prove a system doesn't exist — in-house builds without a named external contract won't surface this way.

### 4. Risk classification (own methodology, not official)

**This is the project's own classification, not Peru's official one** (no official per-system risk list exists yet). Loosely modeled on the EU AI Act's four tiers, applied with independent judgment: high risk (affects a fundamental right or has legal consequences), limited risk (direct citizen interaction, no rights decision), minimal risk (internal use only), or pending classification (insufficient source information).

### 5–6. Record schemas

The full field specification no longer lives here — it was published as an open, versioned, independent standard
at [`docs/esquema/`](esquema/README.md), meant to be adoptable by another jurisdiction without depending on this
repository's code. This methodology section keeps the *fill-in criteria* (what each value means, when to use
each state); `docs/esquema/` keeps the *shape* (which fields exist, of what type, in what order). Field names are
kept in Spanish throughout the dataset for consistency with the sources, with English labels reserved for the
bilingual site UI layer (Phase 4).
