import { obtenerSistemas, obtenerEntidades, resumenCumplimiento } from "@/lib/datos";
import { t } from "@/lib/diccionario";
import PanelCumplimiento from "@/components/PanelCumplimiento";
import IndiceCliente from "@/components/IndiceCliente";

export default function PaginaInicioEn() {
  const d = t("en");
  const entidades = obtenerEntidades();
  const entidadesPorId = Object.fromEntries(entidades.map((e) => [e.id, e]));
  const sistemas = obtenerSistemas().map((s) => ({
    ...s,
    entidadNombre: entidadesPorId[s.entidad_id]?.nombre ?? s.entidad_id,
  }));
  const cumplimiento = resumenCumplimiento();

  return (
    <>
      <h1>{d.inicioTitulo}</h1>
      <p className="intro">{d.inicioIntro}</p>
      <PanelCumplimiento locale="en" cumplimiento={cumplimiento} numeroEntidades={entidades.length} />
      <IndiceCliente locale="en" sistemas={sistemas} baseHrefSistema="/en/systems" />
    </>
  );
}
