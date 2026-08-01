import { t } from "@/lib/diccionario";
import ImagenTramada from "@/components/ImagenTramada";

// Rampa fría de cinco pasos: de la sombra al nevado, pasando por el azul de
// marca. El tramado la vuelve grano en vez de degradado limpio.
const PALETA = [
  [10, 14, 22],
  [26, 48, 80],
  [64, 104, 150],
  [148, 178, 208],
  [236, 242, 248],
];

export default function Hero({ locale }) {
  const d = t(locale);
  return (
    <section className="hero">
      {/* ancho corto a propósito: el lienzo se escala por CSS y así el punteado
          de Bayer se ve como grano en vez de desaparecer. */}
      <ImagenTramada src="/ausangate.jpg" paleta={PALETA} ancho={720} gamma={2.1} className="hero__imagen" />
      {/* Sin JS el lienzo queda vacío y el hero se ve como una caja negra. Va en
          <noscript> y no como fondo CSS a propósito: así quien sí tiene JS nunca
          ve el destello de la foto sin tramar antes de que el lienzo pinte. */}
      <noscript>
        <img src="/ausangate.jpg" alt="" className="hero__imagen hero__imagen--respaldo" />
      </noscript>
      <div className="hero__rejilla" aria-hidden="true" />

      <div className="hero__contenido">
        <p className="hero__producto">
          <span className="hero__marca">{d.marca}</span>
          <span className="hero__barra" aria-hidden="true" />
          {d.heroProducto}
        </p>
        <h1 className="hero__titular">{d.heroTitular}</h1>
        <p className="hero__bajada">{d.heroBajada}</p>
        <a className="hero__enlace" href="#registro">
          {d.heroVerRegistro}
        </a>
      </div>

      <div className="hero__pie">
        <span className="hero__desplazar">{d.heroDesplazar}</span>
        <p className="hero__credito">{d.heroCredito}</p>
      </div>
    </section>
  );
}
