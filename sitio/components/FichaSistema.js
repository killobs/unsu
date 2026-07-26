import Link from "next/link";
import { notFound } from "next/navigation";
import { t } from "@/lib/diccionario";
import EtiquetaRiesgo from "@/components/EtiquetaRiesgo";

export default function FichaSistema({ locale, sistema, entidad, hrefEntidad, hrefIndice }) {
  if (!sistema) notFound();
  const d = t(locale);
  const sd = (v) => (v && String(v).trim() ? v : d.fichaSinDato);

  return (
    <>
      <Link href={hrefIndice} className="volver">
        {d.volverIndice}
      </Link>
      <h1>{sistema.nombre}</h1>
      <dl className="ficha">
        <dt>{d.fichaEntidad}</dt>
        <dd>
          <Link href={hrefEntidad(sistema.entidad_id)}>{entidad?.nombre ?? sistema.entidad_id}</Link>
        </dd>

        <dt>{d.fichaFinalidad}</dt>
        <dd>{sd(sistema.finalidad)}</dd>

        <dt>{d.fichaTecnologias}</dt>
        <dd>{sd(sistema.tecnologias)}</dd>

        <dt>{d.fichaEstado}</dt>
        <dd>{d.estados[sistema.estado] ?? sistema.estado}</dd>

        <dt>{d.fichaRiesgo}</dt>
        <dd>
          <EtiquetaRiesgo locale={locale} valor={sistema.clasificacion_riesgo_propia} />
        </dd>

        <dt>{d.fichaConfianza}</dt>
        <dd>{d.confianzas[sistema.nivel_confianza] ?? sistema.nivel_confianza}</dd>

        <dt>{d.fichaSupervisionHumana}</dt>
        <dd>{d.supervisionHumana[sistema.supervision_humana_declarada] ?? sd(sistema.supervision_humana_declarada)}</dd>

        <dt>{d.fichaProveedor}</dt>
        <dd>{sd(sistema.proveedor)}</dd>

        <dt>{d.fichaVinculo}</dt>
        <dd>{sd(sistema.vinculo_contractual)}</dd>

        <dt>{d.fichaPresupuesto}</dt>
        <dd>{sd(sistema.presupuesto)}</dd>

        <dt>{d.fichaEuAiAct}</dt>
        <dd>{sd(sistema.mapeo_eu_ai_act)}</dd>

        <dt>{d.fichaNistAiRmf}</dt>
        <dd>{sd(sistema.mapeo_nist_ai_rmf)}</dd>

        {sistema.notas ? (
          <>
            <dt>{d.fichaNotas}</dt>
            <dd>{sistema.notas}</dd>
          </>
        ) : null}
      </dl>

      <h2>{d.fichaEvidencia}</h2>
      <ul className="evidencia">
        {(sistema.evidencia ?? []).map((ev, i) => (
          <li key={i}>
            <div>
              <a href={ev.url} target="_blank" rel="noreferrer">
                {ev.url}
              </a>
            </div>
            <div>{ev.descripcion}</div>
            <div className="fecha-captura">{ev.fecha_captura}</div>
          </li>
        ))}
      </ul>
    </>
  );
}
