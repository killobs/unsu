# Registro de IA Pública — Perú

*[English version](README.md) · versión en español*

Registro público y versionado de los sistemas algorítmicos y de inteligencia artificial que el Estado peruano compra y despliega, con clasificación de riesgo propia y seguimiento del cumplimiento de la Ley 31814 y su reglamento (DS 115-2025-PCM).

El valor está en el archivo acumulado: comparar a lo largo del tiempo lo que la norma exige contra lo que las entidades hacen. No hay base de datos. Los archivos YAML versionados son la fuente de verdad y el historial de commits hace de historial del producto.

## Qué hay hoy

Estado al 1 de agosto de 2026.

| | |
|---|---|
| Sistemas documentados | 74 |
| Entidades | 47 |
| Presupuesto identificado | S/ 38 636 581,22 en 43 de los 74 |
| Confirmados por fuente oficial | 32 |
| Inferidos de contrataciones | 42 |

Clasificación de riesgo propia: 17 alto, 33 limitado, 22 mínimo, 2 pendientes.
Estado operativo: 29 en operación, 2 piloto, 43 indeterminado.

El hallazgo principal no es el conteo. **De los 74 sistemas, 73 no declaran supervisión humana ni qué tipo de decisión toman.** Los dos campos existen en el esquema desde el primer día. El único que los declara es EleccIA, del Jurado Nacional de Elecciones, y solo porque su propia directiva describe el paso de validación humana.

## Estado del trabajo

Fases 0 a 4 completas: verificación de terreno, prueba de detectabilidad, carga inicial, extractores automáticos con workflows diarios y semanales, capa de historial sobre Git, y sitio público en `sitio/`.

El 27 de julio de 2026 el registro pasó por una depuración completa, ficha por ficha. De 232 candidatos quedaron 74. Lo retirado se conserva en `datos/excluidos.yaml` con su motivo, y los extractores lo respetan para no volver a darlo de alta.

El 31 de julio se reverificó cada afirmación contra su fuente real, y el 1 de agosto se corrigieron los hallazgos de esa revisión: se fusionaron dos fichas de entidad que eran la misma institución (PROINNOVATE), se limpiaron seis fichas cuya nota contradecía su nivel de confianza, y se reemplazaron tres enlaces de evidencia caídos por copias archivadas. El detalle está en `docs/bitacora.md`.

Pendiente del resto de `docs/estrategia.md`: campos `datos` y `limitaciones` en las fichas, y mapeo a EU AI Act y NIST AI RMF.

## Restricciones del proyecto

Costo cero de operación. Sin base de datos. Repositorio público. El hosting es Cloudflare Pages. Sin secretos en el repositorio. Cada afirmación lleva evidencia con fecha de captura. Interfaz bilingüe español e inglés.

## Estructura

```
registro-ia-publica/
├── .github/workflows/
│   ├── captura-diaria.yml
│   ├── captura-semanal.yml
│   └── verificacion.yml           esquema, pruebas y compilación del sitio
├── extractores/
│   ├── oece_contrataciones.py     detección por términos en contrataciones (activo)
│   ├── enriquecer_oece.py         vuelve a la fuente por proveedor, categoría y montos
│   ├── pnssp.py                   verificación de publicación de código fuente (activo)
│   ├── normas_gobpe.py            políticas institucionales (pendiente)
│   ├── planes_gobierno_digital.py proyectos declarados por entidad (pendiente)
│   └── comun/                     cliente HTTP, esquema YAML, evidencia, estado de corridas
├── datos/
│   ├── sistemas/                  una ficha YAML por sistema
│   ├── entidades/                 una ficha YAML por entidad, con estado de cumplimiento
│   ├── excluidos.yaml             candidatos descartados a mano, con motivo
│   ├── crudos/                    resultados brutos de barridos y estado de extractores
│   ├── documentos/                PDF archivados con fecha en el nombre
│   ├── linea-base-interfases.csv  22 aplicaciones del catálogo académico, con cita
│   └── linea-base-pcm.csv         24 aplicaciones del catálogo oficial PCM/SGTD, con cita
├── historial/
│   ├── generar_historial.py       diferencias campo por campo desde git log y git show
│   ├── clasificar_riesgo.py       aplica la clasificación de docs/metodologia.md §4
│   └── asignar_plazos.py          tramo del DS 115-2025-PCM por tipo de entidad
├── docs/
│   ├── estrategia.md              para qué existe el proyecto y qué no se negocia
│   ├── metodologia.md             criterios de detección y clasificación (ES/EN)
│   ├── esquema/                   especificación de datos, versionada e independiente
│   ├── retomar.md                 cómo volver al proyecto en frío
│   ├── reuse-for-your-country.md  adaptar el esquema a otra jurisdicción
│   ├── verificacion-terreno.md
│   ├── fase-0-detectabilidad.md
│   └── bitacora.md                decisiones técnicas y su motivo
├── LICENSE                        código, MIT
├── LICENSE-DATOS.md               datos, CC BY-SA 4.0
└── requirements.txt
```

```
sitio/                             Next.js con export estático
├── app/(es)/                      /, /sistemas/[id], /entidades/[id], /metodologia
├── app/(en)/en/                   /en, /en/systems/[id], /en/entities/[id], /en/methodology
├── app/sitemap.js, robots.js      descubrimiento, generados desde los mismos YAML
├── lib/datos.js                   lee datos/*.yaml al compilar
├── lib/diccionario.js             textos de interfaz en ambos idiomas
├── scripts/generar-imagenes.mjs   derivados de la foto del hero y la tarjeta social
└── components/                    cabecera, pie, panel de cumplimiento, índice, fichas
```

Los valores de los datos permanecen en español. Traducir nombres, finalidades y sectores es curaduría aparte. Solo la interfaz es bilingüe.

## Cómo se decide qué entra

Un sistema entra solo si hay al menos una fuente pública citable con fecha de captura.

Los candidatos detectados en contrataciones entran marcados como inferidos, nunca como confirmados. Además deben pasar una comprobación: el texto de la contratación tiene que evidenciar inteligencia artificial por sí mismo, sin apoyarse en el término que disparó la búsqueda. Sin esa comprobación, un término mal elegido llena el registro de ruido. Ocurrió con «mantenimiento predictivo», que es una metodología de mantenimiento industrial anterior a la IA y produjo 74 fichas de mantenimiento de transformadores eléctricos.

Los criterios completos están en `docs/metodologia.md`.

## Desplegar en Cloudflare Pages

Requiere una cuenta de Cloudflare.

1. Conectar el repositorio `killobs/unsu` en el panel de Cloudflare Pages.
2. Directorio raíz del build: `sitio`
3. Comando de build: `npm run build`
4. Directorio de salida: `out`
5. Variable de entorno `SITIO_URL` con la URL pública final (sin barra al final). Sin ella el sitemap y las etiquetas Open Graph apuntan al dominio `*.pages.dev` por defecto.

Cada push a `main`, incluidos los commits automáticos de captura, redespliega el sitio con los datos vigentes.

## Esquema de datos

Especificación versionada e independiente en [docs/esquema/](docs/esquema/), pensada para que otra jurisdicción pueda adoptarla sin depender del código de este repositorio. Los criterios de llenado están en [docs/metodologia.md](docs/metodologia.md). Para adaptarlo a otro país, ver [docs/reuse-for-your-country.md](docs/reuse-for-your-country.md).

## Licencia

Licencia dual. El código de `extractores/`, `historial/` y `sitio/` es MIT, en [LICENSE](LICENSE). Los datos de `datos/` son CC BY-SA 4.0, en [LICENSE-DATOS.md](LICENSE-DATOS.md). Usar la línea base de Interfases requiere además su cita académica completa, detallada en ese archivo. La fotografía del sitio tiene su propia licencia CC BY-SA 3.0, también detallada ahí.

## Fuentes

Cada ficha de `datos/sistemas/` lleva sus citas. Las dos líneas base son el catálogo de la PCM/SGTD y el artículo de Huancapaza Hilasaca (2025) en Interfases n.º 22, ambos archivados en `datos/documentos/`. La estrategia y el posicionamiento están en [docs/estrategia.md](docs/estrategia.md).
