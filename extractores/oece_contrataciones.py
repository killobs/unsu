"""Extractor: detección de sistemas de IA por término en contrataciones OECE.

Metodología completa en docs/metodologia.md §3, validada en la Fase 0
(docs/fase-0-detectabilidad.md). Resumen: la API de búsqueda del OECE hace
coincidencia difusa por palabra suelta, no por frase exacta -- hasta 82% de
falsos positivos sin filtrar. Este extractor filtra por frase exacta del lado
del cliente y trata todo resultado como CANDIDATO, nunca como alta directa
confirmada.

Uso:
    python extractores/oece_contrataciones.py             # años recientes
    python extractores/oece_contrataciones.py --historico  # 2004-presente
"""
import datetime
import json
import os
import sys
import re
import unicodedata
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractores.comun import esquema, evidencia, estado_ejecuciones
from extractores.comun.http_cliente import obtener

NOMBRE_EXTRACTOR = "oece_contrataciones"
API_BASE = "https://contratacionesabiertas.oece.gob.pe/api/v1"

# "redes neuronales" se excluyó: en la Fase 0 dio 0% de precisión incluso con
# filtro de frase exacta (ver docs/fase-0-detectabilidad.md §2).
TERMINOS = [
    "inteligencia artificial", "aprendizaje automático", "machine learning",
    "reconocimiento facial", "biometría", "analítica predictiva",
    "procesamiento de lenguaje natural", "chatbot", "asistente virtual",
    "visión computacional", "modelo predictivo", "algoritmo de scoring",
    "deep learning", "IA generativa", "voicebot",
    # Ampliación 2026-07-27.
    "visión artificial", "aprendizaje profundo", "reconocimiento de voz",
    "reconocimiento de imágenes", "reconocimiento biométrico",
    "análisis predictivo", "modelo de lenguaje", "bot conversacional",
    "sistema experto", "minería de datos", "ciencia de datos",
    "automatización robótica de procesos", "gemelo digital",
    "detección automática",
]

# "mantenimiento predictivo" se probó el 2026-07-27 y se retiró el mismo día:
# es una metodología de mantenimiento industrial anterior a la IA (termografía,
# análisis de vibraciones). Generó 74 fichas de mantenimiento de transformadores
# y subestaciones eléctricas, ninguna de ellas un sistema de IA. Es el mismo
# error que "redes neuronales" en la Fase 0: una frase que suena a IA y no lo es.
TERMINOS_DESCARTADOS = ["mantenimiento predictivo", "redes neuronales"]

AÑO_ACTUAL = datetime.date.today().year
# Antes eran solo dos años (el actual y el anterior). Las contrataciones de IA
# arrancan en la práctica a mitad de la década pasada, así que el barrido
# habitual cubre desde 2018.
AÑOS_RECIENTES = [str(a) for a in range(2018, AÑO_ACTUAL + 1)]
AÑOS_HISTORICO = [str(a) for a in range(2004, AÑO_ACTUAL + 1)]

DIR_CRUDOS = os.path.join(esquema.RAIZ, "datos", "crudos")


def _buscar(termino, año, pagina=1, paginateBy=50):
    enc = urllib.parse.quote(termino)
    url = f"{API_BASE}/search?page={pagina}&paginateBy={paginateBy}&search={enc}&year={año}&format=json"
    respuesta = obtener(url)
    return json.loads(respuesta)


# Tope de seguridad: si una consulta devolviera miles de páginas, no queremos
# barrer la API entera. Con 50 por página son hasta 2000 resultados por consulta.
MAX_PAGINAS = 40


def _buscar_todas_las_paginas(termino, año):
    """La API pagina de 50 en 50. Antes solo se leía la primera página, así que
    toda consulta con más de 50 resultados perdía el resto en silencio: por
    ejemplo "inteligencia artificial" en 2025 devuelve 92 y se veían 50."""
    primera = _buscar(termino, año)
    resultados = list(primera.get("results", []))
    paginacion = primera.get("pagination") or {}
    total = paginacion.get("total_results", len(resultados))
    num_paginas = min(paginacion.get("num_pages", 1) or 1, MAX_PAGINAS)

    for pagina in range(2, num_paginas + 1):
        siguiente = _buscar(termino, año, pagina=pagina)
        nuevos = siguiente.get("results", [])
        if not nuevos:
            break
        resultados.extend(nuevos)

    return resultados, total, num_paginas


def _coincide_frase_exacta(termino, resultado):
    tender = resultado.get("compiledRelease", {}).get("tender", {})
    texto = f"{tender.get('title', '')} {tender.get('description', '')}".lower()
    return termino.lower() in texto


def _url_evidencia(resultado):
    releases = resultado.get("releases", [])
    if releases and releases[0].get("url"):
        url = releases[0]["url"]
    else:
        sources = resultado.get("compiledRelease", {}).get("sources", [])
        url = sources[0].get("url", "") if sources else ""
    # La propia API del OECE devuelve, en algunas releases historicas, URLs con
    # el dominio anterior "osce.gob.pe" que ya no resuelve (DNS muerto,
    # confirmado a mano). El dominio vigente es "oece.gob.pe" -- se normaliza
    # aqui para no guardar enlaces rotos como evidencia.
    return url.replace("contratacionesabiertas.osce.gob.pe", "contratacionesabiertas.oece.gob.pe")


def barrer(años):
    candidatos = []
    resumen = []
    for termino in TERMINOS:
        for año in años:
            try:
                resultados, total, paginas = _buscar_todas_las_paginas(termino, año)
            except Exception as e:
                resumen.append({"termino": termino, "año": año, "error": str(e)})
                continue
            coincidencias = [r for r in resultados if _coincide_frase_exacta(termino, r)]
            resumen.append(
                {
                    "termino": termino,
                    "año": año,
                    "bruto": len(resultados),
                    "total_declarado": total,
                    "paginas": paginas,
                    "frase_exacta": len(coincidencias),
                    # Aviso si topamos con el límite: querría decir que aún falta cobertura.
                    "truncado": paginas >= MAX_PAGINAS,
                }
            )
            for r in coincidencias:
                candidatos.append({"termino": termino, "año": año, "resultado": r})
    return candidatos, resumen


def _guardar_crudo(resumen):
    os.makedirs(DIR_CRUDOS, exist_ok=True)
    hoy = datetime.date.today().isoformat()
    ruta = os.path.join(DIR_CRUDOS, f"{hoy}_oece_contrataciones_resumen.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)


RUTA_EXCLUIDOS = os.path.join(esquema.RAIZ, "datos", "excluidos.yaml")

# Un candidato solo entra si su propio texto evidencia IA, sin depender del
# término que disparó la búsqueda. Sin esta puerta, un término mal elegido
# ("mantenimiento predictivo") mete decenas de contratos que no son IA.
#
# NO se aplica a lo confirmado por fuente oficial: "Evaluación de expedientes
# electorales" o "Verificación biométrica en línea" son sistemas de IA reales
# cuya descripción corta no repite la frase "inteligencia artificial".
SENAL_IA = re.compile(
    r"inteligencia artificial|\bia\b|machine learning|aprendizaje autom|"
    r"aprendizaje profundo|deep learning|red(es)? neuronal|algoritmo|chatbot|"
    r"\bbot\b|asistente virtual|voicebot|reconocimiento facial|biometr|"
    r"vision (computacional|artificial)|procesamiento de lenguaje|"
    r"modelo predictivo|generativa|\bllm\b",
    re.I,
)


def _sin_acentos(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def evidencia_propia_de_ia(texto):
    """¿El texto muestra IA por sí mismo, sin apoyarse en el término buscado?"""
    return bool(SENAL_IA.search(_sin_acentos(texto or "")))


def _cargar_excluidos():
    """Candidatos ya revisados a mano y descartados por no ser sistemas de IA.

    Sin esta lista, cada corrida del extractor volvería a dar de alta el mismo
    biorreactor, el mismo congreso y los mismos gabinetes de servidores: la
    revisión manual se perdería en cada barrido.
    """
    if not os.path.isfile(RUTA_EXCLUIDOS):
        return set(), set()
    import yaml as _yaml

    with open(RUTA_EXCLUIDOS, encoding="utf-8") as f:
        datos = _yaml.safe_load(f) or []
    ids = {e.get("id") for e in datos if e.get("id")}
    urls = {e.get("evidencia") for e in datos if e.get("evidencia")}
    return ids, urls


def _incorporar_candidatos(candidatos, entidades, sistemas):
    nuevos_sistemas = 0
    nuevas_entidades = 0
    ids_excluidos, urls_excluidas = _cargar_excluidos()
    for c in candidatos:
        r = c["resultado"]
        tender = r.get("compiledRelease", {}).get("tender", {})
        buyer = r.get("compiledRelease", {}).get("buyer", {}) or tender.get("procuringEntity", {})
        nombre_entidad = buyer.get("name", "").strip()
        if not nombre_entidad:
            continue
        if "MUNICIPALIDAD" in nombre_entidad.upper():
            # Gobiernos locales fuera de alcance en esta version (prompt
            # original §9: sus plazos normativos son de tres años o más).
            continue
        url_ev = _url_evidencia(r)
        if not url_ev:
            continue
        if url_ev in urls_excluidas:
            continue

        titulo_desc = f"{tender.get('title', '')} {tender.get('description', '')}"
        if not evidencia_propia_de_ia(titulo_desc):
            # El termino coincidio pero el texto no evidencia IA por si mismo.
            continue

        eid = esquema.slugify(nombre_entidad)
        titulo = tender.get("title") or tender.get("description", "")[:60]
        sid = f"{eid}--{esquema.slugify(titulo)}--{esquema.slugify(c['termino'])}"

        ya_existe = False
        for s in sistemas.values():
            if esquema.evidencia_ya_registrada(s, url_ev):
                ya_existe = True
                break
        if ya_existe or sid in sistemas or sid in ids_excluidos:
            continue

        # La entidad se crea aqui, no antes: si el candidato se descarta mas
        # arriba, dar de alta la entidad deja una ficha huerfana sin ningun
        # sistema. Asi pasaron a existir 48 de ellas en el barrido del 27 de
        # julio, y el sitio las listaba vacias.
        if eid not in entidades:
            entidades[eid] = esquema.entidad_nueva(nombre_entidad)
            nuevas_entidades += 1

        sistemas[sid] = {
            "id": sid,
            "entidad_id": eid,
            "nombre": titulo,
            "sector": entidades[eid]["sector"],
            "nivel_gobierno": entidades[eid]["nivel_gobierno"],
            "finalidad": tender.get("description", ""),
            "tipo_decision": "",
            "supervision_humana_declarada": "no_declarado",
            "proveedor": "",
            "vinculo_contractual": "",
            "presupuesto": str(tender.get("value", {}).get("amount_PEN", "")),
            "estado": "indeterminado",
            "tecnologias": "",
            "clasificacion_riesgo_propia": "pendiente_de_clasificar",
            "mapeo_eu_ai_act": "",
            "mapeo_nist_ai_rmf": "",
            "nivel_confianza": "inferido_contratacion",
            "evidencia": [evidencia.nueva(
                url_ev,
                f'Candidato detectado por el término "{c["termino"]}" en contrataciones OECE {c["año"]} '
                f"(ocid: {r.get('compiledRelease', {}).get('ocid', '')})."
            )],
            "fecha_alta_registro": datetime.date.today().isoformat(),
            "notas": "Candidato generado automáticamente por extractores/oece_contrataciones.py. Pendiente de revisión y confirmación.",
        }
        nuevos_sistemas += 1
    return nuevos_sistemas, nuevas_entidades


def main():
    historico = "--historico" in sys.argv
    años = AÑOS_HISTORICO if historico else AÑOS_RECIENTES
    try:
        candidatos, resumen = barrer(años)
        _guardar_crudo(resumen)
        entidades = esquema.cargar_entidades()
        sistemas = esquema.cargar_sistemas()
        nuevos_sistemas, nuevas_entidades = _incorporar_candidatos(candidatos, entidades, sistemas)
        for eid, edata in entidades.items():
            esquema.guardar_entidad(edata)
        for sid, sdata in sistemas.items():
            esquema.guardar_sistema(sdata)
        mensaje = f"{len(candidatos)} candidatos brutos, {nuevos_sistemas} sistemas nuevos, {nuevas_entidades} entidades nuevas"
        print(mensaje)
        estado_ejecuciones.registrar_resultado(NOMBRE_EXTRACTOR, ok=True, mensaje=mensaje)
    except Exception as e:
        estado_ejecuciones.registrar_resultado(NOMBRE_EXTRACTOR, ok=False, mensaje=str(e))
        raise


if __name__ == "__main__":
    main()
