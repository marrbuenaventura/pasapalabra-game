from generales.config_manager_algorithmic import *
from generales.generales_pygame import *
from eventos.bucles_eventos import bucle_eventos_config, bucle_eventos_scroll, bucle_eventos_estadisticas

def manejar_eventos_config(estado: dict) -> bool:
    """
    Encapsula el manejo de eventos en la pantalla de configuración.
    Args:
        estado (dict): Diccionario con información de sliders y estado del dragging.

    Returns:
        bool: True si se presiona ESC, False en otro caso.
    """
    return bucle_eventos_config(estado)

def manejar_eventos_scroll():
    """
    Encapsula el manejo de eventos relacionados con el scroll.

    Returns:
        str: Acción detectada por el usuario (arriba, abajo, scroll, salir).
    """
    return bucle_eventos_scroll()

def manejar_eventos_estadisticas() -> bool:
    """
    Encapsula el manejo de eventos en la pantalla de estadísticas.

    Returns:
        bool: True si se presiona ESC, False en otro caso.
    """
    return bucle_eventos_estadisticas()

def alternar_modo(estado_global: dict):
    """
    Alterna entre el modo visual 'normal' y 'daltónico'.
    Actualiza el estado global y el estado inicial con el nuevo modo.

    Args:
        estado_global (dict): Diccionario con las configuraciones y estado actual del programa.
    """
    modo_actual = estado_global.get("modo", "normal")
    
    if modo_actual == "normal":
        estado_global["modo"] = "daltonico"
    else:
        estado_global["modo"] = "normal"
    
    estado_global["estado_inicial"]["modo"] = estado_global["modo"]