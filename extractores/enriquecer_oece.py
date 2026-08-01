"""Vuelve a la fuente OECE de cada ficha y trae lo que el alta inicial no guardó.

El extractor solo se quedaba con título, descripción y monto. La release trae
además:

  - mainProcurementCategory: bienes / servicios / obras. Criterio objetivo para
    decidir si la contratación puede ser un sistema: un sistema de IA se compra
    como SERVICIO. "Bienes" es equipamiento y "obras" es construcción.
  - procurementMethodDetails: tipo de proceso.
  - datePublished y tenderPeriod: cuándo ocurrió.
  - items: el detalle de lo contratado, más preciso que la descripción.
  - parties con rol de proveedor, cuando ya está adjudicado.

Guarda todo en datos/crudos/enriquecimiento_oece.json para no repetir peticiones.

Uso:  python extractores/enriquecer_oece.py [--refrescar]
"""
import glob
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractores.comun import esquema  # noqa: E402
from extractores.comun.http_cliente import obtener  # noqa: E402

CACHE = os.path.join(esquema.RAIZ, "datos", "crudos", "enriquecimiento_oece.json")


def _release(url):
    datos = json.loads(obtener(url))
    if "releases" in datos and datos["releases"]:
        return datos["releases"][0]
    if "compiledRelease" in datos:
        return datos["compiledRelease"]
    return datos


def _extraer(rel):
    t = rel.get("tender", {}) or {}
    partes = rel.get("parties", []) or []

    proveedor = ""
    for p in partes:
        roles = [r.lower() for r in (p.get("roles") or [])]
        if "supplier" in roles:
            proveedor = p.get("name", "")
            break

    items = []
    for it in (t.get("items") or [])[:4]:
        desc = (it.get("description") or "").strip()
        if desc:
            items.append(desc[:180])

    valor = (t.get("value") or {}).get("amount_PEN")

    return {
        "categoria": t.get("mainProcurementCategory") or "",
        "metodo": t.get("procurementMethodDetails") or "",
        "titulo": (t.get("title") or "").strip(),
        "descripcion": (t.get("description") or "").strip(),
        "items": items,
        "valor": valor,
        "fecha": (t.get("datePublished") or rel.get("date") or "")[:10],
        "proveedor": proveedor,
        "postores": t.get("numberOfTenderers"),
        "ocid": rel.get("ocid", ""),
    }


def main():
    refrescar = "--refrescar" in sys.argv
    cache = {}
    if os.path.isfile(CACHE) and not refrescar:
        with open(CACHE, encoding="utf-8") as f:
            cache = json.load(f)

    rutas = sorted(glob.glob(os.path.join(esquema.RAIZ, "datos", "sistemas", "*.yaml")))
    nuevos = errores = 0

    for i, ruta in enumerate(rutas, 1):
        with open(ruta, encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
        sid = d.get("id")
        if not sid or sid in cache:
            continue
        ev = (d.get("evidencia") or [{}])[0].get("url", "")
        if not ev:
            cache[sid] = {"error": "sin evidencia"}
            continue
        try:
            cache[sid] = _extraer(_release(ev))
            nuevos += 1
        except Exception as e:  # noqa: BLE001
            cache[sid] = {"error": str(e)[:120]}
            errores += 1
        if i % 25 == 0:
            print(f"  {i}/{len(rutas)}…", flush=True)
            with open(CACHE, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=1)

    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)

    print(f"{nuevos} fichas enriquecidas, {errores} con error, {len(cache)} en total")
    print(f"-> {CACHE}")


if __name__ == "__main__":
    main()
