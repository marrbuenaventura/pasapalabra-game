import pygame
import sys
import math

def bucle_dibujar_rosco_letras(letras: list[str], letras_estado: dict[str, str], ventana: pygame.Surface,
                              fuente_letra: pygame.font.Font, estado: dict,
                              centro_x: int, centro_y: int, radio: int = 240, radio_letra: int = 28):
    """
    Dibuja cada letra del rosco en un círculo con su estado correspondiente.

    Args:
        letras (list[str]): Lista de letras del abecedario.
        letras_estado (dict[str, str]): Diccionario con el estado de cada letra.
        ventana (pygame.Surface): Superficie donde dibujar.
        fuente_letra (pygame.font.Font): Fuente para renderizar las letras.
        estado (dict): Estado global con colores y configuraciones.
        centro_x (int): Coordenada X del centro del rosco.
        centro_y (int): Coordenada Y del centro del rosco.
        radio (int): Radio del círculo del rosco.
        radio_letra (int): Radio de cada círculo de letra.

    Returns:
        None: Esta función no retorna valores.
    """
    modo_actual = estado.get("modo", "normal")
    colores = estado["colores"][modo_actual]
    
    for i, letra in enumerate(letras):
        angulo = (2 * math.pi / len(letras)) * i - math.pi / 2
        x = centro_x + int(math.cos(angulo) * radio)
        y = centro_y + int(math.sin(angulo) * radio)

        estado_letra = letras_estado.get(letra, "pendiente")

        if estado_letra == "correcta":
            color = colores["VERDE"]
        elif estado_letra == "incorrecta":
            color = colores["ROJO"]
        elif estado_letra == "pasada":
            color = colores["AMARILLO"]
        else:
            color = colores["AZUL"]

        pygame.draw.circle(ventana, color, (x, y), radio_letra)
        letra_render = fuente_letra.render(letra, True, colores["BLANCO"])
        ventana.blit(
            letra_render,
            (x - letra_render.get_width() // 2, y - letra_render.get_height() // 2)
        )

def bucle_filtrar_categoria(preguntas: list[dict], categoria: str) -> list[dict]:
    """
    Filtra una lista de preguntas por categoría específica.

    Args:
        preguntas (list[dict]): Lista de diccionarios con preguntas.
        categoria (str): Categoría por la cual filtrar.

    Returns:
        list[dict]: Lista filtrada de preguntas que coinciden con la categoría.
    """
    filtradas = []
    for pregunta in preguntas:
        if pregunta["categoria"].lower() == categoria.lower():
            filtradas.append(pregunta)
    return filtradas

def bucle_organizar_preguntas_por_letra(preguntas_filtradas: list[dict]) -> dict:
    """
    Organiza preguntas filtradas en un diccionario indexado por letra.

    Args:
        preguntas_filtradas (list[dict]): Lista de preguntas ya filtradas.

    Returns:
        dict: Diccionario con letras como claves y preguntas como valores.
    """
    preguntas_letras = {}
    for pregunta in preguntas_filtradas:
        letra = pregunta["letra"].upper()
        preguntas_letras[letra] = pregunta
    return preguntas_letras

def bucle_buscar_siguiente_letra(indice_actual: int, letras: list[str], letras_estado: dict[str, str], 
                                ronda_pasadas: bool, total_letras: int) -> int | None:
    """
    Busca el índice de la siguiente letra disponible según el estado del juego.

    Args:
        indice_actual (int): Índice actual en la lista de letras.
        letras (list[str]): Lista de letras del juego.
        letras_estado (dict[str, str]): Estado actual de cada letra.
        ronda_pasadas (bool): Indica si está en ronda de pasapalabras.
        total_letras (int): Número total de letras.

    Returns:
        int or None: Índice de la siguiente letra disponible o None si no hay.
    """
    resultado = None
    
    for _ in range(total_letras):
        letra = letras[indice_actual]
        estado = letras_estado[letra]
        if (not ronda_pasadas and estado == "pendiente") or (ronda_pasadas and estado == "pasada"):
            resultado = indice_actual
            break
        indice_actual = (indice_actual + 1) % total_letras
    
    return resultado

def bucle_verificar_estados_juego(letras_estado: dict[str, str]) -> tuple[bool, bool]:
    """
    Verifica si quedan letras pendientes o pasadas en el juego.

    Args:
        letras_estado (dict[str, str]): Estado actual de todas las letras.

    Returns:
        tuple[bool, bool]: Tupla con (quedan_pendientes, quedan_pasadas).
    """
    quedan_pendientes = False
    quedan_pasadas = False
    
    for estado in letras_estado.values():
        if estado == "pendiente":
            quedan_pendientes = True
        elif estado == "pasada":
            quedan_pasadas = True
    
    return quedan_pendientes, quedan_pasadas

def bucle_calcular_estadisticas_finales(letras_estado: dict[str, str]) -> dict:
    """
    Calcula las estadísticas finales del juego contando estados de letras.

    Args:
        letras_estado (dict[str, str]): Estado final de todas las letras.

    Returns:
        dict: Diccionario con conteo de correctas, incorrectas y pasadas.
    """
    conteo = {"correcta": 0, "incorrecta": 0, "pasada": 0}
    
    for estado_letra in letras_estado.values():
        if estado_letra in conteo:
            conteo[estado_letra] += 1
    
    return conteo

def bucle_renderizar_texto_multilinea(texto: str, fuente: pygame.font.Font, 
                                     color: tuple[int, int, int], ancho_max: int) -> list[pygame.Surface]:
    """
    Renderiza texto dividido en múltiples líneas según ancho máximo.

    Args:
        texto (str): Texto a renderizar.
        fuente (pygame.font.Font): Fuente para el renderizado.
        color (tuple[int, int, int]): Color RGB del texto.
        ancho_max (int): Ancho máximo permitido por línea.

    Returns:
        list[pygame.Surface]: Lista de superficies renderizadas, una por línea.
    """
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        test_linea = f"{linea_actual} {palabra}".strip()
        if fuente.size(test_linea)[0] <= ancho_max:
            linea_actual = test_linea
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    lineas.append(linea_actual)

    return [fuente.render(linea, True, color) for linea in lineas]

def bucle_dibujar_texto_multilinea_manual(ventana: pygame.Surface, texto: str, x: int, y: int, 
                                         ancho: int, color: tuple[int, int, int], fuente: pygame.font.Font):
    """
    Dibuja texto multilínea palabra por palabra en la ventana.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        texto (str): Texto a dibujar.
        x (int): Coordenada X inicial.
        y (int): Coordenada Y inicial.
        ancho (int): Ancho máximo disponible.
        color (tuple[int, int, int]): Color RGB del texto.
        fuente (pygame.font.Font): Fuente para el renderizado.

    Returns:
        None: Esta función no retorna valores.
    """
    palabras = texto.split(' ')
    linea = ''
    y_offset = 0
    
    for palabra in palabras:
        prueba_linea = linea + palabra + ' '
        ancho_texto, _ = fuente.size(prueba_linea)
        if ancho_texto > ancho:
            texto_render = fuente.render(linea, True, color)
            ventana.blit(texto_render, (x, y + y_offset))
            y_offset += texto_render.get_height() + 5
            linea = palabra + ' '
        else:
            linea = prueba_linea
    
    texto_render = fuente.render(linea, True, color)
    ventana.blit(texto_render, (x, y + y_offset))

def bucle_dibujar_items_estadisticas(ventana: pygame.Surface, estado_global: dict, textos: list[str], 
                                    contenedor: pygame.Rect, fuente: pygame.font.Font,
                                    padding_vertical: int, alto_item: int, espacio_entre_items: int):
    """
    Dibuja items de estadísticas en formato de lista estilizada.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        estado_global (dict): Estado global con colores y configuraciones.
        textos (list[str]): Lista de textos a mostrar.
        contenedor (pygame.Rect): Rectángulo contenedor.
        fuente (pygame.font.Font): Fuente para el texto.
        padding_vertical (int): Espaciado vertical inicial.
        alto_item (int): Altura de cada item.
        espacio_entre_items (int): Espacio entre items.

    Returns:
        None: Esta función no retorna valores.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    for i, texto in enumerate(textos):
        y = contenedor.y + padding_vertical + i * espacio_entre_items
        item_rect = pygame.Rect(
            contenedor.x + 30, y,
            contenedor.width - 60, alto_item
        )
        pygame.draw.rect(ventana, colores["AZUL"], item_rect, border_radius=12)
        pygame.draw.rect(ventana, colores["NEGRO"], item_rect, 3, border_radius=12)

        texto_render = fuente.render(texto, True, colores["BLANCO"])
        ventana.blit(
            texto_render,
            (item_rect.x + 15, item_rect.y + (alto_item - texto_render.get_height()) // 2)
        )

def bucle_eventos_pantalla_final(continuar: bool) -> bool:
    """
    Maneja eventos para la pantalla final del juego.

    Args:
        continuar (bool): Estado actual del bucle de eventos.

    Returns:
        bool: Nuevo estado del bucle (False para salir).
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                continuar = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            continuar = False
    
    return continuar

def bucle_eventos_mensaje_simple() -> bool:
    """
    Maneja eventos para mensajes simples con espera de usuario.

    Args:
        None

    Returns:
        bool: True si debe seguir esperando, False para salir.
    """
    esperando = True
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            esperando = False
    
    return esperando

def bucle_eventos_mensaje_temporal(segundos: int, tiempo_inicial: int) -> bool:
    """
    Maneja eventos para mensajes con tiempo límite.

    Args:
        segundos (int): Duración del mensaje en segundos.
        tiempo_inicial (int): Timestamp inicial del mensaje.

    Returns:
        bool: True si debe continuar mostrando, False si acabó el tiempo.
    """
    continuar = True
    
    if (pygame.time.get_ticks() - tiempo_inicial) >= segundos * 1000:
        continuar = False
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    return continuar

def bucle_dibujar_encabezado_tabla(ventana: pygame.Surface, fuente_pequena: pygame.font.Font, 
                                  encabezado: list[str], indices: list[int], col_width: int, row_height: int):
    """
    Dibuja el encabezado de una tabla con columnas especificadas.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        fuente_pequena (pygame.font.Font): Fuente para el texto del encabezado.
        encabezado (list[str]): Lista de títulos de columnas.
        indices (list[int]): Índices de columnas a mostrar.
        col_width (int): Ancho de cada columna.
        row_height (int): Altura de la fila del encabezado.

    Returns:
        None: Esta función no retorna valores.
    """
    ancho = ventana.get_width()
    pygame.draw.rect(ventana, (200, 220, 255), (0, 90, ancho, row_height))
    
    for i, idx in enumerate(indices):
        texto = fuente_pequena.render(encabezado[idx].capitalize(), True, (0, 0, 0))
        x = i * col_width + (col_width - texto.get_width()) // 2
        ventana.blit(texto, (x, 95))

def bucle_dibujar_filas_tabla(ventana: pygame.Surface, fuente_pequena: pygame.font.Font,
                             datos: list[list[str]], indices: list[int], col_width: int, row_height: int,
                             scroll: int, mouse_y: int):
    """
    Dibuja las filas de datos de una tabla con scroll y hover.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        fuente_pequena (pygame.font.Font): Fuente para el texto.
        datos (list[list[str]]): Datos de la tabla.
        indices (list[int]): Índices de columnas a mostrar.
        col_width (int): Ancho de cada columna.
        row_height (int): Altura de cada fila.
        scroll (int): Desplazamiento vertical actual.
        mouse_y (int): Posición Y del mouse para hover.

    Returns:
        None: Esta función no retorna valores.
    """
    ancho = ventana.get_width()
    alto = ventana.get_height()
    start_y = 90 + row_height
    
    for i, fila in enumerate(datos):
        y = start_y + i * row_height - scroll
        if y + row_height < 90 or y > alto:
            continue

        hover = 90 + row_height < mouse_y < alto and y < mouse_y < y + row_height
        color = (200, 230, 255) if hover else ((230, 230, 230) if i % 2 == 0 else (255, 255, 255))
        pygame.draw.rect(ventana, color, (0, y, ancho, row_height))

        for j, idx in enumerate(indices):
            if idx < len(fila):
                texto = fuente_pequena.render(fila[idx], True, (0, 0, 0))
            else:
                texto = fuente_pequena.render("", True, (0, 0, 0))

            x = j * col_width + (col_width - texto.get_width()) // 2
            ventana.blit(texto, (x, y + 8))

def bucle_renderizar_estadisticas_pantalla_final(aciertos: int, errores: int, pasadas: int) -> list[str]:
    """
    Genera una lista de strings con estadísticas formateadas para pantalla final.

    Args:
        aciertos (int): Número de respuestas correctas.
        errores (int): Número de respuestas incorrectas.
        pasadas (int): Número de pasapalabras.

    Returns:
        list[str]: Lista de estadísticas formateadas incluyendo porcentaje de precisión.
    """
    estadisticas = [
        f"Respuestas Correctas: {aciertos}",
        f"Respuestas Incorrectas: {errores}",
        f"Pasapalabras: {pasadas}",
    ]
    
    total_preguntas = aciertos + errores + pasadas
    if total_preguntas > 0:
        porcentaje_aciertos = (aciertos / total_preguntas * 100)
        estadisticas.append(f"Precisión: {porcentaje_aciertos:.1f}%")
    
    return estadisticas

def bucle_dibujar_estadisticas_pantalla_final(ventana: pygame.Surface, estadisticas: list[str], fuente: pygame.font.Font, color: tuple[int, int, int],ancho: int, y_inicial: int) -> int:
    """
    Dibuja las estadísticas en la pantalla final y retorna la posición Y final.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        estadisticas (list[str]): Lista de estadísticas a mostrar.
        fuente (pygame.font.Font): Fuente para el texto.
        color (tuple[int, int, int]): Color RGB del texto.
        ancho (int): Ancho de la ventana para centrado.
        y_inicial (int): Posición Y inicial.

    Returns:
        int: Posición Y final después de dibujar todas las estadísticas.
    """
    y_pos = y_inicial
    
    for estadistica in estadisticas:
        texto_stat = fuente.render(estadistica, True, color)
        rect_stat = texto_stat.get_rect(center=(ancho // 2, y_pos))
        ventana.blit(texto_stat, rect_stat)
        y_pos += 35
    
    return y_pos

def bucle_renderizar_lineas_mensaje(mensaje_resultado: str) -> list[str]:
    """
    Procesa un mensaje multilínea y lo divide en líneas individuales.

    Args:
        mensaje_resultado (str): Mensaje que puede contener saltos de línea.

    Returns:
        list[str]: Lista de líneas individuales del mensaje.
    """
    return mensaje_resultado.split('\n')

def bucle_dibujar_lineas_mensaje(ventana: pygame.Surface, lineas_mensaje: list[str], 
                                fuente: pygame.font.Font, color_mensaje: tuple[int, int, int],
                                input_rect: pygame.Rect):
    """
    Dibuja líneas de mensaje debajo de un rectángulo de input.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        lineas_mensaje (list[str]): Lista de líneas a dibujar.
        fuente (pygame.font.Font): Fuente para el texto.
        color_mensaje (tuple[int, int, int]): Color RGB del texto.
        input_rect (pygame.Rect): Rectángulo de referencia para posicionamiento.

    Returns:
        None: Esta función no retorna valores.
    """
    for i, linea in enumerate(lineas_mensaje):
        mensaje_render = fuente.render(linea, True, color_mensaje)
        y_posicion = input_rect.y + input_rect.height + 15 + (i * 30)
        ventana.blit(mensaje_render, (input_rect.x, y_posicion))