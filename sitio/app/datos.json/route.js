// Dataset completo en un solo archivo, sin fricción (docs/estrategia.md §1).
// Se genera en tiempo de build a partir de los mismos YAML que el resto del
// sitio -- no hay una copia paralela que se pueda desincronizar.
import { obtenerSistemas, obtenerEntidades } from "@/lib/datos";

export const dynamic = "force-static";

export async function GET() {
  const cuerpo = {
    generado: new Date().toISOString(),
    licencia: "CC BY-SA 4.0 -- ver LICENSE-DATOS.md en https://github.com/killobs/unsu",
    esquema: "docs/esquema/ en https://github.com/killobs/unsu",
    sistemas: obtenerSistemas(),
    entidades: obtenerEntidades(),
  };
  return Response.json(cuerpo);
}
