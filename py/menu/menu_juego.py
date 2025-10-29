from pantallas.pantallas_mensajes import mostrar_pantalla, mostrar_resultado
from pantallas.pantallas_submenu import pantalla_pre_juego
from pantallas.pantallas_juego import *
import pygame
import sys
from funciones_archivos import *
from musica import *
from menu.bucles_menu import bucle_inicializar_letras, bucle_game_loop_principal

def inicializar_estado_juego(usuario: str, dificultad: str, categoria: str, estado: dict) -> dict:
    """
    Inicializa todas las variables necesarias para el comienzo de una partida.

    Args:
        usuario (str): Nombre del jugador actual.
        dificultad (str): Dificultad seleccionada ('fácil', 'difícil').
        categoria (str): Categoría seleccionada ('cine', 'música', etc.).
        estado (dict): Diccionario general del estado del juego.

    Returns:
        dict: Diccionario con el estado del juego inicializado (letras, preguntas, tiempos, etc.).
    """
    letras, letras_estado = bucle_inicializar_letras()
    preguntas_letras = cargar_preguntas(dificultad, categoria, leer_csv_func=leer_csv)
    
    modo_actual = estado.get("modo", "normal")
    color_mensaje = estado["colores"][modo_actual]["NEGRO"]
    
    return {
        "letras": letras,
        "letras_estado": letras_estado,
        "preguntas_letras": preguntas_letras,
        "imagen_resultado": None,
        "tipo_resultado": None,
        "tiempo_mensaje": None,
        "tiempo_total": 180,
        "inicio": pygame.time.get_ticks(),
        "indice": 0,
        "total_letras": len(letras),
        "respuesta_usuario": "",
        "mensaje_resultado": "",
        "color_mensaje": color_mensaje,
        "ronda_pasadas": False
    }

def inicializar_musica_juego(estado: dict):
    """
    Detiene la música actual (si hay) y reproduce el tema del juego.

    Args:
        estado (dict): Estado general del juego que incluye configuraciones y modo.
    """
    detener_musica()
    reproducir_musica(estado, "MP3/roscoenpantalla.mp3")

def verificar_tiempo_restante(estado_juego: dict) -> tuple[int, bool]:
    """
    Calcula el tiempo restante de la partida y verifica si se acabó el tiempo.

    Args:
        estado_juego (dict): Estado actual de la partida.

    Returns:
        tuple[int, bool]: Tiempo restante (en segundos) y booleano indicando si se acabó el tiempo.
    """
    ahora = pygame.time.get_ticks()
    tiempo_pasado = (ahora - estado_juego["inicio"]) // 1000
    tiempo_restante = max(0, estado_juego["tiempo_total"] - tiempo_pasado)
    tiempo_acabado = tiempo_restante == 0
    
    return tiempo_restante, tiempo_acabado

def verificar_condiciones_fin_juego(estado_juego: dict) -> tuple[bool, bool]:
    """
    Verifica si se cumplen las condiciones para terminar el juego.

    Args:
        estado_juego (dict): Estado actual del juego.

    Returns:
        tuple[bool, bool]: Flags indicando si terminó la ronda y si todas las letras fueron respondidas.
    """
    return verificar_fin_juego(estado_juego["letras_estado"], estado_juego["ronda_pasadas"])

def obtener_siguiente_letra(estado_juego: dict) -> tuple[int, str, bool]:
    """
    Obtiene el índice y la letra de la siguiente pregunta en el rosco.

    Args:
        estado_juego (dict): Estado actual del juego.

    Returns:
        tuple[int, str, bool]: Índice de la letra, la letra en sí, y booleano indicando si se pudo obtener.
    """
    nuevo_indice = siguiente_letra(
        estado_juego["indice"], 
        estado_juego["letras"], 
        estado_juego["letras_estado"], 
        estado_juego["ronda_pasadas"]
    )
    
    if nuevo_indice == None:
        return None, None, False
    
    letra_actual = estado_juego["letras"][nuevo_indice]
    return nuevo_indice, letra_actual, True

def manejar_imagen_resultado(estado_juego: dict, estado: dict) -> pygame.Surface:
    """
    Devuelve la imagen del resultado reciente (acierto, error o pasada) si debe mostrarse.

    Args:
        estado_juego (dict): Estado actual del juego.
        estado (dict): Estado general del sistema.

    Returns:
        pygame.Surface: Imagen correspondiente al resultado, o None si no debe mostrarse.
    """
    if not estado_juego["tipo_resultado"] or not estado_juego["tiempo_mensaje"]:
        return None
    
    ahora = pygame.time.get_ticks()
    
    if ahora - estado_juego["tiempo_mensaje"] < 2000:
        if not estado_juego["imagen_resultado"]:
            estado_juego["imagen_resultado"] = obtener_imagen_resultado(estado_juego["tipo_resultado"], estado)
        return estado_juego["imagen_resultado"]
    else:
        estado_juego["tipo_resultado"] = None
        estado_juego["imagen_resultado"] = None
        estado_juego["mensaje_resultado"] = ""
        estado_juego["tiempo_mensaje"] = None
        return None

def procesar_eventos_juego(estado_juego: dict, boton_pasapalabra: pygame.Rect, estado: dict) -> bool:
    """
    Procesa eventos de teclado, mouse y lógica del juego durante una ronda.

    Args:
        estado_juego (dict): Estado actual del juego.
        boton_pasapalabra (pygame.Rect): Área del botón "Pasapalabra".
        estado (dict): Estado general del sistema.

    Returns:
        bool: True si se desea salir del juego, False en caso contrario.
    """
    from menu.bucles_menu import bucle_procesar_eventos_juego
    salir, cambios = bucle_procesar_eventos_juego(estado_juego, boton_pasapalabra, estado)
    
    estado_juego["respuesta_usuario"] = cambios["respuesta_usuario"]
    
    if cambios["procesar_respuesta"]:
        procesar_respuesta_usuario(estado_juego, estado)
        
    return salir

def procesar_respuesta_usuario(estado_juego: dict, estado: dict):
    """
    Procesa la respuesta ingresada por el usuario, actualizando estados y resultados.

    Args:
        estado_juego (dict): Estado actual del juego.
        estado (dict): Estado general del sistema.
    """
    letra_actual = estado_juego["letras"][estado_juego["indice"]]
    
    tipo_resultado, resultado = procesar_respuesta(
        estado_juego["respuesta_usuario"], 
        letra_actual, 
        estado_juego["preguntas_letras"], 
        estado_juego["letras_estado"], 
        estado
    )
    
    estado_juego["tipo_resultado"] = tipo_resultado
    estado_juego["mensaje_resultado"], estado_juego["color_mensaje"] = resultado
    estado_juego["tiempo_mensaje"] = pygame.time.get_ticks()
    estado_juego["respuesta_usuario"] = ""
    estado_juego["indice"] = (estado_juego["indice"] + 1) % estado_juego["total_letras"]

def finalizar_juego(usuario: str, dificultad: str, estado_juego: dict, pantalla: pygame.Surface, estado: dict):
    """
    Finaliza el juego, muestra resultados, guarda estadísticas y actualiza partidas jugadas.

    Args:
        usuario (str): Nombre del jugador actual.
        dificultad (str): Dificultad seleccionada.
        estado_juego (dict): Estado de la partida finalizada.
        pantalla (pygame.Surface): Superficie donde se muestran los resultados.
        estado (dict): Estado general del sistema.
    """
    detener_musica()
    reproducir_musica(estado, "MP3/tiempo_termino.mp3")
    
    estadisticas = calcular_estadisticas_finales(
        estado_juego["letras_estado"], 
        dificultad, 
        estado_juego["tiempo_total"], 
        estado_juego["tiempo_total"] - (pygame.time.get_ticks() - estado_juego["inicio"]) // 1000
    )
    
    mostrar_pantalla_final(
        pantalla, estado, usuario, 
        estadisticas["aciertos"], 
        estadisticas["errores"], 
        estadisticas["pasadas"], 
        estadisticas["puntaje"], 
        estadisticas["duracion_partida"], 
        dificultad
    )
    
    detener_musica()
    
    guardar_estadisticas_partida({
        "usuario": usuario,
        "aciertos": estadisticas["aciertos"],
        "errores": estadisticas["errores"],
        "pasadas": estadisticas["pasadas"],
        "puntaje": estadisticas["puntaje"],
        "tiempo": estadisticas["duracion_partida"]
    })
    
    incrementar_contador_partidas(usuario)

def pantalla_juego(pantalla: pygame.Surface, estado: dict):
    """
    Controla el ciclo completo de juego: pantalla pre-juego, partida, y finalización.

    Args:
        pantalla (pygame.Surface): Superficie principal de Pygame.
        estado (dict): Estado general del sistema.
    """
    usuario, dificultad, categoria = pantalla_pre_juego(pantalla, estado)
    estado["usuario_actual"] = usuario
    
    estado_juego = inicializar_estado_juego(usuario, dificultad, categoria, estado)
    inicializar_musica_juego(estado)

    while True:
        if bucle_game_loop_principal(pantalla, estado_juego, estado):
            break

    finalizar_juego(usuario, dificultad, estado_juego, pantalla, estado)