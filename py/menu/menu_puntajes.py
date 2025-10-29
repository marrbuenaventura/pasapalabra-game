import pygame
from pantallas.pantallas_componentes import dibujar_boton
from pantallas.pantallas_mensajes import mostrar_titulo
from pantallas.pantallas_submenu import *
from eventos.eventos_menu import manejar_eventos_submenu
from generales.ayuda_menu import validar_modo_colores, aplicar_efectos_pantalla
from menu.menu_ajustes import mostrar_info_usuario_en_menu
from menu.bucles_menu import bucle_crear_botones_menu, bucle_manejar_eventos_puntajes

def crear_botones_puntajes(pantalla: pygame.Surface, estado: dict) -> dict:
    """
    Crea los botones del submenú de puntajes utilizando un bucle reutilizable.

    Args:
        pantalla (pygame.Surface): Superficie de Pygame donde se dibujan los botones.
        estado (dict): Estado global del juego, que incluye colores, fuentes, configuración, etc.

    Returns:
        dict: Diccionario con los botones creados, accesibles por su clave.
    """
    return bucle_crear_botones_menu(pantalla, estado, "puntajes")

def manejar_eventos_puntajes(botones: dict, pantalla: pygame.Surface, estado: dict, lineas_estadisticas: list) -> bool:
    """
    Procesa los eventos en el submenú de puntajes, ejecutando acciones según el botón presionado.

    Args:
        botones (dict): Diccionario con las áreas clicables de los botones.
        pantalla (pygame.Surface): Superficie donde se muestra el menú.
        estado (dict): Diccionario de estado global del juego.
        lineas_estadisticas (list): Lista de estadísticas leídas del archivo CSV.

    Returns:
        bool: True si el usuario quiere salir del submenú (ESC), False en otro caso.
    """
    seleccion = bucle_manejar_eventos_puntajes(botones, pantalla, estado, lineas_estadisticas)

    if seleccion == "ver_puntajes":
        pantalla_estadisticas_general(pantalla, estado)
        return False
    elif seleccion == "ver_estadisticas":
        pantalla_estadisticas_generales(pantalla, estado, lineas_estadisticas)
        return False
    elif seleccion == "ver_historial":
        pantalla_historial_usuario(pantalla, estado)
        return False
    elif seleccion == "ESC":
        return True

    return False

def pantalla_puntajes(pantalla: pygame.Surface, lineas_estadisticas: list, estado: dict):
    """
    Controla el ciclo de ejecución del submenú de puntajes, actualizando la interfaz y delegando eventos.

    Args:
        pantalla (pygame.Surface): Superficie principal de Pygame donde se dibuja la pantalla.
        lineas_estadisticas (list): Lista con los datos del historial del usuario.
        estado (dict): Estado general del juego con configuración y datos del usuario.
    """
    reloj = pygame.time.Clock()

    while True:
        modo_actual, colores = validar_modo_colores(estado)

        pantalla.fill(colores["GRIS"])
        mostrar_titulo(pantalla, "Submenú Puntajes", estado, 80)

        botones = crear_botones_puntajes(pantalla, estado)
        mostrar_info_usuario_en_menu(pantalla, estado)
        aplicar_efectos_pantalla(pantalla, estado)

        reloj.tick(60)

        if manejar_eventos_puntajes(botones, pantalla, estado, lineas_estadisticas):
            break