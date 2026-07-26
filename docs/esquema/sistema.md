# Ficha de sistema / System record

Versión 1.0.0 · parte de la [especificación de esquema](README.md)

*English below.*

## Español

Cada sistema de IA detectado es un registro con estos campos. La implementación de referencia los escribe en
este orden, en `datos/sistemas/{id}.yaml`.

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `id` | string | sí | Identificador estable, único dentro del registro. No debe reutilizarse aunque el sistema se dé de baja. |
| `entidad_id` | string | sí | Referencia al `id` de la ficha de entidad responsable. |
| `nombre` | string | sí | Nombre del sistema o aplicativo, tal como lo nombra la fuente. |
| `sector` | string | sí | Sector de política pública (salud, justicia, educación...). Vocabulario libre, no una lista cerrada. |
| `nivel_gobierno` | enum | sí | `nacional` \| `regional`. Los gobiernos locales están fuera de alcance mientras sus plazos normativos sigan a tres años o más (ver `docs/estrategia.md` §10). |
| `finalidad` | string | no | Qué hace el sistema, en lenguaje llano — el equivalente a "propósito" de una model card. |
| `tipo_decision` | string | no | Qué decisión toma o asiste el sistema, y sobre quién. |
| `supervision_humana_declarada` | enum | no | `si` \| `no` \| `no_declarado`. |
| `proveedor` | string | no | Proveedor o desarrollador, si está identificado. |
| `vinculo_contractual` | string | no | Referencia al contrato o proceso de contratación, si existe. |
| `presupuesto` | string | no | Monto asociado, si se conoce. String, no número — para poder registrar moneda y evitar redondeos falsos. |
| `estado` | enum | sí | `en_operacion` \| `piloto` \| `contratado_sin_desplegar` \| `descontinuado` \| `indeterminado`. |
| `tecnologias` | string | no | Tecnologías declaradas (NLP, visión computacional, modelo específico...). |
| `clasificacion_riesgo_propia` | enum | sí | `alto` \| `limitado` \| `minimo` \| `pendiente_de_clasificar`. Clasificación propia del proyecto, nunca presentada como oficial. Criterios en `docs/metodologia.md`. |
| `mapeo_eu_ai_act` | string | no | Nivel de riesgo equivalente bajo el Reglamento (UE) 2024/1689, como referencia comparada — no como equivalencia jurídica. |
| `mapeo_nist_ai_rmf` | string | no | Función equivalente del NIST AI Risk Management Framework, mismo criterio que el campo anterior. |
| `nivel_confianza` | enum | sí | `confirmado_fuente_oficial` \| `inferido_contratacion` \| `reportado_prensa`. Nunca opcional — ver principio de diseño #3. |
| `evidencia` | lista de objetos | sí, al menos uno | Cada uno: `{url, fecha_captura, descripcion}`. Sin evidencia, el registro no es válido. |
| `fecha_alta_registro` | fecha | sí | Cuándo entró este sistema al registro (no cuándo se desplegó el sistema en la realidad). |
| `notas` | string | no | Contexto adicional que no encaja en otro campo. |

### Campos pendientes de la versión 1.0.0

`docs/estrategia.md` §5.4 pide que la ficha siga la lógica de una *model card* reconocible: propósito, datos,
decisiones, supervisión humana, limitaciones, evidencia. De esos, faltan como campos explícitos en la versión
1.0.0: **datos** (qué datos usa o con qué se entrenó el sistema, si se sabe) y **limitaciones** (qué no se sabe o
qué no se puede verificar sobre el sistema).

`docs/estrategia.md` §5.3 también pide mapeo a **ISO/IEC 42001**, además de EU AI Act y NIST AI RMF. Los dos
últimos ya están (`mapeo_eu_ai_act`, `mapeo_nist_ai_rmf`); falta `mapeo_iso_42001`.

Los tres quedan para una versión 1.1.0 — no se agregaron en esta versión porque no formaban parte del bloque
"fundacionales" priorizado en `docs/bitacora.md`.

## English

Every detected AI system is a record with these fields, written in this order by the reference implementation
at `datos/sistemas/{id}.yaml`.

See the Spanish table above for the authoritative field list (field names stay in Spanish across the dataset for
consistency with the sources — see `docs/metodologia.md` §5). Summary of intent per field:

- `id`, `entidad_id`: stable identifiers, `entidad_id` references the entity record.
- `nombre`, `sector`, `nivel_gobierno`: name, policy sector (free vocabulary), government level (`nacional` |
  `regional` — local governments out of scope, see `docs/estrategia.md` §10).
- `finalidad`, `tipo_decision`, `supervision_humana_declarada`: purpose, what decision it makes or assists, and
  declared human oversight (`si` | `no` | `no_declarado`).
- `proveedor`, `vinculo_contractual`, `presupuesto`: provider, contract reference, associated budget (kept as a
  string to preserve currency and avoid false rounding).
- `estado`: `en_operacion` | `piloto` | `contratado_sin_desplegar` | `descontinuado` | `indeterminado`.
- `tecnologias`: declared technologies.
- `clasificacion_riesgo_propia`: `alto` | `limitado` | `minimo` | `pendiente_de_clasificar` — the project's own
  classification, never presented as official.
- `mapeo_eu_ai_act`, `mapeo_nist_ai_rmf`, `mapeo_iso_42001`: comparative mapping to EU AI Act, NIST AI RMF, and
  ISO/IEC 42001 — reference only, not legal equivalence.
- `nivel_confianza`: `confirmado_fuente_oficial` | `inferido_contratacion` | `reportado_prensa` — mandatory, see
  design principle #3 in the README.
- `evidencia`: list of `{url, fecha_captura, descripcion}`, at least one entry required.
- `fecha_alta_registro`, `notas`: when the record was added to the registry, and free-form notes.

### Fields pending for version 1.0.0

`docs/estrategia.md` §5.4 asks the record to follow the logic of a recognizable model card: purpose, data,
decisions, human oversight, limitations, evidence. Of those, still missing as explicit fields in version 1.0.0:
**data** (what data the system uses or was trained on, if known) and **limitations** (what is unknown or
unverifiable about the system). Planned for a 1.1.0 release.
