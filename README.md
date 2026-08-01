# Public AI Registry — Peru

*English · [versión en español](README.es.md)*

A public, versioned registry of the algorithmic and artificial-intelligence systems the Peruvian State procures and deploys, with an independent risk classification and tracking of compliance with Law 31814 and its implementing regulation (Supreme Decree 115-2025-PCM).

Live site: the registry is published as a static bilingual site built from this repository. The full dataset is downloadable as a single JSON file, with no registration and no delay.

---

## The problem

Peru was the first country in Latin America to pass a specific AI law (Law 31814, 2023), and its implementing regulation took effect in September 2025. The regulation obliges public entities to approve an institutional AI policy, register AI projects in their digital government plan, publish source code, document high-risk systems, declare human oversight mechanisms, and be transparent with the people those systems affect.

There is no official per-system registry. The State does not publish a list of which AI systems it operates, which entity runs them, what decisions they make, or whether a human reviews those decisions. Without that list, the obligations cannot be checked by anyone outside the entity itself.

The gap this project fills is not analysis. It is **the list**, with evidence, kept over time.

## The regulatory framework, briefly

The regulation does **not** set a single deadline for the whole State. Its First Complementary Final Provision staggers implementation **by type of entity**, counting from 10 September 2025:

| Entities | Term | Due |
|---|---|---|
| Executive, Legislative and Judicial branches; constitutionally autonomous bodies | 1 year | 2026-09-10 |
| EsSalud, regional governments, public universities, FONAFE companies, State programmes and projects | 2 years | 2027-09-10 |
| Local governments, types A–C | 3 years | 2028-09-10 |

The sector-based schedule frequently quoted in press summaries (health and finance first, transport and labour second) applies to **private-sector** developers, not to the public entities in this registry. Getting this wrong marks entities as late while they are still within their term, so the assignment lives in an auditable script, [`historial/asignar_plazos.py`](historial/asignar_plazos.py), with the criterion recorded per entity.

## Method

**1. Two baselines.** The registry starts from two citable catalogues: the PCM/SGTD *Catálogo de Aplicaciones con Inteligencia Artificial en el Estado Peruano*, and the academic catalogue published by Huancapaza Hilasaca (2025) in *Interfases* No. 22. Both PDFs are archived in [`datos/documentos/`](datos/documentos/).

**2. Procurement sweep.** An extractor queries the OECE open-contracting API by term and year. The API does fuzzy single-word matching, which is the central difficulty: a naive search returns mostly noise. Phase 0 measured up to **82% false positives** ([`docs/fase-0-detectabilidad.md`](docs/fase-0-detectabilidad.md)).

**3. Two filters, not one.** Results must contain the exact phrase in title or description, *and* the text must evidence artificial intelligence on its own without leaning on the term that triggered the search. Terms that failed were dropped and recorded so they are never added back: «redes neuronales» scored 0% precision, and «mantenimiento predictivo» — an industrial maintenance methodology that predates AI — produced 74 records about electrical transformer servicing.

**4. Nothing is promoted silently.** A procurement hit enters as `inferido_contratacion` and never becomes `confirmado_fuente_oficial` without a separate official source. Manually rejected candidates are kept in [`datos/excluidos.yaml`](datos/excluidos.yaml) with the reason and evidence URL, and the extractors consult that list on every run.

**5. Everything is a file.** There is no database. Versioned YAML files are the source of truth, and the git history *is* the product history. Capture workflows run daily and weekly and commit only when something changed.

## What is fact and what is inference

This distinction is the registry's core claim to credibility, so it is stated in the data itself, not in a footnote. Every record carries one of three levels:

| Level | Count | Meaning |
|---|---|---|
| `confirmado_fuente_oficial` | 32 | Named in an official document: the PCM catalogue, the entity's portal, a regulation or a resolution. |
| `inferido_contratacion` | 42 | Detected by exact-phrase match in public procurement data. Uncorroborated. |
| `reportado_prensa` | 0 | Press coverage only. The registry currently rests on nothing in this category. |

Two things are explicitly **the project's own reading and not official determinations**: the four-tier risk classification, and the deadline tranche assigned to each entity. Both are labelled as such everywhere they appear, and both are reproducible from scripts in this repository.

A third distinction is non-negotiable and enforced by the schema: **`no_verificable_desde_fuentes_publicas` is never rewritten as `no_cumplido`.** Absence of public evidence is not evidence of non-compliance. Every obligation currently tracked sits in that first state; the registry does not record a single entity as breaching anything.

## Findings

State of the registry at 1 August 2026.

| | |
|---|---|
| Systems documented | 74 |
| Entities | 47 |
| Procurement value identified | S/ 38,636,581.22 across 43 of the 74 |
| Obligations tracked | 282 (47 entities × 6) |

Risk classification: 17 high, 33 limited, 22 minimal, 2 pending.
Operational status: 29 in operation, 2 pilot, 43 undetermined.

**The main finding is not the count. Of the 74 systems, 73 declare neither human oversight nor what kind of decision they make.** Both fields have existed in the schema since day one. The single exception is EleccIA, at the National Jury of Elections, and only because its own internal directive describes the human validation step — the field was corrected after reading that directive to the end, not because the entity published the claim as such.

Seventeen systems are classified high risk under this project's criteria, meaning they take or assist a decision affecting a fundamental right or carrying legal consequences: biometric identity verification, electoral file assessment, judicial resolution drafting, oncological diagnosis.

## Three artefacts to look at

- **Risk classification criteria and the deadline rule** — [`docs/metodologia.md`](docs/metodologia.md) §4 and §4.c, applied by [`historial/clasificar_riesgo.py`](historial/clasificar_riesgo.py).
- **A complete system record** — [EleccIA](datos/sistemas/jurado-nacional-de-elecciones--eleccia.yaml), the only record that declares decision type and human oversight, with dated evidence for each claim.
- **An entity compliance record** — [RENIEC](datos/entidades/registro-nacional-de-identificacion-y-estado-civil.yaml), three detected systems and six tracked obligations with their deadline.

## Limitations

Stated plainly, because a registry that does not declare its limits reads as marketing.

- **Absence from the sweep does not prove absence of a system.** Anything built in-house, without a named external contract, does not surface through procurement data.
- **The 282 obligations are a selection, not the regulation.** They are six per entity, drawn from articles 28 and 29. The regulation requires more; article 28 alone has eleven.
- **43 of 74 systems are `indeterminado`.** An awarded contract does not prove a system operates, and the registry does not assume it does.
- **A contract is not a deployment, and a catalogue entry is not an audit.** `confirmado_fuente_oficial` describes where the claim comes from, not a guarantee that the system works as declared.
- **The risk classification is interpretive.** It is modelled on the EU AI Act's tiers, but Peru's framework and the European one are not interchangeable, and no official per-system risk list exists to check it against.
- **One case the three tiers do not cover.** Four systems are facial-recognition attendance control. They fall under minimal risk as internal use, yet they process biometric data of individuals. Their records say so.
- **The registry does not audit model performance.** It documents what is declared and contrasts it with what is required.

## Reuse

The data schema is published as a versioned, independent open specification in [`docs/esquema/`](docs/esquema/), deliberately free of Peru-specific assumptions — every record carries a `jurisdiccion` field even though the current dataset is single-country. To adapt this to another jurisdiction, see [`docs/reuse-for-your-country.md`](docs/reuse-for-your-country.md).

## Running it

```bash
pip install -r requirements.txt
python validar_esquema.py --autoprueba   # the validator rejects what it should
python validar_esquema.py                # every record matches the schema
python pruebas.py                        # data consistency tests
```

```bash
cd sitio && npm ci && npm run build      # static export to sitio/out
```

Deployment to Cloudflare Pages: root directory `sitio`, build command `npm run build`, output directory `out`. Set the `SITIO_URL` environment variable to the final public URL so the sitemap and Open Graph tags use it.

## Licence

Dual. Code in `extractores/`, `historial/` and `sitio/` is MIT ([LICENSE](LICENSE)). Data in `datos/` is CC BY-SA 4.0 ([LICENSE-DATOS.md](LICENSE-DATOS.md)). Records originating from the Interfases baseline additionally require its full academic citation, detailed in that file, as does the site photograph under its own CC BY-SA 3.0 terms.

## Sources

Every record in `datos/sistemas/` carries its own citations. The two baselines are the PCM/SGTD catalogue and Huancapaza Hilasaca, J. E. (2025), *Implementación de inteligencia artificial en el Estado peruano: catálogo analítico de aplicaciones*, Interfases (22), 143-158, <https://doi.org/10.26439/interfases2025.n022.8263>. Both are archived in `datos/documentos/`.
