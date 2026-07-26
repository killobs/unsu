import "../globals.css";
import Cabecera from "@/components/Cabecera";
import Pie from "@/components/Pie";
import { t } from "@/lib/diccionario";

export const metadata = {
  title: t("en").tituloSitio,
  description: t("en").descripcionSitio,
};

export default function LayoutEn({ children }) {
  return (
    <html lang="en">
      <body>
        <Cabecera locale="en" />
        <main>
          <div className="contenedor">{children}</div>
        </main>
        <Pie locale="en" />
      </body>
    </html>
  );
}
