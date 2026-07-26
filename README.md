# Registro de IA Pública — Perú

Registro público, versionado y continuo de los sistemas algorítmicos y de inteligencia artificial que el Estado peruano compra y despliega, con clasificación de riesgo propia y seguimiento del cumplimiento de la Ley 31814 y su reglamento (DS 115-2025-PCM).

El valor del proyecto está en el archivo acumulado y en la comparación entre lo que la norma exige y lo que las entidades hacen — no en una fotografía única. El historial de commits de este repositorio es el motor de historial del producto: no hay base de datos.

## Estado actual

- ✅ Verificación de terreno ([docs/verificacion-terreno.md](docs/verificacion-terreno.md))
- ✅ Fase 0 — prueba de detectabilidad ([docs/fase-0-detectabilidad.md](docs/fase-0-detectabilidad.md))
- ✅ Fase 1 — carga inicial: 28 fichas de sistema, 27 fichas de entidad, dos líneas base citadas (Interfases + catálogo PCM) y dos candidatos descubiertos por barrido de contrataciones
- ⏳ Fase 2 — captura automática (GitHub Actions) — no iniciada
- ⏳ Fase 3 — capa de historial (diffs desde Git) — no iniciada
- ⏳ Fase 4 — sitio público (Next.js, Cloudflare Pages) — no iniciada

## Restricciones del proyecto

Costo cero de operación. Sin base de datos. Repositorio público. Nada de Vercel — el hosting es Cloudflare Pages. Sin secretos en el repositorio. Cada afirmación lleva evidencia con fecha de captura. Bilingüe desde el diseño (español/inglés).

## Estructura

```
registro-ia-publica/
├── datos/
│   ├── crudos/                    resultados brutos de barridos (ej. Fase 0)
│   ├── sistemas/                  una ficha YAML por sistema detectado
│   ├── entidades/                 una ficha YAML por entidad, con estado de cumplimiento
│   ├── documentos/                PDF y capturas archivadas con fecha en el nombre
│   ├── linea-base-interfases.csv  22 aplicaciones del catálogo académico de Interfases, con cita
│   └── linea-base-pcm.csv         24 aplicaciones del catálogo oficial PCM/SGTD, con cita
├── docs/
│   ├── verificacion-terreno.md
│   ├── fase-0-detectabilidad.md
│   ├── metodologia.md             criterios de detección y clasificación de riesgo (ES/EN)
│   └── bitacora.md                decisiones técnicas y su motivo
└── README.md
```

Los directorios `extractores/` (captura automática) y `sitio/` (interfaz pública) se crean en las fases 2 y 4, respectivamente — no antes, para no adelantar trabajo sobre premisas aún no confirmadas.

## Esquema de datos

Ver [docs/metodologia.md](docs/metodologia.md) §5-6 para los campos de `datos/sistemas/*.yaml` y `datos/entidades/*.yaml`, en orden determinista para que el diff de Git sea legible.

## Fuentes

Ver la tabla de fuentes en el prompt original del proyecto y las citas dentro de cada ficha de `datos/sistemas/`.
