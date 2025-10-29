import pygame
from pantallas.bucles_pantallas import bucle_dibujar_encabezado_tabla, bucle_dibujar_filas_tabla

def obtener_colores(estado: dict, modo: str | None = None) -> dict:
    """
    Obtiene el diccionario de colores según el modo especificado o el actual.

    Args:
        estado (dict): Estado global con configuraciones de colores.
        modo (str or None): Modo específico a usar o None para usar el actual.

    Returns:
        dict: Diccionario con los colores del modo seleccionado.
    """
    if modo is None:
        modo = estado.get("modo", "normal")
    return estado["colores"][modo]

def crear_contenedor(proporcion_ancho: float, alto: int, y: int, estado: dict) -> pygame.Rect:
    """
    Crea un rectángulo contenedor centrado con proporciones específicas.

    Args:
        proporcion_ancho (float): Proporción del ancho de ventana a usar (0.0-1.0).
        alto (int): Altura del contenedor en píxeles.
        y (int): Posición Y del contenedor.
        estado (dict): Estado global con configuraciones de ventana.

    Returns:
        pygame.Rect: Rectángulo del contenedor centrado.
    """
    ancho = int(estado["config"]["ventana"]["ancho"] * proporcion_ancho)
    x = (estado["config"]["ventana"]["ancho"] - ancho) // 2
    return pygame.Rect(x, y, ancho, alto)

def dibujar_contenedor_con_sombra(ventana: pygame.Surface, rect: pygame.Rect, estado: dict):
    """
    Dibuja un contenedor con efecto de sombra usando colores del estado actual.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        rect (pygame.Rect): Rectángulo del contenedor.
        estado (dict): Estado global con colores.

    Returns:
        None: Esta función no retorna valores.
    """
    sombra = rect.copy().move(4, 4)
    pygame.draw.rect(ventana, (0, 0, 0), sombra, border_radius=15)
    colores = obtener_colores(estado)
    pygame.draw.rect(ventana, colores["BLANCO"], rect, border_radius=15)

def dibujar_titulo_puntajes(ventana: pygame.Surface, fuente_titulo: pygame.font.Font, estado: dict):
    """
    Dibuja el título "Puntajes" centrado en la parte superior de la ventana.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        fuente_titulo (pygame.font.Font): Fuente para el título.
        estado (dict): Estado global con configuraciones de ventana.

    Returns:
        None: Esta función no retorna valores.
    """
    colores = obtener_colores(estado)
    ancho = estado["config"]["ventana"]["ancho"]
    titulo = fuente_titulo.render("Puntajes", True, (20, 20, 20))
    ventana.blit(titulo, ((ancho - titulo.get_width()) // 2, 20))

def dibujar_encabezado(ventana: pygame.Surface, fuente_pequena: pygame.font.Font, estado: dict,
                       encabezado: list[str], indices: list[int], col_width: int, row_height: int):
    """
    Dibuja el encabezado de una tabla con las columnas especificadas.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        fuente_pequena (pygame.font.Font): Fuente para el texto del encabezado.
        estado (dict): Estado global (no utilizado en la implementación actual).
        encabezado (list[str]): Lista de títulos de columnas.
        indices (list[int]): Índices de columnas a mostrar.
        col_width (int): Ancho de cada columna.
        row_height (int): Altura de la fila del encabezado.

    Returns:
        None: Esta función no retorna valores.
    """
    bucle_dibujar_encabezado_tabla(ventana, fuente_pequena, encabezado, indices, col_width, row_height)

def dibujar_filas(ventana: pygame.Surface, fuente_pequena: pygame.font.Font, estado: dict,
                  datos: list[list[str]], indices: list[int], col_width: int, row_height: int,
                  scroll: int, mouse_y: int):
    """
    Dibuja las filas de datos de una tabla con soporte para scroll y hover.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        fuente_pequena (pygame.font.Font): Fuente para el texto.
        estado (dict): Estado global (no utilizado en la implementación actual).
        datos (list[list[str]]): Datos de la tabla organizados por filas.
        indices (list[int]): Índices de columnas a mostrar.
        col_width (int): Ancho de cada columna.
        row_height (int): Altura de cada fila.
        scroll (int): Desplazamiento vertical actual.
        mouse_y (int): Posición Y del mouse para efecto hover.

    Returns:
        None: Esta función no retorna valores.
    """
    bucle_dibujar_filas_tabla(ventana, fuente_pequena, datos, indices, col_width, row_height, scroll, mouse_y)

def mostrar_imagen_resultado_en_rosco(ventana: pygame.Surface, imagen: pygame.Surface, estado: dict):
    """
    Muestra una imagen de resultado centrada en la zona del rosco.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar la imagen.
        imagen (pygame.Surface): Imagen a mostrar.
        estado (dict): Estado global con configuraciones de ventana.

    Returns:
        None: Esta función no retorna valores.
    """
    if imagen:
        ancho = estado["config"]["ventana"]["ancho"]
        alto = estado["config"]["ventana"]["alto"]
        centro_x = ancho * 3 // 4
        centro_y = alto // 2 - 50
        rect = imagen.get_rect(center=(centro_x, centro_y))
        ventana.blit(imagen, rect)