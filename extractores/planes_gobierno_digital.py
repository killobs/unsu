"""Extractor: proyectos de IA declarados en el Plan de Gobierno Digital (PGD) por entidad.

ponytail: sin implementar todavía, y por una razón estructural, no solo de
tiempo. Se investigó durante la Fase 2 (ver docs/bitacora.md) dónde viven los
PGD: no hay un repositorio único -- cada entidad publica el suyo en su propio
dominio o subdominio (ej. repositorio.minedu.gob.pe, app8.ign.gob.pe,
conadisperu.gob.pe...), casi siempre como PDF, sin URL predecible a partir del
nombre de la entidad. La Presidencia del Consejo de Ministros centraliza los
*lineamientos* para elaborar el PGD, no los PGD mismos.

Sin un índice centralizado y sin presupuesto para un servicio de búsqueda de
pago (el proyecto es de costo cero, ver el prompt original §1.1), no hay una
forma confiable de automatizar esto entidad por entidad. La obligación
"Proyectos de IA incorporados en el Plan de Gobierno Digital" se mantiene en
"no_verificable_desde_fuentes_publicas" para todas las entidades hasta que
aparezca un índice público, o hasta que se decida cargar los PGD a mano
conforme se vayan encontrando (curaduría, no automatización).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractores.comun import estado_ejecuciones

NOMBRE_EXTRACTOR = "planes_gobierno_digital"


def main():
    mensaje = (
        "Extractor sin implementar: no existe un indice centralizado de PGD por "
        "entidad y el proyecto no puede pagar un servicio de busqueda. Ver el "
        "docstring del modulo. No se modifico ningun dato."
    )
    print(mensaje)
    estado_ejecuciones.registrar_resultado(NOMBRE_EXTRACTOR, ok=True, mensaje=mensaje)


if __name__ == "__main__":
    main()
