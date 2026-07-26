"""Registro de corridas de cada extractor, para poder abrir un issue automático
cuando un extractor falla dos corridas seguidas (Fase 2, §7 del prompt original).

Sin base de datos: el estado se guarda como JSON versionado en el repo, igual
que el resto de los datos. Es intencionalmente el único archivo del proyecto
que no sigue el esquema de sistemas/entidades -- es metadato operativo, no dato
del registro.
"""
import datetime
import json
import os

RAIZ = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUTA_ESTADO = os.path.join(RAIZ, "datos", "crudos", "_estado_extractores.json")

UMBRAL_ALERTA = 2


def _cargar():
    if not os.path.exists(RUTA_ESTADO):
        return {}
    with open(RUTA_ESTADO, encoding="utf-8") as f:
        return json.load(f)


def _guardar(estado):
    os.makedirs(os.path.dirname(RUTA_ESTADO), exist_ok=True)
    with open(RUTA_ESTADO, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def registrar_resultado(nombre_extractor, ok, mensaje=""):
    estado = _cargar()
    previo = estado.get(nombre_extractor, {"fallos_consecutivos": 0})
    fallos = 0 if ok else previo.get("fallos_consecutivos", 0) + 1
    estado[nombre_extractor] = {
        "ultima_corrida": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "resultado": "ok" if ok else "error",
        "fallos_consecutivos": fallos,
        "ultimo_mensaje": mensaje,
    }
    _guardar(estado)
    return fallos


def necesita_alerta(nombre_extractor):
    estado = _cargar()
    return estado.get(nombre_extractor, {}).get("fallos_consecutivos", 0) >= UMBRAL_ALERTA
