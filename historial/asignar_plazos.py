"""Escribe en cada obligación el plazo que le toca según el DS 115-2025-PCM.

La Primera Disposición Complementaria Final del reglamento NO da una sola fecha
para todo el Estado: escalona la implementación del artículo 25 y del Capítulo I
del Título VI por TIPO de entidad. El registro mostraba el 10 de setiembre de
2026 para las 48 entidades, que es el tramo más corto y no le aplica a todas.

El reglamento se publicó el martes 9 de setiembre de 2025 en El Peruano y los
plazos cuentan "a partir del día siguiente", así que la cuenta arranca el
2025-09-10.

Tramos de la Primera DCF, para entidades de la Administración Pública:

  a) Poder Ejecutivo, Legislativo y Judicial ............... 1 año  -> 2026-09-10
  b) Organismos Constitucionales Autónomos ................ 1 año  -> 2026-09-10
  c) EsSalud, gobiernos regionales, universidades públicas . 2 años -> 2027-09-10
  d) Gobiernos locales Tipo A, B y C ...................... 3 años -> 2028-09-10
  e) Empresas públicas regionales, locales o bajo FONAFE ... 2 años -> 2027-09-10
  f) Demás entidades de los numerales 7 y 8 del artículo I
     del Título Preliminar de la Ley 27444 ................ 2 años -> 2027-09-10
  g) Gobiernos locales Tipo D a G ......................... facultativo

El corte entre (a) y (f) se apoya en el propio artículo I del Título Preliminar
de la Ley 27444, al que el inciso f) remite: su numeral 1 mete dentro del Poder
Ejecutivo a los "Ministerios y Organismos Públicos Descentralizados", mientras
que su numeral 7 recoge aparte a los "proyectos y programas del Estado". Por eso
los ministerios y los organismos adscritos van al tramo de un año, y los
programas y proyectos de inversión al de dos.

Esta asignación es lectura del proyecto, igual que la clasificación de riesgo, y
así se declara en docs/metodologia.md §4.c. No es una calificación oficial: el
reglamento no publica un padrón que diga qué tramo le toca a cada entidad.

Una entidad sin tramo asignado aquí se queda con `fecha_limite` vacío y el
script avisa. Se prefiere el vacío a heredar una fecha por defecto, porque una
fecha equivocada en un registro de cumplimiento acusa a una entidad de ir tarde
cuando todavía está en plazo.

Uso:  python historial/asignar_plazos.py [--aplicar]
      Sin --aplicar solo muestra qué haría.
"""
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, RAIZ)

from extractores.comun import esquema  # noqa: E402

TRAMOS = {
    "a": ("2026-09-10", "Poder Ejecutivo, Legislativo o Judicial (Primera DCF, inciso a)."),
    "b": ("2026-09-10", "Organismo Constitucional Autónomo (Primera DCF, inciso b)."),
    "c": ("2027-09-10", "EsSalud, gobierno regional o universidad pública (Primera DCF, inciso c)."),
    "e": ("2027-09-10", "Empresa pública regional, local o bajo FONAFE (Primera DCF, inciso e)."),
    "f": ("2027-09-10",
          "Programa o proyecto del Estado, numeral 7 del artículo I del Título Preliminar "
          "de la Ley 27444 (Primera DCF, inciso f)."),
}

# id de entidad -> tramo de la Primera DCF
ASIGNACION = {
    # ── (b) Organismos Constitucionales Autónomos ──────────────────────
    "banco-central-de-reserva-del-peru": "b",
    "contraloria-general-gestion-de-proyectos-y-fortalecimiento-de-capacidades": "b",
    "jurado-nacional-de-elecciones": "b",
    "ministerio-publico": "b",
    "registro-nacional-de-identificacion-y-estado-civil": "b",
    "superintendencia-de-banca-seguros-y-afp": "b",

    # ── (a) Poder Ejecutivo y Poder Judicial ───────────────────────────
    # Ministerios y PCM.
    "ministerio-de-comercio-exterior-y-turismo": "a",
    "ministerio-de-desarrollo-agrario-y-riego": "a",
    "ministerio-de-educacion": "a",
    "ministerio-de-la-mujer-y-poblaciones-vulnerables-administracion-general": "a",
    "ministerio-de-la-produccion": "a",
    "ministerio-de-trabajo-y-promocion-del-empleo": "a",
    "ministerio-de-transportes-y-comunicaciones": "a",
    "ministerio-del-ambiente": "a",
    "ministerio-del-interior": "a",
    "presidencia-del-consejo-de-ministros": "a",
    "poder-judicial": "a",
    # Organismos públicos adscritos a un ministerio o a la PCM: numeral 1 del
    # artículo I del Título Preliminar de la Ley 27444 los cuenta como Poder
    # Ejecutivo, así que comparten el tramo de un año.
    "biblioteca-nacional-del-peru": "a",
    "comision-de-promocion-del-peru-para-la-exportacion-y-el-turismo-promperu": "a",
    "fondo-de-aseguramiento-en-salud-de-la-policia-nacional-del-peru": "a",
    "instituto-de-investigaciones-de-la-amazonia-peruana": "a",
    "instituto-nacional-de-enfermedades-neoplasicas": "a",
    "instituto-nacional-de-salud-del-nino": "a",
    "instituto-tecnologico-de-la-produccion": "a",
    "organismo-de-evaluacion-y-fiscalizacion-ambiental": "a",
    "organismo-de-supervision-de-los-recursos-forestales-y-de-fauna-silvestre": "a",
    "organismo-supervisor-de-inversion-privada-en-telecomunicaciones": "a",
    "organismo-supervisor-de-la-inversion-en-energia-y-mineria": "a",
    "servicio-nacional-de-certificacion-ambiental-para-las-inversiones-sostenibles": "a",
    "superintendencia-nacional-de-aduanas-y-de-administracion-tributaria-sunat": "a",
    "superintendencia-nacional-de-los-registros-publicos": "a",
    "superintendencia-nacional-de-migraciones": "a",
    "superintendencia-nacional-de-servicios-de-saneamiento": "a",

    # ── (c) Gobiernos regionales y universidades públicas ──────────────
    "hospital-regional-de-lambayeque": "c",
    "universidad-nacional-de-la-amazonia-peruana": "c",
    "universidad-nacional-hermilio-valdizan": "c",
    "universidad-nacional-santiago-antunez-de-mayolo": "c",

    # ── (e) Empresas públicas ──────────────────────────────────────────
    "empresa-regional-de-servicio-publico-de-electricidad-del-centro-sa-electrocentro-s-a": "e",
    "fondo-mivivienda-s-a": "e",
    "san-gaban-s-a": "e",
    "servicio-de-agua-potable-y-alcantarillado-de-arequipa": "e",

    # ── (f) Programas y proyectos del Estado ───────────────────────────
    "creacion-y-mejoramiento-del-servicio-de-catastro-en-distritos-seleccionados-de-las-provincias-de-lima-lambayeque-chiclayo-y-piura": "f",
    "mejora-de-la-calidad-de-servicios-registrales-reniec": "f",
    "programa-nacional-de-innovacion-para-la-competitividad-y-productividad": "f",
    "programa-nacional-plataformas-de-accion-para-la-inclusion-social": "f",
    "programa-para-el-mejoramiento-y-ampliacion-de-los-servicios-del-centro-de-empleo-fortalece-peru": "f",
    "proinnovate": "f",
    "unidad-ejecutora-mejoramiento-del-sistema-de-informacion-de-la-sunat-msi": "f",
}


def main():
    aplicar = "--aplicar" in sys.argv
    entidades = list(esquema.cargar_entidades().values())
    cambiadas = 0
    sin_tramo = []

    for e in entidades:
        tramo = ASIGNACION.get(e["id"])
        if tramo is None:
            sin_tramo.append(e["id"])
            continue
        fecha, _criterio = TRAMOS[tramo]
        toco = False
        for o in e.get("obligaciones") or []:
            if o.get("fecha_limite") != fecha:
                o["fecha_limite"] = fecha
                toco = True
        if toco:
            cambiadas += 1
            print(f"  {e['id']} -> {fecha} (tramo {tramo})")
            if aplicar:
                esquema.guardar_entidad(e)

    print(f"\n{cambiadas} entidades con plazo actualizado de {len(entidades)}.")
    reparto = {}
    for eid, tramo in ASIGNACION.items():
        if any(e["id"] == eid for e in entidades):
            reparto[TRAMOS[tramo][0]] = reparto.get(TRAMOS[tramo][0], 0) + 1
    for fecha in sorted(reparto):
        print(f"  {fecha}: {reparto[fecha]} entidades")

    if sin_tramo:
        print(f"\nAVISO: {len(sin_tramo)} entidades sin tramo asignado, se quedan sin fecha:")
        for eid in sin_tramo:
            print("  -", eid)
        print("Añádelas a ASIGNACION en este script tras revisar a qué inciso de la Primera DCF pertenecen.")

    if not aplicar:
        print("\n(simulación: vuelve a correr con --aplicar para escribir)")


if __name__ == "__main__":
    main()
