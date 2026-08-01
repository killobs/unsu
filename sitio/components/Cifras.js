"use client";
import { t } from "@/lib/diccionario";
import { Revelar, Cifra } from "@/components/Movimiento";

// Cliente porque le pasa funciones de formato a <Cifra>, y una función no
// cruza la frontera servidor→cliente como prop.
export default function Cifras({ locale, resumen, obligaciones }) {
  const d = t(locale);
  const loc = locale === "en" ? "en-US" : "es-PE";
  const entero = (n) => Math.round(n).toLocaleString(loc);
  const millones = (n) => `S/ ${(n / 1e6).toLocaleString(loc, { maximumFractionDigits: 1, minimumFractionDigits: 1 })} M`;

  const items = [
    { valor: resumen.sistemas, etiqueta: d.cifraSistemas, formato: entero },
    { valor: resumen.entidades, etiqueta: d.cifraEntidades, formato: entero },
    {
      valor: resumen.presupuesto,
      etiqueta: d.cifraPresupuesto,
      formato: millones,
      nota: d.cifraPresupuestoNota(resumen.conPresupuesto, resumen.sistemas),
    },
    { valor: obligaciones, etiqueta: d.cifraObligaciones, formato: entero },
  ];

  return (
    <section className="cifras">
      {items.map((it, i) => (
        <Revelar key={it.etiqueta} retraso={i * 90} className="cifra">
          <p className="cifra__valor">
            <Cifra valor={it.valor} formato={it.formato} />
          </p>
          <p className="cifra__etiqueta">{it.etiqueta}</p>
          {it.nota ? <p className="cifra__nota">{it.nota}</p> : null}
        </Revelar>
      ))}
    </section>
  );
}
