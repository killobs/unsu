import Link from "next/link";
import { t } from "@/lib/diccionario";

export default function IndiceEntidades({ locale, entidades, hrefEntidad }) {
  const d = t(locale);
  return (
    <>
      <h1>{d.navEntidades}</h1>
      <table className="tabla-sistemas">
        <thead>
          <tr>
            <th>{d.columnaEntidad}</th>
            <th>{d.columnaSector}</th>
          </tr>
        </thead>
        <tbody>
          {entidades.map((e) => (
            <tr key={e.id}>
              <td data-etiqueta={d.columnaEntidad}>
                <Link href={hrefEntidad(e.id)}>{e.nombre}</Link>
              </td>
              <td data-etiqueta={d.columnaSector}>{e.sector}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
