# Verificación de terreno

Fecha de captura de toda la evidencia citada aquí: 26 de julio de 2026.

## 1. ¿Qué contiene realmente `gob.pe/iaperu`?

**No se pudo acceder directamente al canal.** `www.gob.pe` bloquea peticiones automatizadas: tanto la herramienta de fetch como el navegador reciben una página "Acceso restringido" o un HTTP 418, aunque el `robots.txt` del sitio (`https://www.gob.pe/robots.txt`) solo prohíbe `/admin/` y no restringe el resto — el bloqueo es por huella de bot (WAF/JS challenge), no por política declarada. **Esto es en sí mismo un hallazgo relevante para la Fase 2**: un extractor en GitHub Actions probablemente necesitará cabeceras de navegador realista y reintentos, y aun así puede fallar de forma intermitente.

Reconstruí el contenido por vía indirecta (resultados de búsqueda + descarga directa de un PDF enlazado desde ese canal, con tu autorización). Conclusión:

- El canal `iaperu` es un **portal de difusión**: normativa, índices internacionales, investigación, actividades, cooperación digital y un "catálogo de herramientas de IA" — que, según los fragmentos indexados, es una lista de herramientas de IA de uso general (tipo ChatGPT/Copilot) recopilada por la SGTD para servidores públicos, **no** un inventario de sistemas de IA desplegados por el Estado.
- Sí existe, colgado desde ese ecosistema, un documento real: **"Catálogo de Aplicaciones con Inteligencia Artificial en el Estado Peruano"** (PCM — Secretaría de Gobierno y Transformación Digital), PDF de 4 páginas, última modificación 10 de junio de 2026: https://cdn.www.gob.pe/uploads/document/file/8238351/6879780-catalogo-de-aplicaciones-con-ia.pdf (página de referencia: https://www.gob.pe/institucion/pcm/informes-publicaciones/6879780-catalogo-de-aplicaciones-con-inteligencia-artificial-en-el-estado-peruano)

Lo descargué y leí completo. Contenido real:

- **24 sistemas, 23 entidades** (Ministerio de Trabajo, SUNARP, OSIPTEL, PAIS, IIAP, Biblioteca Nacional, Poder Judicial, JNE, PCM, INSN, SUNASS, MINAM, PRODUCE, INEN, RENIEC, OSINFOR, Hospital Lambayeque, SENACE, Migraciones, MINCETUR, MIDAGRI, MTC, PROINNOVATE, San Gabán S.A.).
- Cuatro columnas únicamente: N°, Entidad, Nombre del aplicativo, Finalidad, Tecnologías utilizadas.
- **No tiene**: enlaces de evidencia por sistema, fecha de captura, proveedor/vínculo contractual, presupuesto, estado (operación/piloto/descontinuado), clasificación de riesgo, mapeo a EU AI Act/NIST, ni nivel de confianza. Es autorreportado por cada entidad, sin verificación cruzada visible.
- Es un **PDF estático**, no una base de datos consultable ni versionada. No hay indicio de historial de cambios ni de que se actualice con calendario fijo — la fecha de modificación (junio 2026) sugiere que hay al menos una actualización desde su publicación original, pero no hay forma de rastrear qué cambió.

**Conclusión del punto 1:** no existe un inventario vivo ni un registro de cumplimiento. Existe un catálogo estático oficial más amplio que el de Interfases (24 vs. 22, con alguna superposición y algunas altas nuevas: CURIA del Poder Judicial, EleccIA del JNE, YachAIbot de la PCM, Qhali del INSN, ADETOP v2 de OSINFOR, CadEye de Lambayeque, BIANCA de SENACE, LIA del MTC, INNGENIUS de PROINNOVATE, EVA de San Gabán). **Debe incorporarse como tercera fuente de línea base**, junto a Interfases, precisamente porque el Estado ya declaró estos 24 sistemas — y el proyecto puede documentar todo lo que ese catálogo oficial omite (evidencia, riesgo, cumplimiento, estado, presupuesto).

## 2. Plataforma Nacional de Software Público Peruano (PNSSP)

Portal real: `https://www.softwarepublico.gob.pe` (no `www.gob.pe/14976` como aparece en algunos resultados indexados, ese es solo un enlace de orientación). Es un sitio ASP.NET clásico, sin bloqueo de bot detectado.

- Cataloga **106 aplicaciones de +37 entidades**, organizadas en 10 sectores, con filtro por entidad, sector y tipo de software, y paginación vía `?pag=N` (11 páginas visibles).
- **No es API/JSON** — es HTML renderizado por ASP.NET clásico (`pnsp_js_detalle_catalogo()` en JS, sin endpoint expuesto). Un extractor tendría que hacer scraping de HTML con paginación, viable pero frágil.
- **Hallazgo crítico para el artículo 28.8 del reglamento:** las entradas revisadas (10 de 106) **no enlazan a repositorio de código fuente** (GitHub/GitLab ni equivalente) — solo a documentación o al detalle interno del portal. Esto significa que **no se puede verificar automáticamente, solo con este portal, si una entidad publicó código fuente real conforme al art. 28.8**; solo se puede verificar que la entidad *registró* un software en la plataforma, que es un requisito distinto y más débil que "publicó el código fuente".

**Conclusión del punto 2:** la verificación automática de cumplimiento del art. 28.8 es parcial. El extractor `pnssp.py` puede confirmar registro en la plataforma (señal débil), pero para confirmar publicación real de código fuente habría que abrir cada ficha de detalle y buscar un enlace de descarga/repositorio — a validar en Fase 1, no antes.

## 3. ¿Existe ya un registro equivalente?

No encontré ninguno que cumpla la función descrita en el prompt (vivo, versionado, con seguimiento de cumplimiento normativo frente a la Ley 31814/DS 115-2025-PCM):

- **OSPIA** (Observatorio Sector Público e Inteligencia Artificial, `ospia.org`) — con sede en la Universidad de Cádiz, España. Es un observatorio académico multidisciplinario, no un registro de sistemas peruanos ni hace seguimiento normativo peruano.
- No se encontró un tablero público de seguimiento de las obligaciones del reglamento (política institucional aprobada, PGD con proyectos de IA, código fuente publicado, documentación de riesgo alto, supervisión humana). La búsqueda confirma que la SGTD tiene el rol de autoridad técnico-normativa y hace "labores de monitoreo", pero no hay evidencia de que publique ese monitoreo como dato abierto o tablero público.
- El catálogo de Interfases (línea base académica ya prevista en el prompt) y el catálogo oficial de 24 sistemas (punto 1) son los dos inventarios existentes; ninguno hace seguimiento de cumplimiento.

**Conclusión del punto 3:** no existe un producto equivalente. El vacío que motiva el proyecto es real.

## Recomendación

**Seguir adelante**, con dos ajustes al alcance original de la Fase 1 (sin adelantar trabajo, solo dejarlo anotado para cuando llegue):

1. Sumar el catálogo oficial PCM/SGTD de 24 sistemas como tercera fuente de línea base (`datos/linea-base-pcm.csv` o similar), citado igual que Interfases.
2. En `extractores/pnssp.py`, el criterio de "cumplido con evidencia" para el art. 28.8 debe exigir encontrar un enlace de código fuente real en la ficha de detalle, no solo presencia en el catálogo — si no se logra verificar automáticamente, ese campo debe quedar en "no verificable desde fuentes públicas", conforme a tu regla del punto 6.

No hay nada aquí que invalide el proyecto. Quedo a la espera de tu decisión para pasar a la Fase 0 (prueba de detectabilidad sobre contrataciones OCDS).
