# Verificación de terreno

Fecha de captura de toda la evidencia citada aquí: 26 de julio de 2026.

## 1. ¿Qué contiene realmente `gob.pe/iaperu`?

No se pudo acceder directamente al canal. `www.gob.pe` bloquea peticiones automatizadas: tanto la herramienta de fetch como el navegador reciben una página "Acceso restringido" o un HTTP 418. El `robots.txt` del sitio (`https://www.gob.pe/robots.txt`) solo prohíbe `/admin/` y no restringe el resto, así que el bloqueo es por huella de bot (WAF o desafío por JavaScript), no por política declarada.

Eso ya es un hallazgo para la Fase 2: un extractor en GitHub Actions necesitará cabeceras de navegador realista y reintentos, y aun así puede fallar de forma intermitente.

El contenido se reconstruyó por vía indirecta, con resultados de búsqueda y la descarga directa de un PDF enlazado desde ese canal.

- El canal `iaperu` es un portal de difusión: normativa, índices internacionales, investigación, actividades, cooperación digital y un "catálogo de herramientas de IA". Según los fragmentos indexados, ese catálogo es una lista de herramientas de uso general, del tipo ChatGPT o Copilot, recopilada por la SGTD para servidores públicos. No es un inventario de sistemas de IA desplegados por el Estado.
- Sí existe, colgado desde ese ecosistema, un documento real: "Catálogo de Aplicaciones con Inteligencia Artificial en el Estado Peruano", de la PCM y su Secretaría de Gobierno y Transformación Digital. PDF de 4 páginas, última modificación 10 de junio de 2026: https://cdn.www.gob.pe/uploads/document/file/8238351/6879780-catalogo-de-aplicaciones-con-ia.pdf (página de referencia: https://www.gob.pe/institucion/pcm/informes-publicaciones/6879780-catalogo-de-aplicaciones-con-inteligencia-artificial-en-el-estado-peruano)

Se descargó y leyó completo. Contenido real:

- 24 sistemas en 23 entidades: Ministerio de Trabajo, SUNARP, OSIPTEL, PAIS, IIAP, Biblioteca Nacional, Poder Judicial, JNE, PCM, INSN, SUNASS, MINAM, PRODUCE, INEN, RENIEC, OSINFOR, Hospital Lambayeque, SENACE, Migraciones, MINCETUR, MIDAGRI, MTC, PROINNOVATE y San Gabán S.A.
- Cuatro columnas: N.º, entidad, nombre del aplicativo, finalidad y tecnologías utilizadas.
- No trae enlaces de evidencia por sistema, fecha de captura, proveedor, vínculo contractual, presupuesto, estado de despliegue, clasificación de riesgo, mapeo a EU AI Act o NIST, ni nivel de confianza. Es autorreportado por cada entidad, sin verificación cruzada visible.
- Es un PDF estático, no una base de datos consultable ni versionada. No hay indicio de historial de cambios ni de calendario de actualización. La fecha de modificación de junio de 2026 sugiere al menos una actualización desde su publicación original, pero no hay forma de rastrear qué cambió.

**Conclusión del punto 1.** No existe un inventario vivo ni un registro de cumplimiento. Existe un catálogo estático oficial, más amplio que el de Interfases: 24 sistemas frente a 22, con superposición parcial y algunas altas nuevas (CURIA del Poder Judicial, EleccIA del JNE, YachAIbot de la PCM, Qhali del INSN, ADETOP v2 de OSINFOR, CadEye de Lambayeque, BIANCA de SENACE, LIA del MTC, INNGENIUS de PROINNOVATE y EVA de San Gabán).

Debe incorporarse como tercera fuente de línea base junto a Interfases, precisamente porque el Estado ya declaró esos 24 sistemas. El proyecto puede documentar todo lo que ese catálogo omite: evidencia, riesgo, cumplimiento, estado y presupuesto.

## 2. Plataforma Nacional de Software Público Peruano (PNSSP)

Portal real: `https://www.softwarepublico.gob.pe`. No es `www.gob.pe/14976`, que aparece en algunos resultados indexados y es solo un enlace de orientación. Es un sitio ASP.NET clásico, sin bloqueo de bot detectado.

- Cataloga 106 aplicaciones de más de 37 entidades, organizadas en 10 sectores, con filtro por entidad, sector y tipo de software, y paginación vía `?pag=N` sobre 11 páginas visibles.
- No expone API ni JSON. Es HTML renderizado por ASP.NET clásico, con `pnsp_js_detalle_catalogo()` en JavaScript y sin endpoint accesible. Un extractor tendría que hacer scraping de HTML con paginación, viable pero frágil.
- Hallazgo crítico para el artículo 28.8 del reglamento: las 10 entradas revisadas de 106 no enlazan a un repositorio de código fuente, ni en GitHub ni en GitLab ni equivalente. Solo enlazan a documentación o al detalle interno del portal. Con este portal no se puede verificar automáticamente si una entidad publicó código fuente real conforme al art. 28.8. Solo se puede verificar que registró un software en la plataforma, que es un requisito distinto y más débil.

**Conclusión del punto 2.** La verificación automática del art. 28.8 es parcial. El extractor `pnssp.py` puede confirmar el registro en la plataforma, que es una señal débil. Para confirmar publicación real de código fuente habría que abrir cada ficha de detalle y buscar un enlace de descarga o repositorio, algo a validar en Fase 1.

## 3. ¿Existe ya un registro equivalente?

No se encontró ninguno que cumpla la función descrita en el prompt original: vivo, versionado y con seguimiento de cumplimiento frente a la Ley 31814 y el DS 115-2025-PCM.

- OSPIA, el Observatorio Sector Público e Inteligencia Artificial (`ospia.org`), tiene sede en la Universidad de Cádiz. Es un observatorio académico multidisciplinario. No es un registro de sistemas peruanos ni hace seguimiento normativo peruano.
- No se encontró un tablero público de seguimiento de las obligaciones del reglamento: política institucional aprobada, plan de gobierno digital con proyectos de IA, código fuente publicado, documentación de riesgo alto y supervisión humana. La búsqueda confirma que la SGTD tiene el rol de autoridad técnico-normativa y hace labores de monitoreo, pero no hay evidencia de que publique ese monitoreo como dato abierto.
- El catálogo de Interfases y el catálogo oficial de 24 sistemas son los dos inventarios existentes. Ninguno hace seguimiento de cumplimiento.

**Conclusión del punto 3.** No existe un producto equivalente. El vacío que motiva el proyecto es real.

## Recomendación

Seguir adelante, con dos ajustes al alcance original de la Fase 1, anotados para cuando llegue el momento.

1. Sumar el catálogo oficial de la PCM/SGTD como tercera fuente de línea base, citado igual que Interfases.
2. En `extractores/pnssp.py`, el criterio de "cumplido con evidencia" para el art. 28.8 debe exigir un enlace de código fuente real en la ficha de detalle, no solo presencia en el catálogo. Si no se logra verificar automáticamente, el campo debe quedar en "no verificable desde fuentes públicas".

No hay nada aquí que invalide el proyecto.
