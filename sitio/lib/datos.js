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

// Agregados de portada. El presupuesto vive como cadena en el YAML (viene del
// OECE tal cual), así que se parsea aquí y se ignora lo vacío o no numérico:
// una ficha sin monto no es un cero, es un dato que no se tiene.
export function resumenRegistro() {
  const sistemas = obtenerSistemas();
  const porRiesgo = {};
  const porConfianza = {};
  const porEstado = {};
  let presupuesto = 0;
  let conPresupuesto = 0;

  for (const s of sistemas) {
    porRiesgo[s.clasificacion_riesgo_propia || "pendiente_de_clasificar"] =
      (porRiesgo[s.clasificacion_riesgo_propia || "pendiente_de_clasificar"] ?? 0) + 1;
    porConfianza[s.nivel_confianza] = (porConfianza[s.nivel_confianza] ?? 0) + 1;
    porEstado[s.estado] = (porEstado[s.estado] ?? 0) + 1;

    const monto = Number.parseFloat(s.presupuesto);
    if (Number.isFinite(monto) && monto > 0) {
      presupuesto += monto;
      conPresupuesto += 1;
    }
  }

  return {
    sistemas: sistemas.length,
    entidades: obtenerEntidades().length,
    presupuesto,
    conPresupuesto,
    porRiesgo,
    porConfianza,
    porEstado,
  };
}

// El DS 115-2025-PCM no fija una sola fecha para todo el Estado: su Primera
// Disposición Complementaria Final escalona el plazo por tipo de entidad. Por
// eso la fecha se lee de cada obligación (historial/asignar_plazos.py la
// escribe) en vez de vivir aquí como constante.
export function resumenCumplimiento() {
  const entidades = obtenerEntidades();
  const porEstado = {};
  const entidadesPorFecha = {};
  const cuentasPorEntidad = new Set();
  let total = 0;

  for (const e of entidades) {
    cuentasPorEntidad.add((e.obligaciones ?? []).length);
    for (const o of e.obligaciones ?? []) {
      total += 1;
      porEstado[o.estado] = (porEstado[o.estado] ?? 0) + 1;
    }
    // Todas las obligaciones de una entidad comparten tramo, así que basta la
    // primera con fecha para saber cuándo le vence.
    const fecha = (e.obligaciones ?? []).find((o) => o.fecha_limite)?.fecha_limite;
    if (fecha) entidadesPorFecha[fecha] = (entidadesPorFecha[fecha] ?? 0) + 1;
  }

  const hoy = new Date();
  const plazos = Object.entries(entidadesPorFecha)
    .map(([fecha, entidades]) => ({
      fecha,
      entidades,
      diasRestantes: Math.ceil((new Date(`${fecha}T00:00:00-05:00`) - hoy) / 86400000),
    }))
    .sort((a, b) => a.fecha.localeCompare(b.fecha));

  return {
    total,
    // Sólo tiene sentido decir "N entidades × M obligaciones" si M es el mismo
    // para todas. Si algún día deja de serlo, se devuelve null y el panel calla
    // en vez de afirmar una multiplicación falsa.
    porEntidad: cuentasPorEntidad.size === 1 ? [...cuentasPorEntidad][0] : null,
    cumplidas: porEstado.cumplido_con_evidencia ?? 0,
    noCumplidas: porEstado.no_cumplido ?? 0,
    noVerificables: porEstado.no_verificable_desde_fuentes_publicas ?? 0,
    noAplicaTodavia: porEstado.no_aplica_todavia ?? 0,
    sinPlazo: entidades.length - Object.values(entidadesPorFecha).reduce((a, b) => a + b, 0),
    plazos,
  };
}
