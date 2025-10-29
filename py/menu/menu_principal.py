import pygame
import sys
from pantallas.pantallas_submenu import *
from funciones_historial_pygame import *
from funciones_archivos import *
from pantallas.pantallas_componentes import *
from eventos.eventos_menu import *
from musica import *
from generales.config_manager_algorithmic import *
from generales.ayuda_menu import *

def importar_submenu_puntajes():
    """
    Importa y retorna la función pantalla_puntajes desde el módulo de menú de puntajes.

    Returns:
        function: Función pantalla_puntajes.
    """
    from menu.menu_puntajes import pantalla_puntajes
    return pantalla_puntajes

def importar_submenu_ajustes():
    """
    Importa y retorna la función pantalla_ajustes desde el módulo de menú de ajustes.

    Returns:
        function: Función pantalla_ajustes.
    """
    from menu.menu_ajustes import pantalla_ajustes
    return pantalla_ajustes

def importar_mostrar():
    """
    Importa y retorna la función mostrar_info_usuario_en_menu desde el módulo de ajustes.

    Returns:
        function: Función mostrar_info_usuario_en_menu.
    """
    from menu.menu_ajustes import mostrar_info_usuario_en_menu
    return mostrar_info_usuario_en_menu

def importar_juego_principal():
    """
    Importa y retorna la función pantalla_juego desde el módulo principal del juego.

    Returns:
        function: Función pantalla_juego.
    """
    from menu.menu_juego import pantalla_juego
    return pantalla_juego

pygame.init()

def inicializar_musica_menu(estado: dict):
    """
    Inicializa el sistema de sonido y reproduce la música del menú en bucle.

    Args:
        estado (dict): Diccionario con el estado actual, incluyendo volumen inicial.
    """
    pygame.mixer.init()
    reproducir_musica(estado, "MP3/04. Musica Bar Oficial.mp3", loop=True, volumen=estado["estado_inicial"]["volumen"])

def dibujar_titulo_principal(pantalla: pygame.Surface, estado: dict, colores: dict):
    """
    Dibuja el título principal del menú en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibuja el título.
        estado (dict): Diccionario con fuentes.
        colores (dict): Diccionario con los colores actuales del modo activo.
    """
    titulo = estado["fuentes"]["titulo"].render("PASAPALABRA", True, colores["NEGRO"])
    x_titulo = (estado["config"]["ventana"]["ancho"] - titulo.get_width()) // 2
    pantalla.blit(titulo, (x_titulo, 80))

def crear_botones_menu_principal(pantalla: pygame.Surface, estado: dict) -> dict:
    """
    Crea y dibuja los botones principales del menú (Jugar, Puntajes, Ajustes).

    Args:
        pantalla (pygame.Surface): Superficie sobre la cual se dibujan los botones.
        estado (dict): Diccionario con información de configuración y fuentes.

    Returns:
        dict: Diccionario con los rectángulos de colisión de cada botón.
    """
    ancho_boton = 250
    alto_boton = 80
    x_boton = (estado["config"]["ventana"]["ancho"] - ancho_boton) // 2

    botones = {
        "jugar": dibujar_boton(pantalla, estado, "Jugar", x_boton, 260, ancho_boton, alto_boton),
        "puntajes": dibujar_boton(pantalla, estado, "Puntajes", x_boton, 370, ancho_boton, alto_boton),
        "ajustes": dibujar_boton(pantalla, estado, "Ajustes", x_boton, 480, ancho_boton, alto_boton)
    }

    return botones

def manejar_eventos_menu_principal(pantalla: pygame.Surface, lineas_estadisticas: list, estado: dict, botones: dict):
    """
    Maneja los eventos del menú principal, como clics en los botones.

    Args:
        pantalla (pygame.Surface): Superficie del menú.
        lineas_estadisticas (list): Lista de líneas del archivo de estadísticas.
        estado (dict): Diccionario con estado general del sistema.
        botones (dict): Diccionario con los rectángulos de los botones.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botones["jugar"].collidepoint(evento.pos):
                pantalla_juego = importar_juego_principal()
                pantalla_juego(pantalla, estado)
            elif botones["puntajes"].collidepoint(evento.pos):
                pantalla_puntajes = importar_submenu_puntajes()
                pantalla_puntajes(pantalla, lineas_estadisticas, estado)
            elif botones["ajustes"].collidepoint(evento.pos):
                pantalla_ajustes = importar_submenu_ajustes()
                pantalla_ajustes(pantalla, estado)

def menu_principal(pantalla: pygame.Surface, lineas_estadisticas: list, estado: dict):
    """
    Ejecuta el bucle principal del menú de inicio.

    Args:
        pantalla (pygame.Surface): Superficie de Pygame donde se dibuja el menú.
        lineas_estadisticas (list): Estadísticas cargadas desde el archivo.
        estado (dict): Estado general del juego.
    """
    inicializar_musica_menu(estado)

    while True:
        modo_actual, colores = validar_modo_colores(estado)

        pantalla.fill(colores["GRIS"])
        dibujar_titulo_principal(pantalla, estado, colores)

        botones = crear_botones_menu_principal(pantalla, estado)
        mostrar = importar_mostrar()
        mostrar(pantalla, estado)

        aplicar_efectos_pantalla(pantalla, estado)
        manejar_eventos_menu_principal(pantalla, lineas_estadisticas, estado, botones)