# Ficha de entidad / Entity record

Versión 1.0.0 · parte de la [especificación de esquema](README.md)

*English below.*

## Español

Cada entidad pública con al menos un sistema detectado, o con al menos una obligación bajo seguimiento, es un
registro con estos campos, en `datos/entidades/{id}.yaml`.

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `id` | string | sí | Identificador estable, único dentro del registro. |
| `nombre` | string | sí | Nombre oficial de la entidad. |
| `jurisdiccion` | string | sí | Código ISO 3166-1 alpha-2 del país (`PE` en todos los registros publicados hoy). Presente desde la versión 1.0.0 aunque el conjunto de datos actual sea de un solo país — ver principio de diseño #1 en el README de esta carpeta. |
| `sector` | string | sí | Sector de política pública. Vocabulario libre. |
| `nivel_gobierno` | enum | sí | `nacional` \| `regional`. |
| `obligaciones` | lista de objetos | sí | Una entrada por cada obligación normativa aplicable — ver estructura abajo. |

### Estructura de `obligaciones[]`

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `obligacion` | string | sí | Descripción de la obligación (ej. "Política institucional de IA aprobada"). |
| `estado` | enum | sí | `cumplido_con_evidencia` \| `no_cumplido` \| `no_verificable_desde_fuentes_publicas` \| `no_aplica_todavia`. |
| `fecha_limite` | fecha | no | Plazo normativo aplicable, si existe. |
| `evidencia` | lista de objetos | no | Igual estructura que en la ficha de sistema: `{url, fecha_captura, descripcion}`. |

**Regla no negociable:** `no_verificable_desde_fuentes_publicas` nunca se reescribe como `no_cumplido` sin
evidencia positiva de incumplimiento. La ausencia de evidencia pública no es evidencia de incumplimiento — es
la razón de ser de este estado. Cualquier implementación de este esquema debe preservar esta distinción.

## English

Every public entity with at least one detected system, or at least one obligation under tracking, is a record
with these fields, at `datos/entidades/{id}.yaml`.

- `id`, `nombre`: stable identifier and official name.
- `jurisdiccion`: ISO 3166-1 alpha-2 country code (`PE` for every record published today). Present since version
  1.0.0 even though the current dataset is single-country — see design principle #1 in this folder's README.
- `sector`, `nivel_gobierno`: policy sector (free vocabulary), government level (`nacional` | `regional`).
- `obligaciones`: one entry per applicable regulatory obligation.

### `obligaciones[]` structure

- `obligacion`: description of the obligation.
- `estado`: `cumplido_con_evidencia` | `no_cumplido` | `no_verificable_desde_fuentes_publicas` | `no_aplica_todavia`.
- `fecha_limite`: applicable regulatory deadline, if any.
- `evidencia`: same structure as in the system record: `{url, fecha_captura, descripcion}`.

**Non-negotiable rule:** `no_verificable_desde_fuentes_publicas` never gets rewritten as `no_cumplido` without
positive evidence of non-compliance. Absence of public evidence is not evidence of non-compliance — that is the
entire reason this state exists. Any implementation of this schema must preserve this distinction.
