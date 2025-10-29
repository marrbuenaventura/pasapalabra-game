import pygame
import sys

def bucle_eventos_config(estado: dict) -> bool:
    """
    Maneja los eventos durante la pantalla de configuración.
    Permite ajustar el volumen y brillo mediante sliders, 
    y salir presionando ESC. También actualiza el volumen global del mixer.

    Args:
        estado (dict): Diccionario que contiene los rects de los sliders, 
        estado de dragging y valores actuales de volumen y brillo.

    Returns:
        bool: True si se presiona ESC, False en otro caso.
    """
    resultado = False
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            resultado = True  

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if estado["selector_vol"].collidepoint(evento.pos):
                estado["dragging_vol"] = True
            elif estado["selector_bri"].collidepoint(evento.pos):
                estado["dragging_bri"] = True

        elif evento.type == pygame.MOUSEBUTTONUP:
            estado["dragging_vol"] = False
            estado["dragging_bri"] = False

        elif evento.type == pygame.MOUSEMOTION:
            if estado["dragging_vol"]:
                from generales.generales_pygame import actualizar_selector
                estado["volumen"] = actualizar_selector(evento.pos[0], estado["slider_volumen"], estado["selector_vol"])
                pygame.mixer.music.set_volume(estado["volumen"]) 

            elif estado["dragging_bri"]:
                from generales.generales_pygame import actualizar_selector
                estado["brillo"] = actualizar_selector(evento.pos[0], estado["slider_brillo"], estado["selector_bri"])

    return resultado

def bucle_eventos_scroll() -> str:
    """
    Maneja los eventos de scroll y navegación mediante teclado.

    Returns:
        str: Acción detectada ('salir', 'arriba', 'abajo', 'scroll:<int>'), 
            o cadena vacía si no ocurre nada relevante.
    """
    resultado = ""
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                resultado = "salir"
            elif evento.key == pygame.K_DOWN:
                resultado = "abajo"
            elif evento.key == pygame.K_UP:
                resultado = "arriba"
        elif evento.type == pygame.MOUSEWHEEL:
            resultado = f"scroll:{evento.y}"
    
    return resultado

def bucle_eventos_estadisticas() -> bool:
    """
    Maneja los eventos en la pantalla de estadísticas.

    Returns:
        bool: True si se presiona ESC, False en otro caso.
    """
    bandera = False
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            bandera = True
    
    return bandera

def bucle_eventos_accesibilidad(eventos: list, botones: dict) -> tuple[str | None, bool]:
    """Bucle para procesar eventos de accesibilidad"""
    modo = None
    salir = False

    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            salir = True
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for clave, boton in botones.items():
                if boton.collidepoint(evento.pos):
                    if clave == "daltonico":  
                        modo = "daltonico" 
                    else:
                        modo = clave

    return modo, salir

def bucle_eventos_cuenta_regresiva():
    """
    Maneja los eventos durante la cuenta regresiva previa al inicio del juego.

    Cierra el programa si se detecta un evento de salida.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def bucle_eventos_categoria_elegida():
    """
    Maneja los eventos mientras se muestra la categoría elegida.

    Cierra el programa si se detecta un evento de salida.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def bucle_eventos_input(texto_actual: str) -> tuple[str, bool]:
    """
    Maneja los eventos para ingreso de texto limitado a 20 caracteres.

    Permite escribir, borrar (Backspace) y finalizar (Enter).

    Args:
        texto_actual (str): Texto que se muestra actualmente.

    Returns:
        tuple: Texto actualizado y bandera de finalización (bool).
    """
    nuevo_texto = texto_actual
    finalizar = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                finalizar = True
            elif evento.key == pygame.K_BACKSPACE:
                nuevo_texto = texto_actual[:-1]
            elif len(texto_actual) < 20 and evento.unicode.isprintable():
                nuevo_texto = texto_actual + evento.unicode
    
    return nuevo_texto, finalizar

def bucle_eventos_pedir_texto(texto: str, max_len: int = 15) -> tuple[str, bool]:
    """
    Maneja los eventos para pedir un texto al usuario con longitud máxima.

    Args:
        texto (str): Texto actual ingresado.
        max_len (int, optional): Longitud máxima permitida. Default = 15.

    Returns:
        tuple: Texto actualizado y si se terminó de ingresar (bool).
    """
    terminado = False
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                texto = texto[:-1]
            elif evento.key == pygame.K_RETURN:
                if len(texto) > 0:
                    terminado = True
            else:
                if len(texto) < max_len and evento.unicode.isprintable():
                    texto += evento.unicode
    
    return texto, terminado

def bucle_eventos_submenu(botones: dict[str, pygame.Rect]) -> str:
    """
    Maneja los eventos en un submenú gráfico.

    Detecta si se hace clic sobre algún botón o se presiona ESC.

    Args:
        botones (dict): Diccionario con claves de opción y sus rectángulos.

    Returns:
        str: Clave del botón seleccionado o "ESC" si se presiona escape.
    """
    seleccion = ""
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            seleccion = "ESC"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for clave, rect in botones.items():
                if rect.collidepoint(evento.pos):
                    seleccion = clave
    
    return seleccion

def bucle_eventos_elegir_opcion(opciones: list[str], seleccion: int) -> tuple[int, str | None]:
    """
    Maneja los eventos para elegir una opción usando las flechas y Enter.

    Args:
        opciones (list): Lista de opciones disponibles.
        seleccion (int): Índice actual de selección.

    Returns:
        tuple: Índice actualizado de selección y opción elegida (str) o None.
    """
    opcion_elegida = None
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                seleccion = (seleccion - 1) % len(opciones)
            elif evento.key == pygame.K_DOWN:
                seleccion = (seleccion + 1) % len(opciones)
            elif evento.key == pygame.K_RETURN:
                opcion_elegida = opciones[seleccion]
    
    return seleccion, opcion_elegida