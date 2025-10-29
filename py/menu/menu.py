import pygame
import sys
from pantallas.pantallas_submenu import pantalla_pre_juego
from funciones_archivos import *
from pantallas.pantallas_juego import *
from musica import *
from pantallas.pantallas_mensajes import *
from menu.bucles_menu import bucle_inicializar_letras, bucle_game_loop_principal, bucle_procesar_eventos_juego

def inicializar_estado_juego(usuario: str, dificultad: str, categoria: str, estado: dict) -> dict:
    """
    Inicializa el estado del juego configurando letras, preguntas y variables de control.

    Args:
        usuario (str): Nombre del usuario actual.
        dificultad (str): Nivel de dificultad elegido.
        categoria (str): Categoría de preguntas elegida.
        estado (dict): Estado global del juego.

    Returns:
        dict: Estado del juego inicializado con letras, preguntas y parámetros de juego.
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
        "tiempo_total": 120,
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
    Inicializa la música del juego principal deteniendo cualquier reproducción anterior.

    Args:
        estado (dict): Estado global que contiene configuraciones de volumen.
    """
    detener_musica()
    reproducir_musica(estado, "MP3/roscoenpantalla.mp3")

def verificar_tiempo_restante(estado_juego: dict) -> tuple[int, bool]:
    """
    Verifica el tiempo restante y si se ha agotado.

    Args:
        estado_juego (dict): Estado del juego actual.

    Returns:
        tuple[int, bool]: Tiempo restante en segundos y bandera si el tiempo terminó.
    """
    ahora = pygame.time.get_ticks()
    tiempo_pasado = (ahora - estado_juego["inicio"]) // 1000
    tiempo_restante = max(0, estado_juego["tiempo_total"] - tiempo_pasado)
    tiempo_acabado = tiempo_restante == 0
    
    return tiempo_restante, tiempo_acabado

def verificar_condiciones_fin_juego(estado_juego: dict) -> tuple[bool, bool]:
    """
    Verifica si se cumplieron las condiciones para terminar el juego.

    Args:
        estado_juego (dict): Estado actual del juego.

    Returns:
        tuple[bool, bool]: Tupla que indica si el juego finalizó y si todas las letras fueron resueltas.
    """
    return verificar_fin_juego(estado_juego["letras_estado"], estado_juego["ronda_pasadas"])

def obtener_siguiente_letra(estado_juego: dict) -> tuple[int, str, bool]:
    """
    Obtiene el índice y letra siguiente a responder.

    Args:
        estado_juego (dict): Estado actual del juego.

    Returns:
        tuple[int, str, bool]: Índice, letra correspondiente y bandera de validez.
    """
    nuevo_indice = siguiente_letra(
        estado_juego["indice"], 
        estado_juego["letras"], 
        estado_juego["letras_estado"], 
        estado_juego["ronda_pasadas"]
    )
    
    resultado = (None, None, False)
    if nuevo_indice is not None:
        letra_actual = estado_juego["letras"][nuevo_indice]
        resultado = (nuevo_indice, letra_actual, True)
    
    return resultado

def manejar_imagen_resultado(estado_juego: dict, estado: dict) -> pygame.Surface:
    """
    Controla la imagen a mostrar según el resultado de la respuesta del jugador.

    Args:
        estado_juego (dict): Estado actual del juego.
        estado (dict): Estado global con configuración y colores.

    Returns:
        pygame.Surface: Imagen del resultado a mostrar, o None si no se debe mostrar.
    """
    resultado = None
    
    if estado_juego["tipo_resultado"] and estado_juego["tiempo_mensaje"]:
        ahora = pygame.time.get_ticks()
        
        if ahora - estado_juego["tiempo_mensaje"] < 2000:
            if not estado_juego["imagen_resultado"]:
                estado_juego["imagen_resultado"] = obtener_imagen_resultado(estado_juego["tipo_resultado"], estado)
            resultado = estado_juego["imagen_resultado"]
        else:
            estado_juego["tipo_resultado"] = None
            estado_juego["imagen_resultado"] = None
            estado_juego["mensaje_resultado"] = ""
            estado_juego["tiempo_mensaje"] = None
    
    return resultado

def procesar_eventos_juego(estado_juego: dict, boton_pasapalabra: pygame.Rect, estado: dict) -> bool:
    """
    Procesa los eventos durante el ciclo del juego (inputs del usuario).

    Args:
        estado_juego (dict): Estado del juego.
        boton_pasapalabra (pygame.Rect): Rectángulo del botón "Pasapalabra".
        estado (dict): Estado global.

    Returns:
        bool: True si se debe salir del juego, False en caso contrario.
    """
    salir, cambios = bucle_procesar_eventos_juego(estado_juego, boton_pasapalabra, estado)
    
    estado_juego["respuesta_usuario"] = cambios["respuesta_usuario"]
    
    if cambios["procesar_respuesta"]:
        procesar_respuesta_usuario(estado_juego, estado)
        
    return salir

def procesar_respuesta_usuario(estado_juego: dict, estado: dict):
    """
    Procesa la respuesta actual del usuario y actualiza el estado del juego.

    Args:
        estado_juego (dict): Estado actual del juego.
        estado (dict): Estado general del programa.
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
    Finaliza la partida, muestra la pantalla final y guarda estadísticas.

    Args:
        usuario (str): Nombre del jugador.
        dificultad (str): Nivel de dificultad jugado.
        estado_juego (dict): Estado del juego terminado.
        pantalla (pygame.Surface): Superficie principal del juego.
        estado (dict): Estado global de configuración.
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
    Controla el flujo principal de la pantalla de juego, desde la preselección hasta el fin.

    Args:
        pantalla (pygame.Surface): Superficie principal del juego.
        estado (dict): Estado general del juego.
    """
    usuario, dificultad, categoria = pantalla_pre_juego(pantalla, estado)
    estado["usuario_actual"] = usuario
    
    estado_juego = inicializar_estado_juego(usuario, dificultad, categoria, estado)
    inicializar_musica_juego(estado)

    while True:
        if bucle_game_loop_principal(pantalla, estado_juego, estado):
            break

    finalizar_juego(usuario, dificultad, estado_juego, pantalla, estado)