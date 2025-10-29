import pygame
from pantallas.pantallas_mensajes import *
from eventos.eventos_menu import manejar_eventos_submenu    
from generales.ayuda_menu import *
from pantallas.pantallas_submenu import pantalla_config_visual, pantalla_accesibilidad
from generales.config_manager_algorithmic import *
from funciones_archivos import guardar_preferencias_usuario, cargar_preferencias_usuario
from menu.bucles_menu import bucle_crear_botones_menu, bucle_manejar_eventos_ajustes

def mostrar_info_usuario_en_menu(pantalla, estado):
    """
    Muestra en pantalla la información del usuario actual en el menú principal o ajustes.

    Args:
        pantalla (pygame.Surface): Superficie donde se muestra el texto.
        estado (dict): Diccionario con estado general del juego, incluyendo usuario y fuentes.
    """
    usuario_actual = estado.get("usuario_actual")
    if usuario_actual:
        preferencias = cargar_preferencias_usuario(usuario_actual)
        modo = preferencias.get("modo", "normal")
        partidas = preferencias.get("partidas_jugadas", 0)
        
        info_texto = f"{usuario_actual.title()} | {partidas} partidas"
        if modo == "daltonico":
            info_texto += " | Modo daltónico"
        
        fuente_info = estado["fuentes"]["pequena"]
        color = estado["colores"][estado["modo"]]["NEGRO"]
        texto_render = fuente_info.render(info_texto, True, color)
        pantalla.blit(texto_render, (10, 10))

def actualizar_configuracion_audio_visual(usuario: str, volumen: float, brillo: float):
    """
    Actualiza los valores de volumen y brillo en las preferencias del usuario.

    Args:
        usuario (str): Nombre del usuario actual.
        volumen (float): Nivel de volumen (entre 0.0 y 1.0).
        brillo (float): Nivel de brillo (entre 0.0 y 1.0).
    """
    volumen = max(0.0, min(1.0, volumen))
    brillo = max(0.0, min(1.0, brillo))
    
    preferencias = cargar_preferencias_usuario(usuario)
    preferencias["volumen"] = volumen
    preferencias["brillo"] = brillo
    
    guardar_preferencias_usuario(usuario, preferencias)

def actualizar_modo_usuario(usuario: str, nuevo_modo: str):
    """
    Cambia el modo visual del usuario (normal o daltónico).

    Args:
        usuario (str): Nombre del usuario actual.
        nuevo_modo (str): Modo a aplicar ("normal" o "daltonico").
    """
    if nuevo_modo not in ["normal", "daltonico"]:
        print(f"Error: Modo '{nuevo_modo}' no válido. Debe ser 'normal' o 'daltonico'")
        return
    
    preferencias = cargar_preferencias_usuario(usuario)
    preferencias["modo"] = nuevo_modo
    preferencias["primera_vez"] = False
    
    guardar_preferencias_usuario(usuario, preferencias)

def crear_botones_ajustes(pantalla: pygame.Surface, estado: dict) -> dict:
    """
    Crea los botones del submenú de ajustes.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibujan los botones.
        estado (dict): Estado general con configuraciones y colores.

    Returns:
        dict: Diccionario con botones creados (claves por acción).
    """
    return bucle_crear_botones_menu(pantalla, estado, "ajustes")

def manejar_visual_sonido(pantalla: pygame.Surface, estado: dict):
    """
    Muestra la pantalla de configuración visual y de sonido, y guarda los cambios.

    Args:
        pantalla (pygame.Surface): Superficie principal del juego.
        estado (dict): Estado global del juego con configuraciones actuales.
    """
    v, b = pantalla_config_visual(pantalla, estado)
    estado["estado_inicial"]["volumen"] = v
    estado["estado_inicial"]["brillo"] = b
    pygame.mixer.music.set_volume(estado["estado_inicial"]["volumen"])
    
    usuario_actual = estado.get("usuario_actual")
    if usuario_actual:
        actualizar_configuracion_audio_visual(usuario_actual, v, b)

def manejar_accesibilidad(pantalla: pygame.Surface, estado: dict):
    """
    Muestra la pantalla de accesibilidad y actualiza el modo de visualización.

    Args:
        pantalla (pygame.Surface): Superficie de juego.
        estado (dict): Estado general del juego.
    """
    m, _ = pantalla_accesibilidad(pantalla, estado, estado["modo"], estado["colores"])
    
    if m in estado["colores"]:
        estado["modo"] = m
        estado["estado_inicial"]["modo"] = m
        
        usuario_actual = estado.get("usuario_actual")
        if usuario_actual:
            actualizar_modo_usuario(usuario_actual, m)
    else:
        print(f"WARNING: Modo devuelto '{m}' no es válido. Manteniendo '{estado['modo']}'")

def restaurar_valores_defecto(estado: dict):
    """
    Restaura los valores predeterminados de volumen, brillo y modo visual.

    Args:
        estado (dict): Diccionario de estado general del juego.
    """
    estado["modo"] = "normal"
    estado["estado_inicial"]["modo"] = "normal" 
    estado["estado_inicial"]["volumen"] = 0.5
    estado["estado_inicial"]["brillo"] = 1.0
    
    usuario_actual = estado.get("usuario_actual")
    if usuario_actual:
        actualizar_modo_usuario(usuario_actual, "normal")
        actualizar_configuracion_audio_visual(usuario_actual, 0.5, 1.0)

def manejar_eventos_ajustes(botones: dict, pantalla: pygame.Surface, estado: dict) -> bool:
    """
    Procesa los eventos del submenú de ajustes y ejecuta acciones correspondientes.

    Args:
        botones (dict): Botones activos en el submenú.
        pantalla (pygame.Surface): Superficie donde se muestran los botones.
        estado (dict): Estado actual del juego.

    Returns:
        bool: True si se debe salir del submenú, False si debe continuar.
    """
    seleccion = bucle_manejar_eventos_ajustes(botones, pantalla, estado)

    if seleccion == "visual_sonido":
        manejar_visual_sonido(pantalla, estado)
        return False
    elif seleccion == "accesibilidad":
        manejar_accesibilidad(pantalla, estado)
        return False
    elif seleccion == "restaurar":
        restaurar_valores_defecto(estado)
        return False
    elif seleccion == "ESC":
        return True
    
    return False

def pantalla_ajustes(pantalla: pygame.Surface, estado: dict):
    """
    Ejecuta el bucle principal del submenú de ajustes, mostrando botones y gestionando eventos.

    Args:
        pantalla (pygame.Surface): Superficie de la ventana.
        estado (dict): Estado general del juego.
    """
    reloj = pygame.time.Clock()
    
    while True:
        modo_actual, colores = validar_modo_colores(estado)
        
        pantalla.fill(colores["GRIS"])
        mostrar_titulo(pantalla, "Submenú Ajustes", estado, 80)

        botones = crear_botones_ajustes(pantalla, estado)
        mostrar_info_usuario_en_menu(pantalla, estado)
        aplicar_efectos_pantalla(pantalla, estado)
        
        reloj.tick(60)
        
        if manejar_eventos_ajustes(botones, pantalla, estado):
            break