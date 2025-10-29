import pygame
from funciones_archivos import obtener_estadisticas_usuario_json as obtener_estadisticas_usuario
from pantallas.pantallas_juego import aplicar_brillo

def validar_modo_colores(estado: dict) -> tuple[str, dict]:
    """
    Valida que el modo de color actual exista en el diccionario de colores. Si no existe, lo corrige a 'normal'.

    Args:
        estado (dict): Diccionario global con configuraciones y modo actual.

    Returns:
        tuple[str, dict]: Modo validado y el diccionario de colores correspondiente.
    """
    modo_actual = estado.get("modo", "normal")
    
    if modo_actual not in estado["colores"]:
        print(f"WARNING: Modo '{modo_actual}' no encontrado. Usando 'normal'")
        modo_actual = "normal"
        estado["modo"] = "normal"
    
    colores = estado["colores"][modo_actual]
    return modo_actual, colores

def aplicar_efectos_pantalla(pantalla: pygame.Surface, estado: dict):
    """
    Aplica efectos visuales sobre la pantalla, como brillo, y actualiza la ventana.

    Args:
        pantalla (pygame.Surface): Superficie sobre la que se aplican los efectos.
        estado (dict): Diccionario con la configuración de la ventana y brillo actual.
    """
    aplicar_brillo(pantalla, estado["config"]["ventana"]["ancho"], estado["config"]["ventana"]["alto"], estado["estado_inicial"]["brillo"])
    pygame.display.flip()

def establecer_usuario_actual(estado: dict, usuario: str):
    """
    Guarda el nombre del usuario actual en el estado global.

    Args:
        estado (dict): Diccionario global del juego.
        usuario (str): Nombre del usuario que se desea establecer como actual.
    """
    estado["usuario_actual"] = usuario

def obtener_usuario_actual(estado: dict) -> str:
    """
    Obtiene el nombre del usuario actualmente guardado en el estado global.

    Args:
        estado (dict): Diccionario global del juego.

    Returns:
        str: Nombre del usuario actual, o None si no fue establecido.
    """
    return estado.get("usuario_actual")
