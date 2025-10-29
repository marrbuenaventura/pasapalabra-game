import pygame
from pantallas.bucles_pantallas import (
    bucle_renderizar_texto_multilinea, 
    bucle_dibujar_texto_multilinea_manual,
    bucle_dibujar_items_estadisticas
)

def dibujar_boton(
    ventana: pygame.Surface,
    estado_global: dict,
    texto: str,
    x: int,
    y: int,
    ancho: int,
    alto: int,
    color_fondo: tuple[int, int, int] | None = None,
    color_letra: tuple[int, int, int] | None = None
) -> pygame.Rect:
    """
    Dibuja un botón estilizado con texto centrado y retorna su rectángulo.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar el botón.
        estado_global (dict): Estado global con fuentes y colores.
        texto (str): Texto a mostrar en el botón.
        x (int): Coordenada X del botón.
        y (int): Coordenada Y del botón.
        ancho (int): Ancho del botón.
        alto (int): Alto del botón.
        color_fondo (tuple[int, int, int] or None): Color de fondo personalizado.
        color_letra (tuple[int, int, int] or None): Color de texto personalizado.

    Returns:
        pygame.Rect: Rectángulo del botón para detección de clics.
    """
    rect = pygame.Rect(x, y, ancho, alto)
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    fondo = color_fondo if color_fondo else colores["AZUL"]
    letra = color_letra if color_letra else colores["BLANCO"]

    pygame.draw.rect(ventana, fondo, rect, border_radius=8)
    pygame.draw.rect(ventana, colores["NEGRO"], rect, 3, border_radius=8)

    # Usar la fuente correctamente del estado
    texto_render = estado_global["fuentes"]["boton"].render(texto, True, letra)

    if texto_render.get_width() > ancho - 20:
        fuente_reducida = pygame.font.SysFont("Times New Roman", 30)
        texto_render = fuente_reducida.render(texto, True, letra)

    ventana.blit(
        texto_render,
        (
            x + (ancho - texto_render.get_width()) // 2,
            y + (alto - texto_render.get_height()) // 2,
        ),
    )
    return rect

def dibujar_slider(
    ventana: pygame.Surface,
    estado_global: dict,
    etiqueta: str,
    fuente: pygame.font.Font,
    slider_rect: pygame.Rect,
    selector_rect: pygame.Rect,
    y: int,
    valor_actual: float
) -> float:
    """
    Dibuja un control deslizante con etiqueta y valor actual.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        estado_global (dict): Estado global con colores.
        etiqueta (str): Texto de la etiqueta del slider.
        fuente (pygame.font.Font): Fuente para el texto.
        slider_rect (pygame.Rect): Rectángulo del slider.
        selector_rect (pygame.Rect): Rectángulo del selector.
        y (int): Posición Y para la etiqueta.
        valor_actual (float): Valor actual del slider (0.0-1.0).

    Returns:
        float: Valor actual del slider sin modificar.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    texto = fuente.render(f"{etiqueta}: {int(valor_actual * 100)}%", True, colores["NEGRO"])
    ventana.blit(texto, (slider_rect.x, y - 30))

    pygame.draw.rect(ventana, colores["NEGRO"], slider_rect, border_radius=4)
    pygame.draw.rect(ventana, colores["GRIS_CLARO"], slider_rect.inflate(-4, -4), border_radius=4)

    pygame.draw.rect(ventana, colores["AZUL"], selector_rect, border_radius=6)

    return valor_actual

def renderizar_texto_multilinea(
    texto: str,
    fuente: pygame.font.Font,
    color: tuple[int, int, int],
    ancho_max: int
) -> list[pygame.Surface]:
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
    return bucle_renderizar_texto_multilinea(texto, fuente, color, ancho_max)

def dibujar_timer(
    ventana: pygame.Surface,
    estado_global: dict,
    segundos_restantes: int
):
    """
    Dibuja un timer en la esquina superior derecha de la ventana.

    Args:
        ventana (pygame.Surface): Superficie donde dibujar.
        estado_global (dict): Estado global con fuentes y colores.
        segundos_restantes (int): Segundos restantes a mostrar.

    Returns:
        None: Esta función no retorna valores.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    
    texto = estado_global["fuentes"]["timer"].render(f" {segundos_restantes}s", True, colores["NEGRO"])
    ancho = ventana.get_width()
    ventana.blit(texto, (ancho - texto.get_width() - 20, 20))

def dibujar_texto_multilinea(
    ventana: pygame.Surface,
    texto: str,
    x: int,
    y: int,
    ancho: int,
    color: tuple[int, int, int],
    fuente: pygame.font.Font
):
    """
    Dibuja texto multilínea en la ventana ajustando automáticamente las líneas.

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
    bucle_dibujar_texto_multilinea_manual(ventana, texto, x, y, ancho, color, fuente)

def dibujar_items_estadisticas(
    ventana: pygame.Surface,
    estado_global: dict,
    textos: list[str],
    contenedor: pygame.Rect,
    fuente: pygame.font.Font,
    padding_vertical: int,
    alto_item: int,
    espacio_entre_items: int
):
    """
    Dibuja una lista de items de estadísticas con formato estilizado.

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
    bucle_dibujar_items_estadisticas(ventana, estado_global, textos, contenedor, fuente, 
                                   padding_vertical, alto_item, espacio_entre_items)