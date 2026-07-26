"""Abre un issue de GitHub cuando un extractor lleva 2+ corridas fallando
seguidas (prompt original §7, Fase 2: "sin esa alerta, el proyecto muere en
silencio"). Usa el CLI `gh`, ya autenticado por GITHUB_TOKEN en el runner de
GitHub Actions -- sin dependencias nuevas, sin token propio que gestionar.

Se ejecuta como último paso del workflow, después de correr los extractores.
No falla el workflow si `gh` no está disponible (por ejemplo, en una corrida
local fuera de GitHub Actions) -- solo lo informa.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractores.comun.estado_ejecuciones import RUTA_ESTADO, UMBRAL_ALERTA


def main():
    if not os.path.exists(RUTA_ESTADO):
        print("Sin archivo de estado, nada que alertar.")
        return

    with open(RUTA_ESTADO, encoding="utf-8") as f:
        estado = json.load(f)

    for nombre, info in estado.items():
        if info.get("fallos_consecutivos", 0) < UMBRAL_ALERTA:
            continue
        titulo = f"[alerta] {nombre} lleva {info['fallos_consecutivos']} corridas fallando"
        ya_existe = subprocess.run(
            ["gh", "issue", "list", "--search", titulo, "--state", "open", "--json", "number"],
            capture_output=True, text=True,
        )
        if ya_existe.returncode == 0 and ya_existe.stdout.strip() not in ("", "[]"):
            print(f"Ya existe un issue abierto para {nombre}, no se duplica.")
            continue
        cuerpo = (
            f"El extractor `{nombre}` falló {info['fallos_consecutivos']} corridas seguidas.\n\n"
            f"Última corrida: {info.get('ultima_corrida', '?')}\n\n"
            f"Último mensaje de error:\n```\n{info.get('ultimo_mensaje', '')}\n```\n"
        )
        resultado = subprocess.run(
            ["gh", "issue", "create", "--title", titulo, "--body", cuerpo, "--label", "extractor-fallando"],
            capture_output=True, text=True,
        )
        if resultado.returncode != 0:
            print(f"No se pudo crear el issue para {nombre}: {resultado.stderr}")
        else:
            print(f"Issue creado para {nombre}: {resultado.stdout.strip()}")


if __name__ == "__main__":
    main()
