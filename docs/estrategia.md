# Usnu · Registro de IA Pública — Estrategia y artefactos

Versión 1.0 · 26 de julio de 2026 · Destino en el repositorio: `docs/estrategia.md`

> **Cómo usar este documento.** Complementa al prompt de construcción (`usnu-prompt-claude-code-registro-ia-v1.md`), no lo reemplaza. Aquel dice qué construir; este dice para qué existe y qué decisiones no se pueden tomar en contra. Claude Code debe leerlo antes de proponer arquitectura o funcionalidades, y consultarlo cuando una decisión técnica tenga implicancia de posicionamiento.
>
> Contiene dos partes claramente separadas: lo que ejecuta Claude Code y lo que ejecuta solo Bernardo. La segunda parte está incluida para que las decisiones técnicas no la contradigan, no para que se ejecute.

---

# Parte A. Lo que ejecuta Claude Code

## 1. Regla económica fundacional

**Se publica todo lo que se observa. Se cobra todo lo que se produce.**

Lo observado son los datos extraídos de fuentes oficiales. Son públicos, abiertos y completos, sin retención ni retraso.

Lo producido son los análisis, informes y evaluaciones firmadas. Eso no vive en el repositorio.

Consecuencias técnicas directas, que no se discuten:

- No se implementa autenticación, muro de pago ni registro de usuarios en la versión 1.
- No se publica con retraso deliberado. Nada de datos frescos para suscriptores y datos viejos para el público.
- No se degrada la versión pública para hacer atractiva una versión paga.
- El conjunto de datos completo es descargable en un solo archivo, sin fricción.

El motivo: el retorno principal de este proyecto es reputacional y laboral. Ese retorno se produce cuando otros citan el trabajo, y se cita lo que es gratis y verificable. Cerrar el acceso para proteger un ingreso marginal cambia el retorno principal por el accesorio.

## 2. Suscripción: diferida, con condiciones explícitas

No se construye ahora. No es hipótesis fundacional.

Condiciones para reconsiderarla, todas simultáneas:

1. Existe demanda expresa, no supuesta: personas que pidieron alertas sin que se les ofreciera.
2. El registro tiene al menos un año de historial acumulado.
3. La función a cobrar es atención o producción, nunca acceso al dato.

Si se activa alguna vez, lo cobrable es la vigilancia (aviso cuando cambia algo que le importa a alguien) y el artefacto producido (informe con firma). Nunca la consulta del registro.

## 3. Qué sostiene el valor cuando todo el dato es público

Orden de solidez, de mayor a menor. Sirve para evaluar cualquier idea futura de monetización.

1. **La firma.** Un conjunto de datos abierto no tiene responsable. Un informe con autor, metodología y fecha, que un oficial de cumplimiento puede adjuntar a un descargo, sí lo tiene.
2. **La atención.** El dato público no avisa a nadie cuándo cambió algo relevante.
3. **El artefacto producido**, distinto del dato observado.
4. **Los insumos no públicos:** solicitudes de acceso a la información tramitadas, respuestas de entidades, correcciones enviadas por responsables. Ese corpus se genera, no se raspa.
5. **La latencia.** Última carta y no recomendada: roza el posicionamiento de transparencia.

Nota realista: en 2026 la comodidad de consumir datos ya no es defendible. Cualquiera puede apuntar un modelo al repositorio y obtener la tabla que quiera. Ninguna estrategia debe apoyarse en que el CSV crudo es incómodo.

## 4. Licencia y estándar abierto

- **Datos:** licencia abierta con cláusula de compartir igual. Quien construya un producto comercial encima queda obligado a abrir el suyo. No es un muro, porque cualquiera puede volver a raspar las fuentes originales, pero fija una norma y desincentiva la copia perezosa.
- **Código:** licencia permisiva.
- **Esquema de datos:** se publica como especificación abierta, versionada e independiente del conjunto de datos, en `docs/esquema/`. Debe poder ser adoptada por alguien que quiera construir un registro equivalente en otro país.
- **Atribución obligatoria** a la línea base académica de Interfases donde se use.

El esquema publicado como especificación es una decisión estratégica, no de formato. Si otra organización lo adopta, la autoría deja de ser la de un conjunto de datos peruano y pasa a ser la de un estándar regional.

## 5. Artefactos que el repositorio debe producir

Estos no son documentación interna, son el producto visible y la credencial profesional. Se construyen con el mismo cuidado que el código.

### 5.1 README en inglés, formato estudio de caso

El artefacto más importante del repositorio. Nadie va a leer el código; van a leer el README y decidir en veinte minutos.

Requisitos:

- Escrito en inglés, con versión en español en `README.es.md`.
- Formato de estudio de caso: el problema, el marco normativo, el método, los hallazgos, las limitaciones. No documentación de instalación.
- Enlaza directamente a tres artefactos concretos: la matriz de clasificación de riesgo, una ficha de sistema completa, y un informe de cumplimiento de una entidad.
- Declara explícitamente qué es inferencia y qué es hecho confirmado.
- Incluye las limitaciones del método. Un README que no declara limitaciones lee como marketing y resta credibilidad ante cualquier lector técnico.

### 5.2 Metodología bilingüe

`docs/metodologia.md` y `docs/methodology.md`. Criterios de detección, criterios de clasificación de riesgo, niveles de confianza, reglas de evidencia. Publicada, versionada y abierta a corrección.

### 5.3 Matriz de clasificación de riesgo

Documento y estructura de datos. Clasificación bajo el marco peruano, con columnas de mapeo equivalente a EU AI Act, NIST AI RMF e ISO 42001. Etiquetada en todas partes como clasificación propia, no oficial.

### 5.4 Ficha de sistema con estructura de model card

El formato de la ficha debe seguir la lógica de una model card reconocible internacionalmente: propósito, datos, decisiones que toma, supervisión humana, limitaciones, evidencia. Un lector del campo debe reconocer el formato de inmediato.

### 5.5 Informe de cumplimiento por entidad, generado

Plantilla que produce, desde los datos, un documento presentable por entidad: obligaciones aplicables, estado de cada una, evidencia, fechas límite. Exportable a formato de documento.

Este es el artefacto que después se convierte en servicio pagado. Generarlo automáticamente para el sector público es lo que demuestra que se puede producir a medida para un cliente privado.

### 5.6 Guía de reutilización

`docs/reuse-for-your-country.md`, en inglés. Cómo adaptar el esquema y los extractores a otra jurisdicción. Es lo que convierte el proyecto en referencia y no en caso aislado.

## 6. Cadencia de publicación

**Un informe de estado de cumplimiento al año, publicado siempre en el mismo mes.**

El primero en octubre de 2026, midiendo la situación tras el vencimiento del 10 de setiembre de 2026.

No se compromete boletín mensual ni semanal. Los índices recurrentes se vuelven referencia obligada por repetición, no por frecuencia. Un informe anual sólido durante cuatro años pesa más que un boletín mensual abandonado en el tercer mes.

Entre informes anuales se publica cuando hay algo que decir, no por calendario.

## 7. Resiliencia al abandono

Requisito de diseño, no aspiración. El sistema debe seguir capturando aunque nadie lo toque durante meses, porque el archivo acumulado es el activo y cada día sin capturar se pierde para siempre.

Obligaciones técnicas:

- Los flujos de captura no requieren intervención manual en ninguna circunstancia normal.
- Si un extractor falla dos corridas seguidas, se abre un issue automáticamente.
- Si todos los extractores fallan, el sistema lo hace evidente en el propio sitio, con la fecha de la última captura exitosa visible al público.
- `docs/retomar.md`: instrucciones para volver al proyecto en frío después de tres meses sin tocarlo. Estado actual, qué está corriendo, qué quedó a medias, siguiente paso.

Ese último documento se actualiza al final de cada sesión de trabajo. Es tan importante como la bitácora.

## 8. Tono y reglas editoriales

El proyecto es un observatorio técnico. No es activismo.

- Sin adjetivos valorativos sobre entidades ni funcionarios.
- Nunca afirmar incumplimiento cuando lo que hay es ausencia de evidencia pública. El estado "no verificable desde fuentes públicas" existe precisamente para eso y debe usarse sin timidez.
- Toda afirmación con enlace a fuente y fecha de captura.
- La clasificación de riesgo se presenta siempre como propia y corregible.
- Nada de especulación sobre capacidades no documentadas, con cuidado especial en sistemas de seguridad, vigilancia o defensa.

Motivo práctico, además del ético: si el proyecto se percibe como activismo, cierra puertas laborales en el sector privado y en el propio Estado. La misma disciplina que hace creíble el dato es la que lo hace contratable a su autor.

## 9. Diseño preparado para el segundo acto

El segundo acto, si el registro peruano funciona, es la vista comparativa regional: Chile, Colombia, Brasil, México. No se construye ahora, pero hoy se toman tres decisiones baratas que después serían caras:

1. **Campo de jurisdicción presente en el esquema desde el inicio**, aunque solo tenga un valor.
2. **Sin supuestos peruanos incrustados** en nombres de campos, rutas ni identificadores. Nada de campos llamados `entidad_pcm` o similares.
3. **Internacionalización del sitio prevista en la estructura**, aunque la versión 1 solo tenga dos idiomas.

## 10. Anti alcance permanente

No se construye, aunque parezca natural o alguien lo pida:

- Muro de pago, autenticación o suscripción en la versión 1.
- Publicación diferida de datos.
- Auditoría técnica del desempeño interno de modelos. El registro documenta lo declarado y lo contrasta con lo exigido.
- Gobiernos locales, mientras sus plazos normativos sigan a tres años o más.
- Boletín periódico de alta frecuencia.
- Cualquier función que exija cerrar datos para tener sentido.

---

# Parte B. Lo que ejecuta solo Bernardo

Incluido para contexto. Claude Code no ejecuta nada de esta sección, pero ninguna decisión técnica debe contradecirla.

## 11. La fuente de ingreso real

No es la suscripción. Es consultoría especializada al sector privado regulado: evaluaciones de conformidad, análisis de brecha contra ISO 42001, capacitación y asesoría. Se cobra en miles, no en decenas, y se le vende a empresas privadas, no al Estado.

**El nicho concreto:** gobernanza de IA aplicada a entidades financieras peruanas supervisadas por la SBS. El primer tramo del cronograma vence el 10 de setiembre de 2026 e incluye economía y finanzas. La combinación de experiencia previa documentando controles bajo COBIT y normativa SBS con conocimiento del marco de IA es poco común en el país.

El registro público no vende ese servicio. Es la credencial que hace que llamen.

## 12. Difusión y citas

- Contacto temprano con los autores del catálogo de Interfases, antes de publicar. Citarlos bien cuesta nada y da un aliado académico; publicar sin avisar convierte en competencia.
- Hiperderecho en Perú y Derechos Digitales en la región, como amplificadores naturales.
- Registro del proyecto en observatorios internacionales de política de IA. Perú tiene demanda de atención por ser el primer país de la región con ley específica.
- Publicación académica con DOI, propia o en coautoría. Credencial permanente y citable.

## 13. Credenciales en paralelo

Cerrar la certificación de ISO 42001 mientras el proyecto corre. Certificado sin trabajo aplicado es débil; trabajo aplicado sin certificado no pasa filtros automáticos de selección. Juntos son fuertes.

## 14. Riesgo personal identificado

El antecedente es abandonar cuando el proyecto exige demasiado sostenimiento.

Aquí eso pesa menos, porque la captura automatizada sigue corriendo sola y el archivo se acumula igual durante una ausencia. Esa propiedad debe aprovecharse conscientemente: no imponerse cadencias de publicación, no comprometer entregas periódicas, y volver cuando haya algo que decir.

La única obligación real es que la máquina no se detenga.
