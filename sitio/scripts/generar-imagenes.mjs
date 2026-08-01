// Genera los dos derivados de la foto del hero:
//   1. public/ausangate.jpg reescalado (el original de Wikimedia pesa 744 KB a
//      1024px, y el lienzo del hero sólo dibuja 720px de ancho).
//   2. public/og.png, la tarjeta social, con el mismo tramado que ImagenTramada.js
//      para que lo que se comparte se parezca a lo que se visita.
//
// Se corre a mano cuando cambia la foto:  node scripts/generar-imagenes.mjs
// sharp ya viene como dependencia de Next; no se añade nada al proyecto.
import sharp from "sharp";
import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const RAIZ = join(dirname(fileURLToPath(import.meta.url)), "..");
const ORIGEN = join(RAIZ, "scripts", "ausangate-original.jpg");
const PUBLICO = join(RAIZ, "public");

// Los mismos valores que components/Hero.js y components/ImagenTramada.js.
const PALETA = [
  [10, 14, 22],
  [26, 48, 80],
  [64, 104, 150],
  [148, 178, 208],
  [236, 242, 248],
];
const GAMMA = 2.1;
const BAYER = [
  0, 32, 8, 40, 2, 34, 10, 42, 48, 16, 56, 24, 50, 18, 58, 26, 12, 44, 4, 36, 14, 46, 6, 38, 60, 28, 52, 20, 62, 30,
  54, 22, 3, 35, 11, 43, 1, 33, 9, 41, 51, 19, 59, 27, 49, 17, 57, 25, 15, 47, 7, 39, 13, 45, 5, 37, 63, 31, 55, 23,
  61, 29, 53, 21,
];

function tramar({ data, info }) {
  const { width, height, channels } = info;
  const salida = Buffer.alloc(width * height * 3);
  const ultimo = PALETA.length - 1;
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const i = (y * width + x) * channels;
      const bruta = (0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2]) / 255;
      const luz = Math.pow(bruta, GAMMA);
      const umbral = (BAYER[(y % 8) * 8 + (x % 8)] + 0.5) / 64;
      const pos = luz * ultimo;
      const abajo = Math.floor(pos);
      const color = PALETA[Math.min(ultimo, pos - abajo > umbral ? abajo + 1 : abajo)];
      const o = (y * width + x) * 3;
      salida[o] = color[0];
      salida[o + 1] = color[1];
      salida[o + 2] = color[2];
    }
  }
  return { salida, width, height };
}

const original = await readFile(ORIGEN);

// --- 1. Foto del hero, reescalada ---------------------------------------------
// 800px de ancho deja margen sobre los 720 que dibuja el lienzo, sin pagar los
// 1024 del original.
const reescalada = await sharp(original).resize({ width: 800 }).jpeg({ quality: 82, mozjpeg: true }).toBuffer();
await writeFile(join(PUBLICO, "ausangate.jpg"), reescalada);

// --- 2. Tarjeta social ---------------------------------------------------------
const ANCHO = 1200;
const ALTO = 630;

const crudo = await sharp(original)
  .resize({ width: ANCHO, height: ALTO, fit: "cover", position: "attention" })
  .removeAlpha()
  .raw()
  .toBuffer({ resolveWithObject: true });

const { salida } = tramar(crudo);

// Velo y texto, en la misma línea del hero: oscuro abajo, texto apoyado ahí.
const capa = Buffer.from(`
<svg width="${ANCHO}" height="${ALTO}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="velo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#07090d" stop-opacity="0.45"/>
      <stop offset="35%" stop-color="#07090d" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#07090d" stop-opacity="0.96"/>
    </linearGradient>
  </defs>
  <rect width="${ANCHO}" height="${ALTO}" fill="url(#velo)"/>
  <text x="72" y="404" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="26"
        font-weight="600" letter-spacing="5" fill="#c3ccda">UNSU</text>
  <text x="72" y="470" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="58"
        font-weight="700" fill="#ffffff">Registro de IA Pública</text>
  <text x="72" y="528" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="28"
        fill="#c3ccda">Cada sistema de IA del Estado peruano, con evidencia.</text>
</svg>`);

await sharp(salida, { raw: { width: ANCHO, height: ALTO, channels: 3 } })
  .composite([{ input: capa, top: 0, left: 0 }])
  .png({ compressionLevel: 9 })
  .toFile(join(PUBLICO, "og.png"));

console.log("listo: public/ausangate.jpg y public/og.png regenerados");
