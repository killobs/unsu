export const metadata = {
  title: "Methodology",
  description:
    "Detection criteria, risk classification, confidence levels and evidence rules behind the Public AI Registry.",
  alternates: { canonical: "/en/methodology", languages: { "es-PE": "/metodologia", en: "/en/methodology" } },
};

export default function PaginaMetodologiaEn() {
  return (
    <>
      <h1>Methodology</h1>
      <p className="intro">
        Full documentation, with change history, in{" "}
        <a href="https://github.com/killobs/unsu/blob/main/docs/metodologia.md" target="_blank" rel="noreferrer">
          docs/metodologia.md
        </a>{" "}
        (Spanish and English). Summary:
      </p>

      <h2>Confidence level</h2>
      <p>
        Every system declares one of three levels: <strong>confirmed by official source</strong> (named in an
        official document), <strong>inferred from procurement</strong> (detected via a term match in public
        procurement data, uncorroborated), or <strong>press-reported</strong> (only news coverage, no official
        document or identifiable contract).
      </p>

      <h2>Risk classification</h2>
      <p>
        This is the <strong>project&apos;s own classification, not Peru&apos;s official one</strong> (no official
        per-system risk list exists yet). High: the system decides or assists a decision affecting a fundamental
        right, or with legal consequences. Limited: direct citizen interaction, no rights decision. Minimal: internal
        use only. Pending classification: insufficient source information.
      </p>

      <h2>Procurement-based detection</h2>
      <p>
        The OECE open-contracting search API does fuzzy single-word matching, not exact-phrase matching — up to 82%
        false positives measured unfiltered (see the{" "}
        <a
          href="https://github.com/killobs/unsu/blob/main/docs/fase-0-detectabilidad.md"
          target="_blank"
          rel="noreferrer"
        >
          detectability test
        </a>
        ). The extractor filters for the exact phrase client-side and treats every result as a candidate, never an
        automatic confirmed entry.
      </p>

      <h2>Obligation states</h2>
      <p>
        &quot;Not verifiable from public sources&quot; never becomes &quot;not met&quot; without positive evidence
        of non-compliance. Absence of public evidence is not proof of non-compliance.
      </p>
    </>
  );
}
