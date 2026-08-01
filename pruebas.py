"""Pruebas de la lógica que decide qué entra al registro y con qué nivel.

Sin framework: assert y un mensaje claro cuando algo falla. Cada prueba nace de
un fallo real ocurrido el 27 de julio de 2026, no de un caso inventado.

Uso:  python pruebas.py
"""
import glob
import os
import sys

import yaml

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

from extractores.oece_contrataciones import (  # noqa: E402
    TERMINOS,
    TERMINOS_DESCARTADOS,
    evidencia_propia_de_ia,
)

fallos = []


def comprobar(condicion, mensaje):
    if condicion:
        return
    fallos.append(mensaje)


# ── La puerta de señal de IA ──────────────────────────────────────────────
# Un término mal elegido metió 74 fichas de mantenimiento de transformadores
# eléctricos. La puerta exige que el texto evidencie IA por sí mismo.

comprobar(
    evidencia_propia_de_ia("SERVICIO DE IMPLEMENTACION DE UN ASISTENTE VIRTUAL"),
    "deberia aceptar un asistente virtual",
)
comprobar(
    evidencia_propia_de_ia("Chatbot de atencion al ciudadano"),
    "deberia aceptar un chatbot",
)
comprobar(
    not evidencia_propia_de_ia(
        "Servicio de mantenimiento predictivo, preventivo y correctivo de "
        "subestaciones de transformacion"
    ),
    "NO deberia aceptar mantenimiento electrico sin senal de IA",
)
comprobar(
    not evidencia_propia_de_ia("ADQUISICION DE CAMARA TERMOGRAFICA"),
    "NO deberia aceptar una camara termografica",
)

# Tildes: "biométrica" tiene que coincidir con el patrón "biometr".
comprobar(
    evidencia_propia_de_ia("Verificación biométrica en línea para emisión de documentos"),
    "deberia reconocer 'biometrica' con tilde",
)
comprobar(
    evidencia_propia_de_ia("Sistema de visión computacional"),
    "deberia reconocer 'vision' con tilde",
)

# ── Términos descartados ──────────────────────────────────────────────────
for t in TERMINOS_DESCARTADOS:
    comprobar(
        t not in TERMINOS,
        f"el termino descartado {t!r} no deberia estar en la lista activa",
    )
comprobar(
    "mantenimiento predictivo" in TERMINOS_DESCARTADOS,
    "'mantenimiento predictivo' debe seguir registrado como descartado",
)

# ── Los datos publicados ──────────────────────────────────────────────────
sistemas = [
    yaml.safe_load(open(p, encoding="utf-8"))
    for p in glob.glob(os.path.join(RAIZ, "datos", "sistemas", "*.yaml"))
]
entidades = [
    yaml.safe_load(open(p, encoding="utf-8"))
    for p in glob.glob(os.path.join(RAIZ, "datos", "entidades", "*.yaml"))
]

# Ninguna entidad sin sistemas: el extractor las creaba antes de comprobar si
# el candidato se descartaba, y dejo 48 fichas huerfanas.
con_sistema = {s.get("entidad_id") for s in sistemas}
huerfanas = [e["id"] for e in entidades if e.get("id") not in con_sistema]
comprobar(not huerfanas, f"hay {len(huerfanas)} entidades sin ningun sistema: {huerfanas[:3]}")

# Presupuesto 0 significa "no publicado", nunca gratis.
ceros = [
    s["id"]
    for s in sistemas
    if str(s.get("presupuesto") or "").strip() in ("0", "0.0", "0.00")
]
comprobar(not ceros, f"hay fichas con presupuesto 0 sin normalizar: {ceros[:3]}")

# Toda clasificación asignada lleva su criterio escrito en la ficha.
sin_criterio = [
    s["id"]
    for s in sistemas
    if s.get("clasificacion_riesgo_propia") not in (None, "", "pendiente_de_clasificar")
    and "Clasificación de riesgo:" not in (s.get("notas") or "")
]
comprobar(
    not sin_criterio,
    f"hay clasificaciones sin criterio en 'notas': {sin_criterio[:3]}",
)

# Lo confirmado por fuente oficial nunca se filtra por la puerta de senal:
# si se hiciera, se perderian EleccIA, la biometria de RENIEC y la deteccion
# de tala de OSINFOR, cuyas descripciones cortas no repiten "inteligencia
# artificial".
confirmados = [s for s in sistemas if s.get("nivel_confianza") == "confirmado_fuente_oficial"]
sin_senal = [
    s["id"]
    for s in confirmados
    if not evidencia_propia_de_ia((s.get("finalidad") or "") + " " + (s.get("nombre") or ""))
]
comprobar(
    len(confirmados) > 0,
    "deberia haber sistemas confirmados por fuente oficial",
)
comprobar(
    len(sin_senal) > 0,
    "se espera que algun confirmado NO pase la puerta: es la razon de que la "
    "puerta no se les aplique. Si esto falla, revisar que la exencion siga viva.",
)

# ── Resultado ─────────────────────────────────────────────────────────────
print(f"{len(sistemas)} sistemas y {len(entidades)} entidades comprobados")
if fallos:
    print(f"\n{len(fallos)} fallos:\n")
    for f in fallos:
        print(f"  {f}")
    sys.exit(1)
print("todas las pruebas pasaron")
