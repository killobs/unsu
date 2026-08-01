import { t } from "@/lib/diccionario";

export default function PanelCumplimiento({ locale, cumplimiento, numeroEntidades }) {
  const d = t(locale);
  return (
    <div className="panel-cumplimiento">
      <h2>{d.panelCumplimientoTitulo}</h2>
      <p>{d.panelCumplimientoDetalle(cumplimiento, numeroEntidades)}</p>
      <p className="aviso-cumplimiento">{d.panelCumplimientoAviso}</p>
      {/* El total es entidades × obligaciones seguidas, no el total del
          reglamento: sin esta línea la cifra se lee como si fuera todo lo que
          exige la norma. */}
      {cumplimiento.porEntidad ? (
        <p className="aviso-cumplimiento">
          {d.panelCumplimientoSeleccion(cumplimiento.total, numeroEntidades, cumplimiento.porEntidad)}
        </p>
      ) : null}
      <p>{d.panelCumplimientoPlazo(cumplimiento.plazos)}</p>
    </div>
  );
}
