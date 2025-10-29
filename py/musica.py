import pygame


def reproducir_musica(estado_global: dict, path: str, loop: bool = True, volumen: float = None):
    """
    Reproduce música de fondo desde `path`.
    Si no se pasa `volumen`, toma el volumen actual del estado global.
    """
    pygame.mixer.music.load(path)

    if volumen == None:
        volumen = estado_global["estado_inicial"]["volumen"]

    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1 if loop else 0)

def detener_musica():
    """Detiene la música actual."""
    pygame.mixer.music.stop()

def actualizar_volumen(valor: float):
    """
    Ajusta el volumen de la música según un valor de slider (0 a 100).
    """
    if valor < 0:
        valor = 0
    elif valor > 100:
        valor = 100

    volumen_normalizado = valor / 100  
    pygame.mixer.music.set_volume(volumen_normalizado)
    return volumen_normalizado