import json
import os
import pygame
from typing import Dict, Any, Optional
from generales.bucles_generales import bucle_crear_fuentes, bucle_cargar_imagenes

with open("json/config_json.json", "r", encoding="utf-8") as archivo:
    CONFIG = json.load(archivo)

def get_default_config() -> Dict[str, Any]:
    """
    Devuelve una configuración por defecto completa del sistema.

    Returns:
        dict: Diccionario con la configuración predeterminada de ventana, fuentes, colores, imágenes y estado inicial.
    """
    return {
        "ventana": {"ancho": 1200, "alto": 700, "titulo": "Pasapalabra"},
        "fuentes": {
            "titulo": {"nombre": "Times New Roman", "tamano": 60},
            "boton": {"nombre": "Times New Roman", "tamano": 40},
            "pequena": {"nombre": "Times New Roman", "tamano": 24},
            "letra": {"nombre": "arial", "tamano": 20, "bold": True},
            "timer": {"nombre": "arial", "tamano": 30},
            "default": {"nombre": None, "tamano": 36}
        },
        "colores": {
            "normal": {
                "BLANCO": [255, 255, 255], "AZUL": [30, 60, 150],
                "GRIS": [220, 220, 220], "GRIS_CLARO": [240, 240, 240],
                "NEGRO": [0, 0, 0], "AMARILLO": [255, 230, 0],
                "VERDE": [0, 150, 0], "ROJO": [200, 0, 0],
                "NARANJA": [255, 140, 0]
            },
            "daltonico": {
                "BLANCO": [255, 255, 255], "AZUL": [12, 123, 220],
                "GRIS": [220, 220, 220], "GRIS_CLARO": [240, 240, 240],
                "NEGRO": [0, 0, 0], "AMARILLO": [254, 254, 98],
                "VERDE": [64, 176, 166], "ROJO": [220, 50, 32],
                "NARANJA": [212, 17, 89]
            }
        },
        "estado_inicial": {"modo": "normal", "volumen": 1, "brillo": 1.0},
        "imagenes_resultado": {
            "normal": {
                "correcta": "png/Verde_normal.png",
                "incorrecta": "png/Rojo_normal.png",
                "pasada": "png/Amarillo_normal.png"
            },
            "daltonico": {
                "correcta": "png/Verde_modificado.png",
                "incorrecta": "png/Rojo_modificado.png",
                "pasada": "png/Amarillo_modificado.png"
            }
        }
    }

def load_config() -> Dict[str, Any]:
    """
    Carga la configuración desde un archivo JSON. Si el archivo no existe o es inválido, usa la configuración por defecto.

    Returns:
        dict: Configuración cargada desde archivo o la configuración por defecto.
    """
    config = None
    
    try:
        with open("json/config_json.json", "r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        print("Error: config_json.json no encontrado. Usando configuraciÃ³n por defecto.")
        config = get_default_config()
    except json.JSONDecodeError as e:
        print(f"Error al parsear config_json.json: {e}")
        config = get_default_config()
    
    return config

def get_config_value(config: Dict[str, Any], key: str, default=None) -> Any:
    """
    Obtiene un valor de configuración a partir de una clave anidada separada por puntos.

    Args:
        config (dict): Configuración completa.
        key (str): Clave compuesta (e.g., "colores.normal").
        default (Any, optional): Valor por defecto si la clave no existe.

    Returns:
        Any: Valor correspondiente a la clave o el valor por defecto.
    """
    keys = key.split('.')
    value = config
    
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            value = default
            break
    
    return value

def get_ventana_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Devuelve la configuración de la ventana desde el archivo de configuración.

    Args:
        config (dict): Configuración completa.

    Returns:
        dict: Diccionario con configuración de la ventana (ancho, alto, título).
    """
    return get_config_value(config, "ventana", {})

def get_fuentes_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Devuelve la configuración de las fuentes desde el archivo de configuración.

    Args:
        config (dict): Configuración completa.

    Returns:
        dict: Diccionario con la configuración de las fuentes.
    """
    return get_config_value(config, "fuentes", {})

def get_colores(config: Dict[str, Any], modo: str = "normal") -> Dict[str, list]:
    """
    Obtiene la paleta de colores para un modo específico (normal o daltonico).

    Args:
        config (dict): Configuración completa.
        modo (str, optional): Modo de visualización ("normal" o "daltonico").

    Returns:
        dict: Diccionario de colores correspondientes al modo.
    """
    return get_config_value(config, f"colores.{modo}", get_config_value(config, "colores.normal", {}))

def get_imagenes_resultado(config: Dict[str, Any], modo: str = "normal") -> Dict[str, str]:
    """
    Obtiene las rutas de las imágenes de resultado para un modo visual específico.

    Args:
        config (dict): Configuración completa.
        modo (str, optional): Modo visual ("normal" o "daltonico").

    Returns:
        dict: Diccionario con rutas de imágenes por estado (correcta, incorrecta, pasada).
    """
    return get_config_value(config, f"imagenes_resultado.{modo}", get_config_value(config, "imagenes_resultado.normal", {}))

def get_estado_inicial(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Devuelve el estado inicial de la configuración (modo, volumen, brillo).

    Args:
        config (dict): Configuración completa.

    Returns:
        dict: Diccionario con el estado inicial.
    """
    return get_config_value(config, "estado_inicial", {})

def crear_fuente(config: Dict[str, Any], tipo: str) -> pygame.font.Font:
    """
    Crea una fuente específica a partir de la configuración.

    Args:
        config (dict): Configuración completa.
        tipo (str): Tipo de fuente (clave dentro del diccionario de fuentes).

    Returns:
        pygame.font.Font: Objeto fuente creado.
    """
    fuente_config = get_config_value(config, f"fuentes.{tipo}", get_config_value(config, "fuentes.default", {}))
    nombre = fuente_config.get("nombre")
    tamano = fuente_config.get("tamano", 36)
    bold = fuente_config.get("bold", False)
    
    fuente = None
    if nombre:
        fuente = pygame.font.SysFont(nombre, tamano, bold=bold)
    else:
        fuente = pygame.font.Font(None, tamano)
    
    return fuente

def crear_todas_las_fuentes(config: Dict[str, Any]) -> Dict[str, pygame.font.Font]:
    """
    Crea todas las fuentes definidas en la configuración.

    Args:
        config (dict): Configuración completa.

    Returns:
        dict: Diccionario con todas las fuentes creadas.
    """
    fuentes_config = get_fuentes_config(config)
    return bucle_crear_fuentes(config, fuentes_config)

def cargar_imagen(ruta: str) -> Optional[pygame.Surface]:
    """
    Carga una imagen desde una ruta, si el archivo existe.

    Args:
        ruta (str): Ruta de la imagen.

    Returns:
        pygame.Surface | None: Imagen cargada o None si hubo error.
    """
    imagen = None
    
    if os.path.exists(ruta):
        try:
            imagen = pygame.image.load(ruta)
        except pygame.error as e:
            print(f"Error cargando imagen {ruta}: {e}")
    
    return imagen

def cargar_imagenes_resultado(config: Dict[str, Any], modo: str = "normal") -> Dict[str, pygame.Surface]:
    """
    Carga todas las imágenes de resultado para un modo visual específico.

    Args:
        config (dict): Configuración completa.
        modo (str, optional): Modo visual ("normal" o "daltonico").

    Returns:
        dict: Diccionario con las superficies de imágenes cargadas.
    """
    rutas = get_imagenes_resultado(config, modo)
    return bucle_cargar_imagenes(rutas)

def inicializar_configuracion():
    """
    Inicializa toda la configuración necesaria para el juego, incluyendo colores, fuentes e imágenes.

    Returns:
        dict: Diccionario de estado global con la configuración completa inicializada.
    """
    config = load_config()
    estado_inicial = get_estado_inicial(config)
    modo_inicial = estado_inicial.get("modo", "normal")
    
    colores_normal = get_colores(config, "normal")
    colores_daltonico = get_colores(config, "daltonico")
    
    print(f"DEBUG - colores_normal: {colores_normal}")
    print(f"DEBUG - colores_daltonico: {colores_daltonico}")
    print(f"DEBUG - tipo colores_normal: {type(colores_normal)}")
    print(f"DEBUG - tipo colores_daltonico: {type(colores_daltonico)}")
    
    estado_dict = {
        "config": config,
        "ventana": get_ventana_config(config),
        "fuentes": crear_todas_las_fuentes(config),
        "colores": {
            "normal": colores_normal,
            "daltonico": colores_daltonico,
            "actual": get_colores(config, modo_inicial)
        },
        "imagenes": {
            "normal": cargar_imagenes_resultado(config, "normal"),
            "daltonico": cargar_imagenes_resultado(config, "daltonico"),
            "actual": cargar_imagenes_resultado(config, modo_inicial)
        },
        "estado_inicial": estado_inicial,
        "modo": modo_inicial
    }
    
    print(f"DEBUG - estado_dict['colores'] keys: {list(estado_dict['colores'].keys())}")
    return estado_dict