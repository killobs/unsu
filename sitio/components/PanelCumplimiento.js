import { t } from "@/lib/diccionario";

export default function PanelCumplimiento({ locale, cumplimiento, numeroEntidades }) {
  const d = t(locale);
  return (
    <div className="panel-cumplimiento">
      <h2>{d.panelCumplimientoTitulo}</h2>
      <p>{d.panelCumplimientoDetalle(cumplimiento, numeroEntidades)}</p>
      <p>{d.panelCumplimientoPlazo(cumplimiento.diasRestantes)}</p>
    </div>
  );
}
