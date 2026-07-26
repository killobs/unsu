import Link from "next/link";
import { notFound } from "next/navigation";
import { t } from "@/lib/diccionario";

export default function FichaEntidad({ locale, entidad, sistemas, hrefIndice, hrefSistema }) {
  if (!entidad) notFound();
  const d = t(locale);

  return (
    <>
      <Link href={hrefIndice} className="volver">
        {d.volverIndice}
      </Link>
      <h1>{entidad.nombre}</h1>
      <dl className="ficha">
        <dt>{d.columnaSector}</dt>
        <dd>{entidad.sector}</dd>
      </dl>

      <h2>{d.entidadObligaciones}</h2>
      <table className="tabla-obligaciones">
        <thead>
          <tr>
            <th>{d.columnaObligacion}</th>
            <th>{d.columnaEstadoObligacion}</th>
            <th>{d.columnaFechaLimite}</th>
          </tr>
        </thead>
        <tbody>
          {(entidad.obligaciones ?? []).map((o, i) => (
            <tr key={i}>
              <td>{o.obligacion}</td>
              <td>{d.obligacionEstados[o.estado] ?? o.estado}</td>
              <td>{o.fecha_limite || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>{d.entidadSistemas}</h2>
      {sistemas.length === 0 ? (
        <p className="sin-resultados">{d.entidadSinSistemas}</p>
      ) : (
        <ul className="evidencia">
          {sistemas.map((s) => (
            <li key={s.id}>
              <Link href={hrefSistema(s.id)}>{s.nombre}</Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
