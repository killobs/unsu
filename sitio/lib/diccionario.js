// Textos de interfaz en los dos idiomas. Los VALORES de los datos (nombres,
// finalidades, sectores...) siguen en español -- traducirlos es trabajo de
// curaduría aparte, no de esta fase. Ver docs/metodologia.md y docs/bitacora.md.
// "setiembre" y no "septiembre": es la grafía que usa El Peruano y con la que
// está publicado el DS 115-2025-PCM.
const MESES = {
  es: ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
       "agosto", "setiembre", "octubre", "noviembre", "diciembre"],
  en: ["January", "February", "March", "April", "May", "June", "July",
       "August", "September", "October", "November", "December"],
};

// La fecha llega como "AAAA-MM-DD" y se parte a mano: pasarla por new Date()
// la interpretaría en UTC y en Perú (UTC-5) mostraría el día anterior.
function fechaLarga(iso, locale) {
  const [anio, mes, dia] = iso.split("-").map(Number);
  const nombreMes = MESES[locale][mes - 1];
  return locale === "es"
    ? `${dia} de ${nombreMes} de ${anio}`
    : `${nombreMes} ${dia}, ${anio}`;
}

export const diccionario = {
  es: {
    tituloSitio: "Registro de IA Pública — Perú",
    tituloPlantilla: "%s · Registro de IA Pública",
    saltarAlContenido: "Saltar al contenido",
    descripcionSitio:
      "Registro público, versionado y continuo de los sistemas de inteligencia artificial que el Estado peruano compra y despliega.",
    metaEntidad: (nombre, n) =>
      n === 0
        ? `Obligaciones de cumplimiento de ${nombre} bajo el DS 115-2025-PCM. Todavía no se ha detectado ningún sistema de IA de esta entidad.`
        : `${n} ${n === 1 ? "sistema de IA detectado" : "sistemas de IA detectados"} en ${nombre}, con evidencia fechada, y sus obligaciones de cumplimiento bajo el DS 115-2025-PCM.`,
    metaSistemas: "Índice completo de sistemas de IA detectados en el Estado peruano, con filtros por sector, riesgo y nivel de confianza.",
    metaEntidades: "Entidades del Estado peruano con sistemas de IA detectados y seguimiento de sus obligaciones de cumplimiento.",
    navSistemas: "Sistemas",
    navEntidades: "Entidades",
    navMetodologia: "Metodología",
    navIdioma: "English",
    inicioTitulo: "Sistemas de IA en el Estado peruano",
    inicioIntro:
      "Cada ficha lleva evidencia con fecha de captura. La clasificación de riesgo es propia del proyecto, no oficial. Ver metodología.",
    marca: "Unsu",
    heroProducto: "Registro de IA Pública",
    heroTitular: "Cada sistema de IA del Estado peruano, con evidencia.",
    heroBajada:
      "Registro público, versionado y continuo. Cada ficha cita su fuente con fecha de captura, y declara si el dato es hecho confirmado o inferencia.",
    heroVerRegistro: "Ver el registro",
    heroDesplazar: "Desplázate",
    heroCredito: "Nevado Ausangate, Cusco. Foto de Edubucher (CC BY-SA 3.0), tramada digitalmente.",
    cifraSistemas: "sistemas documentados",
    cifraEntidades: "entidades del Estado",
    cifraPresupuesto: "en contrataciones rastreadas",
    cifraObligaciones: "obligaciones seguidas",
    cifraPresupuestoNota: (n, total) => `Suma de ${n} de ${total} fichas; el resto no declara monto.`,
    distribucionTitulo: "Distribución de riesgo",
    distribucionIntro:
      "Clasificación propia del proyecto, no oficial. Cuatro niveles inspirados en el EU AI Act, aplicados ficha por ficha con el criterio anotado en cada una.",
    confianzaTitulo: "Cómo se detectó cada sistema",
    confianzaIntro:
      "El registro nunca promueve una inferencia a hecho confirmado. Cada ficha declara de dónde salió, y el nivel se muestra con la misma prioridad que cualquier otro campo.",
    confianzaDescripciones: {
      confirmado_fuente_oficial: "Aparece nombrado en un documento oficial: el catálogo de la PCM, el portal de la entidad, una norma o una resolución.",
      inferido_contratacion: "Detectado por coincidencia de frase exacta en una contratación pública del OECE, sin confirmación oficial adicional.",
      reportado_prensa: "Solo aparece en cobertura periodística, sin documento oficial ni contratación identificable.",
    },
    registroTitulo: "El registro",
    piePropiedad: "Unsu · Registro de IA Pública es el primer producto de Unsu.",
    filtroSector: "Sector",
    filtroRiesgo: "Riesgo",
    filtroConfianza: "Nivel de confianza",
    filtroTodos: "Todos",
    buscarPlaceholder: "Buscar por nombre o entidad…",
    columnaSistema: "Sistema",
    columnaEntidad: "Entidad",
    columnaSector: "Sector",
    columnaRiesgo: "Riesgo",
    columnaConfianza: "Confianza",
    columnaEstado: "Estado",
    sinResultados: "Ningún sistema coincide con estos filtros.",
    conteoResultados: (n, total) => (n === total ? `${total} sistemas` : `${n} de ${total} sistemas`),
    limpiarFiltros: "Limpiar filtros",
    panelCumplimientoTitulo: "Cumplimiento frente al reglamento",
    panelCumplimientoDetalle: (c, numeroEntidades) =>
      `De ${c.total} obligaciones seguidas en ${numeroEntidades} entidades: ` +
      `${c.cumplidas} con evidencia de cumplimiento, ` +
      `${c.noCumplidas} con evidencia de incumplimiento y ` +
      `${c.noVerificables} sin fuente pública que acredite ninguna de las dos cosas.`,
    panelCumplimientoAviso:
      "No verificable no quiere decir incumplido. Quiere decir que este registro todavía no " +
      "encontró una fuente pública que lo acredite en un sentido ni en el otro, y no da por " +
      "incumplida ninguna obligación sin evidencia de que lo esté.",
    panelCumplimientoSeleccion: (total, entidades, porEntidad) =>
      `Ese total es ${entidades} entidades × ${porEntidad} obligaciones = ${total}, y no el total de lo que exige el ` +
      `reglamento: las ${porEntidad} son una selección propia del proyecto, tomada de los artículos 28 y 29. ` +
      `Ver metodología.`,
    panelCumplimientoPlazo: (plazos) =>
      plazos.length === 0
        ? "Todavía no hay plazo asignado a estas entidades."
        : "El reglamento escalona el plazo por tipo de entidad: " +
          plazos
            .map(
              (p) =>
                `${p.entidades} ${p.entidades === 1 ? "entidad vence" : "entidades vencen"} el ` +
                `${fechaLarga(p.fecha, "es")}` +
                (p.diasRestantes >= 0 ? ` (faltan ${p.diasRestantes} días)` : " (plazo vencido)"),
            )
            .join(", y ") +
          ".",
    fichaEntidad: "Entidad",
    fichaFinalidad: "Finalidad",
    fichaTecnologias: "Tecnologías utilizadas",
    fichaEstado: "Estado",
    fichaProveedor: "Proveedor",
    fichaVinculo: "Vínculo contractual",
    fichaPresupuesto: "Presupuesto",
    fichaSupervisionHumana: "Supervisión humana declarada",
    fichaRiesgo: "Clasificación de riesgo (propia)",
    fichaEuAiAct: "Mapeo EU AI Act",
    fichaNistAiRmf: "Mapeo NIST AI RMF",
    fichaConfianza: "Nivel de confianza",
    fichaEvidencia: "Evidencia",
    fichaNotas: "Notas",
    fichaSinDato: "No declarado",
    entidadSistemas: "Sistemas de esta entidad",
    entidadObligaciones: "Obligaciones de cumplimiento",
    entidadSinSistemas: "No se detectó ningún sistema de esta entidad todavía.",
    columnaObligacion: "Obligación",
    columnaEstadoObligacion: "Estado",
    columnaFechaLimite: "Fecha límite",
    volverIndice: "← Volver al índice",
    volverEntidad: "← Volver a la entidad",
    piePropia: "Clasificación de riesgo propia del proyecto, no oficial.",
    pieFuente: "Código y datos: ",
    pieDescarga: "Descargar todo el conjunto de datos (JSON)",
    pieLicencia: "Código bajo licencia MIT, datos bajo CC BY-SA 4.0.",
    pieInterfases:
      "Incluye la línea base de Huancapaza Hilasaca, J. E. (2025). Implementación de inteligencia artificial en el Estado peruano: catálogo analítico de aplicaciones. Interfases, (22), 143-158.",
    estados: {
      en_operacion: "En operación",
      piloto: "Piloto",
      contratado_sin_desplegar: "Contratado sin desplegar",
      descontinuado: "Descontinuado",
      indeterminado: "Indeterminado",
    },
    riesgos: {
      alto: "Alto",
      limitado: "Limitado",
      minimo: "Mínimo",
      pendiente_de_clasificar: "Pendiente de clasificar",
    },
    confianzas: {
      confirmado_fuente_oficial: "Confirmado por fuente oficial",
      inferido_contratacion: "Inferido de contratación",
      reportado_prensa: "Reportado por prensa",
    },
    obligacionEstados: {
      cumplido_con_evidencia: "Cumplido con evidencia",
      no_cumplido: "No cumplido",
      no_verificable_desde_fuentes_publicas: "No verificable desde fuentes públicas",
      no_aplica_todavia: "No aplica todavía",
    },
    supervisionHumana: {
      si: "Sí",
      no: "No",
      no_declarado: "No declarado",
    },
  },
  en: {
    tituloSitio: "Public AI Registry — Peru",
    tituloPlantilla: "%s · Public AI Registry",
    saltarAlContenido: "Skip to content",
    descripcionSitio:
      "A public, versioned, ongoing registry of the artificial intelligence systems the Peruvian State procures and deploys.",
    metaEntidad: (nombre, n) =>
      n === 0
        ? `Compliance obligations for ${nombre} under DS 115-2025-PCM. No AI system from this entity has been detected yet.`
        : `${n} AI ${n === 1 ? "system" : "systems"} detected at ${nombre}, with dated evidence, and its compliance obligations under DS 115-2025-PCM.`,
    metaSistemas: "Full index of AI systems detected in the Peruvian State, filterable by sector, risk and confidence level.",
    metaEntidades: "Peruvian State entities with detected AI systems and tracking of their compliance obligations.",
    navSistemas: "Systems",
    navEntidades: "Entities",
    navMetodologia: "Methodology",
    navIdioma: "Español",
    inicioTitulo: "AI systems in the Peruvian State",
    inicioIntro:
      "Every entry carries evidence with a capture date. The risk classification is the project's own, not official. See methodology.",
    marca: "Unsu",
    heroProducto: "Public AI Registry",
    heroTitular: "Every AI system in the Peruvian State, with evidence.",
    heroBajada:
      "A public, versioned, ongoing registry. Every record cites its source with a capture date, and states whether the data is confirmed fact or inference.",
    heroVerRegistro: "See the registry",
    heroDesplazar: "Scroll",
    heroCredito: "Ausangate, Cusco. Photo by Edubucher (CC BY-SA 3.0), digitally dithered.",
    cifraSistemas: "systems documented",
    cifraEntidades: "State entities",
    cifraPresupuesto: "in tracked procurement",
    cifraObligaciones: "obligations tracked",
    cifraPresupuestoNota: (n, total) => `Sum of ${n} of ${total} records; the rest declare no amount.`,
    distribucionTitulo: "Risk distribution",
    distribucionIntro:
      "The project's own classification, not official. Four tiers modeled on the EU AI Act, applied record by record with the criterion noted in each one.",
    confianzaTitulo: "How each system was detected",
    confianzaIntro:
      "The registry never promotes an inference to confirmed fact. Every record states where it came from, and the level is shown with the same priority as any other field.",
    confianzaDescripciones: {
      confirmado_fuente_oficial: "Named in an official document: the PCM catalogue, the entity's own portal, a regulation or a resolution.",
      inferido_contratacion: "Detected by exact-phrase match in OECE public procurement data, with no additional official confirmation.",
      reportado_prensa: "Appears only in press coverage, with no official document or identifiable contract.",
    },
    registroTitulo: "The registry",
    piePropiedad: "Unsu · Public AI Registry is Unsu's first product.",
    filtroSector: "Sector",
    filtroRiesgo: "Risk",
    filtroConfianza: "Confidence level",
    filtroTodos: "All",
    buscarPlaceholder: "Search by name or entity…",
    columnaSistema: "System",
    columnaEntidad: "Entity",
    columnaSector: "Sector",
    columnaRiesgo: "Risk",
    columnaConfianza: "Confidence",
    columnaEstado: "Status",
    sinResultados: "No system matches these filters.",
    conteoResultados: (n, total) => (n === total ? `${total} systems` : `${n} of ${total} systems`),
    limpiarFiltros: "Clear filters",
    panelCumplimientoTitulo: "Compliance with the regulation",
    panelCumplimientoDetalle: (c, numeroEntidades) =>
      `Of ${c.total} obligations tracked across ${numeroEntidades} entities: ` +
      `${c.cumplidas} with evidence of compliance, ` +
      `${c.noCumplidas} with evidence of non-compliance, and ` +
      `${c.noVerificables} with no public source establishing either.`,
    panelCumplimientoAviso:
      "Not verifiable does not mean non-compliant. It means this registry has not yet found a " +
      "public source establishing it either way, and it does not record any obligation as " +
      "breached without evidence that it is.",
    panelCumplimientoSeleccion: (total, entidades, porEntidad) =>
      `That total is ${entidades} entities × ${porEntidad} obligations = ${total}, not the full set the regulation ` +
      `requires: the ${porEntidad} are the project's own selection, drawn from articles 28 and 29. See methodology.`,
    panelCumplimientoPlazo: (plazos) =>
      plazos.length === 0
        ? "No deadline has been assigned to these entities yet."
        : "The regulation staggers the deadline by type of entity: " +
          plazos
            .map(
              (p) =>
                `${p.entidades} ${p.entidades === 1 ? "entity is due" : "entities are due"} on ` +
                `${fechaLarga(p.fecha, "en")}` +
                (p.diasRestantes >= 0 ? ` (${p.diasRestantes} days left)` : " (deadline passed)"),
            )
            .join(", and ") +
          ".",
    fichaEntidad: "Entity",
    fichaFinalidad: "Purpose",
    fichaTecnologias: "Technologies used",
    fichaEstado: "Status",
    fichaProveedor: "Provider",
    fichaVinculo: "Contractual link",
    fichaPresupuesto: "Budget",
    fichaSupervisionHumana: "Declared human oversight",
    fichaRiesgo: "Risk classification (project's own)",
    fichaEuAiAct: "EU AI Act mapping",
    fichaNistAiRmf: "NIST AI RMF mapping",
    fichaConfianza: "Confidence level",
    fichaEvidencia: "Evidence",
    fichaNotas: "Notes",
    fichaSinDato: "Not declared",
    entidadSistemas: "Systems from this entity",
    entidadObligaciones: "Compliance obligations",
    entidadSinSistemas: "No system from this entity has been detected yet.",
    columnaObligacion: "Obligation",
    columnaEstadoObligacion: "Status",
    columnaFechaLimite: "Deadline",
    volverIndice: "← Back to index",
    volverEntidad: "← Back to entity",
    piePropia: "Risk classification is the project's own, not official.",
    pieFuente: "Code and data: ",
    pieDescarga: "Download the full dataset (JSON)",
    pieLicencia: "Code under MIT license, data under CC BY-SA 4.0.",
    pieInterfases:
      "Includes the baseline from Huancapaza Hilasaca, J. E. (2025). Implementación de inteligencia artificial en el Estado peruano: catálogo analítico de aplicaciones. Interfases, (22), 143-158.",
    estados: {
      en_operacion: "In operation",
      piloto: "Pilot",
      contratado_sin_desplegar: "Contracted, not deployed",
      descontinuado: "Discontinued",
      indeterminado: "Undetermined",
    },
    riesgos: {
      alto: "High",
      limitado: "Limited",
      minimo: "Minimal",
      pendiente_de_clasificar: "Pending classification",
    },
    confianzas: {
      confirmado_fuente_oficial: "Confirmed by official source",
      inferido_contratacion: "Inferred from procurement",
      reportado_prensa: "Press-reported",
    },
    obligacionEstados: {
      cumplido_con_evidencia: "Met with evidence",
      no_cumplido: "Not met",
      no_verificable_desde_fuentes_publicas: "Not verifiable from public sources",
      no_aplica_todavia: "Not yet applicable",
    },
    supervisionHumana: {
      si: "Yes",
      no: "No",
      no_declarado: "Not declared",
    },
  },
};

export function t(locale) {
  return diccionario[locale] ?? diccionario.es;
}
