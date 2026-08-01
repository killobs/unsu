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
| `finalidad` | string | no | Qué hace el sistema, en lenguaje llano. Equivale al campo "propósito" de una model card. |
| `tipo_decision` | string | no | Qué decisión toma o asiste el sistema, y sobre quién. |
| `supervision_humana_declarada` | enum | no | `si` \| `no` \| `no_declarado`. |
| `proveedor` | string | no | Proveedor o desarrollador, si está identificado. |
| `vinculo_contractual` | string | no | Referencia al contrato o proceso de contratación, si existe. |
| `presupuesto` | string | no | Monto asociado, si se conoce. Se guarda como texto y no como número, para poder registrar la moneda y evitar redondeos falsos. Un monto de 0 significa que no se publicó, y se registra vacío. |
| `estado` | enum | sí | `en_operacion` \| `piloto` \| `contratado_sin_desplegar` \| `descontinuado` \| `indeterminado`. |
| `tecnologias` | string | no | Tecnologías declaradas (NLP, visión computacional, modelo específico...). |
| `clasificacion_riesgo_propia` | enum | sí | `alto` \| `limitado` \| `minimo` \| `pendiente_de_clasificar`. Clasificación propia del proyecto, nunca presentada como oficial. Criterios en `docs/metodologia.md`. |
| `mapeo_eu_ai_act` | string | no | Nivel de riesgo equivalente bajo el Reglamento (UE) 2024/1689. Es referencia comparada, no equivalencia jurídica. |
| `mapeo_nist_ai_rmf` | string | no | Función equivalente del NIST AI Risk Management Framework, con el mismo criterio que el campo anterior. |
| `nivel_confianza` | enum | sí | `confirmado_fuente_oficial` \| `inferido_contratacion` \| `reportado_prensa`. Nunca opcional. Ver el principio de diseño #3. |
| `evidencia` | lista de objetos | sí, al menos uno | Cada uno: `{url, fecha_captura, descripcion}`. Sin evidencia, el registro no es válido. |
| `fecha_alta_registro` | fecha | sí | Cuándo entró este sistema al registro (no cuándo se desplegó el sistema en la realidad). |
| `notas` | string | no | Contexto adicional que no encaja en otro campo. |

### Campos pendientes de la versión 1.0.0

`docs/estrategia.md` §5.4 pide que la ficha siga la lógica de una model card reconocible: propósito, datos,
decisiones, supervisión humana, limitaciones y evidencia. Faltan dos campos explícitos en la versión 1.0.0.
`datos` registraría qué datos usa el sistema o con qué se entrenó, si se sabe. `limitaciones` registraría qué
no se sabe o no se puede verificar sobre él.

`docs/estrategia.md` §5.3 también pide mapeo a ISO/IEC 42001, además de EU AI Act y NIST AI RMF. Los dos
últimos ya existen como campos. Falta `mapeo_iso_42001`.

Los tres quedan para la versión 1.1.0. No se agregaron aquí porque no formaban parte del bloque de
fundacionales priorizado en `docs/bitacora.md`.

## English

Every detected AI system is a record with these fields, written in this order by the reference implementation
at `datos/sistemas/{id}.yaml`.

The Spanish table above is the authoritative field list. Field names stay in Spanish across the dataset for
consistency with the sources, as described in `docs/metodologia.md` §5. Summary of intent per field:

- `id`, `entidad_id`: stable identifiers, `entidad_id` references the entity record.
- `nombre`, `sector`, `nivel_gobierno`: name, policy sector (free vocabulary), government level (`nacional` |
  `regional`). Local governments are out of scope, see `docs/estrategia.md` §10.
- `finalidad`, `tipo_decision`, `supervision_humana_declarada`: purpose, what decision it makes or assists, and
  declared human oversight (`si` | `no` | `no_declarado`).
- `proveedor`, `vinculo_contractual`, `presupuesto`: provider, contract reference, associated budget. The budget
  is kept as a string to preserve currency and avoid false rounding. A budget of 0 means unpublished and is
  recorded as empty.
- `estado`: `en_operacion` | `piloto` | `contratado_sin_desplegar` | `descontinuado` | `indeterminado`.
- `tecnologias`: declared technologies.
- `clasificacion_riesgo_propia`: `alto` | `limitado` | `minimo` | `pendiente_de_clasificar`. The project's own
  classification, never presented as official.
- `mapeo_eu_ai_act`, `mapeo_nist_ai_rmf`: comparative mapping to the EU AI Act and NIST AI RMF. Reference only,
  not legal equivalence. A third field for ISO/IEC 42001 is planned but does not exist yet, see below.
- `nivel_confianza`: `confirmado_fuente_oficial` | `inferido_contratacion` | `reportado_prensa`. Mandatory, see
  design principle #3 in the README.
- `evidencia`: list of `{url, fecha_captura, descripcion}`, at least one entry required.
- `fecha_alta_registro`, `notas`: when the record was added to the registry, and free-form notes.

### Fields pending for version 1.0.0

`docs/estrategia.md` §5.4 asks the record to follow the logic of a recognizable model card: purpose, data,
decisions, human oversight, limitations and evidence. Two explicit fields are still missing in version 1.0.0.
`datos` would record what data the system uses or was trained on, if known. `limitaciones` would record what is
unknown or unverifiable about it.

`docs/estrategia.md` §5.3 also asks for a mapping to ISO/IEC 42001. The field `mapeo_iso_42001` does not exist
yet.

All three are planned for version 1.1.0.
