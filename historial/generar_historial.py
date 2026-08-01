"""Fase 3: capa de historial. Lee el historial de Git de una ficha (sistema o
entidad) y produce la lista de cambios: fecha, campo, valor anterior, valor
nuevo y el commit como fuente.

"No programes un motor de diffs propio; Git ya lo es" (prompt original §7,
Fase 3) -- este script no reimplementa diffing de texto: usa `git log` para
encontrar los commits que tocaron el archivo y `git show` para leer cada
versión, y compara los VALORES YA PARSEADOS de YAML campo por campo. Todo el
trabajo de detectar qué cambió a nivel de bytes lo sigue haciendo Git.

No genera ni commitea un historial estático para cada ficha del repositorio:
con el historial de Git tan corto todavía, eso serían ~100 archivos casi
vacíos ("alta inicial") por generar de nuevo en cada corrida. Se calcula al
vuelo, aquí y luego en el sitio (Fase 4) -- exactamente como cualquier otro
dato derivable de algo que ya está versionado.

Uso:
    python historial/generar_historial.py datos/entidades/poder-judicial.yaml
    python historial/generar_historial.py datos/entidades/poder-judicial.yaml --json
"""
import json
import subprocess
import sys
import os

import yaml

RAIZ = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def _ejecutar_git(args):
    # encoding explícito: sin él, Python decodifica la salida de git con la
    # codificación local, que en Windows es cp1252, y revienta con las tildes
    # de cualquier ficha. Git entrega UTF-8 siempre.
    resultado = subprocess.run(
        ["git", *args],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
        errors="replace",
    )
    return resultado.stdout


def _commits_del_archivo(ruta_relativa):
    """De más antiguo a más nuevo."""
    salida = _ejecutar_git(["log", "--follow", "--format=%H|%aI", "--", ruta_relativa])
    lineas = [l for l in salida.strip().splitlines() if l]
    commits = [tuple(l.split("|", 1)) for l in lineas]
    return list(reversed(commits))


def _contenido_en_commit(commit_hash, ruta_relativa):
    try:
        salida = _ejecutar_git(["show", f"{commit_hash}:{ruta_relativa}"])
    except subprocess.CalledProcessError:
        return None
    return yaml.safe_load(salida)


# Listas de sub-registros del esquema (docs/metodologia.md §5-6) que conviene
# comparar por su clave natural en vez de como bloque completo -- si no, un
# cambio de una sola obligación reporta las seis como "cambiadas".
LISTAS_CON_CLAVE = {"obligaciones": "obligacion", "evidencia": "url"}


def _diferencias_lista(clave_campo, clave_natural, antes, despues):
    antes = antes or []
    despues = despues or []
    por_clave_antes = {item.get(clave_natural): item for item in antes if isinstance(item, dict)}
    por_clave_despues = {item.get(clave_natural): item for item in despues if isinstance(item, dict)}
    cambios = []
    for k in sorted(set(por_clave_antes) | set(por_clave_despues)):
        a, d = por_clave_antes.get(k), por_clave_despues.get(k)
        if a == d:
            continue
        if a is None:
            cambios.append({"campo": f"{clave_campo}[{k}]", "valor_anterior": None, "valor_nuevo": d})
        elif d is None:
            cambios.append({"campo": f"{clave_campo}[{k}]", "valor_anterior": a, "valor_nuevo": None})
        else:
            for subclave in sorted(set(a) | set(d)):
                if a.get(subclave) != d.get(subclave):
                    cambios.append({
                        "campo": f"{clave_campo}[{k}].{subclave}",
                        "valor_anterior": a.get(subclave), "valor_nuevo": d.get(subclave),
                    })
    return cambios


def _diferencias(anterior, nuevo):
    """Compara dos dicts ya parseados, campo por campo (no línea por línea)."""
    cambios = []
    claves = set((anterior or {}).keys()) | set((nuevo or {}).keys())
    for clave in sorted(claves):
        v_antes = (anterior or {}).get(clave, None)
        v_despues = (nuevo or {}).get(clave, None)
        if v_antes == v_despues:
            continue
        if clave in LISTAS_CON_CLAVE:
            cambios.extend(_diferencias_lista(clave, LISTAS_CON_CLAVE[clave], v_antes, v_despues))
        else:
            cambios.append({"campo": clave, "valor_anterior": v_antes, "valor_nuevo": v_despues})
    return cambios


def generar(ruta_relativa):
    commits = _commits_del_archivo(ruta_relativa)
    historial = []
    anterior = None
    for commit_hash, fecha in commits:
        actual = _contenido_en_commit(commit_hash, ruta_relativa)
        if anterior is None:
            historial.append({
                "fecha": fecha, "commit": commit_hash, "tipo": "alta_inicial",
                "cambios": _diferencias({}, actual),
            })
        else:
            cambios = _diferencias(anterior, actual)
            if cambios:
                historial.append({
                    "fecha": fecha, "commit": commit_hash, "tipo": "actualizacion",
                    "cambios": cambios,
                })
        anterior = actual
    return historial


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    ruta_relativa = sys.argv[1]
    historial = generar(ruta_relativa)
    if "--json" in sys.argv:
        print(json.dumps(historial, ensure_ascii=False, indent=2, default=str))
        return
    for entrada in historial:
        print(f"{entrada['fecha']}  [{entrada['tipo']}]  {entrada['commit'][:8]}")
        for c in entrada["cambios"]:
            print(f"  - {c['campo']}: {c['valor_anterior']!r} -> {c['valor_nuevo']!r}")


if __name__ == "__main__":
    main()
