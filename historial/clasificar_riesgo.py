"""Aplica la clasificación de riesgo de docs/metodologia.md §4 a las fichas.

Se hace como script y no a mano para que quede auditable: cada asignación
lleva aquí su criterio, y volver a correrlo da el mismo resultado.

Los cuatro niveles de la metodología:
  alto            decide o asiste una decisión que afecta un derecho
                  fundamental o un proceso con consecuencias legales
  limitado        interactúa con la ciudadanía sin decidir sobre derechos
  minimo          uso interno, sin interacción pública ni decisión
  pendiente_de_clasificar  información insuficiente en la fuente

Uso:  python historial/clasificar_riesgo.py [--aplicar]
      Sin --aplicar solo muestra qué haría.
"""
import glob
import os
import sys

import yaml

RAIZ = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, RAIZ)

# Se escribe con el volcado del propio proyecto (orden de campos fijo) y no con
# yaml.safe_dump: si no, cada ficha se reordenaría entera y el diff de Git
# taparía el único campo que de verdad cambió.
from extractores.comun import esquema  # noqa: E402

DIR = os.path.join(RAIZ, "datos", "sistemas")

# Fragmento identificador -> (nivel, criterio)
# El fragmento se busca dentro del id de la ficha.
CLASIFICACION = {
    # ── Riesgo alto ────────────────────────────────────────────────────
    # Los cinco primeros calzan literalmente con los ejemplos de la metodología.
    "hospital-regional-de-lambayeque": (
        "alto", "Diagnóstico médico (ejemplo literal de la metodología §4)."),
    "instituto-nacional-de-enfermedades-neoplasicas": (
        "alto", "Diagnóstico médico (ejemplo literal de la metodología §4)."),
    "jurado-nacional-de-elecciones--eleccia": (
        "alto", "Evaluación de expedientes electorales (ejemplo literal de la metodología §4)."),
    "poder-judicial": (
        "alto", "Proyección de resoluciones judiciales (ejemplo literal de la metodología §4)."),
    "registro-nacional-de-identificacion-y-estado-civil--biofacial": (
        "alto", "Verificación biométrica para identidad (ejemplo literal de la metodología §4)."),
    # Los dos siguientes son interpretación del proyecto, no ejemplo literal.
    "ministerio-de-trabajo-y-promocion-del-empleo": (
        "alto",
        "Interpretación del proyecto, no ejemplo literal de la metodología: la "
        "intermediación laboral condiciona el acceso al empleo. El EU AI Act trata "
        "el empleo como alto riesgo (Anexo III)."),
    "organismo-de-supervision-de-los-recursos-forestales": (
        "alto",
        "Interpretación del proyecto, no ejemplo literal de la metodología: la "
        "detección alimenta fiscalización con consecuencias legales para el titular "
        "de la concesión."),

    # ── Riesgo limitado: atienden al público, no deciden sobre derechos ──
    "biblioteca-nacional-del-peru": ("limitado", "Chatbot de atención al público."),
    "comision-de-promocion-del-peru": ("limitado", "Herramienta de orientación al público."),
    "fondo-de-aseguramiento-en-salud": ("limitado", "Voicebot de atención a asegurados."),
    "fondo-mivivienda": ("limitado", "Plataforma de atención ciudadana."),
    "instituto-de-investigaciones-de-la-amazonia": ("limitado", "App de consulta para usuarios; no decide."),
    "instituto-nacional-de-salud-del-nino": ("limitado", "Orientación informativa al público."),
    "instituto-tecnologico-de-la-produccion": ("limitado", "Herramienta de identificación; no decide sobre derechos."),
    "ministerio-de-la-produccion": ("limitado", "Asesoría empresarial informativa."),
    "ministerio-de-transportes-y-comunicaciones": ("limitado", "Asistente virtual de atención ciudadana."),
    "organismo-supervisor-de-inversion-privada-en-telecomunicaciones": (
        "limitado", "Asesor virtual de atención al usuario."),
    "presidencia-del-consejo-de-ministros": ("limitado", "Chatbot informativo sobre normas."),
    "registro-nacional-de-identificacion-y-estado-civil--res-proc": (
        "limitado", "Chatbot de atención; no realiza la verificación de identidad."),
    "servicio-de-agua-potable-y-alcantarillado-de-arequipa": ("limitado", "Contact center con bot de atención."),
    "servicio-nacional-de-certificacion-ambiental": ("limitado", "Orientación normativa al administrado."),
    "superintendencia-nacional-de-aduanas": ("limitado", "Asistente virtual SOFIA de atención al contribuyente."),
    "superintendencia-nacional-de-los-registros-publicos": (
        "limitado", "Lectura en audio de esquelas; accesibilidad, no decisión."),

    # ── Riesgo mínimo: uso interno ──────────────────────────────────────
    "banco-central-de-reserva-del-peru": ("minimo", "Uso interno, sin interacción con el público."),
    "creacion-y-mejoramiento-del-servicio-de-catastro": ("minimo", "Gestión interna de un servicio catastral."),
    "ministerio-de-comercio-exterior-y-turismo": ("minimo", "Apoyo documental interno."),
    "ministerio-de-desarrollo-agrario-y-riego": ("minimo", "Consulta sobre visor geográfico."),
    "ministerio-del-ambiente": ("minimo", "Soporte al reporte administrativo de municipalidades."),
    "ministerio-del-interior": ("minimo", "Monitoreo de servidores (ejemplo literal de la metodología §4)."),
    "organismo-supervisor-de-la-inversion-en-energia": ("minimo", "Infraestructura y soporte interno."),
    "programa-nacional-plataformas-de-accion": ("minimo", "Asistencia técnica a personal interno."),
    "san-gaban": ("minimo", "Selección de normas para uso interno."),
    "superintendencia-nacional-de-migraciones": ("minimo", "Administración interna de tickets."),
    "superintendencia-nacional-de-servicios-de-saneamiento": ("minimo", "Automatización de informes internos."),
}

# Fichas que se dejan pendientes a propósito, con el motivo explícito.
# La metodología §4 reserva "pendiente_de_clasificar" para información
# insuficiente: eso es exactamente lo que pasa aquí.
PENDIENTES = {
    "ministerio-de-educacion": "La ficha no registra finalidad; sin ella no se puede asignar nivel.",
    "proinnovate": (
        "No consta qué papel cumple la IA en la evaluación de postulaciones. "
        "Si decide o pondera, sería riesgo alto; hace falta revisar la fuente."),
}


# Solo se clasifican las fichas revisadas a mano el 2026-07-27, que son las
# dadas de alta el 2026-07-26. Las 193 que trajo el barrido ampliado NO se han
# leído una por una y deben quedarse en "pendiente_de_clasificar": es
# información honesta, no un hueco que tapar.
REVISADAS_HASTA = "2026-07-26"


RUTA_MANUAL = os.path.join(os.path.dirname(__file__), "clasificacion_manual.yaml")


def _manuales():
    """Decisiones tomadas leyendo ficha por ficha, con id completo.

    Van en un archivo aparte y por id exacto — no por fragmento de entidad,
    que en una corrida anterior clasificó fichas nunca revisadas solo por
    compartir entidad con otra.
    """
    if not os.path.isfile(RUTA_MANUAL):
        return {}
    with open(RUTA_MANUAL, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


MANUAL = _manuales()


def nivel_para(sid, alta):
    m = MANUAL.get(sid)
    if m:
        return m["nivel"], m["criterio"]
    if alta != REVISADAS_HASTA:
        return None, None
    for frag, (nivel, criterio) in CLASIFICACION.items():
        if frag in sid:
            return nivel, criterio
    for frag, motivo in PENDIENTES.items():
        if frag in sid:
            return "pendiente_de_clasificar", motivo
    return None, None


MARCA = "Clasificación de riesgo:"


def _limpiar_nota(nota):
    """Quita una marca de clasificación puesta por una corrida anterior."""
    i = nota.find(MARCA)
    return nota[:i].strip() if i >= 0 else nota.strip()


def main():
    aplicar = "--aplicar" in sys.argv
    cuenta = {}
    sin_asignar = []

    reparadas = 0

    for ruta in sorted(glob.glob(os.path.join(DIR, "*.yaml"))):
        with open(ruta, encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
        sid = d.get("id", "")
        nivel, criterio = nivel_para(sid, d.get("fecha_alta_registro", ""))

        if nivel is None:
            sin_asignar.append(sid)
            # Deshace una clasificación que una corrida anterior puso por error
            # sobre una ficha no revisada.
            nota = d.get("notas") or ""
            if MARCA in nota or d.get("clasificacion_riesgo_propia") != "pendiente_de_clasificar":
                if aplicar:
                    d["clasificacion_riesgo_propia"] = "pendiente_de_clasificar"
                    d["notas"] = _limpiar_nota(nota)
                    esquema.guardar_sistema(d)
                reparadas += 1
            continue

        cuenta[nivel] = cuenta.get(nivel, 0) + 1
        if not aplicar:
            continue

        d["clasificacion_riesgo_propia"] = nivel
        nota = _limpiar_nota(d.get("notas") or "")
        d["notas"] = f"{nota} {MARCA} {criterio}".strip()
        esquema.guardar_sistema(d)

    if reparadas:
        print(f"{reparadas} fichas devueltas a pendiente (no revisadas)\n")

    for nivel, n in sorted(cuenta.items(), key=lambda kv: -kv[1]):
        print(f"{n:3}  {nivel}")
    if sin_asignar:
        print(f"\nSIN REGLA ({len(sin_asignar)}) — revisar a mano:")
        for s in sin_asignar:
            print("   ", s)
    print("\naplicado" if aplicar else "\nsimulación: nada escrito (usa --aplicar)")


if __name__ == "__main__":
    main()
