import "../globals.css";
import Cabecera from "@/components/Cabecera";
import Pie from "@/components/Pie";
import { t } from "@/lib/diccionario";

export const metadata = {
  title: t("es").tituloSitio,
  description: t("es").descripcionSitio,
};

export default function LayoutEs({ children }) {
  return (
    <html lang="es">
      <body>
        <Cabecera locale="es" />
        <main>
          <div className="contenedor">{children}</div>
        </main>
        <Pie locale="es" />
      </body>
    </html>
  );
}
