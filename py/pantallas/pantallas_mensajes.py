import pygame
import sys
from pantallas.pantallas_layout import *
from pantallas.pantallas_juego import *
from pantallas.pantallas_componentes import *
from pantallas.bucles_pantallas import (
    bucle_eventos_mensaje_simple,
    bucle_eventos_mensaje_temporal,
    bucle_renderizar_lineas_mensaje,
    bucle_dibujar_lineas_mensaje
)

def mostrar_titulo(ventana: pygame.Surface, texto: str, estado_global: dict, y_pos: int):
    """
    Muestra un título centrado en la pantalla en la posición Y especificada.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar el título.
        texto (str): Texto del título a mostrar.
        estado_global (dict): Estado global con fuentes y colores.
        y_pos (int): Posición Y donde mostrar el título.

    Returns:
        None: Esta función no retorna valores.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    render = estado_global["fuentes"]["titulo"].render(texto, True, colores["NEGRO"])
    ancho = ventana.get_width()
    ventana.blit(render, ((ancho - render.get_width()) // 2, y_pos))

def mostrar_mensaje(ventana: pygame.Surface, texto: str, estado_global: dict, alto: int):
    """
    Muestra un mensaje centrado y espera interacción del usuario para continuar.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar el mensaje.
        texto (str): Texto del mensaje a mostrar.
        estado_global (dict): Estado global con fuentes y colores.
        alto (int): Alto de la ventana para centrado vertical.

    Returns:
        None: Esta función no retorna valores.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    ventana.fill(colores["GRIS"])
    mensaje = estado_global["fuentes"]["boton"].render(texto, True, colores["NEGRO"])
    ancho = ventana.get_width()
    ventana.blit(mensaje, ((ancho - mensaje.get_width()) // 2, alto // 2))
    pygame.display.flip()

    esperando = True
    while esperando:
        esperando = bucle_eventos_mensaje_simple()

def mostrar_error(ventana: pygame.Surface, mensaje: str, estado_global: dict, alto: int):
    """
    Muestra un mensaje de error en color rojo por 1.5 segundos.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar el error.
        mensaje (str): Texto del mensaje de error.
        estado_global (dict): Estado global con fuentes y colores.
        alto (int): Alto de la ventana para centrado vertical.

    Returns:
        None: Esta función no retorna valores.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    ventana.fill(colores["GRIS"])
    render = estado_global["fuentes"]["titulo"].render(mensaje, True, (255, 0, 0))
    ancho = ventana.get_width()
    ventana.blit(render, ((ancho - render.get_width()) // 2, alto // 2))
    pygame.display.flip()
    pygame.time.wait(1500)

def mostrar_cargando(ventana: pygame.Surface, mensaje: str, estado_global: dict, alto: int):
    """
    Muestra un mensaje de carga por 0.5 segundos.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar el mensaje.
        mensaje (str): Texto del mensaje de carga.
        estado_global (dict): Estado global con fuentes y colores.
        alto (int): Alto de la ventana para centrado vertical.

    Returns:
        None: Esta función no retorna valores.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    ventana.fill(colores["GRIS"])
    render = estado_global["fuentes"]["titulo"].render(mensaje, True, colores["NEGRO"])
    ancho = ventana.get_width()
    ventana.blit(render, ((ancho - render.get_width()) // 2, alto // 2))
    pygame.display.flip()
    pygame.time.wait(500)

def mostrar_mensaje_temporal(ventana: pygame.Surface, mensaje: str, color: tuple[int, int, int], estado_global: dict, segundos: int = 2):
    """
    Muestra un mensaje temporal durante el número de segundos especificado.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar el mensaje.
        mensaje (str): Texto del mensaje a mostrar.
        color (tuple[int, int, int]): Color RGB del texto del mensaje.
        estado_global (dict): Estado global con fuentes y colores.
        segundos (int): Duración del mensaje en segundos.

    Returns:
        None: Esta función no retorna valores.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    reloj = pygame.time.Clock()
    ancho = ventana.get_width()
    alto = ventana.get_height()
    tiempo_inicial = pygame.time.get_ticks()
    
    continuar = True
    while continuar:
        continuar = bucle_eventos_mensaje_temporal(segundos, tiempo_inicial)
        
        ventana.fill(colores["GRIS"])
        texto_render = estado_global["fuentes"]["titulo"].render(mensaje, True, color)
        ventana.blit(texto_render, ((ancho - texto_render.get_width()) // 2, alto // 2))
        pygame.display.flip()
        reloj.tick(30)

def mostrar_pantalla(
    ventana: pygame.Surface,
    estado_global: dict,
    letra_actual: str,
    preguntas_letras: dict,
    letras: list,
    letras_estado: dict,
    respuesta_usuario: str,
    mensaje_resultado: str,
    color_mensaje: tuple[int, int, int],
    tiempo_restante: int,
    tiempo_mensaje: int,
    imagen_resultado: pygame.Surface = None
) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Muestra la pantalla principal del juego con todos sus elementos.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar la pantalla.
        estado_global (dict): Estado global con configuraciones, fuentes y colores.
        letra_actual (str): Letra que se está respondiendo actualmente.
        preguntas_letras (dict): Diccionario con preguntas organizadas por letra.
        letras (list): Lista de todas las letras del juego.
        letras_estado (dict): Estado actual de cada letra.
        respuesta_usuario (str): Respuesta ingresada por el usuario.
        mensaje_resultado (str): Mensaje de resultado a mostrar.
        color_mensaje (tuple[int, int, int]): Color del mensaje de resultado.
        tiempo_restante (int): Tiempo restante en segundos.
        tiempo_mensaje (int): Timestamp del mensaje para controlar duración.
        imagen_resultado (pygame.Surface): Imagen de resultado opcional.

    Returns:
        tuple[pygame.Rect, pygame.Rect]: Tupla con rectángulos del input y botón pasapalabra.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    ancho = ventana.get_width()
    alto = ventana.get_height()
    ventana.fill(colores["BLANCO"])
    centro_x = ancho * 3 // 4
    centro_y = alto // 2 - 50

    dibujar_rosco(letras, letras_estado, ventana, estado_global["fuentes"]["letra"], estado_global, centro_x=centro_x, centro_y=centro_y, radio=210, radio_letra=24)
    dibujar_timer(ventana, estado_global, tiempo_restante)

    estado = letras_estado.get(letra_actual, "")
    if letra_actual in preguntas_letras and estado in ("pendiente", "pasada"):
        texto_pregunta = preguntas_letras[letra_actual]["pregunta"]
    else:
        texto_pregunta = "Letra sin pregunta o ya respondida."

    lineas_renderizadas = renderizar_texto_multilinea(texto_pregunta, estado_global["fuentes"]["boton"], colores["NEGRO"], 500)
    for i, linea in enumerate(lineas_renderizadas):
        ventana.blit(linea, (50, 150 + i * 35))

    input_rect = pygame.Rect(50, 400, 500, 55)
    pygame.draw.rect(ventana, colores["AZUL"], input_rect, border_radius=5)
    texto_respuesta = estado_global["fuentes"]["boton"].render(respuesta_usuario, True, colores["BLANCO"])
    ventana.blit(texto_respuesta, (input_rect.x + 10, input_rect.y + 8))

    boton = dibujar_boton(
        ventana,
        estado_global,
        "Pasapalabra",
        centro_x - 90,
        560,
        180,
        50,
        color_fondo=colores["AMARILLO"],
        color_letra=colores["NEGRO"]
    )

    if mensaje_resultado and pygame.time.get_ticks() - tiempo_mensaje < 2000:
        # CORRECCIÓN: Manejar mensajes multilínea usando bucles
        lineas_mensaje = bucle_renderizar_lineas_mensaje(mensaje_resultado)
        bucle_dibujar_lineas_mensaje(ventana, lineas_mensaje, estado_global["fuentes"]["boton"], 
                                   color_mensaje, input_rect)

    if imagen_resultado:
        mostrar_imagen_resultado_en_rosco(ventana, imagen_resultado, estado_global)

    aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
    return input_rect, boton