// 404 de toda la aplicación. Va aparte porque el sitio tiene dos root layouts
// (es/en) y no hay uno único desde el que componerlo. Como se salta el layout,
// tiene que traerse los estilos y la fuente por su cuenta.
import { Inter } from "next/font/google";
import "./globals.css";
import { t } from "@/lib/diccionario";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const d = t("es");

export const metadata = {
  title: "Página no encontrada · Registro de IA Pública",
  description: "La dirección solicitada no corresponde a ninguna ficha del registro.",
};

export default function NoEncontrada() {
  return (
    <html lang="es" className={inter.variable}>
      <body>
        <header className="cabecera">
          <div className="contenedor">
            <a href="/" className="marca">
              <span className="marca__nombre">{d.marca}</span>
              <span className="marca__producto">{d.heroProducto}</span>
            </a>
          </div>
        </header>
        <main>
          <div className="contenedor">
            <section className="bloque error404">
              <p className="error404__codigo">404</p>
              <h1 className="bloque__titulo">Esta dirección no existe en el registro</h1>
              <p className="bloque__intro">
                Puede que la ficha se haya renombrado o que el enlace esté incompleto. El índice completo de
                sistemas y entidades sigue disponible.
              </p>
              <p className="error404__enlaces">
                <a href="/">Ir al registro</a>
                <a href="/entidades/">Ver entidades</a>
                <a href="/en/">English</a>
              </p>
            </section>
          </div>
        </main>
      </body>
    </html>
  );
}
