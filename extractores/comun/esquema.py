"""Esquema de datos y utilidades de lectura/escritura determinista.

Ver docs/metodologia.md §5-6 para la definición de cada campo. El orden de
las claves es parte del contrato: no se reordena entre corridas, para que
el diff de Git muestre solo lo que cambió de verdad (ver prompt original, §4).
"""
import glob
import os
import re
import unicodedata

import yaml

RAIZ = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
DIR_SISTEMAS = os.path.join(RAIZ, "datos", "sistemas")
DIR_ENTIDADES = os.path.join(RAIZ, "datos", "entidades")

SISTEMA_ORDEN = [
    "id", "entidad_id", "nombre", "sector", "nivel_gobierno", "finalidad", "tipo_decision",
    "supervision_humana_declarada", "proveedor", "vinculo_contractual", "presupuesto",
    "estado", "tecnologias", "clasificacion_riesgo_propia", "mapeo_eu_ai_act", "mapeo_nist_ai_rmf",
    "nivel_confianza", "evidencia", "fecha_alta_registro", "notas",
]

ENTIDAD_ORDEN = ["id", "nombre", "sector", "nivel_gobierno", "obligaciones"]

OBLIGACIONES_BASE = [
    "Politica institucional de IA aprobada",
    "Proyectos de IA incorporados en el Plan de Gobierno Digital",
    "Codigo fuente publicado en la Plataforma Nacional de Software Publico Peruano",
    "Documentacion de sistemas de riesgo alto",
    "Mecanismos de supervision humana declarados",
    "Transparencia algoritmica frente al usuario",
]


def slugify(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto).strip("-").lower()
    return texto


def _volcar_ordenado(d, orden):
    salida = {k: d.get(k, "") for k in orden}
    return yaml.dump(salida, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)


def guardar_sistema(datos):
    with open(os.path.join(DIR_SISTEMAS, f"{datos['id']}.yaml"), "w", encoding="utf-8") as f:
        f.write(_volcar_ordenado(datos, SISTEMA_ORDEN))


def guardar_entidad(datos):
    with open(os.path.join(DIR_ENTIDADES, f"{datos['id']}.yaml"), "w", encoding="utf-8") as f:
        f.write(_volcar_ordenado(datos, ENTIDAD_ORDEN))


def cargar_sistemas():
    sistemas = {}
    for ruta in glob.glob(os.path.join(DIR_SISTEMAS, "*.yaml")):
        with open(ruta, encoding="utf-8") as f:
            d = yaml.safe_load(f)
        sistemas[d["id"]] = d
    return sistemas


def cargar_entidades():
    entidades = {}
    for ruta in glob.glob(os.path.join(DIR_ENTIDADES, "*.yaml")):
        with open(ruta, encoding="utf-8") as f:
            d = yaml.safe_load(f)
        entidades[d["id"]] = d
    return entidades


def entidad_nueva(nombre, sector="Por clasificar", nivel_gobierno="nacional"):
    return {
        "id": slugify(nombre),
        "nombre": nombre,
        "sector": sector,
        "nivel_gobierno": nivel_gobierno,
        "obligaciones": [
            {"obligacion": o, "estado": "no_verificable_desde_fuentes_publicas", "fecha_limite": "", "evidencia": []}
            for o in OBLIGACIONES_BASE
        ],
    }


def evidencia_ya_registrada(sistema, url):
    """Evita duplicar una ficha si la misma URL de evidencia ya está registrada."""
    return any(e.get("url") == url for e in sistema.get("evidencia", []))
