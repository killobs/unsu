import { obtenerSistemas, obtenerSistema, obtenerEntidad } from "@/lib/datos";
import { metadatosSistema } from "@/lib/metadatos";
import FichaSistema from "@/components/FichaSistema";

export function generateStaticParams() {
  return obtenerSistemas().map((s) => ({ id: s.id }));
}

export async function generateMetadata({ params }) {
  const { id } = await params;
  const sistema = obtenerSistema(id);
  return metadatosSistema("en", sistema, sistema ? obtenerEntidad(sistema.entidad_id) : null);
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
