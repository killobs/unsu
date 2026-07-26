// Lee los datos versionados en /datos (fuera de sitio/) en tiempo de build.
// No hay base de datos -- los archivos YAML son la fuente de verdad, tal
// como está documentado en el prompt original y en docs/metodologia.md.
import fs from "node:fs";
import path from "node:path";
import { load as cargarYaml } from "js-yaml";

const RAIZ_DATOS = path.join(process.cwd(), "..", "datos");

function leerYamlDir(subdir) {
  const dir = path.join(RAIZ_DATOS, subdir);
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".yaml"))
    .map((f) => cargarYaml(fs.readFileSync(path.join(dir, f), "utf-8")));
}

export function obtenerSistemas() {
  return leerYamlDir("sistemas").sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
}

export function obtenerEntidades() {
  return leerYamlDir("entidades").sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
}

export function obtenerSistema(id) {
  return obtenerSistemas().find((s) => s.id === id) ?? null;
}

export function obtenerEntidad(id) {
  return obtenerEntidades().find((e) => e.id === id) ?? null;
}

export function sistemasDeEntidad(id) {
  return obtenerSistemas().filter((s) => s.entidad_id === id);
}

const FECHA_LIMITE = "2026-09-10";

export function resumenCumplimiento() {
  const entidades = obtenerEntidades();
  let total = 0;
  let cumplidas = 0;
  for (const e of entidades) {
    for (const o of e.obligaciones ?? []) {
      total += 1;
      if (o.estado === "cumplido_con_evidencia") cumplidas += 1;
    }
  }
  const hoy = new Date();
  const limite = new Date(`${FECHA_LIMITE}T00:00:00-05:00`);
  const diasRestantes = Math.ceil((limite - hoy) / 86400000);
  return { total, cumplidas, fechaLimite: FECHA_LIMITE, diasRestantes };
}
