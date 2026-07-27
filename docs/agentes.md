# Agentes del Registro de IA Pública — especificación

Versión 1.0 · 26 de julio de 2026 · Destino: `docs/agentes.md`

> **Cómo usar este documento.** Es la especificación para construir los agentes de verificación del
> proyecto. Está escrito para que una sesión de Claude Code que **no participó** en las sesiones anteriores
> pueda implementarlos leyendo solo esto más los documentos que aquí se citan. Si algo de este documento
> contradice a `docs/estrategia.md` o al prompt de construcción original, ellos mandan.
>
> **Modelo sugerido para implementar:** Sonnet. **Modelo sugerido para que los agentes corran:** Sonnet
> (son tareas de investigación acotada con criterios ya escritos, no de diseño).

---

## 1. Contexto mínimo

**Qué es el proyecto.** Un registro público, versionado y de costo cero de los sistemas de inteligencia
artificial que el Estado peruano compra y despliega, con clasificación de riesgo propia y seguimiento del
cumplimiento de la Ley 31814 y su reglamento (DS 115-2025-PCM).

**Dónde vive.** `D:\Unsu\registro-ia-publica` · repositorio público `github.com/killobs/unsu` · rama `main`.

**Cómo se almacenan los datos.** No hay base de datos. Un archivo YAML por registro:
- `datos/sistemas/{id}.yaml` — un sistema de IA detectado.
- `datos/entidades/{id}.yaml` — una entidad pública y su estado de cumplimiento.

El historial de commits de Git es el motor de historial del producto. Por eso el orden de los campos es
determinista y **no se debe reordenar**: un diff limpio es parte del producto.

**Documentos que hay que leer antes de implementar, en orden de autoridad:**

| Documento | Qué define |
|---|---|
| `docs/estrategia.md` | Para qué existe el proyecto y qué decisiones no se toman en contra |
| `docs/metodologia.md` | Criterios de detección, niveles de confianza, **criterios de clasificación de riesgo (§4)** |
| `docs/esquema/` | Especificación de campos de `sistema.yaml` y `entidad.yaml` |
| `docs/fase-0-detectabilidad.md` | Por qué la detección automática produce candidatos y no altas |
| `docs/bitacora.md` | Decisiones técnicas previas y su motivo |

**Utilidades ya construidas que los agentes deben usar** (no reimplementar):

```python
import sys; sys.path.insert(0, "D:/Unsu/registro-ia-publica")
from extractores.comun import esquema, evidencia as ev

sistemas = esquema.cargar_sistemas()      # dict {id: dict}
entidades = esquema.cargar_entidades()    # dict {id: dict}
esquema.guardar_sistema(sistema)          # escribe con orden determinista
esquema.guardar_entidad(entidad)
esquema.evidencia_ya_registrada(sistema, url)   # bool, evita evidencia duplicada
ev.nueva(url, descripcion, fecha_captura)       # construye una entrada de evidencia
```

**Valores válidos de los campos que los agentes escriben:**

```
estado                      en_operacion | piloto | contratado_sin_desplegar | descontinuado | indeterminado
nivel_confianza             confirmado_fuente_oficial | inferido_contratacion | reportado_prensa
clasificacion_riesgo_propia alto | limitado | minimo | pendiente_de_clasificar
supervision_humana_declarada si | no | no_declarado
obligaciones[].estado       cumplido_con_evidencia | no_cumplido | no_verificable_desde_fuentes_publicas | no_aplica_todavia
```

---

## 2. Reglas que ningún agente puede romper

Estas no son preferencias de estilo. Son la razón por la que el registro es citable.

1. **Sin evidencia no hay afirmación.** Todo cambio de estado, precio o clasificación lleva al menos una
   entrada en `evidencia` con URL y `fecha_captura`. Si no se encontró fuente, el campo no se toca.
2. **"No verificable" nunca se convierte en "no cumplido".** La ausencia de evidencia pública no es
   evidencia de incumplimiento. Convertir una en otra es la línea que separa un observatorio de una
   acusación. Un agente solo puede escribir `no_cumplido` si encontró evidencia **positiva** de que la
   entidad no cumplió (por ejemplo, un informe de Contraloría), nunca por no haber encontrado nada.
3. **No inventar.** Si la investigación no encontró nada, el agente lo escribe explícitamente en `notas`
   ("Sin evidencia adicional encontrada, búsqueda realizada el {fecha}"). El silencio se ve igual que la
   pereza; la constancia explícita, no.
4. **Las contradicciones se documentan, no se resuelven a dedo.** Si dos fuentes serias se contradicen
   (ya pasó con el resonador del INEN), se anotan ambas en `notas` y el estado se queda en
   `indeterminado`. Un agente no elige la versión que le gusta más.
5. **La clasificación de riesgo es propia, no oficial.** Siempre etiquetada como tal. El marco peruano no
   publica un listado por sistema; nuestra clasificación es una elaboración del proyecto, corregible.
6. **Sin adjetivos valorativos sobre entidades ni funcionarios.** Es un observatorio técnico, no
   activismo. `docs/estrategia.md` §8 explica por qué también es una decisión práctica.
7. **Nada de especulación sobre capacidades no documentadas**, con cuidado especial en sistemas de
   seguridad, vigilancia o defensa.
8. **Gobiernos locales fuera de alcance** mientras sus plazos normativos sigan a tres años o más. Si un
   agente encuentra un sistema de una municipalidad, lo reporta pero no lo da de alta.
9. **No borrar registros.** Si un registro resulta ser un falso positivo o un duplicado, se anota en
   `notas` y, si es duplicado confirmado, se fusiona preservando la evidencia de ambos. Borrar sin dejar
   rastro rompe el historial, que es el activo.

---

## 3. Arquitectura: qué se agenda y qué no

Hay una tensión real que conviene resolver explícitamente antes de implementar.

El proyecto tiene una restricción no negociable de **costo cero de operación** (`docs/estrategia.md` §1,
prompt original §1.1). Los extractores corren gratis en GitHub Actions porque son scripts de Python. Un
agente, en cambio, necesita un modelo — y meter una clave de API en GitHub Actions sería un servicio de
pago para el proyecto.

**Solución adoptada, y por qué:**

```
CAPA AUTOMÁTICA (GitHub Actions, gratis, corre sola)
  extractores/*.py  →  detecta candidatos  →  commit automático
                                                    ↓
                                        deja trabajo pendiente marcado
                                                    ↓
CAPA DE JUICIO (Claude Code, cuando Bernardo abre una sesión)
  agentes  →  investigan, verifican, clasifican  →  commit
```

Los agentes **no se agendan en GitHub Actions**. Se invocan desde una sesión de Claude Code, con la
cadencia que Bernardo decida. El costo es su suscripción existente, no infraestructura nueva del
proyecto — la restricción se respeta.

Esto encaja además con la regla de resiliencia al abandono (`docs/estrategia.md` §7): la captura sigue
corriendo sola durante una ausencia, y el trabajo de juicio se acumula en una cola visible que se puede
retomar en frío. **La máquina no se detiene aunque nadie invoque un agente en tres meses.**

---

## 4. Formato de archivo de agente

Cada agente es un archivo en `.claude/agents/{nombre}.md` (crear el directorio, hoy no existe):

```markdown
---
name: nombre-del-agente
description: Cuándo usar este agente. Se lee para decidir si aplica a una tarea.
tools: Read, Write, Edit, Bash, WebSearch, WebFetch, Glob, Grep
model: sonnet
---

Aquí va el prompt de sistema del agente: quién es, qué hace, qué reglas sigue,
qué formato de salida produce.
```

**Reglas de tooling comunes a todos:**
- `WebSearch` + `WebFetch` para investigar.
- `Bash` para leer/escribir los YAML vía los helpers de `extractores/comun/esquema.py` (más seguro que
  editar YAML a mano: garantiza el orden determinista de campos).
- **Ningún agente ejecuta `git push`.** Escriben archivos; Bernardo revisa el diff y decide.
- Límite de búsquedas: 2-3 por elemento investigado. Si no encuentra nada, lo reporta y sigue. Sin esto,
  un agente se puede quedar dando vueltas sobre un sistema que simplemente no tiene cobertura pública.

---

## 5. Los agentes

### 5.1 `verificador-sistemas` — prioridad 1

**Problema que resuelve.** Los extractores corren a diario y cada corrida agrega candidatos con
`nivel_confianza: inferido_contratacion` y `estado: indeterminado`. Nadie sabe si esos sistemas se
construyeron, se usan o se cancelaron. Hoy hay **22 sistemas** en ese estado.

**Cuándo se invoca.** Después de cada corrida de captura que agregue candidatos nuevos, o en tandas
cuando se hayan acumulado.

**Entrada.** Los sistemas de `datos/sistemas/*.yaml` donde `nivel_confianza == "inferido_contratacion"`
o `estado == "indeterminado"`.

**Proceso, por sistema:**
1. Buscar en la web: nombre del sistema + entidad; número de proceso de contratación; nombre comercial si
   lo hay.
2. Determinar el estado real con evidencia: ¿se implementó? ¿sigue en piloto? ¿se canceló? ¿no hay rastro?
3. Buscar el monto real del contrato (adjudicado, no solo referencial) y el proveedor adjudicado.
4. Evaluar si el registro **realmente describe un sistema de IA**. Éste es el punto que ningún filtro de
   texto resuelve: el barrido detecta correctamente la frase "inteligencia artificial", pero muchos
   resultados son compras de equipamiento de laboratorio, cursos de capacitación o eventos *sobre* IA. Si
   es el caso, anotarlo en `notas` con la evaluación de relevancia — no borrar el registro.
5. Detectar duplicados: mismo proceso de contratación capturado varias veces (mismo monto + misma
   finalidad + código de proceso con sufijo distinto es la señal típica).

**Salida — campos que escribe:**
`estado`, `presupuesto` (solo con fuente), `proveedor`, `vinculo_contractual`, `nivel_confianza`
(subir a `confirmado_fuente_oficial` solo si hay fuente oficial o cobertura seria), `evidencia` (agregar,
nunca reemplazar), `notas`.

**Lo que NO debe hacer:**
- Marcar `en_operacion` porque "parece razonable que ya esté funcionando". Solo con evidencia.
- Sobrescribir un presupuesto existente sin citar la fuente de la cifra nueva.
- Fusionar duplicados por su cuenta si la coincidencia no es clara: reportarlos para revisión humana.

**Criterio de éxito.** Cada sistema procesado queda o bien con estado verificado y evidencia nueva, o bien
con una nota explícita de que se buscó y no se encontró nada, con la fecha de la búsqueda.

---

### 5.2 `clasificador-riesgo` — prioridad 1

**Problema que resuelve.** La clasificación de riesgo es *el* diferenciador del proyecto frente al
catálogo oficial de la PCM, que no la tiene. Hoy está **vacía en los 54 sistemas** (`pendiente_de_clasificar`),
igual que `mapeo_eu_ai_act` y `mapeo_nist_ai_rmf`.

**Cuándo se invoca.** Una primera pasada sobre todo el conjunto; después, sobre cada sistema nuevo que
entre al registro.

**Entrada.** Sistemas con `clasificacion_riesgo_propia == "pendiente_de_clasificar"`.

**Proceso.** Leer **primero** `docs/metodologia.md` §4 — los criterios ya están escritos y el agente los
aplica, no los inventa. Resumen (el documento manda sobre este resumen):

| Nivel | Criterio |
|---|---|
| `alto` | Toma o asiste una decisión que afecta un derecho fundamental o tiene consecuencias legales para la persona (evaluación de expedientes electorales, proyección de resoluciones judiciales, verificación biométrica de identidad, diagnóstico médico) |
| `limitado` | Interactúa directamente con la ciudadanía pero no decide sobre derechos (chatbots de atención, asistentes informativos) |
| `minimo` | Uso interno, soporte administrativo, sin interacción directa con el público ni decisión sobre derechos |
| `pendiente_de_clasificar` | Información insuficiente en la fuente para asignar nivel |

**Salida:** `clasificacion_riesgo_propia`, `mapeo_eu_ai_act`, `mapeo_nist_ai_rmf`, `tipo_decision`,
`supervision_humana_declarada`, y en `notas` **el razonamiento de la clasificación** (por qué ese nivel y
no otro).

**Lo que NO debe hacer:**
- Dejar la clasificación sin justificar. Si no se puede explicar en una frase por qué es ese nivel, el
  valor correcto es `pendiente_de_clasificar`.
- Presentar el mapeo a EU AI Act / NIST como equivalencia jurídica. Es referencia comparada; el marco
  peruano y el europeo no son intercambiables.
- Clasificar como `minimo` por defecto cuando falta información — para eso está `pendiente_de_clasificar`.

**Nota pendiente del esquema.** `docs/esquema/sistema.md` deja anotado que faltan tres campos para la
versión 1.1.0: `mapeo_iso_42001`, `datos` y `limitaciones` (los dos últimos, para que la ficha siga la
lógica de una *model card*). Si se agregan al esquema antes de correr este agente, entran en su alcance.

---

### 5.3 `verificador-cumplimiento` — prioridad 1, con fecha

**Problema que resuelve.** Es lo que convierte al proyecto en observatorio y no en catálogo. Hoy las
**252 obligaciones** (42 entidades × 6) están en `no_verificable_desde_fuentes_publicas` — el valor por
defecto de la carga inicial. Ninguna ha sido verificada de verdad.

**Por qué es un agente y no un extractor.** Se intentó como scraper y no funciona: no existe un índice
centralizado de Planes de Gobierno Digital ni de políticas institucionales de IA. Cada entidad publica lo
suyo en su propio dominio, casi siempre en PDF, sin URL predecible. Los archivos
`extractores/normas_gobpe.py` y `extractores/planes_gobierno_digital.py` documentan este callejón sin
salida en sus docstrings. Es trabajo de investigación, no de raspado.

**Urgencia.** El primer tramo del cronograma del reglamento vence el **10 de setiembre de 2026**. El panel
de cumplimiento del sitio ya muestra la cuenta regresiva contra ese conteo — hoy dice 0 de 252 cumplidas,
que es literalmente cierto pero refleja falta de verificación, no incumplimiento del Estado. Cerrar esa
brecha antes de la fecha es lo que da valor al primer informe anual (`docs/estrategia.md` §6, previsto
para octubre de 2026).

**Entrada.** Una entidad por vez, de `datos/entidades/*.yaml`. Priorizar entidades con sistemas
confirmados en operación y con sistemas de riesgo alto.

**Proceso, por cada una de las 6 obligaciones:**
1. Buscar en el portal de la entidad en `gob.pe`, su sección de normas legales y su portal de
   transparencia: resoluciones, políticas institucionales de IA, Plan de Gobierno Digital.
2. Para "código fuente publicado": consultar la Plataforma Nacional de Software Público
   (`softwarepublico.gob.pe`). **Ojo:** ya está verificado que el catálogo declara una "Licencia" como
   texto pero **no enlaza a repositorios**. Estar registrado ahí ≠ haber publicado el código. Solo cuenta
   como `cumplido_con_evidencia` si hay enlace real a un repositorio.
3. Registrar el estado con evidencia y, cuando aplique, la fecha límite del cronograma.

**Salida:** `obligaciones[].estado`, `obligaciones[].fecha_limite`, `obligaciones[].evidencia`.

**Lo que NO debe hacer — lo más importante de todo el documento:**
> No encontrar la política institucional de una entidad **no significa** que no la tenga. Significa que no
> es verificable desde fuentes públicas. Ese es el estado correcto y se usa sin timidez. Escribir
> `no_cumplido` sin evidencia positiva de incumplimiento convierte el registro en una acusación
> infundada y destruye su credibilidad de un solo golpe.

**Nota técnica.** `www.gob.pe` tiene protección anti-bot. Deja pasar peticiones con un User-Agent de
Chrome completo, pero bloquea navegadores headless y User-Agents genéricos. El cliente
`extractores/comun/http_cliente.py` ya tiene la cabecera correcta configurada; reutilizarlo.

---

### 5.4 `descubridor-sistemas` — prioridad 2

**Problema que resuelve.** La detección por contrataciones tiene un techo medido: en la Fase 0 se
comprobó que solo **~45%** de los sistemas conocidos se encuentran buscando su nombre en contrataciones
públicas. El resto se desarrolla internamente o se contrata con una descripción genérica. Durante la
verificación de julio 2026 apareció por accidente un asistente de RENIEC llamado **"Renata"** que no está
en el registro — evidencia directa de que el hueco es real.

**Cuándo se invoca.** Periódicamente, sin urgencia. Es expansión de cobertura, no relleno de campos vacíos.

**Proceso.** Buscar anuncios de sistemas de IA del Estado peruano en prensa seria, comunicados
institucionales y portales de entidades; contrastar contra los sistemas ya registrados; proponer altas
nuevas con `nivel_confianza: reportado_prensa` o `confirmado_fuente_oficial` según la fuente.

**Lo que NO debe hacer.** Dar de alta un sistema por una sola mención de prensa sin fuente institucional
que la respalde. Y respetar el fuera de alcance: nada de gobiernos locales.

---

## 6. Lo que NO debe ser un agente

**Verificador de enlaces rotos.** Es un bucle sobre las URLs de `evidencia` con una petición HEAD. Un
modelo ahí es desperdicio puro. Va como script (`historial/verificar_enlaces.py`) y, si se quiere, como
paso del workflow semanal de GitHub Actions.

Ya hay un hallazgo real que justifica tenerlo: la propia API del OECE devuelve, en algunas releases
históricas, URLs con el dominio `osce.gob.pe`, que ya no resuelve. Se corrigieron 5 casos y se normalizó
el dominio en el extractor, pero el chequeo periódico conviene igual — el anexo del prompt original
advierte que la PLADICOP está reemplazando progresivamente al SEACE, así que las fuentes van a cambiar de
estructura.

---

## 7. Cómo saber qué está pendiente (cola de trabajo)

Para que los agentes no dependan de que alguien recuerde qué falta, conviene un script pequeño que
imprima la cola. Sugerencia de implementación en la misma sesión:

`historial/pendientes.py` → imprime, leyendo los YAML:
- sistemas con `nivel_confianza == "inferido_contratacion"` → cola de `verificador-sistemas`
- sistemas con `clasificacion_riesgo_propia == "pendiente_de_clasificar"` → cola de `clasificador-riesgo`
- entidades con obligaciones en `no_verificable_desde_fuentes_publicas` → cola de `verificador-cumplimiento`
- fecha de la última corrida de cada extractor (leer `datos/crudos/_estado_extractores.json`)

Esto sirve además para `docs/retomar.md`, que `docs/estrategia.md` §7 pide y que todavía no existe:
volver al proyecto en frío después de tres meses debería ser correr un comando y ver qué falta.

---

## 8. Orden de implementación sugerido

1. **`historial/pendientes.py`** — primero la cola. Sin ella no se sabe sobre qué corren los agentes.
2. **`clasificador-riesgo`** — el más autocontenido: no necesita web, solo aplicar criterios ya escritos
   a datos que ya están. Buen primer agente para validar el formato y el flujo de escritura de YAML.
3. **`verificador-sistemas`** — el de mayor valor recurrente.
4. **`verificador-cumplimiento`** — el más valioso para el producto, y el que tiene fecha (10 de
   setiembre de 2026).
5. **`historial/verificar_enlaces.py`** — script, rápido.
6. **`descubridor-sistemas`** — cuando lo anterior esté rodando.

---

## 9. Cómo probar cada agente antes de darlo por bueno

No dar por bueno un agente hasta que se cumpla esto. La regla del proyecto es evidencia antes que
afirmación, y aplica también al código que lo construye.

1. **Correrlo sobre 2-3 registros, no sobre los 54.** Revisar el diff de Git a mano.
2. **Verificar que el diff sea legible**: si el orden de los campos cambió, el agente no está usando
   `esquema.guardar_sistema()` y hay que corregirlo.
3. **Buscar el error más peligroso**: ¿escribió `no_cumplido` o `en_operacion` en algún caso donde en
   realidad no encontró evidencia? Si pasa una sola vez, el prompt del agente necesita endurecerse antes
   de correrlo sobre el resto.
4. **Reconstruir el sitio** (`cd sitio && npm run build`) para confirmar que los datos siguen siendo
   válidos y ninguna ficha rompe el build.
5. **Anotar en `docs/bitacora.md`** qué se construyó y por qué, incluidos los errores encontrados al
   probar. La bitácora registra decisiones y tropiezos, no solo éxitos.
