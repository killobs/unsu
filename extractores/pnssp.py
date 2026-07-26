"""Extractor: Plataforma Nacional de Software Público Peruano (PNSSP).

Verifica el artículo 28.8 del reglamento (publicación de código fuente) -- con
una salvedad importante confirmada en la Fase 0 (docs/fase-0-detectabilidad.md
§2): las fichas de detalle del PNSSP declaran una "Licencia" (Libre/Abierta)
pero NO enlazan a un repositorio de código descargable. Por eso este extractor
nunca marca la obligación como "cumplido_con_evidencia" solo por encontrar el
software registrado -- eso confirma registro, no publicación de código.

ponytail: el listado se scrapea con regex sobre bloques <article>, no con un
parser HTML de verdad -- la plantilla del portal es estable y simple (una
tarjeta por sistema, dos badges, un enlace). Si el portal cambia de plantilla
esto se rompe con claridad (deja de encontrar coincidencias) en vez de fallar
en silencio. Subir a BeautifulSoup si el HTML se vuelve más irregular.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractores.comun import esquema, estado_ejecuciones
from extractores.comun.http_cliente import obtener

NOMBRE_EXTRACTOR = "pnssp"
BASE = "https://www.softwarepublico.gob.pe"

RE_TARJETA = re.compile(r"<article.*?</article>", re.S)
RE_BADGE = re.compile(r'inline-flex items-center justify-center[^"]*"[^>]*>([^<]+)</span>')
RE_ENLACE = re.compile(r'pnsp_js_detalle_catalogo\((\d+),\s*(\d+)\)"[^>]*>([^<]+)</a>')


def _listar_catalogo():
    # El portal no devuelve vacío al pasarse de la última página: repite la
    # última página real indefinidamente (confirmado probando ?pag=15..30).
    # Por eso el corte es "esta página no trajo ningún par (id_catalogo,
    # id_entidad) nuevo", no "esta página vino vacía".
    entradas = []
    vistos = set()
    pagina = 1
    while True:
        html = obtener(f"{BASE}/catalogo/catalogo_servicios.aspx?pag={pagina}")
        tarjetas = RE_TARJETA.findall(html)
        if not tarjetas:
            break
        nuevas_en_pagina = 0
        for tarjeta in tarjetas:
            m = RE_ENLACE.search(tarjeta)
            if not m:
                continue
            id_catalogo, id_entidad, nombre = m.groups()
            clave = (id_catalogo, id_entidad)
            if clave in vistos:
                continue
            vistos.add(clave)
            nuevas_en_pagina += 1
            badges = RE_BADGE.findall(tarjeta)
            entidad = badges[1].strip() if len(badges) > 1 else ""
            entradas.append({
                "id_catalogo": id_catalogo, "id_entidad": id_entidad,
                "nombre": nombre.strip(), "entidad": entidad,
            })
        if nuevas_en_pagina == 0:
            break
        pagina += 1
        if pagina > 50:  # tope de seguridad, el catálogo no debería tener 500 páginas
            break
    return entradas


def _detalle(id_catalogo, id_entidad):
    html = obtener(
        f"{BASE}/catalogo/catalogo_detalle.aspx",
        datos_post=f"id_catalogo={id_catalogo}&id_entidad={id_entidad}&accion=M",
    )
    texto = re.sub(r"<[^>]+>", " ", html)
    texto = re.sub(r"\s+", " ", texto)
    m = re.search(r"Licencia\s+([A-Za-zÀ-ÿ ]+?)\s+Año", texto)
    licencia = m.group(1).strip() if m else ""
    tiene_enlace_codigo = bool(re.search(r"github\.com|gitlab\.com", html, re.I))
    return {"licencia": licencia, "tiene_enlace_codigo": tiene_enlace_codigo}


def ejecutar():
    entidades = esquema.cargar_entidades()
    entradas = _listar_catalogo()
    hoy = datetime.date.today().isoformat()
    actualizadas = 0

    entradas_por_entidad = {}
    for e in entradas:
        entradas_por_entidad.setdefault(esquema.slugify(e["entidad"]), []).append(e)

    for eid, edata in entidades.items():
        registros = entradas_por_entidad.get(eid, [])
        if not registros:
            continue
        obligacion = next(
            (o for o in edata["obligaciones"]
             if o["obligacion"].startswith("Codigo fuente publicado")),
            None,
        )
        if obligacion is None:
            continue

        tiene_codigo_real = False
        licencias_libres = []
        for r in registros:
            try:
                d = _detalle(r["id_catalogo"], r["id_entidad"])
            except Exception:
                continue
            if d["tiene_enlace_codigo"]:
                tiene_codigo_real = True
            if "libre" in d["licencia"].lower() or "abiert" in d["licencia"].lower():
                licencias_libres.append(r["nombre"])

        if tiene_codigo_real:
            obligacion["estado"] = "cumplido_con_evidencia"
        else:
            # registrado en PNSSP con licencia declarada libre, pero sin
            # repositorio verificable: sigue siendo "no verificable", no
            # "cumplido" (ver docs/metodologia.md §3) ni "no cumplido"
            # (el registro en sí es evidencia parcial, no ausencia de ella).
            obligacion["estado"] = "no_verificable_desde_fuentes_publicas"

        nombres_unicos = sorted(set(licencias_libres))
        nota = f"{len(registros)} software(s) registrados en PNSSP"
        if nombres_unicos:
            listado = ", ".join(nombres_unicos[:8])
            if len(nombres_unicos) > 8:
                listado += f" y {len(nombres_unicos) - 8} más"
            nota += f", con licencia declarada libre/abierta: {listado}"
        nota += ". Sin enlace a repositorio de código verificable en la ficha de detalle." if not tiene_codigo_real else "."
        obligacion["evidencia"] = [{
            "url": f"{BASE}/catalogo/catalogo_servicios.aspx",
            "fecha_captura": hoy,
            "descripcion": nota,
        }]
        actualizadas += 1

    for edata in entidades.values():
        esquema.guardar_entidad(edata)

    return f"{len(entradas)} fichas revisadas en PNSSP, {actualizadas} entidades actualizadas"


def main():
    try:
        mensaje = ejecutar()
        print(mensaje)
        estado_ejecuciones.registrar_resultado(NOMBRE_EXTRACTOR, ok=True, mensaje=mensaje)
    except Exception as e:
        estado_ejecuciones.registrar_resultado(NOMBRE_EXTRACTOR, ok=False, mensaje=str(e))
        raise


if __name__ == "__main__":
    main()
