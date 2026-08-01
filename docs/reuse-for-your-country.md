# Reuse this for your country

This registry is built so it can be copied. The schema is published as an independent specification, the extractors are thin, and nothing about the architecture is specific to Peru. What follows is what actually has to change, and — more usefully — what we got wrong so you do not repeat it.

You do not need permission or attribution to build an equivalent registry. The data licence asks that derivative *datasets* stay open; the code is MIT.

---

## What you need before writing any code

**1. A regulation with named obligations.** The registry's value is contrasting what the rule requires against what entities do. Without an obligation list, you have a catalogue, not a compliance registry. Peru's is Law 31814 and Supreme Decree 115-2025-PCM.

**2. An open procurement API, or an equivalent.** This is the engine of continuous detection. Peru has OECE's open contracting portal, which follows the OCDS standard — if your country publishes OCDS, the extractor is close to reusable. If it does not, you need another recurring, machine-readable source, or the registry becomes a manual catalogue that decays.

**3. At least one citable baseline.** Starting from zero against a procurement firehose is miserable. An official catalogue or an academic paper gives you a seed of confirmed entries and a benchmark for measuring your detector's precision.

## The architecture, and why it is this dull

No database. Versioned YAML files are the source of truth, the git history is the product history, and the site is a static export built from those files. Two GitHub Actions workflows capture on a schedule and commit only when something changed.

This is not minimalism for its own sake. It has one property that mattered more than any feature: **it keeps running while nobody is looking at it, at zero cost, and the accumulated archive is the actual asset.** Every day not captured is lost forever. A design that needs a paid server, a database migration, or a human to press a button will eventually stop.

If you copy one decision, copy this one.

## What to change

| Change | Where |
|---|---|
| The procurement extractor for your API | `extractores/oece_contrataciones.py` |
| Search terms, in your language | same file |
| Obligation list and deadline rule | `historial/asignar_plazos.py`, entity records |
| Risk classification criteria | `docs/metodologia.md` §4, `historial/clasificar_riesgo.py` |
| Interface strings | `sitio/lib/diccionario.js` |
| `jurisdiccion` field value | every record — the field already exists |

The schema in [`esquema/`](esquema/) should need **no** changes. It carries `jurisdiccion` on every record from version 1.0.0 precisely so a multi-country comparison is possible later without a migration, and field names deliberately avoid Peru-specific terms.

## The mistakes worth inheriting

**Fuzzy search will drown you.** Peru's procurement API matches single words, not phrases. Phase 0 measured up to **82% false positives** on naive term search. The fix was two filters, not one: require the exact phrase, *and* require the text to evidence AI on its own without leaning on the term that triggered the match. Measure your own precision before trusting any term.

**Some terms are poison.** «Mantenimiento predictivo» (predictive maintenance) is an industrial methodology that predates AI by decades; it produced 74 records about electrical transformer servicing. «Redes neuronales» scored 0% precision. Test each term against a sample and record the rejects in the extractor so nobody adds them back in six months.

**Keep the rejects.** Manually discarded candidates live in `datos/excluidos.yaml` with reason and evidence URL, and extractors consult it on every run. Without this, every sweep re-proposes the same noise and you re-adjudicate it forever.

**Separate confirmation from detection, in the data.** A procurement hit is `inferido_contratacion` and never silently becomes `confirmado_fuente_oficial`. Readers can then discount the inferred half themselves instead of having to trust you wholesale.

**Do not let "unverifiable" drift into "non-compliant".** This is the single rule the schema enforces hardest. An entity with no public evidence is not an entity in breach. Collapsing the two turns a registry into an accusation, and one wrong accusation against a named public body costs more credibility than the whole dataset earns.

**Read your evidence to the end.** One record here declared "human oversight: not declared" while the very directive it cited described the human validation step in its §7.7. The citation was correct and unread. Budget time for re-reading sources, not just collecting them.

**A contract is not a deployment.** An awarded contract proves money moved, nothing more. Default such records to an undetermined operational status.

## Deadlines are where you will get it wrong

Peru's regulation staggers implementation **by type of entity**, not by sector — while the schedule circulating in press summaries is the sector one, which applies to private developers. Using the wrong one marks entities as late while they are still within their term.

Two defences, both cheap:

1. Put the assignment in a script with the criterion recorded per entity, so it is auditable and reproducible rather than buried in a spreadsheet.
2. When a tranche cannot be determined, leave the deadline **empty and warn**. An inherited default date is worse than no date.

## Editorial line

The project is a technical observatory, not advocacy. No evaluative adjectives about entities or officials. Every claim carries a source link and a capture date. Interpretations — risk tier, deadline tranche — are labelled as the project's own everywhere they appear, and are correctable.

This is not only ethics. A registry read as activism loses the institutional readers who make it useful, and the same discipline that makes the data credible is what makes it citable.

## If you build one

Adopting the schema is what turns this from a Peruvian dataset into a regional standard, which is worth more to everyone than any single country's registry. If you build an equivalent, opening an issue on this repository is enough to get it linked from here.
