# Especificación de esquema — Registro de IA Pública

**Versión 1.0.0** · 26 de julio de 2026

*English below.*

## Español

Esta es la especificación del formato de datos de este registro, publicada como estándar abierto e independiente
del conjunto de datos que hoy vive en `datos/`. El objetivo es que alguien pueda construir un registro equivalente
en otro país adoptando este mismo esquema, sin tener que copiar ni depender del código de este repositorio.

- [`sistema.md`](sistema.md) — ficha de un sistema de IA.
- [`entidad.md`](entidad.md) — ficha de una entidad pública y su cumplimiento normativo.

### Principios de diseño

1. **Sin supuestos de una sola jurisdicción.** Ningún nombre de campo asume Perú (nada de `entidad_pcm` ni
   similares). El campo `jurisdiccion` existe desde la versión 1.0.0 aunque hoy solo tenga el valor `PE` en los
   datos publicados — está para cuando el segundo país adopte este esquema.
2. **Orden de campos determinista.** La implementación de referencia (`extractores/comun/esquema.py`) siempre
   escribe los campos en el mismo orden. No es parte de la especificación en sí (YAML/JSON no garantizan orden),
   pero cualquier implementación debería mantenerlo por la misma razón: que el diff de Git muestre solo lo que
   cambió de verdad.
3. **Nivel de confianza y evidencia son obligatorios, no opcionales.** Un registro sin evidencia con fecha de
   captura, o sin declarar si es un hecho confirmado o una inferencia, no es válido bajo este esquema.
4. **"No verificable" es un estado de primera clase**, distinto de "no cumplido". Cualquier implementación de este
   esquema debe preservar esa distinción — colapsarlas en una sola convierte ausencia de evidencia en acusación.

### Formato de archivo

La implementación de referencia usa un archivo YAML por registro (`datos/sistemas/{id}.yaml`,
`datos/entidades/{id}.yaml`). El esquema en sí es agnóstico de formato: es igual de válido implementarlo en JSON,
en filas de una base de datos, o en cualquier otro formato estructurado, siempre que se conserven los campos y
sus tipos.

### Versionado

Cambios que agregan un campo opcional nuevo son versión menor (1.1.0, 1.2.0...). Cambios que renombran, eliminan
o cambian el tipo de un campo existente son versión mayor (2.0.0) y deben documentarse aquí con la fecha y el
motivo. No hay cambios registrados todavía después de la 1.0.0.

## English

This is the data format specification for this registry, published as an open standard independent from the
dataset that lives under `datos/` today. The goal is for someone to build an equivalent registry in another
country by adopting this same schema, without needing to copy or depend on this repository's code.

- [`sistema.md`](sistema.md) — AI system record.
- [`entidad.md`](entidad.md) — public entity record and its regulatory compliance.

### Design principles

1. **No single-jurisdiction assumptions.** No field name assumes Peru (nothing like `entidad_pcm`). The
   `jurisdiccion` field has existed since version 1.0.0, even though today's published data only has the value
   `PE` — it's there for when a second country adopts this schema.
2. **Deterministic field order.** The reference implementation (`extractores/comun/esquema.py`) always writes
   fields in the same order. This isn't part of the spec itself (YAML/JSON don't guarantee order), but any
   implementation should preserve it for the same reason: so a Git diff shows only what actually changed.
3. **Confidence level and evidence are mandatory, not optional.** A record with no dated evidence, or that
   doesn't declare whether it's a confirmed fact or an inference, is not valid under this schema.
4. **"Not verifiable" is a first-class state**, distinct from "not met". Any implementation of this schema must
   preserve that distinction — collapsing them into one turns absence of evidence into an accusation.

### File format

The reference implementation uses one YAML file per record. The schema itself is format-agnostic: it's equally
valid to implement it in JSON, database rows, or any other structured format, as long as the fields and their
types are preserved.

### Versioning

Changes that add a new optional field are a minor version bump (1.1.0, 1.2.0...). Changes that rename, remove,
or change the type of an existing field are a major version bump (2.0.0) and must be documented here with date
and reason. No changes recorded yet after 1.0.0.
