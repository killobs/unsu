# Registro de IA Pública — Perú

Registro público, versionado y continuo de los sistemas algorítmicos y de inteligencia artificial que el Estado peruano compra y despliega, con clasificación de riesgo propia y seguimiento del cumplimiento de la Ley 31814 y su reglamento (DS 115-2025-PCM).

El valor del proyecto está en el archivo acumulado y en la comparación entre lo que la norma exige y lo que las entidades hacen — no en una fotografía única. El historial de commits de este repositorio es el motor de historial del producto: no hay base de datos.

## Estado actual

- ✅ Verificación de terreno ([docs/verificacion-terreno.md](docs/verificacion-terreno.md))
- ✅ Fase 0 — prueba de detectabilidad ([docs/fase-0-detectabilidad.md](docs/fase-0-detectabilidad.md))
- ✅ Fase 1 — carga inicial: 28 fichas de sistema, 27 fichas de entidad, dos líneas base citadas (Interfases + catálogo PCM) y dos candidatos descubiertos por barrido de contrataciones
- ✅ Fase 2 — captura automática: extractores para OECE y PNSSP, workflows diarios/semanales, alertas automáticas por fallo repetido. `normas_gobpe.py` y `planes_gobierno_digital.py` documentados como pendientes (sin índice centralizado que scrapear, ver `docs/bitacora.md`)
- ✅ Fase 3 — capa de historial: `historial/generar_historial.py` lee `git log`/`git show` y compara los YAML ya parseados campo por campo (incluida una comparación por clave natural para `obligaciones` y `evidencia`, no por bloque completo) — no reimplementa diffing de texto, esa parte la sigue haciendo Git
- ✅ Fase 4 — sitio en `sitio/` (Next.js 16, App Router, export estático): índice filtrable por sector/riesgo/nivel de confianza, ficha por sistema, ficha por entidad con sus obligaciones, panel de cumplimiento con cuenta regresiva al 10 de setiembre de 2026, bilingüe (es/en). **Falta conectar el hosting en Cloudflare Pages** — eso requiere tu cuenta, ver abajo.
- ✅ Bloque "fundacionales" de [docs/estrategia.md](docs/estrategia.md): licencia dual, esquema publicado como especificación independiente, dataset completo descargable en un solo archivo, campo de jurisdicción. **Pendientes del resto de la estrategia** (README en inglés formato estudio de caso, model cards completas, mapeo ISO 42001, informe de cumplimiento exportable, guía de reutilización, `docs/retomar.md`, estado de última captura visible en el sitio) — ver la auditoría completa en `docs/bitacora.md`, entrada del 2026-07-26.

## Restricciones del proyecto

Costo cero de operación. Sin base de datos. Repositorio público. Nada de Vercel — el hosting es Cloudflare Pages. Sin secretos en el repositorio. Cada afirmación lleva evidencia con fecha de captura. Bilingüe desde el diseño (español/inglés).

## Estructura

```
registro-ia-publica/
├── .github/workflows/
│   ├── captura-diaria.yml
│   └── captura-semanal.yml
├── extractores/
│   ├── oece_contrataciones.py     detección por términos en contrataciones (activo)
│   ├── pnssp.py                   verificación de publicación de código fuente (activo)
│   ├── normas_gobpe.py            políticas institucionales (pendiente, ver docs/bitacora.md)
│   ├── planes_gobierno_digital.py proyectos de IA declarados por entidad (pendiente, ídem)
│   └── comun/                     cliente HTTP, esquema YAML, evidencia, estado de corridas
├── datos/
│   ├── crudos/                    resultados brutos de barridos y estado de extractores
│   ├── sistemas/                  una ficha YAML por sistema detectado
│   ├── entidades/                 una ficha YAML por entidad, con estado de cumplimiento
│   ├── documentos/                PDF y capturas archivadas con fecha en el nombre
│   ├── linea-base-interfases.csv  22 aplicaciones del catálogo académico de Interfases, con cita
│   └── linea-base-pcm.csv         24 aplicaciones del catálogo oficial PCM/SGTD, con cita
├── docs/
│   ├── estrategia.md               para qué existe el proyecto y qué decisiones no se toman en contra
│   ├── verificacion-terreno.md
│   ├── fase-0-detectabilidad.md
│   ├── metodologia.md              criterios de detección y clasificación de riesgo (ES/EN)
│   ├── esquema/                    especificación de datos, versionada e independiente (ES/EN)
│   └── bitacora.md                 decisiones técnicas y su motivo
├── LICENSE                         código, MIT
├── LICENSE-DATOS.md                datos, CC BY-SA 4.0 (ES/EN)
├── requirements.txt
└── README.md
```

```
sitio/                             Next.js, export estático (Fase 4)
├── app/(es)/                      árbol en español: /, /sistemas/[id], /entidades/[id], /metodologia
├── app/(en)/en/                   árbol en inglés: /en, /en/systems/[id], /en/entities/[id], /en/methodology
├── lib/datos.js                   lee datos/*.yaml en tiempo de build (sin base de datos, igual que el resto)
├── lib/diccionario.js             textos de interfaz en ambos idiomas (los VALORES de los datos siguen en español)
└── components/                    Cabecera, Pie, PanelCumplimiento, IndiceCliente (filtros), fichas
```

Los valores de los datos (nombres, finalidades, sectores) permanecen en español — traducirlos es curaduría aparte, no de esta fase. Solo la interfaz (navegación, encabezados, etiquetas de estado) es bilingüe.

### Desplegar en Cloudflare Pages

Esto necesita tu cuenta de Cloudflare, no lo puedo hacer yo:

1. En el dashboard de Cloudflare Pages, conectar el repositorio `killobs/unsu`.
2. Directorio raíz del build: `sitio`
3. Comando de build: `npm run build`
4. Directorio de salida: `out`

Cada push a `main` (incluidos los commits automáticos de captura diaria/semanal) va a redesplegar el sitio con los datos más recientes.

## Esquema de datos

Especificación versionada e independiente en [docs/esquema/](docs/esquema/) — pensada para que alguien pueda adoptarla en otro país, no solo para documentar este repositorio. Ver también [docs/metodologia.md](docs/metodologia.md) §5-6 para los criterios de llenado.

## Licencia

Licencia dual: el **código** (`extractores/`, `sitio/`, `historial/`) es MIT — ver [LICENSE](LICENSE). Los **datos** (`datos/`) son CC BY-SA 4.0 (atribución + compartir igual) — ver [LICENSE-DATOS.md](LICENSE-DATOS.md). Cualquier uso de la línea base de Interfases requiere además su cita académica completa, detallada en ese mismo archivo.

## Fuentes

Ver la tabla de fuentes en el prompt original del proyecto y las citas dentro de cada ficha de `datos/sistemas/`. La estrategia y las decisiones de posicionamiento del proyecto están en [docs/estrategia.md](docs/estrategia.md).
