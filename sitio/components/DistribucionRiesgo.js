import { t } from "@/lib/diccionario";
import { Revelar } from "@/components/Movimiento";

// Orden fijo de mayor a menor consecuencia, no por frecuencia: la barra debe
// leerse siempre igual aunque cambien los conteos.
const ORDEN = ["alto", "limitado", "minimo", "pendiente_de_clasificar"];

export default function DistribucionRiesgo({ locale, porRiesgo, total }) {
  const d = t(locale);
  const tramos = ORDEN.map((clave) => ({
    clave,
    n: porRiesgo[clave] ?? 0,
    pct: total ? ((porRiesgo[clave] ?? 0) / total) * 100 : 0,
  })).filter((tr) => tr.n > 0);

  return (
    <section className="bloque" id="riesgo">
      <Revelar>
        <h2 className="bloque__titulo">{d.distribucionTitulo}</h2>
        <p className="bloque__intro">{d.distribucionIntro}</p>
      </Revelar>

      <Revelar retraso={120}>
        <div className="barra" role="img" aria-label={tramos.map((tr) => `${d.riesgos[tr.clave]}: ${tr.n}`).join(", ")}>
          {tramos.map((tr) => (
            <span key={tr.clave} className={`barra__tramo riesgo-${tr.clave}`} style={{ width: `${tr.pct}%` }} />
          ))}
        </div>
        <ul className="leyenda">
          {tramos.map((tr) => (
            <li key={tr.clave}>
              <span className={`leyenda__punto riesgo-${tr.clave}`} aria-hidden="true" />
              <span className="leyenda__n">{tr.n}</span>
              <span className="leyenda__txt">{d.riesgos[tr.clave]}</span>
              <span className="leyenda__pct">{Math.round(tr.pct)}%</span>
            </li>
          ))}
        </ul>
      </Revelar>
    </section>
  );
}
