import { t } from "@/lib/diccionario";
import { Revelar } from "@/components/Movimiento";

// De más fuerte a más débil. Se muestran los tres aunque alguno esté en cero:
// la categoría vacía también informa — dice que el registro no se apoya ahí.
const ORDEN = ["confirmado_fuente_oficial", "inferido_contratacion", "reportado_prensa"];

export default function Confianza({ locale, porConfianza, total }) {
  const d = t(locale);

  return (
    <section className="bloque" id="confianza">
      <Revelar>
        <h2 className="bloque__titulo">{d.confianzaTitulo}</h2>
        <p className="bloque__intro">{d.confianzaIntro}</p>
      </Revelar>

      <ol className="niveles">
        {ORDEN.map((clave, i) => {
          const n = porConfianza[clave] ?? 0;
          const pct = total ? (n / total) * 100 : 0;
          return (
            <Revelar key={clave} etiqueta="li" retraso={i * 100} className="nivel">
              <p className="nivel__n">{n}</p>
              <div className="nivel__cuerpo">
                <h3 className="nivel__titulo">{d.confianzas[clave]}</h3>
                <p className="nivel__desc">{d.confianzaDescripciones[clave]}</p>
              </div>
              <span className="nivel__pct">{Math.round(pct)}%</span>
              {/* la proporción va como variable, no como transform en línea: si
                  fuera en línea le ganaría a .es-oculto y no habría animación */}
              <span className="nivel__medida" style={{ "--pct": pct / 100 }} aria-hidden="true" />
            </Revelar>
          );
        })}
      </ol>
    </section>
  );
}
