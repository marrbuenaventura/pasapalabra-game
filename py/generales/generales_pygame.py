import os
from pantallas.pantallas_mensajes import *
from eventos.eventos_input import *
import pygame
from colorama import *
from funciones_archivos import *
from generales.generales import *
from generales.bucles_generales import (
    bucle_procesar_estadisticas_lineas, 
    bucle_procesar_datos_estadisticas,
    bucle_elegir_opcion_pygame,
    bucle_manejar_selector,
    bucle_generar_textos_estadisticas
)
import sys
from funciones_historial_pygame import *

init(autoreset=True)

def calcular_estadisticas(lineas: list) -> dict:
    """
    Calcula estadísticas generales (promedios y máximos) a partir de líneas de datos de juego.

    Args:
        lineas (list): Lista de líneas extraídas de un archivo de estadísticas.

    Returns:
        dict: Diccionario con los valores de promedio de aciertos, errores, tiempo y el máximo de errores.
    """
    if len(lineas) <= 1:
        estadisticas = {
            "promedio_aciertos": 0,
            "promedio_errores": 0,
            "promedio_tiempo": 0,
            "max_errores": 0
        }
        return estadisticas

    aciertos, errores, tiempos = bucle_procesar_estadisticas_lineas(lineas)

    estadisticas = {
        "promedio_aciertos": calcular_promedio_total(aciertos),
        "promedio_errores": calcular_promedio_total(errores),
        "promedio_tiempo": calcular_promedio_total(tiempos),
        "max_errores": buscar_maximo(errores)
    }
    return estadisticas

def obtener_usuario_validado(ventana: pygame.Surface, estado_global: dict) -> str:
    """
    Solicita al usuario su nombre y valida si ya jugó anteriormente.

    Si el usuario ya existe y confirma que ha jugado, se permite el acceso. Si no, se solicita un nombre nuevo.

    Args:
        ventana (pygame.Surface): Superficie principal del juego.
        estado_global (dict): Diccionario con la configuración general del sistema.

    Returns:
        str: Nombre de usuario validado.
    """
    while True:
        usuario = pedir_texto(ventana, estado_global, "Ingreso de Usuario", "Ingrese nombre de usuario: ")
        
        if verificar_usuario_existe(usuario):
            if preguntar_si_ya_jugo(ventana, estado_global, usuario):
                return usuario
            else:
                mostrar_mensaje_temporal(ventana, "Usuario no disponible, pruebe otro.", (255, 0, 0), estado_global, 2)
        else:
            return usuario

def preguntar_si_ya_jugo(ventana: pygame.Surface, estado_global: dict, usuario: str) -> bool:
    """
    Pregunta al usuario si ya ha jugado antes.

    Args:
        ventana (pygame.Surface): Superficie principal del juego.
        estado_global (dict): Diccionario con la configuración general del sistema.
        usuario (str): Nombre de usuario a consultar.

    Returns:
        bool: True si el usuario confirma que ya jugó, False en caso contrario.
    """
    respuesta = pedir_texto(ventana, estado_global, "Confirmación", f"¿Ya jugaste antes? (si/no): ", max_len=3)
    return respuesta.lower() == "si"

def elegir_opcion_titulo(ventana: pygame.Surface, estado_global: dict, titulo_texto: str, opciones: list[str]) -> str:
    """
    Muestra un menú interactivo con un título y varias opciones, y permite al usuario elegir una.

    Args:
        ventana (pygame.Surface): Superficie principal del juego.
        estado_global (dict): Diccionario con la configuración general del sistema.
        titulo_texto (str): Título a mostrar en pantalla.
        opciones (list[str]): Lista de opciones a presentar.

    Returns:
        str: Opción seleccionada por el usuario.
    """
    reloj = pygame.time.Clock()
    seleccion = 0
    ancho = ventana.get_width()
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]

    while True:
        ventana.fill(colores["GRIS"])

        titulo = estado_global["fuentes"]["titulo"].render(titulo_texto, True, colores["NEGRO"])
        ventana.blit(titulo, ((ancho - titulo.get_width()) // 2, 50))

        for i, opcion in enumerate(opciones):
            color = colores["AZUL"] if i == seleccion else colores["NEGRO"]
            texto_render = estado_global["fuentes"]["boton"].render(opcion.capitalize(), True, color)
            ventana.blit(texto_render, ((ancho // 2) - 50, 200 + i * 60))

        pygame.display.flip()

        seleccion, opcion_elegida = bucle_elegir_opcion_pygame(ventana, estado_global, opciones, seleccion)
        if opcion_elegida:
            return opcion_elegida

        reloj.tick(30)

def actualizar_selector(pos_x: int, slider_rect: pygame.Rect, selector_rect: pygame.Rect) -> float:
    """
    Actualiza la posición del selector dentro del slider según la posición del mouse.

    Args:
        pos_x (int): Posición horizontal del cursor.
        slider_rect (pygame.Rect): Rectángulo que representa el área del slider.
        selector_rect (pygame.Rect): Rectángulo que representa el selector.

    Returns:
        float: Valor proporcional (0 a 1) correspondiente a la posición del selector.
    """
    x = max(min(pos_x, slider_rect.right), slider_rect.left)
    selector_rect.x = x - selector_rect.width // 2
    return (x - slider_rect.left) / slider_rect.width

def manejar_eventos_selector(slider_rect: pygame.Rect, selector_rect: pygame.Rect):
    """
    Controla los eventos del selector del slider (movimiento con mouse).

    Args:
        slider_rect (pygame.Rect): Rectángulo que representa el área del slider.
        selector_rect (pygame.Rect): Rectángulo que representa el selector.
    """
    bucle_manejar_selector(slider_rect, selector_rect)

def crear_selector(slider_rect: pygame.Rect, valor: float) -> pygame.Rect:
    """
    Crea un rectángulo que representa el selector en una posición relativa al slider.

    Args:
        slider_rect (pygame.Rect): Rectángulo que representa el área del slider.
        valor (float): Valor entre 0 y 1 que determina la posición horizontal del selector.

    Returns:
        pygame.Rect: Rectángulo del selector posicionado correctamente.
    """
    x_pos = slider_rect.left + int(valor * slider_rect.width) - 5
    return pygame.Rect(x_pos, slider_rect.top - 5, 10, 20)

def generar_textos_estadisticas(estadisticas: dict) -> list[str]:
    """
    Genera una lista de textos formateados a partir de los valores de estadísticas.

    Args:
        estadisticas (dict): Diccionario con valores estadísticos.

    Returns:
        list[str]: Lista de cadenas listas para ser renderizadas o mostradas.
    """
    return bucle_generar_textos_estadisticas(estadisticas)

def procesar_estadisticas(lineas_estadisticas: list) -> tuple[list, list, list]:
    """
    Procesa las líneas del archivo de estadísticas para obtener encabezados, datos e índices.

    Args:
        lineas_estadisticas (list): Lista de líneas del archivo de estadísticas.

    Returns:
        tuple: Tupla que contiene:
            - list: Encabezados de columnas.
            - list: Datos por usuario.
            - list: Índices de filas válidas.
    """
    if len(lineas_estadisticas) <= 1:
        return [], [], []
    
    encabezado, datos = bucle_procesar_datos_estadisticas(lineas_estadisticas)
    indices = list(range(len(encabezado)))
    
    return encabezado, datos, indices

def limitar_scroll(estado_global: dict, target_scroll: int, cantidad_filas: int, row_height: int) -> int:
    """
    Restringe el valor de scroll vertical a un rango válido según el tamaño del contenido y de la ventana.

    Args:
        estado_global (dict): Diccionario con la configuración global del juego.
        target_scroll (int): Valor deseado de desplazamiento vertical.
        cantidad_filas (int): Cantidad total de filas a mostrar.
        row_height (int): Altura de cada fila.

    Returns:
        int: Valor corregido de scroll, limitado entre 0 y el máximo permitido.
    """
    ventana_alto = estado_global["config"]["ventana"]["alto"]
    max_scroll = cantidad_filas * row_height - (ventana_alto - 140)
    
    if max_scroll < 0:
        max_scroll = 0

    if target_scroll < 0:
        return 0
    elif target_scroll > max_scroll:
        return max_scroll
    else:
        return target_scroll