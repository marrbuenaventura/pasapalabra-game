import re
import json
import os
import builtins
import csv
from bucles_funciones import *

def guardar_estadisticas_partida(estadistica: dict, ruta_general="csv/estadisticas.csv", carpeta_historiales="csv/historiales"):
    """
    Guarda la estadística de una partida:
    - En el archivo CSV general (como siempre)
    - En el archivo JSON unificado SOLO para historiales (sin duplicar en CSV)

    Args:
        estadistica (dict): Diccionario con claves: usuario, aciertos, errores, tiempo, puntaje.
        ruta_general (str): Ruta del archivo CSV general de estadísticas.
        carpeta_historiales (str): Se ignora, mantenido por compatibilidad.
    """
    if not os.path.exists(os.path.dirname(ruta_general)):
        os.makedirs(os.path.dirname(ruta_general))

    linea = f'{estadistica["usuario"]};{estadistica["aciertos"]};{estadistica["errores"]};{estadistica["tiempo"]};{estadistica["puntaje"]}\n'
    archivo_existe = os.path.exists(ruta_general)
    with open(ruta_general, "a", encoding="utf-8") as archivo_general:
        if not archivo_existe:
            archivo_general.write("usuario;aciertos;errores;tiempo;puntaje\n")
        archivo_general.write(linea)

    guardar_en_json_unificado(estadistica)

def guardar_en_json_unificado(estadistica: dict):
    """
    Guarda la partida en UN SOLO archivo JSON que contiene todos los usuarios.
    """
    archivo_json = "json/historiales_todos_usuarios.json"
    os.makedirs("json", exist_ok=True)
    
    datos = {}
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except:
            datos = {}
    
    usuario = estadistica["usuario"].lower()
    if usuario not in datos:
        datos[usuario] = []
    
    nueva_partida = {
        "aciertos": estadistica["aciertos"],
        "errores": estadistica["errores"],
        "tiempo": estadistica["tiempo"],
        "puntaje": estadistica["puntaje"]
    }
    
    datos[usuario].append(nueva_partida)
    
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def guardar_preferencias_usuario(usuario: str, preferencias: dict):
    """
    Guarda las preferencias de un usuario en el archivo JSON unificado de preferencias.
    
    Args:
        usuario (str): Nombre del usuario
        preferencias (dict): Diccionario con las preferencias del usuario
    """
    archivo_json = "json/preferencias_todos_usuarios.json"
    os.makedirs("json", exist_ok=True)
    
    datos = {}
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except:
            datos = {}
    
    usuario_lower = usuario.lower()
    datos[usuario_lower] = preferencias
    
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def cargar_preferencias_usuario(usuario: str) -> dict:
    """
    Carga las preferencias de un usuario desde el archivo JSON unificado.
    
    Args:
        usuario (str): Nombre del usuario
        
    Returns:
        dict: Preferencias del usuario o preferencias por defecto
    """
    archivo_json = "json/preferencias_todos_usuarios.json"
    preferencias_default = {
        "modo": "normal",
        "volumen": 1.0,
        "brillo": 1.0,
        "primera_vez": True,
        "fecha_ultima_partida": None,
        "partidas_jugadas": 0
    }
    
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                todos_los_datos = json.load(f)
            
            usuario_lower = usuario.lower()
            preferencias = todos_los_datos.get(usuario_lower, preferencias_default.copy())
            
            for clave, valor_default in preferencias_default.items():
                if clave not in preferencias:
                    preferencias[clave] = valor_default
            
            return preferencias
        except:
            return preferencias_default.copy()
    
    return preferencias_default.copy()

def verificar_usuario_existe(usuario: str) -> bool:
    """
    Verifica si un usuario tiene historial registrado.
    
    Args:
        usuario: nombre del usuario
        
    Returns:
        bool: True si existe, False si no
    """
    historial = leer_historial_usuario_json(usuario)
    return len(historial) > 0

def es_usuario_nuevo(usuario: str) -> bool:
    """
    Verifica si es la primera vez que el usuario juega.
    
    Args:
        usuario: nombre del usuario
        
    Returns:
        bool: True si es nuevo, False si ya jugó antes
    """
    preferencias = cargar_preferencias_usuario(usuario)
    return preferencias.get("primera_vez", True)

def aplicar_preferencias_al_estado(usuario: str, estado: dict) -> dict:
    """
    Aplica las preferencias del usuario al estado global del juego.
    
    Args:
        usuario: nombre del usuario
        estado: estado global del juego
        
    Returns:
        dict: estado actualizado con las preferencias
    """
    preferencias = cargar_preferencias_usuario(usuario)
    
    if preferencias["modo"] in estado["colores"]:
        estado["modo"] = preferencias["modo"]
        estado["estado_inicial"]["modo"] = preferencias["modo"]
    
    estado["estado_inicial"]["volumen"] = preferencias.get("volumen", 1.0)
    estado["estado_inicial"]["brillo"] = preferencias.get("brillo", 1.0)
    
    try:
        import pygame
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(estado["estado_inicial"]["volumen"])
    except:
        pass
    
    return estado

def mostrar_mensaje_bienvenida(usuario: str) -> str:
    """
    Genera mensaje de bienvenida personalizado según historial del usuario.
    
    Args:
        usuario: nombre del usuario
        
    Returns:
        str: mensaje de bienvenida personalizado
    """
    if es_usuario_nuevo(usuario):
        return f"¡Bienvenido {usuario.title()}! ¡Primera vez jugando Pasapalabra!"
    else:
        preferencias = cargar_preferencias_usuario(usuario)
        partidas = preferencias.get("partidas_jugadas", 0)
        modo = preferencias.get("modo", "normal")
        
        mensaje = f"¡Hola de nuevo {usuario.title()}! "
        
        if partidas == 1:
            mensaje += "¡Segunda partida!"
        elif partidas < 5:
            mensaje += f"Partida número {partidas + 1}."
        elif partidas < 10:
            mensaje += f"¡Ya llevas {partidas} partidas! ¡Eres un veterano!"
        else:
            mensaje += f"¡Increíble! ¡{partidas} partidas jugadas! ¡Eres un experto!"
        
        if modo == "daltonico":
            mensaje += " (Modo daltónico activado)"
            
        return mensaje

def inicializar_usuario_en_juego(usuario: str, estado: dict) -> tuple[dict, str]:
    """
    Inicializa un usuario en el juego aplicando sus preferencias.
    
    Args:
        usuario: nombre del usuario
        estado: estado global del juego
        
    Returns:
        tuple: estado actualizado y mensaje de bienvenida
    """
    estado_actualizado = aplicar_preferencias_al_estado(usuario, estado)
    mensaje = mostrar_mensaje_bienvenida(usuario)
    
    if es_usuario_nuevo(usuario):
        preferencias_iniciales = {
            "modo": estado_actualizado["modo"],
            "volumen": estado_actualizado["estado_inicial"]["volumen"],
            "brillo": estado_actualizado["estado_inicial"]["brillo"],
            "primera_vez": True,
            "partidas_jugadas": 0
        }
        guardar_preferencias_usuario(usuario, preferencias_iniciales)
    
    return estado_actualizado, mensaje

def incrementar_contador_partidas(usuario: str):
    """
    Incrementa el contador de partidas jugadas del usuario.
    
    Args:
        usuario: nombre del usuario
    """
    preferencias = cargar_preferencias_usuario(usuario)
    preferencias["partidas_jugadas"] = preferencias.get("partidas_jugadas", 0) + 1
    preferencias["primera_vez"] = False
    
    import datetime
    preferencias["fecha_ultima_partida"] = datetime.datetime.now().isoformat()
    
    guardar_preferencias_usuario(usuario, preferencias)

def leer_historial_usuario_json(usuario: str) -> list:
    """
    Lee el historial de un usuario desde el archivo JSON unificado.
    
    Args:
        usuario (str): Nombre del usuario
        
    Returns:
        list: Lista de partidas del usuario
    """
    archivo_json = "json/historiales_todos_usuarios.json"
    resultado = []
    
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                todos_los_datos = json.load(f)
            
            usuario_lower = usuario.lower()
            resultado = todos_los_datos.get(usuario_lower, [])
        except:
            resultado = []
    
    return resultado

def convertir_json_a_lineas_csv(usuario: str) -> list:
    """
    Convierte el JSON de usuario a formato de líneas CSV.
    Para compatibilidad con pantallas que esperan formato CSV.
    """
    historial_json = leer_historial_usuario_json(usuario)
    return bucle_convertir_historial_a_csv(historial_json, usuario)

def listar_todos_los_usuarios() -> list:
    """
    Obtiene una lista de todos los usuarios que tienen partidas registradas.
    
    Returns:
        list: Lista de nombres de usuarios
    """
    archivo_json = "json/historiales_todos_usuarios.json"
    usuarios = []
    
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                todos_los_datos = json.load(f)
            usuarios = list(todos_los_datos.keys())
        except:
            usuarios = []
    
    return usuarios

def obtener_estadisticas_usuario_json(usuario: str) -> dict:
    """
    Calcula estadísticas de un usuario desde el JSON unificado.
    
    Args:
        usuario (str): Nombre del usuario
        
    Returns:
        dict: Estadísticas del usuario
    """
    historial = leer_historial_usuario_json(usuario)
    
    estadisticas_default = {
        "partidas_jugadas": 0,
        "promedio_aciertos": 0,
        "promedio_errores": 0,
        "promedio_tiempo": 0,
        "promedio_puntaje": 0,
        "mejor_puntaje": 0
    }
    
    if historial:
        total_aciertos, total_errores, total_tiempo, total_puntaje, mejor_puntaje, total_partidas = bucle_calcular_estadisticas_usuario(historial)
        
        estadisticas_default = {
            "partidas_jugadas": total_partidas,
            "promedio_aciertos": round(total_aciertos / total_partidas, 1),
            "promedio_errores": round(total_errores / total_partidas, 1),
            "promedio_tiempo": round(total_tiempo / total_partidas, 1),
            "promedio_puntaje": round(total_puntaje / total_partidas, 1),
            "mejor_puntaje": mejor_puntaje
        }
    
    return estadisticas_default

def obtener_ranking_general_json(limite=10) -> list:
    """
    Obtiene un ranking de los mejores puntajes de todos los usuarios.
    
    Args:
        limite (int): Número máximo de entradas
        
    Returns:
        list: Lista de mejores puntajes en formato compatible con pantallas
    """
    archivo_json = "json/historiales_todos_usuarios.json"
    lineas = ["usuario;aciertos;errores;tiempo;puntaje\n"]
    
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                todos_los_datos = json.load(f)
            
            ranking = bucle_procesar_ranking_general(todos_los_datos)
            ranking.sort(key=lambda x: x["puntaje"], reverse=True)
            
            lineas = bucle_generar_lineas_ranking(ranking, limite)
        except:
            pass
    
    return lineas

def leer_estadisticas(path_estadisticas: str):
    """
    Lee estadísticas desde un archivo CSV (VUELVE A FUNCIONAR NORMAL).
    """
    resultado = []
    try:
        with builtins.open(path_estadisticas, "r", encoding="utf-8") as archivo:
            resultado = archivo.readlines()
    except:
        pass
    
    return resultado

def verificar_si_existe_archivo(path_estadisticas: str):
    """
    Verifica si existe el archivo CSV de estadísticas, si no lo crea (VUELVE A FUNCIONAR NORMAL).
    """
    if not os.path.exists(path_estadisticas):
        directorio = os.path.dirname(path_estadisticas)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(path_estadisticas, "w", encoding="utf-8") as archivo:
            archivo.write("usuario;aciertos;errores;tiempo;puntaje\n")

def guardar_preguntas_csv(lista_preguntas: list, path: str):
    """
    Guarda una lista de preguntas en un archivo CSV con formato delimitado por punto y coma.

    Args:
        lista_preguntas (list): Lista de preguntas, cada una representada como un diccionario con claves específicas.
        path (str): Ruta del archivo CSV donde se guardarán las preguntas.
    """
    try:
        with open(path, "w", encoding="utf-8") as archivo:
            archivo.write("letra;pregunta;respuesta;categoria;dificultad;puntaje;estado;fallos\n")
            bucle_recorrer_lista_con_archivo(lista_preguntas, archivo, escribir_pregunta)
    except Exception as e:
        print(f"[Error al guardar preguntas CSV] {e}")

def escribir_pregunta(pregunta, archivo):
    """
    Escribe una única pregunta en una línea del archivo CSV.

    Args:
        pregunta (dict): Diccionario con los campos de una pregunta (letra, pregunta, respuesta, etc.).
        archivo: Archivo abierto en modo escritura donde se escribirá la línea CSV correspondiente.
    """
    linea = (
    f'{pregunta["letra"]};{pregunta["pregunta"]};{pregunta["respuesta"]};{pregunta["categoria"]};{pregunta["dificultad"]};{pregunta["puntaje"]};{pregunta["estado"]};{pregunta["fallos"]}\n'
    )
    archivo.write(linea)

def recorrer_lista_con_archivo(lista: list, archivo, funcion):
    """
    Recorre una lista y aplica la función 'funcion' a cada elemento, pasando también el archivo.

    Args:
        lista (list): Lista de elementos.
        archivo: Archivo abierto en modo escritura o similar.
        funcion (callable): Función que recibe (elemento, archivo).
    """
    bucle_recorrer_lista_con_archivo(lista, archivo, funcion)

def cargar_preguntas_csv(path: str) -> list:
    """
    Carga preguntas desde un archivo CSV y las devuelve como una lista de diccionarios.

    Args:
        path (str): Ruta del archivo CSV.

    Returns:
        list: Lista de preguntas como diccionarios.
    """
    lista_preguntas = []
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            archivo.readline() 
            lineas = archivo.readlines()
            bucle_recorrer_lista_con_archivo(lineas, lista_preguntas, agregar_pregunta_desde_linea)
    except FileNotFoundError:
        print(f"[Archivo no encontrado] {path}")
    except Exception as e:
        print(f"[Error al cargar preguntas CSV] {e}")
    
    return lista_preguntas

def agregar_pregunta_desde_linea(linea: str, lista: list):
    """
    Procesa una línea del archivo CSV y, si es válida, la convierte en una pregunta y la agrega a la lista.

    Args:
        linea (str): Línea del archivo CSV.
        lista (list): Lista donde se agregará la pregunta.
    """
    registro = re.split(";|\n", linea)
    if len(registro) >= 8:
        pregunta = {
            "letra": registro[0],
            "pregunta": registro[1],
            "respuesta": registro[2],
            "categoria": registro[3],
            "dificultad": registro[4],
            "puntaje": int(registro[5]),
            "estado": registro[6],
            "fallos": int(registro[7])
        }
        lista.append(pregunta)

def leer_csv(path: str) -> list[dict]:
    """
    Lee un archivo CSV de preguntas y devuelve una lista de diccionarios.
    """
    preguntas = []
    try:
        with open(path, encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo, delimiter=";")
            for fila in lector:
                if "puntaje" in fila and fila["puntaje"]:
                    fila["puntaje"] = int(fila["puntaje"])
                if "fallos" in fila and fila["fallos"]:
                    fila["fallos"] = int(fila["fallos"])
                preguntas.append(fila)
    except FileNotFoundError:
        print(f"[Archivo CSV no encontrado] {path}")
    except Exception as e:
        print(f"[Error al leer CSV] {e}")
    
    return preguntas

def guardar_config_json(config: dict, path: str):
    """Guarda configuración en formato JSON"""
    try:
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump(config, archivo, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Error al guardar configuración JSON] {e}")

def cargar_config(path: str):
    """
    Carga la configuración desde un archivo JSON.

    Args:
        path (str): Ruta del archivo JSON.

    Returns:
        dict: Diccionario con la configuración cargada o vacío si hay error.
    """
    config = {}
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            config = json.load(archivo)
    except FileNotFoundError:
        print(f"[Archivo de configuración no encontrado] {path}")
    except json.JSONDecodeError:
        print(f"[Error de formato en el archivo JSON] {path}")
    except Exception as e:
        print(f"[Error al cargar configuración] {e}")
    
    return config

try:
    preguntas = cargar_preguntas_csv("csv/preguntas_facil.csv")
    preguntas += cargar_preguntas_csv("csv/preguntas_dificil.csv")
except Exception as e:
    preguntas = []
    print(f"[Error cargando preguntas] {e}")

config = {}
config["Cantidad"] = len(preguntas)
config["Tiempo"] = 120
config["Accesibilidad"] = "neurotipico"