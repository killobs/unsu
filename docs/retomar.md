# Retomar el proyecto en frío

Este documento existe porque el riesgo identificado en `estrategia.md` §14 es abandonar cuando el proyecto exige demasiado sostenimiento. La máquina sigue capturando sola durante una ausencia; lo que se pierde es el contexto. Esto lo repone.

**Se actualiza al final de cada sesión de trabajo.** Última actualización: 1 de agosto de 2026.

---

## 1. Lo primero: comprobar que la máquina no se detuvo

```bash
python validar_esquema.py --autoprueba && python validar_esquema.py && python pruebas.py
```

Si eso pasa, los datos están sanos. Después, mirar si las capturas siguen corriendo:

- Pestaña **Actions** del repo: `Captura diaria` (04:17 hora Perú) y `Captura semanal` (domingos 03:37).
- `datos/crudos/_estado_extractores.json` guarda la última corrida de cada extractor.
- Si un extractor falla dos corridas seguidas, el workflow abre un issue solo. Revisar issues abiertos antes que nada.

El sitio muestra al público la fecha de la última captura exitosa, así que un parón prolongado es visible desde fuera.

## 2. Estado actual

Fases 0 a 4 completas. El registro tiene 74 sistemas y 47 entidades, con 282 obligaciones bajo seguimiento.

Lo que está corriendo solo:

| Qué | Cuándo | Dónde |
|---|---|---|
| Barrido de contrataciones OECE (años recientes) | diario | `.github/workflows/captura-diaria.yml` |
| Barrido histórico completo 2004-presente | semanal | `.github/workflows/captura-semanal.yml` |
| Esquema, pruebas y compilación del sitio | cada push y PR | `.github/workflows/verificacion.yml` |

Extractores activos: `oece_contrataciones.py`, `enriquecer_oece.py`, `pnssp.py`.
Extractores escritos pero no activados: `normas_gobpe.py`, `planes_gobierno_digital.py`.

## 3. Qué quedó a medias

Del alcance que fija `estrategia.md`:

- **Campos `datos` y `limitaciones` en las fichas de sistema.** El formato de model card los pide (§5.4) y el esquema todavía no los define.
- **Mapeo a EU AI Act y NIST AI RMF.** Los campos existen en el esquema y están vacíos en las 74 fichas.
- **Informe de cumplimiento por entidad, exportable a documento** (§5.5). El sitio muestra el estado por entidad, pero no genera el documento presentable que después se convierte en servicio.
- **Los dos extractores pendientes.** Sin ellos, las obligaciones de política institucional y de plan de gobierno digital solo pueden verificarse a mano.
- **El artículo 28.2 obliga a usar la NTP-ISO/IEC 42001:2025.** En los pendientes figuraba como «mapeo ISO 42001», tratado como comparativo: es exigible, y el seguimiento debería reflejarlo.

Anotaciones de calidad de dato que siguen abiertas (detalle en `bitacora.md`):

- Dos fichas (Smart Churay Yachay, Monitoreo de servidores) están como `confirmado_fuente_oficial` con el artículo de Interfases como única evidencia. Una revista arbitrada no es documento oficial según `metodologia.md` §2.
- `nivel_gobierno` dice `nacional` en las tres universidades, San Gabán, Electrocentro y Fondo Mivivienda. El enum solo admite `nacional | regional` y no da para representarlas. Los plazos no dependen de este campo, pero el dato induce a error.
- La cuenta de días hasta el vencimiento se calcula al compilar. Como la captura solo commitea si cambió algo, en semanas sin cambios el número envejece.

## 4. Siguiente paso

**Publicar.** El sitio está listo y verificado; falta conectar el repositorio en el panel de Cloudflare Pages con la configuración que documenta el README, y definir `SITIO_URL`.

Después de eso, la fecha que manda es el **10 de setiembre de 2026**: vence el primer tramo para 33 de las 47 entidades. El informe anual comprometido en `estrategia.md` §6 se publica en octubre de 2026 midiendo esa situación. Es el único compromiso de calendario del proyecto.

## 5. Dónde está cada cosa

- Por qué existe el proyecto y qué no se negocia → `estrategia.md`
- Criterios de detección y clasificación → `metodologia.md`
- Forma de los datos, como especificación independiente → `esquema/`
- Decisiones técnicas y su motivo, en orden cronológico → `bitacora.md`
- Qué se probó y no funcionó → `fase-0-detectabilidad.md`, `verificacion-terreno.md`
- Cómo adaptar esto a otro país → `reuse-for-your-country.md`

## 6. Reglas que no se negocian, por si se olvidan

1. Sin evidencia no hay ficha.
2. «No verificable desde fuentes públicas» nunca se convierte en «no cumplido» sin evidencia positiva de incumplimiento.
3. Una inferencia de contratación nunca se asciende a confirmada sin fuente oficial adicional.
4. La clasificación de riesgo y el tramo de plazo se declaran siempre como propios del proyecto, no oficiales.
5. Sin adjetivos valorativos sobre entidades ni funcionarios. Esto es un observatorio técnico, no activismo.
