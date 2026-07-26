"use client";
import { useMemo, useState } from "react";
import Link from "next/link";
import { t } from "@/lib/diccionario";
import EtiquetaRiesgo from "@/components/EtiquetaRiesgo";

export default function IndiceCliente({ locale, sistemas, baseHrefSistema }) {
  const d = t(locale);
  const [busqueda, setBusqueda] = useState("");
  const [sector, setSector] = useState("");
  const [riesgo, setRiesgo] = useState("");
  const [confianza, setConfianza] = useState("");

  const sectores = useMemo(
    () => Array.from(new Set(sistemas.map((s) => s.sector).filter(Boolean))).sort((a, b) => a.localeCompare(b, "es")),
    [sistemas]
  );

  const filtrados = useMemo(() => {
    const q = busqueda.trim().toLowerCase();
    return sistemas.filter((s) => {
      if (sector && s.sector !== sector) return false;
      if (riesgo && s.clasificacion_riesgo_propia !== riesgo) return false;
      if (confianza && s.nivel_confianza !== confianza) return false;
      if (q && !`${s.nombre} ${s.entidadNombre}`.toLowerCase().includes(q)) return false;
      return true;
    });
  }, [sistemas, busqueda, sector, riesgo, confianza]);

  return (
    <>
      <div className="filtros">
        <label>
          {d.buscarPlaceholder}
          <input
            type="text"
            value={busqueda}
            placeholder={d.buscarPlaceholder}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </label>
        <label>
          {d.filtroSector}
          <select value={sector} onChange={(e) => setSector(e.target.value)}>
            <option value="">{d.filtroTodos}</option>
            {sectores.map((sec) => (
              <option key={sec} value={sec}>
                {sec}
              </option>
            ))}
          </select>
        </label>
        <label>
          {d.filtroRiesgo}
          <select value={riesgo} onChange={(e) => setRiesgo(e.target.value)}>
            <option value="">{d.filtroTodos}</option>
            {Object.entries(d.riesgos).map(([valor, etiqueta]) => (
              <option key={valor} value={valor}>
                {etiqueta}
              </option>
            ))}
          </select>
        </label>
        <label>
          {d.filtroConfianza}
          <select value={confianza} onChange={(e) => setConfianza(e.target.value)}>
            <option value="">{d.filtroTodos}</option>
            {Object.entries(d.confianzas).map(([valor, etiqueta]) => (
              <option key={valor} value={valor}>
                {etiqueta}
              </option>
            ))}
          </select>
        </label>
      </div>

      {filtrados.length === 0 ? (
        <p className="sin-resultados">{d.sinResultados}</p>
      ) : (
        <table className="tabla-sistemas">
          <thead>
            <tr>
              <th>{d.columnaSistema}</th>
              <th>{d.columnaEntidad}</th>
              <th>{d.columnaSector}</th>
              <th>{d.columnaRiesgo}</th>
              <th>{d.columnaConfianza}</th>
              <th>{d.columnaEstado}</th>
            </tr>
          </thead>
          <tbody>
            {filtrados.map((s) => (
              <tr key={s.id}>
                <td data-etiqueta={d.columnaSistema}>
                  <Link href={`${baseHrefSistema}/${s.id}`}>{s.nombre}</Link>
                </td>
                <td data-etiqueta={d.columnaEntidad}>{s.entidadNombre}</td>
                <td data-etiqueta={d.columnaSector}>{s.sector}</td>
                <td data-etiqueta={d.columnaRiesgo}>
                  <EtiquetaRiesgo locale={locale} valor={s.clasificacion_riesgo_propia} />
                </td>
                <td data-etiqueta={d.columnaConfianza}>{d.confianzas[s.nivel_confianza] ?? s.nivel_confianza}</td>
                <td data-etiqueta={d.columnaEstado}>{d.estados[s.estado] ?? s.estado}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
