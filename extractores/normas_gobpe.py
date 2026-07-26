"""Extractor: políticas institucionales, designaciones y resoluciones en gob.pe.

ponytail: esto NO es un scraper completo todavía -- es honesto sobre por qué.
Cada entidad publica sus normas legales en una URL propia dentro de gob.pe
(patrón `gob.pe/institucion/{slug}/normas-legales`), pero:

1. No hay un índice público que mapee nombre de entidad -> slug de gob.pe.
   Construirlo a mano para ~27 entidades es viable, pero es trabajo de
   curaduría, no de scraping, y no se hizo en esta pasada.
2. gob.pe tiene protección anti-bot activa (ver docs/fase-0-detectabilidad.md
   y docs/verificacion-terreno.md) que bloquea al navegador headless pero deja
   pasar peticiones con un User-Agent de Chrome completo -- de comportamiento
   no garantizado ni documentado por la entidad, puede cambiar sin aviso.
3. El buscador de gob.pe/busquedas es una aplicación de página única (SPA);
   su API real no se identificó en el tiempo de esta sesión.

Mientras esto no se resuelva, cada entidad se queda en
"no_verificable_desde_fuentes_publicas" para "Política institucional de IA
aprobada" y "Mecanismos de supervisión humana declarados" -- que es
exactamente el valor por defecto y el correcto según docs/metodologia.md §6.

Subir de nivel esto requiere, en orden: (a) construir y versionar el mapeo
entidad -> slug de gob.pe en datos/crudos/slugs_gobpe.csv, (b) confirmar que
las cabeceras usadas en extractores/comun/http_cliente.py siguen bastando
para pasar la protección anti-bot en una corrida real de GitHub Actions
(la IP y el user-agent runner-a-runner pueden comportarse distinto a esta
sesión), y solo entonces escribir el scraping por entidad.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractores.comun import estado_ejecuciones

NOMBRE_EXTRACTOR = "normas_gobpe"


def main():
    mensaje = (
        "Extractor sin implementar: falta el mapeo entidad -> slug de gob.pe "
        "y confirmar acceso estable desde GitHub Actions. Ver el docstring del "
        "módulo. No se modificó ningún dato."
    )
    print(mensaje)
    estado_ejecuciones.registrar_resultado(NOMBRE_EXTRACTOR, ok=True, mensaje=mensaje)


if __name__ == "__main__":
    main()
