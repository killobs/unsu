"use client";
import { useEffect, useRef } from "react";

// Matriz de Bayer 8×8: el patrón ordenado clásico de imprenta. Cada celda da el
// umbral con el que se decide si un píxel sube al siguiente color de la paleta,
// y es lo que produce el punteado regular en vez de ruido aleatorio.
const BAYER = [
  0, 32, 8, 40, 2, 34, 10, 42, 48, 16, 56, 24, 50, 18, 58, 26, 12, 44, 4, 36, 14, 46, 6, 38, 60, 28, 52, 20, 62, 30,
  54, 22, 3, 35, 11, 43, 1, 33, 9, 41, 51, 19, 59, 27, 49, 17, 57, 25, 15, 47, 7, 39, 13, 45, 5, 37, 63, 31, 55, 23,
  61, 29, 53, 21,
];

// gamma > 1 oscurece los medios antes de mapear: es lo que manda el cielo claro
// de la foto a la banda azul marino de la paleta y deja el blanco solo para la
// nieve. Sin esto el cielo sale pálido y el texto encima no contrasta.
export default function ImagenTramada({ src, paleta, ancho = 900, gamma = 1, className }) {
  const refLienzo = useRef(null);

  useEffect(() => {
    const lienzo = refLienzo.current;
    if (!lienzo) return;

    let cancelado = false;
    const imagen = new Image();
    imagen.crossOrigin = "anonymous";

    imagen.onload = () => {
      if (cancelado) return;
      const alto = Math.round((imagen.naturalHeight / imagen.naturalWidth) * ancho);
      lienzo.width = ancho;
      lienzo.height = alto;

      const ctx = lienzo.getContext("2d", { willReadFrequently: true });
      ctx.drawImage(imagen, 0, 0, ancho, alto);

      const datos = ctx.getImageData(0, 0, ancho, alto);
      const px = datos.data;
      const ultimo = paleta.length - 1;

      for (let y = 0; y < alto; y++) {
        for (let x = 0; x < ancho; x++) {
          const i = (y * ancho + x) * 4;
          const bruta = (0.2126 * px[i] + 0.7152 * px[i + 1] + 0.0722 * px[i + 2]) / 255;
          const luz = gamma === 1 ? bruta : Math.pow(bruta, gamma);
          const umbral = (BAYER[(y % 8) * 8 + (x % 8)] + 0.5) / 64;

          // Posición continua dentro de la paleta; la parte decimal es la que
          // se resuelve con el umbral, y de ahí sale la mezcla punteada.
          const posicion = luz * ultimo;
          const abajo = Math.floor(posicion);
          const indice = Math.min(ultimo, posicion - abajo > umbral ? abajo + 1 : abajo);
          const color = paleta[indice];

          px[i] = color[0];
          px[i + 1] = color[1];
          px[i + 2] = color[2];
        }
      }

      ctx.putImageData(datos, 0, 0);
    };

    imagen.src = src;
    return () => {
      cancelado = true;
    };
  }, [src, paleta, ancho, gamma]);

  return <canvas ref={refLienzo} className={className} aria-hidden="true" />;
}
