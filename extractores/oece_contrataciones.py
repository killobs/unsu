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
]

AÑO_ACTUAL = datetime.date.today().year
AÑOS_RECIENTES = [str(a) for a in range(AÑO_ACTUAL - 1, AÑO_ACTUAL + 1)]
AÑOS_HISTORICO = [str(a) for a in range(2004, AÑO_ACTUAL + 1)]

DIR_CRUDOS = os.path.join(esquema.RAIZ, "datos", "crudos")


def _buscar(termino, año, pagina=1, paginateBy=50):
    enc = urllib.parse.quote(termino)
    url = f"{API_BASE}/search?page={pagina}&paginateBy={paginateBy}&search={enc}&year={año}&format=json"
    respuesta = obtener(url)
    return json.loads(respuesta)


def _coincide_frase_exacta(termino, resultado):
    tender = resultado.get("compiledRelease", {}).get("tender", {})
    texto = f"{tender.get('title', '')} {tender.get('description', '')}".lower()
    return termino.lower() in texto


def _url_evidencia(resultado):
    releases = resultado.get("releases", [])
    if releases and releases[0].get("url"):
        return releases[0]["url"]
    sources = resultado.get("compiledRelease", {}).get("sources", [])
    if sources:
        return sources[0].get("url", "")
    return ""


def barrer(años):
    candidatos = []
    resumen = []
    for termino in TERMINOS:
        for año in años:
            try:
                data = _buscar(termino, año)
            except Exception as e:
                resumen.append({"termino": termino, "año": año, "error": str(e)})
                continue
            resultados = data.get("results", [])
            coincidencias = [r for r in resultados if _coincide_frase_exacta(termino, r)]
            resumen.append({"termino": termino, "año": año, "bruto": len(resultados), "frase_exacta": len(coincidencias)})
            for r in coincidencias:
                candidatos.append({"termino": termino, "año": año, "resultado": r})
    return candidatos, resumen


def _guardar_crudo(resumen):
    os.makedirs(DIR_CRUDOS, exist_ok=True)
    hoy = datetime.date.today().isoformat()
    ruta = os.path.join(DIR_CRUDOS, f"{hoy}_oece_contrataciones_resumen.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)


def _incorporar_candidatos(candidatos, entidades, sistemas):
    nuevos_sistemas = 0
    nuevas_entidades = 0
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

        eid = esquema.slugify(nombre_entidad)
        if eid not in entidades:
            entidades[eid] = esquema.entidad_nueva(nombre_entidad)
            nuevas_entidades += 1

        titulo = tender.get("title") or tender.get("description", "")[:60]
        sid = f"{eid}--{esquema.slugify(titulo)}--{esquema.slugify(c['termino'])}"

        ya_existe = False
        for s in sistemas.values():
            if esquema.evidencia_ya_registrada(s, url_ev):
                ya_existe = True
                break
        if ya_existe or sid in sistemas:
            continue

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
