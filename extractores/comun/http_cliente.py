"""Cliente HTTP compartido por los extractores: reintentos con espera creciente,
respeto a robots.txt, demora entre peticiones y un User-Agent identificable.

Se necesita un User-Agent de navegador real -- gob.pe bloquea peticiones con
User-Agent genérico ("Mozilla/5.0" solo) pero permite una cadena de Chrome
completa. Ver docs/verificacion-terreno.md y docs/fase-0-detectabilidad.md.
"""
import time
import urllib.request
import urllib.robotparser
from urllib.parse import urlparse

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
    "(RegistroIAPublicaPeru/1.0; +https://github.com/)"
)

DEMORA_ENTRE_PETICIONES_SEG = 1.0
REINTENTOS = 4
ESPERA_INICIAL_SEG = 2.0

_robots_cache = {}
_ultima_peticion = {}


def _permitido_por_robots(url):
    # No se usa RobotFileParser.read() directo: ante un 401/403 asume
    # "prohibido todo" (comportamiento estándar de la librería para robots.txt
    # protegido), pero varios hosts de API de este proyecto (ej. OECE) devuelven
    # 403 en /robots.txt simplemente porque no sirven archivos estáticos ahí,
    # no porque estén negando acceso -- confirmado a mano en la Fase 0/2.
    # Por eso se pide el contenido primero y solo se interpreta como
    # robots.txt real si el servidor respondió 200 con contenido de texto.
    partes = urlparse(url)
    origen = f"{partes.scheme}://{partes.netloc}"
    if origen not in _robots_cache:
        try:
            req = urllib.request.Request(f"{origen}/robots.txt", headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as resp:
                cuerpo = resp.read().decode("utf-8", errors="replace")
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(cuerpo.splitlines())
            _robots_cache[origen] = rp
        except Exception:
            # sin robots.txt accesible (404, 403, timeout, etc.): no hay
            # restricción declarada que se pueda verificar, se permite.
            _robots_cache[origen] = None
    rp = _robots_cache[origen]
    if rp is None:
        return True
    return rp.can_fetch(USER_AGENT, url)


def _esperar_entre_peticiones(url):
    origen = urlparse(url).netloc
    ahora = time.monotonic()
    transcurrido = ahora - _ultima_peticion.get(origen, 0)
    if transcurrido < DEMORA_ENTRE_PETICIONES_SEG:
        time.sleep(DEMORA_ENTRE_PETICIONES_SEG - transcurrido)
    _ultima_peticion[origen] = time.monotonic()


def obtener(url, datos_post=None, headers=None):
    """GET o POST (si datos_post no es None) con reintentos y espera creciente.

    Lanza la última excepción si se agotan los reintentos. Respeta robots.txt
    y aplica una demora mínima entre peticiones al mismo dominio.
    """
    if not _permitido_por_robots(url):
        raise PermissionError(f"robots.txt prohíbe acceder a {url}")

    cabeceras = {"User-Agent": USER_AGENT}
    if headers:
        cabeceras.update(headers)

    cuerpo = None
    if datos_post is not None:
        cuerpo = datos_post.encode("utf-8") if isinstance(datos_post, str) else datos_post
        cabeceras.setdefault("Content-Type", "application/x-www-form-urlencoded")

    ultimo_error = None
    for intento in range(REINTENTOS):
        _esperar_entre_peticiones(url)
        try:
            req = urllib.request.Request(url, data=cuerpo, headers=cabeceras)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode(resp.headers.get_content_charset() or "utf-8", errors="replace")
        except Exception as e:
            ultimo_error = e
            if intento < REINTENTOS - 1:
                time.sleep(ESPERA_INICIAL_SEG * (2 ** intento))
    raise ultimo_error
