import pygame
from eventos.eventos_config import *
from eventos.bucles_eventos import bucle_eventos_cuenta_regresiva, bucle_eventos_accesibilidad, bucle_eventos_categoria_elegida

def cuenta_regresiva(estado_global: dict):
    """
    Muestra una cuenta regresiva animada (3, 2, 1) en pantalla antes de iniciar el juego.

    Se actualiza la pantalla cada segundo y se procesan eventos para permitir cerrar la ventana.

    Args:
        estado_global (dict): Diccionario con configuraciones generales, fuentes y colores.
    """
    reloj = pygame.time.Clock()
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    for i in [3, 2, 1]:
        ventana = pygame.display.get_surface()
        ventana.fill(colores["GRIS"])
        
        texto = estado_global["fuentes"]["titulo"].render(str(i), True, colores["AZUL"])
        ancho_ventana = estado_global["config"]["ventana"]["ancho"]
        alto_ventana = estado_global["config"]["ventana"]["alto"]
        
        ventana.blit(texto, ((ancho_ventana - texto.get_width()) // 2, (alto_ventana - texto.get_height()) // 2))
        pygame.display.flip()
        pygame.time.delay(1000)
        
        bucle_eventos_cuenta_regresiva()
        reloj.tick(30)

def manejar_eventos_accesibilidad(eventos, botones: dict) -> tuple[str | None, bool]:
    """
    Encapsula la lógica de detección de eventos en la pantalla de accesibilidad.
    Permite detectar qué modo fue seleccionado o si se desea salir.

    Args:
        eventos: Lista de eventos (no se usa directamente, se mantiene por compatibilidad).
        botones (dict): Diccionario con claves de modo y sus rects correspondientes.

    Returns:
        tuple: Modo elegido (str o None) y una bandera booleana indicando si se presionó ESC.
    """
    eventos, salir = bucle_eventos_accesibilidad(eventos, botones)
    return eventos, salir

def mostrar_categoria_elegida(estado_global: dict, categoria: str):
    """
    Muestra en pantalla animadamente la categoría elegida por el usuario, letra por letra.

    Luego de mostrar completamente la palabra, espera una pausa antes de continuar.
    Procesa eventos mientras se muestra el texto.

    Args:
        estado_global (dict): Diccionario con configuraciones generales, fuentes y colores.
        categoria (str): Nombre de la categoría seleccionada.
    """
    reloj = pygame.time.Clock()
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    ventana = pygame.display.get_surface()
    ancho_ventana = estado_global["config"]["ventana"]["ancho"]
    alto_ventana = estado_global["config"]["ventana"]["alto"]
    
    texto_base = "Categoría seleccionada:"
    categoria_texto = categoria.capitalize()
    
    letras_mostradas = 0
    tiempo_letra = 300 
    tiempo_ultimo = pygame.time.get_ticks()
    pausa_final = 1500  
    mostrando_pausa = False
    tiempo_pausa_inicio = 0

    while True:
        ventana.fill(colores["GRIS"])

        base_render = estado_global["fuentes"]["titulo"].render(texto_base, True, colores["NEGRO"])
        ventana.blit(base_render, ((ancho_ventana - base_render.get_width()) // 2, alto_ventana // 2 - 60))

        parcial = categoria_texto[:letras_mostradas]
        categoria_render = estado_global["fuentes"]["titulo"].render(parcial, True, colores["AZUL"])
        ventana.blit(categoria_render, ((ancho_ventana - categoria_render.get_width()) // 2, alto_ventana // 2))

        pygame.display.flip()

        bucle_eventos_categoria_elegida()

        ahora = pygame.time.get_ticks()

        if mostrando_pausa == False:
            if ahora - tiempo_ultimo > tiempo_letra:
                letras_mostradas += 1
                tiempo_ultimo = ahora
                if letras_mostradas > len(categoria_texto):
                    mostrando_pausa = True
                    tiempo_pausa_inicio = ahora
        else:
            if ahora - tiempo_pausa_inicio > pausa_final:
                break  

        reloj.tick(60)