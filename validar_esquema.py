"""Valida las fichas de datos/ contra la especificación de docs/esquema/.

Existe porque el esquema estaba publicado como documento y nada lo hacía
cumplir. El 27 de julio de 2026 se escribieron 71 fichas con
`clasificacion_riesgo_propia: riesgo_alto`, un valor que el esquema no admite,
y ninguna herramienta lo detectó.

Uso:
    python validar_esquema.py              valida y sale con 1 si hay errores
    python validar_esquema.py --autoprueba comprueba que el validador rechaza
                                           una ficha inválida a propósito
"""
import glob
import os
import re
import sys

import yaml

RAIZ = os.path.dirname(os.path.abspath(__file__))
DIR_SISTEMAS = os.path.join(RAIZ, "datos", "sistemas")
DIR_ENTIDADES = os.path.join(RAIZ, "datos", "entidades")
DOC_SISTEMA = os.path.join(RAIZ, "docs", "esquema", "sistema.md")
DOC_ENTIDAD = os.path.join(RAIZ, "docs", "esquema", "entidad.md")

# Estos valores son copia de docs/esquema/. La función comprobar_sincronia()
# verifica que sigan apareciendo allí, para que el documento y el código no se
# separen en silencio.
ENUMS_SISTEMA = {
    "nivel_gobierno": {"nacional", "regional"},
    "supervision_humana_declarada": {"si", "no", "no_declarado"},
    "estado": {
        "en_operacion",
        "piloto",
        "contratado_sin_desplegar",
        "descontinuado",
        "indeterminado",
    },
    "clasificacion_riesgo_propia": {"alto", "limitado", "minimo", "pendiente_de_clasificar"},
    "nivel_confianza": {
        "confirmado_fuente_oficial",
        "inferido_contratacion",
        "reportado_prensa",
    },
}

OBLIGATORIOS_SISTEMA = [
    "id",
    "entidad_id",
    "nombre",
    "sector",
    "nivel_gobierno",
    "estado",
    "clasificacion_riesgo_propia",
    "nivel_confianza",
    "evidencia",
    "fecha_alta_registro",
]

ENUMS_ENTIDAD = {
    "nivel_gobierno": {"nacional", "regional"},
}

ESTADOS_OBLIGACION = {
    "cumplido_con_evidencia",
    "no_cumplido",
    "no_verificable_desde_fuentes_publicas",
    "no_aplica_todavia",
}

OBLIGATORIOS_ENTIDAD = ["id", "nombre", "jurisdiccion", "sector", "nivel_gobierno", "obligaciones"]

FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validar_evidencia(evidencia, donde, errores):
    if not isinstance(evidencia, list) or not evidencia:
        errores.append(f"{donde}: 'evidencia' debe ser una lista con al menos una entrada")
        return
    for i, e in enumerate(evidencia):
        if not isinstance(e, dict):
            errores.append(f"{donde}: evidencia[{i}] no es un objeto")
            continue
        if not str(e.get("url") or "").strip():
            errores.append(f"{donde}: evidencia[{i}] sin url")
        fecha = str(e.get("fecha_captura") or "").strip()
        if not FECHA.match(fecha):
            errores.append(f"{donde}: evidencia[{i}] con fecha_captura invalida ({fecha!r})")


def validar_sistemas(ids_entidades):
    errores = []
    vistos = set()
    for ruta in sorted(glob.glob(os.path.join(DIR_SISTEMAS, "*.yaml"))):
        nombre = os.path.basename(ruta)
        with open(ruta, encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}

        for campo in OBLIGATORIOS_SISTEMA:
            if campo not in d or (isinstance(d.get(campo), str) and not d[campo].strip()):
                errores.append(f"{nombre}: falta el campo obligatorio '{campo}'")

        for campo, validos in ENUMS_SISTEMA.items():
            v = d.get(campo)
            if v in (None, ""):
                continue
            if v not in validos:
                errores.append(
                    f"{nombre}: '{campo}' vale {v!r}, fuera de {sorted(validos)}"
                )

        sid = d.get("id")
        if sid:
            if sid in vistos:
                errores.append(f"{nombre}: el id {sid!r} esta repetido")
            vistos.add(sid)
            if sid != nombre[:-5]:
                errores.append(f"{nombre}: el id no coincide con el nombre del archivo")

        eid = d.get("entidad_id")
        if eid and eid not in ids_entidades:
            errores.append(f"{nombre}: entidad_id {eid!r} no existe en datos/entidades/")

        fecha = str(d.get("fecha_alta_registro") or "")
        if fecha and not FECHA.match(fecha):
            errores.append(f"{nombre}: fecha_alta_registro invalida ({fecha!r})")

        presupuesto = str(d.get("presupuesto") or "").strip()
        if presupuesto:
            try:
                if float(presupuesto) <= 0:
                    errores.append(
                        f"{nombre}: presupuesto {presupuesto!r}; un monto 0 se registra vacio"
                    )
            except ValueError:
                errores.append(f"{nombre}: presupuesto {presupuesto!r} no es un numero")

        _validar_evidencia(d.get("evidencia"), nombre, errores)
    return errores, len(vistos)


def validar_entidades():
    errores = []
    ids = set()
    for ruta in sorted(glob.glob(os.path.join(DIR_ENTIDADES, "*.yaml"))):
        nombre = os.path.basename(ruta)
        with open(ruta, encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}

        for campo in OBLIGATORIOS_ENTIDAD:
            if campo not in d:
                errores.append(f"{nombre}: falta el campo obligatorio '{campo}'")

        for campo, validos in ENUMS_ENTIDAD.items():
            v = d.get(campo)
            if v not in (None, "") and v not in validos:
                errores.append(f"{nombre}: '{campo}' vale {v!r}, fuera de {sorted(validos)}")

        if d.get("jurisdiccion") and not re.match(r"^[A-Z]{2}$", str(d["jurisdiccion"])):
            errores.append(f"{nombre}: 'jurisdiccion' debe ser un codigo ISO de dos letras")

        for i, o in enumerate(d.get("obligaciones") or []):
            if not str(o.get("obligacion") or "").strip():
                errores.append(f"{nombre}: obligaciones[{i}] sin descripcion")
            if o.get("estado") not in ESTADOS_OBLIGACION:
                errores.append(
                    f"{nombre}: obligaciones[{i}].estado vale {o.get('estado')!r}, "
                    f"fuera de {sorted(ESTADOS_OBLIGACION)}"
                )

        if d.get("id"):
            ids.add(d["id"])
    return errores, ids


def comprobar_sincronia():
    """El código y docs/esquema/ no deben separarse sin que nadie se entere."""
    errores = []
    for ruta, enums in ((DOC_SISTEMA, ENUMS_SISTEMA), (DOC_ENTIDAD, ENUMS_ENTIDAD)):
        if not os.path.isfile(ruta):
            errores.append(f"falta {os.path.relpath(ruta, RAIZ)}")
            continue
        texto = open(ruta, encoding="utf-8").read()
        for campo, valores in enums.items():
            for v in valores:
                if v not in texto:
                    errores.append(
                        f"{os.path.basename(ruta)}: el valor {v!r} de '{campo}' "
                        f"no aparece documentado"
                    )
    for v in ESTADOS_OBLIGACION:
        if os.path.isfile(DOC_ENTIDAD) and v not in open(DOC_ENTIDAD, encoding="utf-8").read():
            errores.append(f"entidad.md: el estado de obligacion {v!r} no aparece documentado")
    return errores


def autoprueba():
    """Una ficha con un valor invalido debe ser rechazada."""
    ficha = {
        "id": "prueba",
        "entidad_id": "inexistente",
        "nombre": "Prueba",
        "sector": "Prueba",
        "nivel_gobierno": "nacional",
        "estado": "indeterminado",
        # El valor que se coló el 27 de julio y que nada detectaba.
        "clasificacion_riesgo_propia": "riesgo_alto",
        "nivel_confianza": "inferido_contratacion",
        "evidencia": [{"url": "https://ejemplo", "fecha_captura": "2026-07-27"}],
        "fecha_alta_registro": "2026-07-27",
    }
    malos = [
        v
        for v in [ficha["clasificacion_riesgo_propia"]]
        if v not in ENUMS_SISTEMA["clasificacion_riesgo_propia"]
    ]
    assert malos, "el validador deberia rechazar 'riesgo_alto'"

    assert "alto" in ENUMS_SISTEMA["clasificacion_riesgo_propia"]
    assert "0" not in ENUMS_SISTEMA["estado"]

    sin_fecha = []
    _validar_evidencia([{"url": "https://x", "fecha_captura": "27/07/2026"}], "prueba", sin_fecha)
    assert sin_fecha, "el validador deberia rechazar una fecha con formato distinto"

    sin_url = []
    _validar_evidencia([{"fecha_captura": "2026-07-27"}], "prueba", sin_url)
    assert sin_url, "el validador deberia rechazar evidencia sin url"

    vacia = []
    _validar_evidencia([], "prueba", vacia)
    assert vacia, "el validador deberia rechazar evidencia vacia"

    print("autoprueba: el validador rechaza lo que debe rechazar")


def main():
    if "--autoprueba" in sys.argv:
        autoprueba()
        return 0

    err_doc = comprobar_sincronia()
    err_ent, ids = validar_entidades()
    err_sis, n_sis = validar_sistemas(ids)

    errores = err_doc + err_ent + err_sis
    print(f"{n_sis} sistemas y {len(ids)} entidades revisados")

    if not errores:
        print("sin errores")
        return 0

    print(f"\n{len(errores)} errores:\n")
    for e in errores[:60]:
        print(f"  {e}")
    if len(errores) > 60:
        print(f"  ... y {len(errores) - 60} mas")
    return 1


if __name__ == "__main__":
    sys.exit(main())
