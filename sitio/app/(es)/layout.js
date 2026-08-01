import { Inter } from "next/font/google";
import "../globals.css";
import Cabecera from "@/components/Cabecera";
import Pie from "@/components/Pie";
import { t } from "@/lib/diccionario";
import { URL_SITIO } from "@/lib/sitio";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

const d = t("es");

export const metadata = {
  metadataBase: new URL(URL_SITIO),
  // plantilla: las páginas hijas ponen sólo su parte distintiva y el sufijo se
  // añade solo, sin repetirlo en cada ficha
  title: { default: d.tituloSitio, template: d.tituloPlantilla },
  description: d.descripcionSitio,
  alternates: {
    canonical: "/",
    languages: { "es-PE": "/", en: "/en" },
  },
  openGraph: {
    type: "website",
    siteName: d.tituloSitio,
    locale: "es_PE",
    url: "/",
    title: d.tituloSitio,
    description: d.descripcionSitio,
    images: [{ url: "/og.png", width: 1200, height: 630, alt: d.tituloSitio }],
  },
  twitter: {
    card: "summary_large_image",
    title: d.tituloSitio,
    description: d.descripcionSitio,
    images: ["/og.png"],
  },
};

export default function LayoutEs({ children }) {
  return (
    <html lang="es" className={inter.variable}>
      <body>
        <a href="#contenido" className="salto">
          {d.saltarAlContenido}
        </a>
        <Cabecera locale="es" />
        <main id="contenido">
          <div className="contenedor">{children}</div>
        </main>
        <Pie locale="es" />
      </body>
    </html>
  );
}
