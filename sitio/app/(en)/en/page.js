import { obtenerSistemas, obtenerEntidades, resumenCumplimiento, resumenRegistro } from "@/lib/datos";
import { t } from "@/lib/diccionario";
import Hero from "@/components/Hero";
import Cifras from "@/components/Cifras";
import DistribucionRiesgo from "@/components/DistribucionRiesgo";
import Confianza from "@/components/Confianza";
import PanelCumplimiento from "@/components/PanelCumplimiento";
import IndiceCliente from "@/components/IndiceCliente";
import { Revelar } from "@/components/Movimiento";

export default function PaginaInicioEn() {
  const d = t("en");
  const entidades = obtenerEntidades();
  const entidadesPorId = Object.fromEntries(entidades.map((e) => [e.id, e]));
  const sistemas = obtenerSistemas().map((s) => ({
    ...s,
    entidadNombre: entidadesPorId[s.entidad_id]?.nombre ?? s.entidad_id,
  }));
  const cumplimiento = resumenCumplimiento();
  const resumen = resumenRegistro();

  return (
    <>
      <Hero locale="en" />
      <Cifras locale="en" resumen={resumen} obligaciones={cumplimiento.total} />
      <DistribucionRiesgo locale="en" porRiesgo={resumen.porRiesgo} total={resumen.sistemas} />
      <Confianza locale="en" porConfianza={resumen.porConfianza} total={resumen.sistemas} />

      <section className="bloque" id="registro">
        <Revelar>
          <h2 className="bloque__titulo">{d.registroTitulo}</h2>
          <p className="bloque__intro">{d.inicioIntro}</p>
          <PanelCumplimiento locale="en" cumplimiento={cumplimiento} numeroEntidades={entidades.length} />
        </Revelar>
        <IndiceCliente locale="en" sistemas={sistemas} baseHrefSistema="/en/systems" />
      </section>
    </>
  );
}
