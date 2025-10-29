import pygame
import sys
import random
from eventos.eventos_input import pedir_usuario
from eventos.bucles_eventos import bucle_eventos_submenu, bucle_eventos_elegir_opcion

def manejar_eventos_submenu(botones: dict[str, pygame.Rect]) -> str:
    """
    Maneja los eventos del submenú delegando al bucle correspondiente.

    Args:
        botones (dict[str, pygame.Rect]): Diccionario de botones con claves identificadoras y sus rectángulos.

    Returns:
        str: Clave del botón seleccionado o "ESC" si se presionó Escape.
    """
    return bucle_eventos_submenu(botones)

def elegir_opcion_titulo(estado_global: dict, titulo_texto: str, opciones: list[str]) -> str:
    """
    Muestra una pantalla con un título y un listado de opciones seleccionables con flechas y Enter.

    Args:
        estado_global (dict): Diccionario con configuraciones globales, colores y fuentes.
        titulo_texto (str): Texto del título a mostrar arriba.
        opciones (list[str]): Lista de opciones disponibles.

    Returns:
        str: Opción seleccionada por el usuario.
    """
    reloj = pygame.time.Clock()
    seleccion = 0
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ventana = pygame.display.get_surface()
    ancho_ventana = estado_global["config"]["ventana"]["ancho"]

    while True:
        ventana.fill(colores["GRIS"])

        titulo = estado_global["fuentes"]["titulo"].render(titulo_texto, True, colores["NEGRO"])
        ventana.blit(titulo, ((ancho_ventana - titulo.get_width()) // 2, 50))

        for i, opcion in enumerate(opciones):
            color = colores["AZUL"] if i == seleccion else colores["NEGRO"]
            texto_render = estado_global["fuentes"]["boton"].render(opcion.capitalize(), True, color)
            ventana.blit(texto_render, ((ancho_ventana // 2) - 50, 200 + i * 60))

        pygame.display.flip()

        seleccion, opcion_elegida = bucle_eventos_elegir_opcion(opciones, seleccion)
        if opcion_elegida:
            return opcion_elegida

        reloj.tick(30)

def elegir_dificultad(estado_global: dict) -> str:
    """
    Solicita al usuario elegir entre dificultad 'fácil' o 'difícil'.

    Args:
        estado_global (dict): Diccionario con configuraciones globales del juego.

    Returns:
        str: Dificultad seleccionada ('facil' o 'dificil').
    """
    dificultad_elegida = elegir_opcion_titulo(estado_global, "Elija Dificultad", ["facil", "dificil"])
    return dificultad_elegida

def elegir_categoria_aleatoria() -> str:
    """
    Elige aleatoriamente una categoría entre 'cine' y 'musica'.

    Returns:
        str: Categoría seleccionada aleatoriamente.
    """
    categorias = ["cine", "musica"]
    return random.choice(categorias)

def obtener_usuario_validado(estado_global: dict) -> str:
    """
    Solicita un nombre de usuario hasta que se ingrese uno válido (no vacío ni espacios).

    Args:
        estado_global (dict): Diccionario con configuraciones globales y datos de la interfaz.

    Returns:
        str: Nombre de usuario validado y sin espacios extremos.
    """
    while True:
        usuario = pedir_usuario(estado_global)
        if usuario and usuario.strip():
            return usuario.strip()