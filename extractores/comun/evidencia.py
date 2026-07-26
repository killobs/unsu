"""Construcción de entradas de evidencia con fecha de captura (§5 del esquema)."""
import datetime


def nueva(url, descripcion, fecha_captura=None):
    return {
        "url": url,
        "fecha_captura": fecha_captura or datetime.date.today().isoformat(),
        "descripcion": descripcion,
    }
