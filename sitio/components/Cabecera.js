import Link from "next/link";
import { t } from "@/lib/diccionario";

export default function Cabecera({ locale }) {
  const d = t(locale);
  const enlaces =
    locale === "en"
      ? { inicio: "/en", entidades: "/en/entities", metodologia: "/en/methodology", otroIdioma: "/" }
      : { inicio: "/", entidades: "/entidades", metodologia: "/metodologia", otroIdioma: "/en" };
  return (
    <header className="cabecera">
      <div className="contenedor">
        <Link href={enlaces.inicio} className="marca">
          {d.tituloSitio}
        </Link>
        <nav className="navegacion">
          <Link href={enlaces.inicio}>{d.navSistemas}</Link>
          <Link href={enlaces.entidades}>{d.navEntidades}</Link>
          <Link href={enlaces.metodologia}>{d.navMetodologia}</Link>
          <Link href={enlaces.otroIdioma}>{d.navIdioma}</Link>
        </nav>
      </div>
    </header>
  );
}
