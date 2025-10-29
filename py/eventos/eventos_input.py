import pygame
from eventos.bucles_eventos import bucle_eventos_input, bucle_eventos_pedir_texto

def manejar_eventos_input(texto_actual: str) -> tuple[str, bool]:
    """
    Encapsula el manejo de eventos de texto delegando al bucle correspondiente.

    Args:
        texto_actual (str): Texto actual ingresado por el usuario.

    Returns:
        tuple[str, bool]: Texto actualizado y bandera booleana que indica si se presionó Enter.
    """
    return bucle_eventos_input(texto_actual)

def pedir_texto(ventana: pygame.Surface, estado_global: dict, titulo: str, prompt: str, max_len: int = 15) -> str:
    """
    Solicita al usuario ingresar un texto mediante Pygame, mostrando un título y un prompt.

    La función muestra una interfaz básica con texto y campo de entrada, y limita la longitud
    máxima permitida del texto.

    Args:
        ventana (pygame.Surface): Superficie donde se dibuja la interfaz.
        estado_global (dict): Diccionario con configuraciones, fuentes y colores del modo actual.
        titulo (str): Título principal que se muestra arriba del campo.
        prompt (str): Texto que precede al campo de entrada.
        max_len (int, opcional): Longitud máxima permitida. Por defecto es 15.

    Returns:
        str: Texto ingresado por el usuario, convertido a minúsculas.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho_ventana = estado_global["config"]["ventana"]["ancho"]
    alto_ventana = estado_global["config"]["ventana"]["alto"]
    
    texto = ""
    while True:
        ventana.fill(colores["GRIS"])
        
        titulo_render = estado_global["fuentes"]["titulo"].render(titulo, True, colores["NEGRO"])
        ventana.blit(titulo_render, ((ancho_ventana - titulo_render.get_width()) // 2, 50))

        prompt_render = estado_global["fuentes"]["boton"].render(prompt + texto, True, colores["AZUL"])
        ventana.blit(prompt_render, (100, alto_ventana // 2))

        pygame.display.flip()

        texto, terminado = bucle_eventos_pedir_texto(texto, max_len)
        if terminado:
            return texto.lower()

def input_text(estado_global: dict, prompt: str, fuente: pygame.font.Font, ancho: int, alto: int) -> str:
    """
    Muestra una interfaz centrada para ingresar texto usando un cuadro de entrada rectangular.

    Muestra un prompt en la parte superior y permite al usuario escribir hasta que presione Enter.

    Args:
        estado_global (dict): Diccionario con configuraciones, fuentes y colores del modo actual.
        prompt (str): Texto que se muestra encima del cuadro de entrada.
        fuente (pygame.font.Font): Fuente utilizada para renderizar el texto.
        ancho (int): Ancho de la ventana.
        alto (int): Alto de la ventana.

    Returns:
        str: Texto ingresado por el usuario, sin espacios al principio o al final.
    """
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ventana = pygame.display.get_surface()
    
    user_text = ""
    input_box = pygame.Rect(ancho // 4, alto // 2, ancho // 2, 40)

    while True:
        ventana.fill(colores["GRIS"])

        render_prompt = fuente.render(prompt, True, colores["NEGRO"])
        ventana.blit(render_prompt, ((ancho - render_prompt.get_width()) // 2, alto // 3))

        pygame.draw.rect(ventana, colores["BLANCO"], input_box)
        pygame.draw.rect(ventana, colores["NEGRO"], input_box, 2)

        render_texto = fuente.render(user_text, True, colores["NEGRO"])
        ventana.blit(render_texto, (input_box.x + 10, input_box.y + 5))

        pygame.display.flip()

        user_text, terminado = manejar_eventos_input(user_text)
        if terminado:
            return user_text.strip()

def pedir_usuario(estado_global: dict) -> str | None:
    """
    Solicita al usuario ingresar su nombre utilizando la función `input_text`.

    Esta función utiliza una fuente predefinida y las dimensiones actuales de la ventana.

    Args:
        estado_global (dict): Diccionario con configuraciones generales, incluyendo tamaño de ventana.

    Returns:
        str | None: Nombre de usuario ingresado, o None si no se completa.
    """
    fuente_input = pygame.font.SysFont("Arial", 30)
    return input_text(estado_global,
        prompt="Ingrese nombre de usuario:",
        fuente=fuente_input,
        ancho=estado_global["config"]["ventana"]["ancho"],
        alto=estado_global["config"]["ventana"]["alto"]
    )