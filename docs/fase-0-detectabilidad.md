# Fase 0 — Prueba de detectabilidad

Fecha de captura de toda la evidencia: 26 de julio de 2026. Fuente: API pública del Portal de Contrataciones Abiertas del OECE (`https://contratacionesabiertas.oece.gob.pe`).

## 0. La API real (hallazgo previo necesario)

El portal es un SPA en Angular; no publica los datos vía `robots.txt`/HTML estático sino vía una API REST propia, sin autenticación, sin bloqueo anti-bot (a diferencia de `gob.pe`):

- `GET /api/v1/search?search={término}&year={año}&page={n}&paginateBy={n}&format=json` — resultados completos en formato cercano a OCDS (`compiledRelease`, `releases`).
- `GET /api/v1/recordsYearFilter?search={término}&format=json` — conteo agregado por año (con `year` omitido, agrega todos los años disponibles: 2004–2026). Con `year` presente, exige un valor.
- Filtros hermanos equivalentes por entidad, mes, fuente, categoría, etapa (`recordsBuyerFilter`, `recordsMonthFilter`, etc.).

Esta API es más usable que las páginas HTML de `gob.pe` y es la base recomendada para `extractores/oece_contrataciones.py`, en vez de descargar datasets masivos de datos abiertos.

## 1. Candidatos por año (conteo bruto de la API, sin filtrar)

La API hace **coincidencia difusa por palabra (OR de tokens), no por frase exacta**. Esto se confirmó comparando: el término de dos palabras "inteligencia artificial" da recuentos del mismo orden de magnitud que cada palabra por separado ("inteligencia" sola, "artificial" sola), y en años como 2004 da 624 resultados — imposible que sean contrataciones reales de IA en 2004. Con esa salvedad, el conteo bruto por término (histórico 2004–2026 vs. últimos 4 años) es:

| Término | Total histórico (bruto) | 2023–2026 (bruto) |
|---|---:|---:|
| procesamiento de lenguaje natural | 21 090 | 1 375 |
| redes neuronales | 20 297 | 2 865 |
| asistente virtual | 15 080 | 630 |
| modelo predictivo | 7 140 | 842 |
| inteligencia artificial | 3 708 | 320 |
| aprendizaje automático | 2 421 | 369 |
| reconocimiento facial | 658 | 52 |
| visión computacional | 191 | 14 |
| machine learning | 177 | 48 |
| deep learning | 168 | 42 |
| analítica predictiva | 115 | 49 |
| algoritmo de scoring | 24 | 1 |
| chatbot | 18 | 9 |
| biometría | 6 | 4 |
| IA generativa | 2 | 2 |
| voicebot | 1 | 1 |

**Estos números brutos no son utilizables directamente** — son la cuenta de coincidencia difusa de la API, no de procesos realmente relacionados con IA. Los términos de mayor volumen ("procesamiento de lenguaje natural", "redes neuronales", "asistente virtual", "modelo predictivo") son también los de mayor ruido, porque contienen palabras sueltas de uso común en compras públicas ("redes" = redes de salud/eléctricas/de agua; "asistente" = asistente administrativo; "modelo" = modelo de vehículo/formulario).

## 2. Proporción de falsos positivos (muestreo manual)

Se revisó a mano una muestra de resultados reales (no solo el conteo) para cuatro términos representativos:

| Término | Muestra | Coincidencias reales con IA | Ejemplos de falso positivo |
|---|---:|---:|---|
| redes neuronales | 15 (2024) | 0 | "Dirección de Redes Integradas de Salud" (redes de salud, no redes neuronales) |
| reconocimiento facial | 15 (2025) | 1 | Medallas de premiación, vehículos "de reconocimiento" 4x4, secuenciamiento genético, implante cráneo-facial |
| asistente virtual | 15 (2024) | 4 | "Biblioteca virtual", "aula virtual", "asistente de archivo" (asistente/virtual como palabras sueltas) |
| chatbot | 4 (2025) | 4 (1 contrato único, 4 versiones del mismo release) | — (término preciso) |

Falsos positivos en la muestra combinada: **40 de 49 (≈82%)** usando la búsqueda difusa de la API tal cual. Repetí la prueba aplicando un **filtro de frase exacta del lado del cliente** (buscar el término literal dentro de título+descripción de los resultados brutos):

| Término | Resultados brutos (año de prueba) | Con frase exacta | Nota |
|---|---:|---:|---|
| asistente virtual (2024) | 50 | 4 (4 contratos únicos) | El filtro de frase exacta sí funciona aquí: 100% de precisión tras filtrar |
| reconocimiento facial (2025) | 18 | 0 | El filtro es *demasiado* estricto: pierde el caso real "captura biométrica - facial", que no usa la frase exacta |
| redes neuronales (2024) | 50 | 0 | Confirma que el término es inútil incluso con filtro |

**Conclusión:** el filtro de frase exacta reduce el ruido casi a cero, pero también genera falsos negativos (pierde formulaciones alternativas como "biométrica - facial" en vez de "reconocimiento facial"). No hay atajo: la detección automática solo puede producir **candidatos**, nunca altas directas. Esto confirma que el campo "nivel de confianza" del esquema (§5 del prompt original) no es opcional — es estructural.

## 3. Recall frente a la línea base

No tuve acceso al texto completo del catálogo de Interfases (22 aplicaciones, artículo académico con paywall/journal), así que probé recall contra los **24 sistemas del catálogo oficial PCM** (línea base ya cargada en `datos/linea-base-pcm.csv`), buscando cada nombre de producto directamente en la API:

| Sistema (nombre de producto) | Encontrado por nombre |
|---|---|
| Qhali | Sí (6 resultados) |
| SIGERSOL | Sí (5) |
| MAIA | Sí (4, ambiguo — nombre corto) |
| EleccIA | Sí (9) |
| CURIA | Sí (18, con riesgo de falso positivo por ser palabra latina común) |
| CadEye | No |
| ADETOP | No |
| BIANCA | No |
| YachAIbot | No |
| Biofacial | No |
| InnGenius | No |

**5 de 11 (≈45%)** se encuentran por nombre de producto. Los 6 restantes no aparecen — la hipótesis más probable es que fueron desarrollados internamente (sin contratación externa que mencione el nombre comercial) o que la contratación asociada usa una descripción genérica ("servicio de desarrollo de software") sin el nombre del producto. **Esto es una limitación estructural, no un error de método**: la detección por contrataciones nunca va a alcanzar el 100% de recall, porque una parte de los sistemas de IA del Estado no pasa por una compra pública nombrada así.

Hallazgo positivo inesperado: la búsqueda por término genérico ("asistente virtual") encontró, dentro de la muestra, al menos **dos sistemas que no están en ninguna de las dos líneas base** (Interfases ni el catálogo PCM): un asistente virtual de PROINNOVATE con IBM Cloud ("SOFIA") y un asistente virtual con IA para SEDAPAR S.A. Esto confirma que el método sí tiene valor de **descubrimiento**, más allá de solo confirmar lo ya conocido.

## 4. Campos utilizables por resultado

Cada resultado de `/api/v1/search` trae, dentro de `compiledRelease`:

- `tender.procuringEntity.name` / `.id` (entidad, con ID CONSUCODE estable) y `buyer` equivalente.
- `tender.description` y `tender.title` (texto para filtrar y para mostrar evidencia).
- `tender.value.amount`, `.currency`, `.amount_PEN` (presupuesto).
- `tender.tenderPeriod.startDate` / `.endDate` y `date` de la release (fechas).
- `ocid` (identificador OCDS permanente y estable — ideal como parte del identificador del sistema).
- `sources[].url` (enlace directo a SEACE, sirve como evidencia primaria).
- `awards[].id` / `contracts[].id` (para profundizar en adjudicación si se necesita el proveedor exacto — no viene el nombre del proveedor en el nivel raíz, hay que resolverlo vía el award).

No viene directamente el nombre del proveedor adjudicado en `compiledRelease` de forma consistente (algunos resultados no tienen `awards`); se necesitaría una llamada adicional por `award.id` para completar ese campo cuando exista.

## Recomendación

**Seguir adelante**, con el método ajustado (no es un simple "buscar término → dar de alta"):

1. El extractor busca cada término de la lista contra `/api/v1/search` por año.
2. Aplica **filtro de frase exacta** sobre título+descripción para eliminar el ~80% de ruido de la búsqueda difusa de la API.
3. Cada resultado que pasa el filtro entra como **candidato**, nunca como alta directa — corresponde al nivel de confianza "inferido de contratación" del esquema (§5), pendiente de revisión.
4. Además del término genérico, el extractor debe intentar el nombre de producto de cada sistema ya conocido (de las líneas base), como verificación cruzada — con el entendido de que ~55% de los sistemas no se van a encontrar así, y eso no es un fallo del extractor sino un límite real de la fuente.
5. `algoritmo de scoring`, `voicebot`, `IA generativa`, `biometría` tienen volumen bajo — conviene revisarlos manualmente completos en vez de filtrarlos, dado el bajo costo. `redes neuronales` en solitario no aporta señal utilizable y se debe excluir o exigir co-ocurrencia con otro término.

Nada de esto invalida el proyecto: el problema (falsos positivos altos, recall parcial) es exactamente el que el campo "nivel de confianza" del esquema ya estaba diseñado para absorber. Quedo a la espera de tu decisión para pasar a la arquitectura (Fase 1).
