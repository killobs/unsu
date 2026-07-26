import { obtenerSistemas, obtenerSistema, obtenerEntidad } from "@/lib/datos";
import FichaSistema from "@/components/FichaSistema";

export function generateStaticParams() {
  return obtenerSistemas().map((s) => ({ id: s.id }));
}

export default async function PaginaSistemaEn({ params }) {
  const { id } = await params;
  const sistema = obtenerSistema(id);
  const entidad = sistema ? obtenerEntidad(sistema.entidad_id) : null;
  return (
    <FichaSistema
      locale="en"
      sistema={sistema}
      entidad={entidad}
      hrefEntidad={(eid) => `/en/entities/${eid}`}
      hrefIndice="/en"
    />
  );
}
