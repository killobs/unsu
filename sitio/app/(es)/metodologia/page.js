export const metadata = {
  title: "Metodología",
  description:
    "Criterios de detección, clasificación de riesgo, niveles de confianza y reglas de evidencia del Registro de IA Pública.",
  alternates: { canonical: "/metodologia", languages: { "es-PE": "/metodologia", en: "/en/methodology" } },
};

export default function PaginaMetodologiaEs() {
  return (
    <>
      <h1>Metodología</h1>
      <p className="intro">
        Documentación completa, con historial de cambios, en{" "}
        <a href="https://github.com/killobs/unsu/blob/main/docs/metodologia.md" target="_blank" rel="noreferrer">
          docs/metodologia.md
        </a>
        . Resumen:
      </p>

      <h2>Nivel de confianza</h2>
      <p>
        Cada sistema declara uno de tres niveles: <strong>confirmado por fuente oficial</strong> (aparece en un
        documento oficial nombrado), <strong>inferido de contratación</strong> (detectado por coincidencia de
        términos en una contratación pública, sin confirmación oficial adicional) o{" "}
        <strong>reportado por prensa</strong> (solo cobertura periodística, sin documento oficial ni contratación
        identificable).
      </p>

      <h2>Clasificación de riesgo</h2>
      <p>
        Es una elaboración <strong>propia del proyecto, no la clasificación oficial</strong> del reglamento peruano.
        Alto: decide o asiste una decisión que afecta un derecho fundamental o tiene consecuencias legales. Limitado:
        interactúa con la ciudadanía pero no decide sobre derechos. Mínimo: uso interno, sin interacción directa con
        el público. Pendiente de clasificar: información insuficiente en la fuente.
      </p>

      <h2>Detección por contrataciones</h2>
      <p>
        La búsqueda de la API del Portal de Contrataciones Abiertas del OECE hace coincidencia difusa por palabra
        suelta, no por frase exacta — hasta 82% de falsos positivos sin filtrar (medido en la{" "}
        <a
          href="https://github.com/killobs/unsu/blob/main/docs/fase-0-detectabilidad.md"
          target="_blank"
          rel="noreferrer"
        >
          prueba de detectabilidad
        </a>
        ). El extractor filtra por frase exacta del lado del cliente y trata todo resultado como candidato, nunca
        como alta directa.
      </p>

      <h2>Estados de obligación</h2>
      <p>
        &quot;No verificable desde fuentes públicas&quot; nunca se convierte en &quot;no cumplido&quot; sin evidencia
        positiva de incumplimiento. La ausencia de evidencia pública no es prueba de incumplimiento.
      </p>
    </>
  );
}
