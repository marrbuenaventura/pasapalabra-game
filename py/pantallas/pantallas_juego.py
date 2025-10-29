import math
import sys
import pygame
from pantallas.bucles_pantallas import (
    bucle_dibujar_rosco_letras,
    bucle_filtrar_categoria,
    bucle_organizar_preguntas_por_letra,
    bucle_buscar_siguiente_letra,
    bucle_verificar_estados_juego,
    bucle_calcular_estadisticas_finales,
    bucle_eventos_pantalla_final,
    bucle_renderizar_estadisticas_pantalla_final,
    bucle_dibujar_estadisticas_pantalla_final
)

def dibujar_rosco(letras: list[str], letras_estado: dict[str, str], ventana: pygame.Surface,
                  fuente_letra: pygame.font.Font, estado: dict,
                  centro_x: int, centro_y: int, radio: int = 240, radio_letra: int = 28):
    """
    Dibuja el rosco con las letras y su estado.

    Args:
        letras: lista de letras
        letras_estado: dict letra -> estado ("correcta", "incorrecta", "pasada", "pendiente")
        ventana: superficie pygame donde dibujar
        fuente_letra: fuente para dibujar letras
        estado: dict con configuraciones y estado actual (debe incluir colores y modo)
        centro_x, centro_y: posición central del rosco
        radio: radio del círculo
        radio_letra: radio para cada letra
    """
    bucle_dibujar_rosco_letras(letras, letras_estado, ventana, fuente_letra, estado,
                              centro_x, centro_y, radio, radio_letra)

def aplicar_brillo(ventana: pygame.Surface, ancho: int, alto: int, brillo: float):
    """
    Aplica capa de brillo oscureciendo la pantalla.

    Args:
        ventana: superficie pygame
        ancho: ancho ventana
        alto: alto ventana
        brillo: float 0.0-1.0
    """
    overlay = pygame.Surface((ancho, alto))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(int((1 - brillo) * 255))
    ventana.blit(overlay, (0, 0))

def filtrar_categoria(preguntas: list[dict], categoria: str) -> list[dict]:
    return bucle_filtrar_categoria(preguntas, categoria)

def cargar_preguntas(dificultad: str, categoria: str, leer_csv_func) -> dict:
    """
    Carga preguntas filtradas y organizadas por letra.

    Args:
        dificultad: "facil" o "dificil"
        categoria: categoría a filtrar
        leer_csv_func: función para leer csv que devuelve lista de dicts

    Returns:
        dict letra->pregunta
    """
    preguntas_filtradas = filtrar_categoria(leer_csv_func(f"csv/preguntas_{dificultad}.csv"), categoria)
    return bucle_organizar_preguntas_por_letra(preguntas_filtradas)

def siguiente_letra(indice_actual: int, letras: list[str], letras_estado: dict[str, str], ronda_pasadas: bool) -> int | None:
    """
    Devuelve el índice de la siguiente letra a responder según estado y ronda.

    Args:
        indice_actual: índice actual
        letras: lista de letras
        letras_estado: dict letra->estado
        ronda_pasadas: bool indicando si está en ronda de pasadas

    Returns:
        índice siguiente letra o None si no hay
    """
    total_letras = len(letras)
    return bucle_buscar_siguiente_letra(indice_actual, letras, letras_estado, ronda_pasadas, total_letras)

def obtener_imagen_resultado(tipo: str, estado: dict) -> pygame.Surface | None:
    """
    Devuelve imagen pygame según tipo y modo actual.

    Args:
        tipo: "correcta", "incorrecta", "pasada"
        estado: dict con modo actual (normal/daltonico) e imágenes

    Returns:
        pygame.Surface o None
    """
    modo = estado.get("modo", "normal")
    imagenes = estado.get("imagenes", {}).get(modo, {})
    
    return imagenes.get(tipo)

def mostrar_pantalla_final(pantalla: pygame.Surface, estado: dict,
                           usuario: str, aciertos: int, errores: int,
                           pasadas: int, puntaje: int, duracion_partida: int, dificultad: str):
    """
    Muestra pantalla final con estadísticas.

    Args:
        pantalla: pygame.Surface
        estado: dict con colores, modo, etc.
        usuario: nombre jugador
        aciertos, errores, pasadas: ints
        puntaje: int
        duracion_partida: segundos int
        dificultad: str
    """
    ancho = pantalla.get_width()
    alto = pantalla.get_height()
    modo_actual = estado.get("modo", "normal")
    colores = estado["colores"][modo_actual]

    fuente_titulo = estado["fuentes"]["titulo"]
    fuente_boton = estado["fuentes"]["boton"]
    fuente_pequena = estado["fuentes"]["pequena"]

    total_preguntas = aciertos + errores + pasadas
    porcentaje_aciertos = (aciertos / total_preguntas * 100) if total_preguntas > 0 else 0

    if porcentaje_aciertos >= 90:
        mensaje_rendimiento = "¡EXCELENTE!"
        color_rendimiento = colores["VERDE"]
    elif porcentaje_aciertos >= 70:
        mensaje_rendimiento = "¡MUY BIEN!"
        color_rendimiento = colores["AZUL"]
    elif porcentaje_aciertos >= 50:
        mensaje_rendimiento = "¡BIEN!"
        color_rendimiento = colores["NARANJA"]
    else:
        mensaje_rendimiento = "¡SIGUE INTENTANDO!"
        color_rendimiento = colores["ROJO"]

    minutos = duracion_partida // 60
    segundos = duracion_partida % 60
    tiempo_texto = f"{minutos}:{segundos:02d}"

    clock = pygame.time.Clock()
    continuar = True

    while continuar:
        continuar = bucle_eventos_pantalla_final(continuar)

        pantalla.fill(colores["BLANCO"])

        texto_titulo = fuente_titulo.render("¡JUEGO TERMINADO!", True, colores["AZUL"])
        rect_titulo = texto_titulo.get_rect(center=(ancho // 2, 80))
        pantalla.blit(texto_titulo, rect_titulo)

        texto_rendimiento = fuente_boton.render(mensaje_rendimiento, True, color_rendimiento)
        rect_rendimiento = texto_rendimiento.get_rect(center=(ancho // 2, 150))
        pantalla.blit(texto_rendimiento, rect_rendimiento)

        y_pos = 220

        texto_usuario = fuente_pequena.render(f"Jugador: {usuario}", True, colores["NEGRO"])
        rect_usuario = texto_usuario.get_rect(center=(ancho // 2, y_pos))
        pantalla.blit(texto_usuario, rect_usuario)
        y_pos += 40

        texto_dificultad = fuente_pequena.render(f"Dificultad: {dificultad.capitalize()}", True, colores["NEGRO"])
        rect_dificultad = texto_dificultad.get_rect(center=(ancho // 2, y_pos))
        pantalla.blit(texto_dificultad, rect_dificultad)
        y_pos += 60

        estadisticas = bucle_renderizar_estadisticas_pantalla_final(aciertos, errores, pasadas)
        y_pos = bucle_dibujar_estadisticas_pantalla_final(pantalla, estadisticas, fuente_pequena, 
                                                         colores["NEGRO"], ancho, y_pos)

        y_pos += 20
        texto_puntaje = fuente_boton.render(f"PUNTAJE FINAL: {puntaje}", True, colores["VERDE"])
        rect_puntaje = texto_puntaje.get_rect(center=(ancho // 2, y_pos))
        pantalla.blit(texto_puntaje, rect_puntaje)
        y_pos += 50

        texto_tiempo = fuente_pequena.render(f"Tiempo jugado: {tiempo_texto}", True, colores["NEGRO"])
        rect_tiempo = texto_tiempo.get_rect(center=(ancho // 2, y_pos))
        pantalla.blit(texto_tiempo, rect_tiempo)

        texto_continuar = fuente_pequena.render("Presiona ENTER, ESC o clic para volver al menú", True, colores["GRIS"])
        rect_continuar = texto_continuar.get_rect(center=(ancho // 2, alto - 50))
        pantalla.blit(texto_continuar, rect_continuar)

        pygame.display.flip()
        clock.tick(60)

def verificar_fin_juego(letras_estado: dict[str, str], ronda_pasadas: bool) -> tuple[bool, bool]:
    """
    Verifica si el juego debe terminar.

    Returns:
        (debe_terminar: bool, cambiar_a_ronda_pasadas: bool)
    """
    quedan_pendientes, quedan_pasadas = bucle_verificar_estados_juego(letras_estado)

    if not ronda_pasadas and not quedan_pendientes:
        if quedan_pasadas:
            resultado = (False, True)
        else:
            resultado = (True, False)
    elif ronda_pasadas and not quedan_pasadas:
        resultado = (True, False)
    else:
        resultado = (False, False)
    
    return resultado

def mostrar_resultado(tipo_resultado: str, estado: dict, respuesta_correcta: str = None) -> tuple[str, tuple[int, int, int]]:
    """
    Devuelve mensaje y color según tipo de resultado.

    Args:
        tipo_resultado: "correcta", "incorrecta", "pasada", "tiempo"
        estado: dict con colores
        respuesta_correcta: respuesta correcta para mostrar

    Returns:
        (mensaje, color)
    """
    modo_actual = estado.get("modo", "normal")
    colores = estado["colores"][modo_actual]

    if tipo_resultado == "correcta":
        resultado = ("¡CORRECTO!", colores["VERDE"])
    elif tipo_resultado == "incorrecta":
        if respuesta_correcta and len(respuesta_correcta) > 15:
            respuesta_cortada = respuesta_correcta[:15] + "..."
            mensaje = f"¡INCORRECTO!\nLa respuesta era:\n{respuesta_cortada}"
        else:
            mensaje = f"¡INCORRECTO!\nLa respuesta era: {respuesta_correcta}"
        resultado = (mensaje, colores["ROJO"])
    elif tipo_resultado == "pasada":
        resultado = ("¡PASAPALABRA!", colores["AMARILLO"])
    elif tipo_resultado == "tiempo":
        resultado = ("¡SE ACABÓ EL TIEMPO!", colores["ROJO"])
    else:
        resultado = ("", colores["NEGRO"])
    
    return resultado

def procesar_respuesta(respuesta_usuario: str, letra_actual: str, preguntas_letras: dict, letras_estado: dict[str, str], estado: dict) -> tuple[str, tuple[str, tuple[int, int, int]]]:
    """
    Procesa respuesta, actualiza letras_estado y devuelve tipo resultado y mensaje.

    Returns:
        (tipo_resultado, (mensaje, color))
    """
    respuesta_usuario_lower = respuesta_usuario.lower()
    correcta = preguntas_letras[letra_actual]["respuesta"].lower()

    if respuesta_usuario_lower == "pasapalabra":
        letras_estado[letra_actual] = "pasada"
        tipo = "pasada"
    elif respuesta_usuario_lower == correcta:
        letras_estado[letra_actual] = "correcta"
        tipo = "correcta"
    else:
        letras_estado[letra_actual] = "incorrecta"
        tipo = "incorrecta"

    mensaje = mostrar_resultado(tipo, estado, preguntas_letras[letra_actual]["respuesta"])
    return tipo, mensaje

def manejar_eventos_juego(evento: pygame.event.EventType, respuesta_usuario: str, letra_actual: str, preguntas_letras: dict, letras_estado: dict, boton_pasapalabra: pygame.Rect) -> dict:
    """
    Maneja eventos y devuelve dict con cambios.

    Keys en dict devuelto:
        - respuesta_usuario: string actualizado
        - procesar_respuesta: bool si se debe procesar
        - salir: bool para salir

    """
    cambios = {
        "respuesta_usuario": respuesta_usuario,
        "procesar_respuesta": False,
        "salir": False
    }

    if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            cambios["salir"] = True
        elif evento.key == pygame.K_BACKSPACE:
            cambios["respuesta_usuario"] = respuesta_usuario[:-1]
        elif evento.key == pygame.K_RETURN:
            cambios["procesar_respuesta"] = True
        else:
            if len(respuesta_usuario) < 20 and evento.unicode.isprintable():
                cambios["respuesta_usuario"] = respuesta_usuario + evento.unicode
    elif evento.type == pygame.MOUSEBUTTONDOWN:
        if boton_pasapalabra.collidepoint(evento.pos):
            cambios["procesar_respuesta"] = True
            cambios["respuesta_usuario"] = "pasapalabra"

    return cambios

def calcular_estadisticas_finales(letras_estado: dict[str, str], dificultad: str, tiempo_total: int, tiempo_restante: int) -> dict:
    """
    Calcula y devuelve estadísticas finales.

    Returns:
        dict con aciertos, errores, pasadas, puntaje y duración.
    """
    conteo = bucle_calcular_estadisticas_finales(letras_estado)

    aciertos = conteo["correcta"]
    errores = conteo["incorrecta"]
    pasadas = conteo["pasada"]
    puntaje = aciertos * (10 if dificultad == "facil" else 20)
    duracion_partida = tiempo_total - tiempo_restante

    return {
        "aciertos": aciertos,
        "errores": errores,
        "pasadas": pasadas,
        "puntaje": puntaje,
        "duracion_partida": duracion_partida,
    }

def obtener_colores(estado: dict, modo: str | None = None) -> dict:
    if modo == None:
        modo = estado.get("modo", "normal")
    return estado["colores"][modo]