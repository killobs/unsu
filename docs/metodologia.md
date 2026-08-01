# Metodología / Methodology

*English version below.*

## Español

### 1. Qué entra al registro

Un sistema entra a `datos/sistemas/` solo si hay al menos una fuente pública citable con fecha de captura. No hay excepciones. Sin evidencia no hay ficha, por más plausible que parezca la existencia del sistema.

### 2. Nivel de confianza de la detección

Cada sistema declara uno de estos tres niveles. Se muestra en la interfaz con la misma prioridad que cualquier otro campo, nunca como nota al pie.

- `confirmado_fuente_oficial`: aparece en un documento oficial nombrado, como el catálogo de la PCM, el portal de la entidad, una norma o una resolución.
- `inferido_contratacion`: se detectó por coincidencia de términos en una contratación pública, según el §3, sin confirmación oficial adicional. Va acompañado del proceso de contratación exacto como evidencia.
- `reportado_prensa`: solo aparece en cobertura periodística, sin documento oficial ni contratación identificable.

### 3. Criterio de detección por contrataciones

La API de búsqueda del Portal de Contrataciones Abiertas del OECE hace coincidencia difusa por palabra suelta. Un término de dos o más palabras puede traer miles de resultados irrelevantes. La Fase 0 midió hasta 82% de falsos positivos sin filtrar (ver `docs/fase-0-detectabilidad.md`).

El criterio operativo tiene cuatro pasos.

1. Buscar cada término de la lista contra `/api/v1/search`, por año, recorriendo todas las páginas. La API entrega 50 resultados por página.
2. Descartar todo resultado cuyo título y descripción no contengan la frase exacta del término.
3. Descartar además todo resultado cuyo texto no evidencie inteligencia artificial por sí mismo, sin apoyarse en el término que disparó la búsqueda. Esta comprobación no se aplica a lo confirmado por fuente oficial, porque hay sistemas reales cuya descripción corta no repite la frase «inteligencia artificial».
4. Lo que sobrevive entra como candidato, con `nivel_confianza: inferido_contratacion`. No se promueve a confirmado sin revisión humana o fuente oficial adicional.

La ausencia de un sistema en el barrido no prueba que no exista. Puede haberse desarrollado internamente, sin contratación externa nombrada.

**Términos descartados.** «Redes neuronales» dio 0% de precisión en la Fase 0 incluso con filtro de frase exacta. «Mantenimiento predictivo» se probó y se retiró el mismo día: es una metodología de mantenimiento industrial anterior a la IA, basada en termografía y análisis de vibraciones, y produjo 74 fichas de mantenimiento de transformadores y subestaciones eléctricas. Ambos están registrados en el extractor para que no vuelvan a añadirse.

Los candidatos revisados a mano y descartados se anotan en `datos/excluidos.yaml` con su motivo y la URL de su evidencia. Los extractores consultan esa lista para no darlos de alta otra vez en cada corrida.

### 4. Clasificación de riesgo, propia y no oficial

Esta clasificación es una elaboración del proyecto. No es la clasificación oficial del reglamento peruano, que a la fecha no publica un listado por sistema. Cada ficha lo declara. La estructura de cuatro niveles se inspira en el EU AI Act, aplicada con lectura propia a cada caso.

- **Riesgo alto**: el sistema toma o asiste una decisión que afecta directamente un derecho fundamental o un proceso con consecuencias legales para la persona. Ejemplos: evaluación de expedientes electorales, proyección de resoluciones judiciales, verificación biométrica para identidad, diagnóstico médico.
- **Riesgo limitado**: interactúa directamente con la ciudadanía pero no decide sobre derechos. Ejemplos: chatbots de atención, asistentes virtuales informativos.
- **Riesgo mínimo**: uso interno o soporte administrativo, sin interacción directa con el público ni decisión sobre derechos. Ejemplos: monitoreo de servidores, herramientas de productividad interna.
- **Pendiente de clasificar**: información insuficiente en la fuente para asignar un nivel.

Cada ficha registra en `notas` el criterio concreto que sustenta su nivel, y distingue si corresponde a un ejemplo literal de esta metodología o a una interpretación del proyecto.

El mapeo a EU AI Act y NIST AI RMF se registra como referencia comparada. No es equivalencia jurídica: el marco peruano y el europeo no son intercambiables.

**Supuesto que esta versión no cubre.** Cuatro sistemas son control de asistencia de trabajadores con reconocimiento facial. Encajan en riesgo mínimo por ser uso interno, pero procesan datos biométricos de personas, un caso que los tres niveles no contemplan. Sus fichas lo dejan anotado.

### 4.b Criterio para el campo `estado`

El esquema admite `en_operacion`, `piloto`, `contratado_sin_desplegar`, `descontinuado` e `indeterminado`. Se asigna solo con evidencia.

- `en_operacion`: una fuente oficial lo lista como aplicación existente en el Estado. El Catálogo de Aplicaciones con Inteligencia Artificial en el Estado Peruano (PCM/SGTD) sirve a este efecto, porque documenta aplicaciones con las tecnologías que usan.
- `piloto`: la propia fuente lo describe como piloto o prueba.
- `contratado_sin_desplegar`: consta el contrato adjudicado y además una fuente indica que todavía no está en producción. El contrato por sí solo no basta.
- `descontinuado`: hay evidencia de que dejó de usarse.
- `indeterminado`: solo consta la contratación.

Un contrato adjudicado no prueba que el sistema opere. Este registro no lo da por hecho, así que `indeterminado` es el valor por defecto de todo candidato detectado en contrataciones.

### 4.c Criterio para el campo `fecha_limite` de las obligaciones

El DS 115-2025-PCM **no fija una sola fecha para todo el Estado**. Su Primera Disposición Complementaria Final escalona la implementación del artículo 25 y del Capítulo I del Título VI según el tipo de entidad. El reglamento se publicó el 9 de setiembre de 2025 y los plazos corren «a partir del día siguiente», así que la cuenta arranca el 2025-09-10:

| Inciso | Entidades | Plazo | Vence |
|---|---|---|---|
| a | Poder Ejecutivo, Legislativo y Judicial | 1 año | 2026-09-10 |
| b | Organismos Constitucionales Autónomos | 1 año | 2026-09-10 |
| c | EsSalud, gobiernos regionales y universidades públicas | 2 años | 2027-09-10 |
| d | Gobiernos locales Tipo A, B y C | 3 años | 2028-09-10 |
| e | Empresas públicas regionales, locales o bajo FONAFE | 2 años | 2027-09-10 |
| f | Demás entidades de los numerales 7 y 8 del artículo I del Título Preliminar de la Ley 27444 | 2 años | 2027-09-10 |
| g | Gobiernos locales Tipo D a G | facultativo | — |

El cronograma **por sector** que suele citarse (salud, educación, justicia, seguridad, economía y finanzas al primer año; transporte, comercio y trabajo al segundo) es el del **desarrollador o implementador del sector privado**, y no aplica a las entidades de este registro.

El corte entre el inciso a) y el f) se apoya en el propio artículo I del Título Preliminar de la Ley 27444, al que el reglamento remite: su numeral 1 cuenta dentro del Poder Ejecutivo a los «Ministerios y Organismos Públicos Descentralizados», mientras que su numeral 7 recoge aparte a los «proyectos y programas del Estado». De ahí que los ministerios y los organismos adscritos vayan al tramo de un año, y los programas y proyectos de inversión al de dos.

Igual que la clasificación de riesgo, **esta asignación es lectura del proyecto y no una calificación oficial**: el reglamento no publica un padrón que diga qué tramo le toca a cada entidad. La asignación vive en `historial/asignar_plazos.py`, con el criterio de cada entidad anotado, para que sea auditable y reproducible. Una entidad sin tramo asignado se queda con `fecha_limite` vacío y el script avisa: se prefiere el vacío a una fecha heredada por defecto, porque una fecha equivocada da por tarde a una entidad que todavía está en plazo.

### 5–6. Esquema de las fichas de sistema y entidad

La especificación completa de campos se publicó como estándar abierto, versionado e independiente en [`docs/esquema/`](esquema/README.md), pensado para que otra jurisdicción pueda adoptarlo sin depender del código de este repositorio.

Esta sección de metodología se queda con los criterios de llenado: qué significa cada valor y cuándo usar cada estado. El esquema se queda con la forma: qué campos existen, de qué tipo y en qué orden.

---

## English

### 1. What enters the registry

A system enters `datos/sistemas/` only if there is at least one citable public source with a capture date. No exceptions.

### 2. Detection confidence level

- `confirmado_fuente_oficial`: named in an official document.
- `inferido_contratacion`: detected via term match in public procurement data, uncorroborated.
- `reportado_prensa`: only in news coverage.

### 3. Procurement-based detection criterion

The OECE open-contracting search API does fuzzy single-word matching rather than exact-phrase matching. Phase 0 measured up to 82% false positives on naive term search (see `docs/fase-0-detectabilidad.md`).

The operating rule: search by term and year across all result pages, filter client-side for the exact phrase in title and description, then require the text to evidence artificial intelligence on its own without relying on the search term. That second filter never applies to entries confirmed by an official source, because real systems often carry short descriptions that do not repeat the phrase «artificial intelligence». Survivors enter as candidates, never as automatic confirmed entries.

Absence from the sweep does not prove a system does not exist. In-house builds without a named external contract do not surface this way.

Two terms were tested and dropped. «Redes neuronales» scored 0% precision in Phase 0. «Mantenimiento predictivo» is an industrial maintenance methodology that predates AI and produced 74 records of electrical transformer maintenance. Both are recorded in the extractor so they are not added again.

Manually rejected candidates are listed in `datos/excluidos.yaml` with their reason and evidence URL. The extractors consult that list so rejected entries do not reappear on each run.

### 4. Risk classification, the project's own and not official

This is the project's classification, not Peru's official one. No official per-system risk list exists yet. It is loosely modeled on the EU AI Act's four tiers and applied with independent judgment: high risk affects a fundamental right or carries legal consequences; limited risk means direct citizen interaction without decisions on rights; minimal risk means internal use only; pending classification means the source lacks enough information.

Each record states in `notas` the concrete criterion behind its level, and whether that criterion is a literal example from this methodology or an interpretation by the project.

Mapping to the EU AI Act and NIST AI RMF is recorded as comparative reference, not legal equivalence.

### 4.b Criterion for the `estado` field

Values are assigned only with evidence. `en_operacion` requires an official source listing the system as an existing application. `piloto` requires the source to describe it as a pilot. `contratado_sin_desplegar` requires both an awarded contract and a source indicating it is not yet in production. `descontinuado` requires evidence it was retired. `indeterminado` means only the contract is on record.

An awarded contract does not prove a system operates, so `indeterminado` is the default for every candidate detected in procurement.

### 4.c Criterion for the obligations' `fecha_limite` field

DS 115-2025-PCM sets **no single date for the whole State**. Its First Complementary Final Provision staggers implementation of article 25 and Title VI Chapter I by type of entity. The regulation was published on 9 September 2025 and the terms run «from the following day», so the count starts on 2025-09-10:

| Item | Entities | Term | Due |
|---|---|---|---|
| a | Executive, Legislative and Judicial branches | 1 year | 2026-09-10 |
| b | Constitutionally Autonomous Bodies | 1 year | 2026-09-10 |
| c | EsSalud, regional governments and public universities | 2 years | 2027-09-10 |
| d | Local governments Type A, B and C | 3 years | 2028-09-10 |
| e | Public companies, regional, local or under FONAFE | 2 years | 2027-09-10 |
| f | Remaining entities under items 7 and 8 of article I of the Preliminary Title of Law 27444 | 2 years | 2027-09-10 |
| g | Local governments Type D to G | optional | — |

The **sector-based** schedule often quoted (health, education, justice, security, economy and finance in the first year; transport, commerce and labour in the second) applies to the **private-sector developer or implementer**, not to the entities in this registry.

The line between item a) and item f) rests on article I of the Preliminary Title of Law 27444, which the regulation cites: its item 1 counts «Ministries and Decentralised Public Bodies» as part of the Executive branch, while its item 7 separately covers «State projects and programmes». Hence ministries and attached bodies fall in the one-year tranche, and programmes and investment projects in the two-year one.

Like the risk classification, **this assignment is the project's own reading and not an official determination**: the regulation publishes no roster stating which tranche each entity falls into. The assignment lives in `historial/asignar_plazos.py`, with the criterion recorded per entity, so it is auditable and reproducible. An entity with no tranche assigned keeps an empty `fecha_limite` and the script warns: an empty value is preferred over an inherited default, because a wrong date marks an entity as late while it is still within its term.

### 5–6. Record schemas

The full field specification was published as an open, versioned, independent standard at [`docs/esquema/`](esquema/README.md), meant to be adoptable by another jurisdiction without depending on this repository's code.

This methodology section keeps the fill-in criteria: what each value means and when to use each state. The schema keeps the shape: which fields exist, of what type, in what order.

Field names stay in Spanish throughout the dataset for consistency with the sources. English labels are reserved for the bilingual site interface.
