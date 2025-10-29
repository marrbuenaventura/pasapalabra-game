import pygame
import sys

def bucle_buscar_maximo(lista: list) -> int | float:
    """
    Busca el valor máximo dentro de una lista de números.

    Args:
        lista (list): Lista de números.

    Returns:
        int | float: El valor máximo encontrado.
    """
    maximo = lista[0]
    for i in range(1, len(lista)):
        if lista[i] > maximo:
            maximo = lista[i]
    return maximo

def bucle_calcular_promedio(lista: list) -> float:
    """
    Calcula el promedio de una lista de números.

    Args:
        lista (list): Lista de números.

    Returns:
        float: Promedio de los valores en la lista.
    """
    total = 0
    cantidad = 0
    for i in range(len(lista)):
        total = total + lista[i]
        cantidad = cantidad + 1
    return total / cantidad

def bucle_ordenar_burbuja(lista: list) -> list:
    """
    Ordena una lista de tuplas por el segundo valor de cada tupla de forma descendente.

    Args:
        lista (list): Lista de tuplas, donde el segundo elemento es un número.

    Returns:
        list: Lista ordenada de forma descendente por el segundo elemento.
    """
    for i in range(len(lista)-1):
        for j in range(i+1, len(lista)):
            if lista[j][1] > lista[i][1]:
                auxiliar = lista[i]
                lista[i] = lista[j]
                lista[j] = auxiliar
    return lista

def bucle_procesar_estadisticas_lineas(lineas: list) -> tuple[list, list, list]:
    """
    Procesa las líneas de estadísticas para extraer aciertos, errores y tiempos.

    Args:
        lineas (list): Lista de líneas del archivo CSV de estadísticas.

    Returns:
        tuple[list, list, list]: Tres listas con los valores numéricos de aciertos, errores y tiempos.
    """
    if len(lineas) <= 1:
        return [], [], []
    
    aciertos = []
    errores = []
    tiempos = []

    for linea in lineas[1:]:
        datos = linea.strip().split(";")
        if len(datos) < 5:
            continue
        if datos[1].isdigit() and datos[2].isdigit() and datos[3].isdigit():
            aciertos.append(int(datos[1]))
            errores.append(int(datos[2]))
            tiempos.append(int(datos[3]))
    
    return aciertos, errores, tiempos

def bucle_procesar_datos_estadisticas(lineas_estadisticas: list) -> tuple[list, list]:
    """
    Procesa las estadísticas completas separando encabezado y datos válidos.

    Args:
        lineas_estadisticas (list): Líneas del archivo CSV de estadísticas.

    Returns:
        tuple[list, list]: Encabezado (lista de campos) y datos válidos (lista de listas).
    """
    if len(lineas_estadisticas) <= 1:
        return [], []
    
    encabezado = lineas_estadisticas[0].strip().split(";")
    datos = []
    
    for linea in lineas_estadisticas[1:]:
        fila = linea.strip().split(";")
        if len(fila) >= len(encabezado):
            datos.append(fila)
    
    return encabezado, datos

def bucle_elegir_opcion_pygame(ventana: pygame.Surface, estado_global: dict, opciones: list[str], seleccion: int) -> tuple[int, str | None]:
    """
    Maneja eventos de teclado para navegar un menú de opciones en Pygame.

    Args:
        ventana (pygame.Surface): Superficie donde se muestran las opciones.
        estado_global (dict): Diccionario de estado general del juego.
        opciones (list[str]): Lista de opciones disponibles.
        seleccion (int): Índice actualmente seleccionado.

    Returns:
        tuple[int, str | None]: Nueva selección y opción elegida si se presiona Enter.
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

def bucle_manejar_selector(slider_rect: pygame.Rect, selector_rect: pygame.Rect) -> bool:
    """
    Maneja el movimiento de un selector en un slider (barra deslizante).

    Args:
        slider_rect (pygame.Rect): Rectángulo del slider.
        selector_rect (pygame.Rect): Rectángulo del selector.

    Returns:
        bool: Verdadero si se está arrastrando el selector, falso en caso contrario.
    """
    arrastrando = False
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if selector_rect.collidepoint(evento.pos):
                arrastrando = True
            elif slider_rect.collidepoint(evento.pos):
                from generales.generales_pygame import actualizar_selector
                actualizar_selector(evento.pos[0], slider_rect, selector_rect)
                arrastrando = True
        elif evento.type == pygame.MOUSEBUTTONUP:
            arrastrando = False
        elif evento.type == pygame.MOUSEMOTION:
            if arrastrando:
                from generales.generales_pygame import actualizar_selector
                actualizar_selector(evento.pos[0], slider_rect, selector_rect)
    
    return arrastrando

def bucle_crear_fuentes(config: dict, fuentes_config: dict) -> dict:
    """
    Crea las fuentes necesarias a partir de la configuración dada.

    Args:
        config (dict): Configuración general de la ventana.
        fuentes_config (dict): Diccionario con las claves de tipos de fuente.

    Returns:
        dict: Diccionario con las fuentes generadas.
    """
    fuentes = {}
    
    for tipo in fuentes_config.keys():
        from generales.config_manager_algorithmic import crear_fuente
        fuentes[tipo] = crear_fuente(config, tipo)
    
    return fuentes

def bucle_cargar_imagenes(rutas: dict) -> dict:
    """
    Carga múltiples imágenes a partir de un diccionario de rutas.

    Args:
        rutas (dict): Diccionario con claves y rutas de imágenes.

    Returns:
        dict: Diccionario con las imágenes cargadas exitosamente.
    """
    imagenes = {}
    
    for tipo, ruta in rutas.items():
        from generales.config_manager_algorithmic import cargar_imagen
        imagen = cargar_imagen(ruta)
        if imagen:
            imagenes[tipo] = imagen
    
    return imagenes

def bucle_generar_textos_estadisticas(estadisticas: dict) -> list[str]:
    """
    Genera textos descriptivos a partir de estadísticas calculadas.

    Args:
        estadisticas (dict): Diccionario con estadísticas (promedios y máximos).

    Returns:
        list[str]: Lista de cadenas con los textos descriptivos.
    """
    textos = []
    campos = [
        ('promedio_aciertos', 'Promedio de aciertos'),
        ('promedio_errores', 'Promedio de errores'), 
        ('promedio_tiempo', 'Promedio de tiempo'),
        ('max_errores', 'Máximo de errores')
    ]
    
    for campo, descripcion in campos:
        if campo in estadisticas:
            if campo == 'promedio_tiempo':
                textos.append(f"{descripcion}: {estadisticas[campo]:.1f}s")
            else:
                textos.append(f"{descripcion}: {estadisticas[campo]:.1f}")
    
    return textos