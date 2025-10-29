import pygame
import sys

def bucle_inicializar_letras() -> tuple[list, dict]:
    """
    Inicializa las letras del alfabeto (sin incluir 'Ñ') y su estado inicial.

    Returns:
        tuple[list, dict]: Lista de letras en mayúscula y diccionario con cada letra asociada a su estado "pendiente".
    """
    letras = []
    for i in range(65, 91):
        if chr(i) != "Ñ":
            letras.append(chr(i))
    
    letras_estado = {}
    for letra in letras:
        letras_estado[letra] = "pendiente"
    
    return letras, letras_estado

def bucle_procesar_eventos_juego(estado_juego: dict, boton_pasapalabra: pygame.Rect, estado: dict) -> tuple[bool, dict]:
    """
    Procesa los eventos del juego para una letra actual, incluyendo entrada del usuario y botón Pasapalabra.

    Args:
        estado_juego (dict): Diccionario con el estado actual del juego.
        boton_pasapalabra (pygame.Rect): Rectángulo del botón Pasapalabra.
        estado (dict): Diccionario de configuración global.

    Returns:
        tuple[bool, dict]: Indicador de si se debe salir del juego y diccionario con los cambios del evento.
    """
    cambios_eventos = {"salir": False, "respuesta_usuario": estado_juego["respuesta_usuario"], "procesar_respuesta": False}
    
    for evento in pygame.event.get():
        from pantallas.pantallas_juego import manejar_eventos_juego
        cambios = manejar_eventos_juego(
            evento, 
            estado_juego["respuesta_usuario"], 
            estado_juego["letras"][estado_juego["indice"]], 
            estado_juego["preguntas_letras"], 
            estado_juego["letras_estado"], 
            boton_pasapalabra
        )
        
        if cambios["salir"]:
            pygame.quit()
            sys.exit()
        
        cambios_eventos = cambios
        break 
    
    return cambios_eventos["salir"], cambios_eventos

def bucle_eventos_menu_principal(pantalla: pygame.Surface, lineas_estadisticas: list, estado: dict, botones: dict) -> bool:
    """
    Maneja los eventos del menú principal (Jugar, Puntajes, Ajustes).

    Args:
        pantalla (pygame.Surface): Superficie principal del juego.
        lineas_estadisticas (list): Datos de estadísticas leídas.
        estado (dict): Diccionario de configuración global.
        botones (dict): Diccionario de botones en pantalla.

    Returns:
        bool: True si se ejecutó alguna acción (navegación), False si no hubo interacción.
    """
    accion_realizada = False
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botones["jugar"].collidepoint(evento.pos):
                from menu.menu_principal import importar_juego_principal
                pantalla_juego = importar_juego_principal()
                pantalla_juego(pantalla, estado)
                accion_realizada = True
            elif botones["puntajes"].collidepoint(evento.pos):
                from menu.menu_principal import importar_submenu_puntajes
                pantalla_puntajes = importar_submenu_puntajes()
                pantalla_puntajes(pantalla, lineas_estadisticas, estado)
                accion_realizada = True
            elif botones["ajustes"].collidepoint(evento.pos):
                from menu.menu_principal import importar_submenu_ajustes
                pantalla_ajustes = importar_submenu_ajustes()
                pantalla_ajustes(pantalla, estado)
                accion_realizada = True
    
    return accion_realizada

def bucle_manejar_eventos_ajustes(botones: dict, pantalla: pygame.Surface, estado: dict) -> str:
    """
    Procesa los eventos dentro del submenú de ajustes.

    Args:
        botones (dict): Diccionario de botones disponibles.
        pantalla (pygame.Surface): Superficie principal del juego.
        estado (dict): Diccionario de configuración global.

    Returns:
        str: Clave del botón seleccionado.
    """
    from eventos.eventos_menu import manejar_eventos_submenu
    seleccion = manejar_eventos_submenu(botones)
    return seleccion

def bucle_manejar_eventos_puntajes(botones: dict, pantalla: pygame.Surface, estado: dict, lineas_estadisticas: list) -> str:
    """
    Procesa los eventos dentro del submenú de puntajes.

    Args:
        botones (dict): Diccionario de botones disponibles.
        pantalla (pygame.Surface): Superficie principal del juego.
        estado (dict): Diccionario de configuración global.
        lineas_estadisticas (list): Datos estadísticos.

    Returns:
        str: Clave del botón seleccionado.
    """
    from eventos.eventos_menu import manejar_eventos_submenu
    seleccion = manejar_eventos_submenu(botones)
    return seleccion

def bucle_crear_botones_menu(pantalla: pygame.Surface, estado: dict, tipo_menu: str) -> dict:
    """
    Crea y dibuja botones en pantalla según el tipo de menú (principal, ajustes, puntajes).

    Args:
        pantalla (pygame.Surface): Superficie donde se dibujan los botones.
        estado (dict): Diccionario de configuración global.
        tipo_menu (str): Tipo de menú ("principal", "ajustes", "puntajes").

    Returns:
        dict: Diccionario de botones creados.
    """
    from pantallas.pantallas_componentes import dibujar_boton
    
    if tipo_menu == "principal":
        ancho_boton = 250
        alto_boton = 80
        x_boton = (estado["config"]["ventana"]["ancho"] - ancho_boton) // 2
        
        botones = {}
        opciones = [("jugar", "Jugar", 260), ("puntajes", "Puntajes", 370), ("ajustes", "Ajustes", 480)]
        
        for clave, texto, y_pos in opciones:
            botones[clave] = dibujar_boton(pantalla, estado, texto, x_boton, y_pos, ancho_boton, alto_boton)
        
        return botones
    
    elif tipo_menu == "ajustes":
        botones = {}
        opciones = [
            ("visual_sonido", "Visual y sonido", 250),
            ("accesibilidad", "Accesibilidad", 330),
            ("restaurar", "Restaurar valores", 410)
        ]
        
        for clave, texto, y_pos in opciones:
            botones[clave] = dibujar_boton(pantalla, estado, texto, 450, y_pos, 300, 65)
        
        return botones
    
    elif tipo_menu == "puntajes":
        ancho_boton = 300
        alto_boton = 65
        x_boton = (estado["config"]["ventana"]["ancho"] - ancho_boton) // 2
        
        botones = {}
        opciones = [
            ("ver_puntajes", "Ver puntajes", 240),
            ("ver_estadisticas", "Ver estadísticas", 320),
            ("ver_historial", "Ver historial usuario", 400)
        ]
        
        for clave, texto, y_pos in opciones:
            botones[clave] = dibujar_boton(pantalla, estado, texto, x_boton, y_pos, ancho_boton, alto_boton)
        
        return botones
    
    return {}

def bucle_game_loop_principal(pantalla: pygame.Surface, estado_juego: dict, estado: dict) -> bool:
    """
    Bucle principal del juego. Controla el flujo por letra, tiempo, rondas y muestra pantalla actual.

    Args:
        pantalla (pygame.Surface): Superficie del juego.
        estado_juego (dict): Estado del juego (preguntas, respuestas, letra actual, etc.).
        estado (dict): Configuración global del sistema.

    Returns:
        bool: True si el juego debe finalizar, False si debe continuar.
    """
    from pantallas.pantallas_mensajes import mostrar_resultado, mostrar_pantalla
    from menu.menu_juego import verificar_tiempo_restante
    tiempo_restante, tiempo_acabado = verificar_tiempo_restante(estado_juego)
    
    if tiempo_acabado:
        mostrar_resultado("tiempo", estado)
        return True

    from menu.menu_juego import verificar_condiciones_fin_juego
    debe_terminar, cambiar_ronda = verificar_condiciones_fin_juego(estado_juego)
    
    if cambiar_ronda:
        estado_juego["ronda_pasadas"] = True
        estado_juego["indice"] = 0
        estado_juego["respuesta_usuario"] = ""
        estado_juego["mensaje_resultado"] = ""
        return False
    
    if debe_terminar:
        return True

    from menu.menu_juego import obtener_siguiente_letra
    nuevo_indice, letra_actual, continuar = obtener_siguiente_letra(estado_juego)
    if not continuar:
        return True
    
    estado_juego["indice"] = nuevo_indice

    from menu.menu_juego import manejar_imagen_resultado
    imagen_resultado_actual = manejar_imagen_resultado(estado_juego, estado)

    input_rect, boton_pasapalabra = mostrar_pantalla(
        pantalla, estado, letra_actual, estado_juego["preguntas_letras"], 
        estado_juego["letras"], estado_juego["letras_estado"],
        estado_juego["respuesta_usuario"], estado_juego["mensaje_resultado"], 
        estado_juego["color_mensaje"], tiempo_restante, estado_juego["tiempo_mensaje"], 
        imagen_resultado_actual
    )
    
    pygame.display.flip()

    salir, cambios = bucle_procesar_eventos_juego(estado_juego, boton_pasapalabra, estado)
    if salir:
        return True
        
    estado_juego["respuesta_usuario"] = cambios["respuesta_usuario"]
    
    if cambios["procesar_respuesta"]:
        from menu.menu_juego import procesar_respuesta_usuario
        procesar_respuesta_usuario(estado_juego, estado)
    
    return False