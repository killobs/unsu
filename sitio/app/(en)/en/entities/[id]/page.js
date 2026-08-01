import { obtenerEntidades, obtenerEntidad, sistemasDeEntidad } from "@/lib/datos";
import { metadatosEntidad } from "@/lib/metadatos";
import FichaEntidad from "@/components/FichaEntidad";

export function generateStaticParams() {
  return obtenerEntidades().map((e) => ({ id: e.id }));
}

export async function generateMetadata({ params }) {
  const { id } = await params;
  const entidad = obtenerEntidad(id);
  return metadatosEntidad("en", entidad, entidad ? sistemasDeEntidad(id) : []);
}

export default async function PaginaEntidadEn({ params }) {
  const { id } = await params;
  const entidad = obtenerEntidad(id);
  const sistemas = entidad ? sistemasDeEntidad(id) : [];
  return (
    <FichaEntidad
      locale="en"
      entidad={entidad}
      sistemas={sistemas}
      hrefIndice="/en/entities"
      hrefSistema={(sid) => `/en/systems/${sid}`}
    />
  );
}
