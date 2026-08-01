import { Inter } from "next/font/google";
import "../globals.css";
import Cabecera from "@/components/Cabecera";
import Pie from "@/components/Pie";
import { t } from "@/lib/diccionario";
import { URL_SITIO } from "@/lib/sitio";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

const d = t("en");

export const metadata = {
  metadataBase: new URL(URL_SITIO),
  title: { default: d.tituloSitio, template: d.tituloPlantilla },
  description: d.descripcionSitio,
  alternates: {
    canonical: "/en",
    languages: { "es-PE": "/", en: "/en" },
  },
  openGraph: {
    type: "website",
    siteName: d.tituloSitio,
    locale: "en_US",
    url: "/en",
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

export default function LayoutEn({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <a href="#contenido" className="salto">
          {d.saltarAlContenido}
        </a>
        <Cabecera locale="en" />
        <main id="contenido">
          <div className="contenedor">{children}</div>
        </main>
        <Pie locale="en" />
      </body>
    </html>
  );
}
