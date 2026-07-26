import { obtenerEntidades, obtenerEntidad, sistemasDeEntidad } from "@/lib/datos";
import FichaEntidad from "@/components/FichaEntidad";

export function generateStaticParams() {
  return obtenerEntidades().map((e) => ({ id: e.id }));
}

export default async function PaginaEntidadEs({ params }) {
  const { id } = await params;
  const entidad = obtenerEntidad(id);
  const sistemas = entidad ? sistemasDeEntidad(id) : [];
  return (
    <FichaEntidad
      locale="es"
      entidad={entidad}
      sistemas={sistemas}
      hrefIndice="/entidades"
      hrefSistema={(sid) => `/sistemas/${sid}`}
    />
  );
}
